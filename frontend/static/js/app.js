// Main application JavaScript
class MusicGenreApp {
    constructor() {
        this.apiBaseUrl = '/api';
        this.init();
    }

    init() {
        this.bindEvents();
        this.checkHealth();
    }

    bindEvents() {
        // Prediction form submission
        const predictionForm = document.getElementById('predictionForm');
        if (predictionForm) {
            predictionForm.addEventListener('submit', (e) => this.handlePrediction(e));
        }

        // Batch prediction
        const batchPredictionBtn = document.getElementById('batchPredictBtn');
        if (batchPredictionBtn) {
            batchPredictionBtn.addEventListener('click', () => this.handleBatchPrediction());
        }
    }

    async checkHealth() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/health`);
            const data = await response.json();

            if (data.status === 'healthy') {
                console.log('✅ API is healthy');
                this.updateHealthIndicator('healthy');
            } else {
                this.updateHealthIndicator('unhealthy');
            }
        } catch (error) {
            console.error('❌ Health check failed:', error);
            this.updateHealthIndicator('unhealthy');
        }
    }

    updateHealthIndicator(status) {
        const indicator = document.getElementById('healthIndicator');
        if (indicator) {
            indicator.className = `badge bg-${status === 'healthy' ? 'success' : 'danger'}`;
            indicator.textContent = status === 'healthy' ? 'API Healthy' : 'API Unavailable';
        }
    }

    async handlePrediction(e) {
        e.preventDefault();

        const analyzeBtn = document.getElementById('analyzeBtn');
        const loadingSpinner = document.getElementById('loadingSpinner');
        const resultsContainer = document.getElementById('resultsContainer');

        // Show loading state
        analyzeBtn.disabled = true;
        loadingSpinner.style.display = 'block';
        resultsContainer.style.display = 'none';

        try {
            const formData = this.getFormData();
            const response = await this.makePrediction(formData);
            this.displayResults(response);
        } catch (error) {
            this.displayError(error);
        } finally {
            analyzeBtn.disabled = false;
            loadingSpinner.style.display = 'none';
        }
    }

    getFormData() {
        return {
            track_name: document.getElementById('trackName').value,
            artists: document.getElementById('artists').value,
            album_name: document.getElementById('albumName').value,
            danceability: parseFloat(document.getElementById('danceability').value),
            energy: parseFloat(document.getElementById('energy').value),
            loudness: parseFloat(document.getElementById('loudness').value),
            speechiness: parseFloat(document.getElementById('speechiness').value),
            acousticness: parseFloat(document.getElementById('acousticness').value),
            instrumentalness: parseFloat(document.getElementById('instrumentalness').value),
            liveness: parseFloat(document.getElementById('liveness').value),
            valence: parseFloat(document.getElementById('valence').value),
            tempo: parseFloat(document.getElementById('tempo').value),
            popularity: parseFloat(document.getElementById('popularity').value)
        };
    }

    async makePrediction(trackData) {
        const response = await fetch(`${this.apiBaseUrl}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(trackData)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Prediction failed');
        }

        return await response.json();
    }

    // Add this function to your existing app.js file

function initPredictionChart(predictions) {
    if (typeof initPredictionChart === 'function') {
        initPredictionChart(predictions);
    }
}

// Update the displayResults function to include charts
// Replace the existing displayResults function with this enhanced version:

displayResults(data) {
    const resultsContainer = document.getElementById('resultsContainer');

    const resultsHTML = `
        <div class="card result-card mt-4">
            <div class="card-header bg-success text-white">
                <h4 class="mb-0">
                    <i class="fas fa-chart-bar me-2"></i>Analysis Results
                </h4>
            </div>
            <div class="card-body">
                <!-- Track Info -->
                <div class="row mb-4">
                    <div class="col-md-6">
                        <h5>${data.track}</h5>
                        <p class="text-muted">by ${data.artists}</p>
                    </div>
                    <div class="col-md-6 text-end">
                        <div class="confidence-score">
                            <h5>Overall Confidence</h5>
                            <div class="progress mb-2" style="height: 25px;">
                                <div class="progress-bar bg-success"
                                     style="width: ${data.confidence * 100}%">
                                    ${(data.confidence * 100).toFixed(1)}%
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Top Genres -->
                ${data.top_genres.length > 0 ? `
                <div class="mb-4">
                    <h6><i class="fas fa-trophy me-2"></i>Predicted Genres</h6>
                    <div class="row">
                        ${data.top_genres.map(genre => `
                            <div class="col-md-3 mb-2">
                                <div class="card bg-light">
                                    <div class="card-body text-center py-2">
                                        <h6 class="card-title mb-1">${genre.replace('_', ' ').toUpperCase()}</h6>
                                        <span class="badge bg-primary rounded-pill">
                                            ${(data.predictions[genre] * 100).toFixed(1)}%
                                        </span>
                                    </div>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
                ` : '<p class="text-warning">No strong genre predictions above 50% confidence</p>'}

                <!-- Chart -->
                <div class="mb-4">
                    <h6><i class="fas fa-chart-bar me-2"></i>Genre Confidence Distribution</h6>
                    <div class="chart-container">
                        <canvas id="predictionChart"></canvas>
                    </div>
                </div>

                <!-- Detailed Probabilities -->
                <div>
                    <h6><i class="fas fa-list-alt me-2"></i>Detailed Genre Analysis</h6>
                    <div class="row">
                        ${Object.entries(data.predictions).map(([genre, prob]) => `
                            <div class="col-md-6 mb-2">
                                <div class="probability-item">
                                    <div class="d-flex justify-content-between align-items-center">
                                        <span>${genre.replace('_', ' ').toUpperCase()}</span>
                                        <span class="badge bg-primary rounded-pill">
                                            ${(prob * 100).toFixed(1)}%
                                        </span>
                                    </div>
                                    <div class="progress" style="height: 6px;">
                                        <div class="progress-bar"
                                             style="width: ${prob * 100}%">
                                        </div>
                                    </div>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>

                <!-- Model Info -->
                <div class="mt-4 pt-3 border-top">
                    <small class="text-muted">
                        <i class="fas fa-robot me-1"></i>
                        Model: ${data.model_version} • Timestamp: ${new Date(data.timestamp).toLocaleString()}
                    </small>
                </div>
            </div>
        </div>
    `;

    resultsContainer.innerHTML = resultsHTML;
    resultsContainer.style.display = 'block';

    // Initialize chart
    if (typeof initPredictionChart === 'function') {
        setTimeout(() => {
            initPredictionChart(data.predictions);
        }, 100);
    }

    // Scroll to results
    resultsContainer.scrollIntoView({ behavior: 'smooth' });
}

    displayError(error) {
        const resultsContainer = document.getElementById('resultsContainer');
        resultsContainer.innerHTML = `
            <div class="alert alert-danger" role="alert">
                <h4 class="alert-heading">
                    <i class="fas fa-exclamation-triangle me-2"></i>Prediction Error
                </h4>
                <p>${error.message}</p>
                <hr>
                <p class="mb-0">Please check your input and try again.</p>
            </div>
        `;
        resultsContainer.style.display = 'block';
    }

    async handleBatchPrediction() {
        // Implementation for batch prediction
        console.log('Batch prediction feature coming soon...');
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new MusicGenreApp();
});

// Utility functions
const AppUtils = {
    formatPercentage: (value) => `${(value * 100).toFixed(1)}%`,

    capitalize: (str) => str.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),

    debounce: (func, wait) => {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
};