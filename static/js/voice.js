let isListening = false;
let recognition = null;
let synth = window.speechSynthesis;

const speechLangCodes = {
    en: 'en-US',
    te: 'te-IN',
    hi: 'hi-IN'
};

function initSpeechRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
        console.warn("Speech Recognition API is not supported in this browser.");
        return null;
    }

    const rec = new SpeechRecognition();
    rec.continuous = false;
    rec.interimResults = false;
    return rec;
}

function getSelectedLanguage() {
    const langSelect = document.getElementById('langSelect');
    return langSelect ? langSelect.value : 'en';
}

function toggleVoiceCommand() {
    if (isListening) {
        stopVoiceCommand();
    } else {
        startVoiceCommand();
    }
}

function startVoiceCommand() {
    recognition = initSpeechRecognition();
    if (!recognition) {
        alert("Speech recognition is not supported in your browser. Please use Chrome, Edge, or Safari.");
        return;
    }

    const currentLang = getSelectedLanguage();
    recognition.lang = speechLangCodes[currentLang] || 'en-US';

    const micBtnText = document.getElementById('micBtnText');
    const micIcon = document.getElementById('micIcon');
    const transcriptBox = document.getElementById('voiceTranscriptBox');
    const transcriptText = document.getElementById('speechTranscriptText');

    recognition.onstart = () => {
        isListening = true;
        if (micBtnText) micBtnText.innerText = "Listening... Speak Now 🎙️";
        if (micIcon) micIcon.classList.add('text-danger', 'animate-pulse');
        if (transcriptBox) transcriptBox.classList.remove('d-none');
        if (transcriptText) transcriptText.innerText = "Listening to your voice...";
    };

    recognition.onresult = (event) => {
        const spokenText = event.results[0][0].transcript;
        if (transcriptText) transcriptText.innerText = `"${spokenText}"`;
        
        // Query backend AI Agronomist with spoken query
        processSpokenQuery(spokenText, currentLang);
    };

    recognition.onerror = (event) => {
        console.error("Speech recognition error:", event.error);
        stopVoiceCommand();
        if (transcriptText) transcriptText.innerText = `Error listening: ${event.error}. Please try again.`;
    };

    recognition.onend = () => {
        stopVoiceCommand();
    };

    try {
        recognition.start();
    } catch (e) {
        console.error("Speech start error:", e);
    }
}

function stopVoiceCommand() {
    isListening = false;
    if (recognition) {
        try { recognition.stop(); } catch (e) {}
    }
    const micBtnText = document.getElementById('micBtnText');
    const micIcon = document.getElementById('micIcon');

    if (micBtnText) micBtnText.innerText = "🎤 Start Voice Command";
    if (micIcon) micIcon.classList.remove('animate-pulse');
}

function processSpokenQuery(queryText, lang) {
    fetch('/api/voice/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: queryText, lang: lang })
    })
    .then(res => res.json())
    .then(data => {
        if (data.response) {
            // Show AI response in AI Agronomist card as well
            const aiBox = document.getElementById('aiResponseBox');
            const aiText = document.getElementById('aiRespText');
            if (aiBox && aiText) {
                aiText.innerText = data.response;
                aiBox.classList.remove('d-none');
            }
            
            // Speak response using browser SpeechSynthesis API
            speakText(data.response, lang);
        }
    })
    .catch(err => console.error("Voice query failed:", err));
}

function speakText(text, lang = null) {
    if (!synth) {
        console.warn("Speech synthesis unavailable");
        return;
    }

    synth.cancel(); // Stop any ongoing speech

    const selectedLang = lang || getSelectedLanguage();
    const targetLangCode = speechLangCodes[selectedLang] || 'en-US';

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = targetLangCode;
    utterance.rate = 0.95;
    utterance.pitch = 1.0;

    // Pick matching voice if available
    const voices = synth.getVoices();
    const matchedVoice = voices.find(v => v.lang.toLowerCase().startsWith(selectedLang));
    if (matchedVoice) {
        utterance.voice = matchedVoice;
    }

    synth.speak(utterance);
}

function playVoiceCropReport() {
    const lang = getSelectedLanguage();

    fetch(`/api/voice/report?lang=${lang}`)
        .then(res => res.json())
        .then(data => {
            if (data.report_text) {
                const transcriptBox = document.getElementById('voiceTranscriptBox');
                const transcriptText = document.getElementById('speechTranscriptText');
                if (transcriptBox && transcriptText) {
                    transcriptBox.classList.remove('d-none');
                    transcriptText.innerText = `🔊 Playing Crop Summary Report (${lang.toUpperCase()})`;
                }
                speakText(data.report_text, lang);
            }
        })
        .catch(err => console.error("Failed to load crop report audio script:", err));
}

function startAgronomistVoiceInput() {
    startVoiceCommand();
}

// Pre-load voices on load
if (synth && synth.onvoiceschanged !== undefined) {
    synth.onvoiceschanged = () => synth.getVoices();
}
