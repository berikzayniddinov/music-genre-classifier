// Charts.js - Chart initialization and management

class ChartManager {
    constructor() {
        this.charts = new Map();
    }

    initGenreDistributionChart() {
        const ctx = document.getElementById('genreDistributionChart');
        if (!ctx) return;

        // Destroy existing chart if it exists
        if (this.charts.has('genreDistribution')) {
            this.charts.get('genreDistribution').destroy();
        }

        const chart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Pop', 'Rock', 'Hip Hop', 'Jazz', 'Electronic', 'Classical', 'R&B', 'Country', 'Metal', 'Folk'],
                datasets: [{
                    data: [25, 18, 15, 8, 12, 6, 10, 5, 3, 2],
                    backgroundColor: [
                        '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
                        '#FF9F40', '#FF6384', '#C9CBCF', '#4BC0C0', '#FF6384'
                    ],
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right',
                        labels: {
                            boxWidth: 12,
                            padding: 15
                        }
                    },
                    title: {
                        display: true,
                        text: 'Prediction Distribution by Genre'
                    }
                },
                cutout: '60%'
            }
        });

        this.charts.set('genreDistribution', chart);
    }

    initPerformanceChart() {
        const ctx = document.getElementById('performanceChart');
        if (!ctx) return;

        // Destroy existing chart if it exists
        if (this.charts.has('performance')) {
            this.charts.get('performance').destroy();
        }

        const chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                datasets: [{
                    label: 'Model Accuracy',
                    data: [92.1, 92.8, 93.2, 93.5, 93.8, 94.1, 94.3, 94.5, 94.6, 94.7, 94.8, 94.8],
                    borderColor: '#36A2EB',
                    backgroundColor: 'rgba(54, 162, 235, 0.1)',
                    tension: 0.4,
                    fill: true
                }, {
                    label: 'F1 Score',
                    data: [40.1, 41.5, 42.8, 43.2, 43.8, 44.1, 44.5, 44.8, 45.0, 45.1, 45.1, 45.1],
                    borderColor: '#FF6384',
                    backgroundColor: 'rgba(255, 99, 132, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Model Performance Over Time'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: false,
                        min: 40,
                        max: 100,
                        title: {
                            display: true,
                            text: 'Percentage (%)'
                        }
                    }
                }
            }
        });

        this.charts.set('performance', chart);
    }

    initPredictionChart(predictions) {
        const ctx = document.getElementById('predictionChart');
        if (!ctx) return;

        // Destroy existing chart if it exists
        if (this.charts.has('prediction')) {
            this.charts.get('prediction').destroy();
        }

        const labels = Object.keys(predictions);
        const data = Object.values(predictions).map(val => val * 100);

        const chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels.map(label => label.replace('_', ' ').toUpperCase()),
                datasets: [{
                    label: 'Confidence (%)',
                    data: data,
                    backgroundColor: data.map(val =>
                        val > 70 ? '#28a745' :
                        val > 50 ? '#ffc107' :
                        '#dc3545'
                    ),
                    borderColor: data.map(val =>
                        val > 70 ? '#218838' :
                        val > 50 ? '#e0a800' :
                        '#c82333'
                    ),
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    title: {
                        display: true,
                        text: 'Genre Prediction Confidence'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        title: {
                            display: true,
                            text: 'Confidence (%)'
                        }
                    },
                    x: {
                        ticks: {
                            autoSkip: false,
                            maxRotation: 45
                        }
                    }
                }
            }
        });

        this.charts.set('prediction', chart);
    }

    destroyAllCharts() {
        this.charts.forEach((chart, key) => {
            chart.destroy();
        });
        this.charts.clear();
    }
}

// Global chart functions
const chartManager = new ChartManager();

function initGenreDistributionChart() {
    chartManager.initGenreDistributionChart();
}

function initPerformanceChart() {
    chartManager.initPerformanceChart();
}

function initPredictionChart(predictions) {
    chartManager.initPredictionChart(predictions);
}

// Initialize charts when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Check if Chart.js is loaded
    if (typeof Chart === 'undefined') {
        console.error('Chart.js is not loaded');
        return;
    }

    // Initialize admin dashboard charts if on admin page
    if (document.getElementById('genreDistributionChart')) {
        initGenreDistributionChart();
    }
    if (document.getElementById('performanceChart')) {
        initPerformanceChart();
    }
});