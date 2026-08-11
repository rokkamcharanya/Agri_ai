let cropChart = null;

const chartDataSets = {
    labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    health: [92, 90, 88, 87, 84, 85, 86],
    temp: [30, 31, 33, 32, 34, 33, 32],
    rain: [10, 15, 60, 45, 20, 10, 60]
};

function initCropChart() {
    const ctx = document.getElementById('cropHealthChart');
    if (!ctx) return;

    // Fetch live history from backend if available
    fetch('/api/crop/history')
        .then(res => res.json())
        .then(data => {
            if (data.history && data.history.length > 0) {
                const recent = data.history.slice(-7);
                chartDataSets.labels = recent.map((item, idx) => {
                    const date = new Date(item.created_at);
                    return isNaN(date.getDay()) ? `Day ${idx + 1}` : date.toLocaleDateString('en-US', { weekday: 'short' });
                });
                chartDataSets.health = recent.map(item => item.health_score);
            }
            renderChart('health');
        })
        .catch(() => {
            renderChart('health');
        });
}

function renderChart(metric) {
    const ctx = document.getElementById('cropHealthChart');
    if (!ctx) return;

    if (cropChart) {
        cropChart.destroy();
    }

    let datasetLabel = 'Crop Health (%)';
    let borderColor = '#2d6a4f';
    let bgColor = 'rgba(45, 106, 79, 0.15)';
    let dataValues = chartDataSets.health;

    if (metric === 'temp') {
        datasetLabel = 'Temperature (°C)';
        borderColor = '#e63946';
        bgColor = 'rgba(230, 57, 70, 0.15)';
        dataValues = chartDataSets.temp;
    } else if (metric === 'rain') {
        datasetLabel = 'Rain Probability (%)';
        borderColor = '#457b9d';
        bgColor = 'rgba(69, 123, 157, 0.15)';
        dataValues = chartDataSets.rain;
    }

    cropChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: chartDataSets.labels,
            datasets: [{
                label: datasetLabel,
                data: dataValues,
                borderColor: borderColor,
                backgroundColor: bgColor,
                borderWidth: 3,
                pointBackgroundColor: borderColor,
                pointRadius: 5,
                pointHoverRadius: 7,
                fill: true,
                tension: 0.35
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        font: { family: 'Outfit', size: 13, weight: '600' }
                    }
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    backgroundColor: '#1b4332',
                    padding: 10,
                    cornerRadius: 8
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    grid: { color: 'rgba(0, 0, 0, 0.05)' },
                    ticks: { font: { family: 'Outfit' } }
                },
                x: {
                    grid: { display: false },
                    ticks: { font: { family: 'Outfit' } }
                }
            }
        }
    });
}

function switchChartMetric(metric) {
    document.getElementById('btnChartHealth')?.classList.remove('active', 'btn-agri-primary');
    document.getElementById('btnChartHealth')?.classList.add('btn-light');
    document.getElementById('btnChartTemp')?.classList.remove('active', 'btn-agri-primary');
    document.getElementById('btnChartTemp')?.classList.add('btn-light');
    document.getElementById('btnChartRain')?.classList.remove('active', 'btn-agri-primary');
    document.getElementById('btnChartRain')?.classList.add('btn-light');

    if (metric === 'health') {
        document.getElementById('btnChartHealth')?.classList.add('active', 'btn-agri-primary');
        document.getElementById('btnChartHealth')?.classList.remove('btn-light');
    } else if (metric === 'temp') {
        document.getElementById('btnChartTemp')?.classList.add('active', 'btn-agri-primary');
        document.getElementById('btnChartTemp')?.classList.remove('btn-light');
    } else if (metric === 'rain') {
        document.getElementById('btnChartRain')?.classList.add('active', 'btn-agri-primary');
        document.getElementById('btnChartRain')?.classList.remove('btn-light');
    }

    renderChart(metric);
}

document.addEventListener('DOMContentLoaded', () => {
    initCropChart();
});
