let selectedCropFile = null;

document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('cropImageInput');
    const dropzone = document.getElementById('dropzone');

    if (input) {
        input.addEventListener('change', (e) => {
            if (e.target.files && e.target.files[0]) {
                handleFileSelected(e.target.files[0]);
            }
        });
    }

    if (dropzone) {
        dropzone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropzone.classList.add('bg-success-subtle');
        });

        dropzone.addEventListener('dragleave', (e) => {
            e.preventDefault();
            dropzone.classList.remove('bg-success-subtle');
        });

        dropzone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropzone.classList.remove('bg-success-subtle');
            if (e.dataTransfer.files && e.dataTransfer.files[0]) {
                handleFileSelected(e.dataTransfer.files[0]);
            }
        });
    }
});

function handleFileSelected(file) {
    if (!file.type.startsWith('image/')) {
        alert('Please select a valid image file (PNG, JPG, JPEG, WEBP).');
        return;
    }

    if (file.size > 16 * 1024 * 1024) {
        alert('Image file size exceeds 16MB limit.');
        return;
    }

    selectedCropFile = file;

    const reader = new FileReader();
    reader.onload = (e) => {
        const previewImg = document.getElementById('previewImg');
        const uploadPlaceholder = document.getElementById('uploadPlaceholder');
        const uploadPreview = document.getElementById('uploadPreview');

        if (previewImg && uploadPlaceholder && uploadPreview) {
            previewImg.src = e.target.result;
            uploadPlaceholder.classList.add('d-none');
            uploadPreview.classList.remove('d-none');
        }
    };
    reader.readAsDataURL(file);
}

function removeSelectedImage() {
    selectedCropFile = null;
    const input = document.getElementById('cropImageInput');
    const uploadPlaceholder = document.getElementById('uploadPlaceholder');
    const uploadPreview = document.getElementById('uploadPreview');

    if (input) input.value = '';
    if (uploadPlaceholder) uploadPlaceholder.classList.remove('d-none');
    if (uploadPreview) uploadPreview.classList.add('d-none');
}

function analyzeCropImage() {
    if (!selectedCropFile) {
        alert('Please select or upload a crop leaf image first.');
        return;
    }

    const spinner = document.getElementById('analysisSpinner');
    const resultBox = document.getElementById('analysisResult');
    const btnAnalyze = document.getElementById('btnAnalyze');

    if (spinner) spinner.classList.remove('d-none');
    if (resultBox) resultBox.classList.add('d-none');
    if (btnAnalyze) btnAnalyze.disabled = true;

    const formData = new FormData();
    formData.append('crop_image', selectedCropFile);

    fetch('/api/crop/analyze', {
        method: 'POST',
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        if (spinner) spinner.classList.add('d-none');
        if (btnAnalyze) btnAnalyze.disabled = false;

        if (data.error) {
            alert(`Analysis Error: ${data.error}`);
            return;
        }

        if (data.success && data.analysis) {
            updateAnalysisUI(data.analysis);
            if (resultBox) resultBox.classList.remove('d-none');
            
            // Refresh graph with newly added point
            if (typeof initCropChart === 'function') {
                initCropChart();
            }
        }
    })
    .catch(err => {
        if (spinner) spinner.classList.add('d-none');
        if (btnAnalyze) btnAnalyze.disabled = false;
        alert(`Server connection failed: ${err.message}`);
    });
}

function updateAnalysisUI(analysis) {
    const scoreVal = document.getElementById('resultScoreVal');
    const cropVal = document.getElementById('resultCropVal');
    const condVal = document.getElementById('resultCondVal');
    const riskVal = document.getElementById('resultRiskVal');
    const diseaseVal = document.getElementById('resultDisease');
    const confVal = document.getElementById('resultConfidence');
    const recVal = document.getElementById('resultRec');
    const circlePath = document.getElementById('scoreCirclePath');

    // Top Summary Card elements
    const summaryHealthScore = document.getElementById('summaryHealthScore');
    const summaryHealthBadge = document.getElementById('summaryHealthBadge');
    const summaryCropName = document.getElementById('summaryCropName');

    if (scoreVal) scoreVal.innerText = `${analysis.health_score}%`;
    if (cropVal) cropVal.innerText = analysis.crop_name;
    if (condVal) condVal.innerText = analysis.condition;
    if (riskVal) riskVal.innerText = `Risk: ${analysis.disease_risk}`;
    if (diseaseVal) diseaseVal.innerText = `Disease: ${analysis.disease}`;
    if (confVal) confVal.innerText = `Conf: ${analysis.confidence}%`;
    if (recVal) recVal.innerText = analysis.recommendation;

    if (circlePath) {
        const score = Math.max(0, Math.min(100, analysis.health_score));
        circlePath.setAttribute('stroke-dasharray', `${score}, 100`);
    }

    if (summaryHealthScore) summaryHealthScore.innerText = `${analysis.health_score}%`;
    if (summaryHealthBadge) summaryHealthBadge.innerText = analysis.condition;
    if (summaryCropName) summaryCropName.innerText = analysis.crop_name;
}
