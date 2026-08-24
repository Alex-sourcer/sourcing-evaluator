// DOM Elements - Evaluator Tab
const jobDescriptionEl = document.getElementById('jobDescription');
const candidatesListEl = document.getElementById('candidatesList');
const addCandidateBtnEl = document.getElementById('addCandidateBtn');
const evaluateBtnEl = document.getElementById('evaluateBtn');
const clearBtnEl = document.getElementById('clearBtn');
const loadingEl = document.getElementById('loadingIndicator');
const errorMessageEl = document.getElementById('errorMessage');
const resultsSection = document.getElementById('resultsSection');
const resultsListEl = document.getElementById('resultsList');
const exportCsvBtnEl = document.getElementById('exportCsvBtn');
const shareBtnEl = document.getElementById('shareBtn');
const newEvalBtnEl = document.getElementById('newEvalBtn');
const shareModalEl = document.getElementById('shareModal');
const shareLinkEl = document.getElementById('shareLink');
const copyLinkBtnEl = document.getElementById('copyLinkBtn');
const modalCloseEl = document.querySelector('.modal-close');

// DOM Elements - Search Tab
const searchJobDescEl = document.getElementById('searchJobDescription');
const generateSearchBtnEl = document.getElementById('generateSearchBtn');
const clearSearchBtnEl = document.getElementById('clearSearchBtn');
const searchLoadingEl = document.getElementById('searchLoadingIndicator');
const searchErrorEl = document.getElementById('searchErrorMessage');
const searchResultsEl = document.getElementById('searchResultsSection');
const searchQueriesListEl = document.getElementById('searchQueriesList');
const searchTipsListEl = document.getElementById('searchTipsList');
const idealProfileEl = document.getElementById('idealProfile');

// DOM Elements - Dashboard
const dashboardLoadingEl = document.getElementById('dashboardLoading');
const dashboardContentEl = document.getElementById('dashboardContent');
const totalEvalsEl = document.getElementById('totalEvals');
const avgScoreEl = document.getElementById('avgScore');
const topUserEl = document.getElementById('topUser');
const strongYesEl = document.getElementById('strongYes');
const recommendationChartEl = document.getElementById('recommendationChart');
const userChartEl = document.getElementById('userChart');
const activityChartEl = document.getElementById('activityChart');
const deptListEl = document.getElementById('deptList');

// State
let currentEvaluationId = null;
let currentShareToken = null;
let currentResults = null;
let candidateCount = 1;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupTabNavigation();
    checkIfSharedEvaluation();
    setupEventListeners();
    loadDashboard();
});

function setupTabNavigation() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabName = btn.dataset.tab;
            switchTab(tabName);
        });
    });
}

function switchTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });

    // Remove active from all buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    // Show selected tab
    const tabEl = document.getElementById(`${tabName}-tab`);
    if (tabEl) {
        tabEl.classList.add('active');
    }

    // Mark button as active
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');

    // Load dashboard if switching to dashboard
    if (tabName === 'dashboard') {
        loadDashboard();
    }

    // Load admin metrics if switching to admin
    if (tabName === 'admin') {
        loadAdminMetrics();
    }
}

function setupEventListeners() {
    // Evaluator tab
    addCandidateBtnEl.addEventListener('click', addCandidate);
    evaluateBtnEl.addEventListener('click', evaluateCandidates);
    clearBtnEl.addEventListener('click', clearForm);
    exportCsvBtnEl.addEventListener('click', exportToCSV);
    shareBtnEl.addEventListener('click', openShareModal);
    newEvalBtnEl.addEventListener('click', newEvaluation);
    copyLinkBtnEl.addEventListener('click', copyShareLink);
    modalCloseEl.addEventListener('click', closeShareModal);
    shareModalEl.addEventListener('click', (e) => {
        if (e.target === shareModalEl) closeShareModal();
    });

    candidatesListEl.addEventListener('click', (e) => {
        if (e.target.classList.contains('btn-remove')) {
            e.target.closest('.candidate-input').remove();
        }
        if (e.target.classList.contains('btn-upload-cv')) {
            e.target.closest('.candidate-input').querySelector('.candidate-cv-file').click();
        }
    });

    candidatesListEl.addEventListener('change', (e) => {
        if (e.target.classList.contains('candidate-cv-file')) {
            handleCVFileUpload(e);
        }
    });

    // Search tab
    generateSearchBtnEl.addEventListener('click', generateSearchQueries);
    clearSearchBtnEl.addEventListener('click', clearSearchForm);

    // Export to Google Sheets
    const exportSheetsBtn = document.getElementById('exportSheetsBtn');
    if (exportSheetsBtn) {
        exportSheetsBtn.addEventListener('click', exportToGoogleSheets);
    }
}

function addCandidate() {
    const index = candidateCount++;
    const candidateDiv = document.createElement('div');
    candidateDiv.className = 'candidate-input';
    candidateDiv.dataset.index = index;
    candidateDiv.innerHTML = `
        <div class="candidate-row">
            <input type="text" class="candidate-name" placeholder="Candidate name">
            <textarea class="candidate-profile" placeholder="Profile: experience, skills, years, tech stack, achievements..."></textarea>
            <button type="button" class="btn-upload-cv" title="Upload CV">📄</button>
            <button type="button" class="btn-remove" title="Remove">×</button>
        </div>
        <input type="file" class="candidate-cv-file" style="display: none;" accept=".txt,.pdf">
    `;
    candidatesListEl.appendChild(candidateDiv);
}

function getCandidates() {
    const candidates = [];
    let missingNames = false;

    document.querySelectorAll('.candidate-input').forEach((div) => {
        const name = div.querySelector('.candidate-name').value.trim();
        const profile = div.querySelector('.candidate-profile').value.trim();

        if (profile && !name) {
            missingNames = true;
        }

        if (name && profile) {
            candidates.push({ name, profile, linkedin: "" });
        }
    });

    if (missingNames) {
        showError('Candidate name is required for all entries');
        return [];
    }

    return candidates;
}

async function handleCVFileUpload(e) {
    const file = e.target.files[0];
    if (!file) return;

    const candidateInput = e.target.closest('.candidate-input');
    const profileField = candidateInput.querySelector('.candidate-profile');
    const nameField = candidateInput.querySelector('.candidate-name');

    loadingEl.classList.remove('hidden');
    loadingEl.querySelector('p').textContent = 'Processing CV...';

    try {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch('/api/extract-cv', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to process CV');
        }

        const data = await response.json();

        // Auto-fill fields
        if (data.candidate_name && !nameField.value) {
            nameField.value = data.candidate_name;
        }
        profileField.value = data.profile;

        loadingEl.classList.add('hidden');

        // Show success message with candidate name
        const candidateName = data.candidate_name || file.name.replace(/\.[^/.]+$/, '');
        showSuccessMessage(`✓ CV loaded: ${candidateName}`);

        // Reset file input
        e.target.value = '';
    } catch (error) {
        loadingEl.classList.add('hidden');
        showError('Error processing CV: ' + error.message);
    }
}

function showSuccessMessage(message) {
    const div = document.createElement('div');
    div.className = 'success-toast';
    div.textContent = message;
    div.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: linear-gradient(135deg, #4FB645, #2d8a3a);
        color: white;
        padding: 14px 20px;
        border-radius: 10px;
        font-weight: 600;
        z-index: 1000;
        box-shadow: 0 4px 12px rgba(79, 182, 69, 0.3);
        animation: slideIn 0.3s ease;
    `;
    document.body.appendChild(div);
    setTimeout(() => {
        div.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => div.remove(), 300);
    }, 3000);
}

function showError(message) {
    errorMessageEl.textContent = message;
    errorMessageEl.classList.remove('hidden');
    setTimeout(() => {
        errorMessageEl.classList.add('hidden');
    }, 5000);
}

async function evaluateCandidates() {
    const jobDescription = jobDescriptionEl.value.trim();
    const candidates = getCandidates();

    if (!jobDescription) {
        showError('Por favor, ingresa una descripción del puesto');
        return;
    }

    if (candidates.length === 0) {
        showError('Por favor, agrega al menos un candidato');
        return;
    }

    loadingEl.classList.remove('hidden');
    evaluateBtnEl.disabled = true;

    try {
        const response = await fetch('/api/evaluate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                job_description: jobDescription,
                candidates: candidates
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Error en la evaluación');
        }

        const data = await response.json();
        currentEvaluationId = data.evaluation_id;
        currentShareToken = data.share_token;
        currentResults = data.results;

        displayResults(data.results);
        resultsSection.classList.remove('hidden');
    } catch (error) {
        showError(error.message);
    } finally {
        loadingEl.classList.add('hidden');
        evaluateBtnEl.disabled = false;
    }
}

function displayResults(results) {
    resultsListEl.innerHTML = '';

    results.forEach((result) => {
        const card = createResultCard(result);
        resultsListEl.appendChild(card);
    });
}

function createResultCard(result) {
    const card = document.createElement('div');
    card.className = 'result-card';

    const matchScore = parseInt(result.match_score);
    let scoreClass = 'low';
    if (matchScore >= 70) scoreClass = 'high';
    else if (matchScore >= 50) scoreClass = 'medium';

    const recommendationClass = result.recommendation.toLowerCase().replace(' ', '-');

    card.innerHTML = `
        <div class="card-header">
            <div class="candidate-name-card">${escapeHtml(result.candidate_name)}</div>
            <div class="score-badge ${scoreClass}">${matchScore}%</div>
        </div>

        <div class="card-field">
            <div class="card-field-label">Technical Fit</div>
            <div class="card-field-value">${escapeHtml(result.technical_fit)}</div>
        </div>

        <div class="card-field">
            <div class="card-field-label">Strengths</div>
            <ul class="field-list">
                ${result.strengths.map(s => `<li>${escapeHtml(s)}</li>`).join('')}
            </ul>
        </div>

        ${result.red_flags && result.red_flags.length > 0 ? `
        <div class="card-field">
            <div class="card-field-label">Red Flags</div>
            <ul class="field-list">
                ${result.red_flags.map(r => `<li>${escapeHtml(r)}</li>`).join('')}
            </ul>
        </div>
        ` : ''}

        <div class="card-field">
            <div class="card-field-label">Interview Questions</div>
            <ul class="field-list">
                ${result.questions.map(q => `<li>${escapeHtml(q)}</li>`).join('')}
            </ul>
        </div>

        <div class="card-field">
            <div class="card-field-label">Recommendation</div>
            <div class="recommendation ${recommendationClass}">${escapeHtml(result.recommendation)}</div>
        </div>

        <div class="card-field">
            <div class="card-field-label">Reasoning</div>
            <div class="card-field-value">${escapeHtml(result.reasoning)}</div>
        </div>
    `;

    return card;
}

function exportToCSV() {
    if (!currentResults) return;

    const headers = ['Candidato', 'Match Score', 'Technical Fit', 'Strengths', 'Red Flags', 'Interview Questions', 'Recommendation', 'Reasoning'];
    const rows = currentResults.map(result => [
        result.candidate_name,
        result.match_score,
        result.technical_fit,
        result.strengths.join('; '),
        result.red_flags ? result.red_flags.join('; ') : '',
        result.questions.join('; '),
        result.recommendation,
        result.reasoning
    ]);

    let csv = headers.join(',') + '\n';
    rows.forEach(row => {
        csv += row.map(cell => `"${String(cell).replace(/"/g, '""')}"`).join(',') + '\n';
    });

    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `evaluacion-candidatos-${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
}

function openShareModal() {
    if (!currentShareToken) return;

    const shareUrl = `${window.location.origin}?share=${currentShareToken}`;
    shareLinkEl.value = shareUrl;
    shareModalEl.classList.remove('hidden');
}

function closeShareModal() {
    shareModalEl.classList.add('hidden');
}

function copyShareLink() {
    shareLinkEl.select();
    document.execCommand('copy');
    copyLinkBtnEl.textContent = '✓ Copiado';
    setTimeout(() => {
        copyLinkBtnEl.textContent = 'Copiar';
    }, 2000);
}

function newEvaluation() {
    clearForm();
    resultsSection.classList.add('hidden');
    currentEvaluationId = null;
    currentShareToken = null;
    currentResults = null;
}

function clearForm() {
    jobDescriptionEl.value = '';
    candidatesListEl.innerHTML = '';
    candidateCount = 1;
    addCandidate();
    errorMessageEl.classList.add('hidden');
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// Search Candidates Functions
async function generateSearchQueries() {
    const jobDesc = searchJobDescEl.value.trim();

    if (!jobDesc) {
        showSearchError('Por favor, ingresa una descripción del puesto');
        return;
    }

    searchLoadingEl.classList.remove('hidden');
    generateSearchBtnEl.disabled = true;

    try {
        const response = await fetch('/api/search-candidates', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                job_description: jobDesc,
                candidates: []
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Error generating search queries');
        }

        const data = await response.json();
        displaySearchResults(data.data);
        searchResultsEl.classList.remove('hidden');
    } catch (error) {
        showSearchError(error.message);
    } finally {
        searchLoadingEl.classList.add('hidden');
        generateSearchBtnEl.disabled = false;
    }
}

function displaySearchResults(data) {
    // Ideal profile
    if (data.ideal_profile) {
        idealProfileEl.innerHTML = `<p><strong>Candidato Ideal:</strong> ${escapeHtml(data.ideal_profile)}</p>`;
    }

    // Search queries
    searchQueriesListEl.innerHTML = '';
    if (data.search_queries) {
        data.search_queries.forEach((q, idx) => {
            const div = document.createElement('div');
            div.className = 'search-query-item';
            div.innerHTML = `
                <div class="query-text">${escapeHtml(q.query)}</div>
                <div class="query-desc">${escapeHtml(q.description)}</div>
            `;
            div.addEventListener('click', () => {
                navigator.clipboard.writeText(q.query);
                const originalText = div.querySelector('.query-text').textContent;
                div.querySelector('.query-text').textContent = '✓ Copiado';
                setTimeout(() => {
                    div.querySelector('.query-text').textContent = originalText;
                }, 1500);
            });
            searchQueriesListEl.appendChild(div);
        });
    }

    // Tips
    searchTipsListEl.innerHTML = '';
    if (data.search_tips) {
        data.search_tips.forEach(tip => {
            const li = document.createElement('li');
            li.textContent = tip;
            searchTipsListEl.appendChild(li);
        });
    }
}

function clearSearchForm() {
    searchJobDescEl.value = '';
    searchResultsEl.classList.add('hidden');
    searchErrorEl.classList.add('hidden');
}

function showSearchError(message) {
    searchErrorEl.textContent = message;
    searchErrorEl.classList.remove('hidden');
    setTimeout(() => {
        searchErrorEl.classList.add('hidden');
    }, 5000);
}

// Dashboard Functions
async function loadDashboard() {
    dashboardLoadingEl.classList.remove('hidden');
    dashboardContentEl.classList.add('hidden');

    try {
        const response = await fetch('/api/dashboard/stats');
        if (!response.ok) throw new Error('Failed to load dashboard');

        const stats = await response.json();
        renderDashboard(stats);

        // Also load conversion analytics
        await loadConversionAnalytics();
    } catch (error) {
        console.error('Dashboard error:', error);
    } finally {
        dashboardLoadingEl.classList.add('hidden');
    }
}

function renderDashboard(stats) {
    // KPI Cards
    totalEvalsEl.textContent = stats.total_evaluations;
    avgScoreEl.textContent = stats.avg_match_score + '%';

    if (stats.evaluations_by_user.length > 0) {
        topUserEl.textContent = stats.evaluations_by_user[0].email.split('@')[0];
    }

    const strongYesCount = stats.recommendation_distribution['STRONG YES'] || 0;
    strongYesEl.textContent = strongYesCount;

    // Recommendation distribution chart
    renderRecommendationChart(stats.recommendation_distribution);

    // User chart
    renderUserChart(stats.evaluations_by_user);

    // Activity chart
    renderActivityChart(stats.evaluations_by_date);

    // Department chart
    renderDeptChart(stats.evaluations_by_department);

    dashboardContentEl.classList.remove('hidden');
}

function renderRecommendationChart(distribution) {
    const colors = {
        'STRONG YES': '#00BA63',
        'YES': '#00D46F',
        'MAYBE': '#FFB81C',
        'NO': '#E01E37'
    };

    recommendationChartEl.innerHTML = '';

    Object.entries(distribution).forEach(([rec, count]) => {
        const div = document.createElement('div');
        div.style.marginBottom = '12px';
        const color = colors[rec] || '#999';
        const percentage = count > 0 ? count : 0;

        div.innerHTML = `
            <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                <span style="font-weight: 600; color: var(--text);">${escapeHtml(rec)}</span>
                <span style="color: var(--text-secondary);">${count}</span>
            </div>
            <div style="height: 8px; background: var(--border); border-radius: 4px; overflow: hidden;">
                <div style="height: 100%; background: ${color}; width: ${Math.min(percentage * 5, 100)}%;"></div>
            </div>
        `;
        recommendationChartEl.appendChild(div);
    });
}

function renderUserChart(users) {
    userChartEl.innerHTML = '';
    users.slice(0, 5).forEach(user => {
        const div = document.createElement('div');
        div.style.marginBottom = '12px';
        div.innerHTML = `
            <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                <span style="font-weight: 600; color: var(--text);">${escapeHtml(user.email.split('@')[0])}</span>
                <span style="color: var(--text-secondary);">${user.count}</span>
            </div>
            <div style="height: 8px; background: var(--border); border-radius: 4px; overflow: hidden;">
                <div style="height: 100%; background: var(--primary); width: ${Math.min(user.count * 10, 100)}%;"></div>
            </div>
        `;
        userChartEl.appendChild(div);
    });
}

function renderActivityChart(dates) {
    activityChartEl.innerHTML = '';
    dates.slice(0, 30).forEach(item => {
        const bar = document.createElement('div');
        bar.className = 'activity-bar';
        const maxCount = Math.max(...dates.map(d => d.count), 1);
        const height = (item.count / maxCount) * 100;
        bar.style.backgroundColor = `rgba(0, 82, 163, ${0.2 + (item.count / maxCount) * 0.8})`;
        bar.title = `${item.date}: ${item.count} evaluations`;
        activityChartEl.appendChild(bar);
    });
}

function renderDeptChart(departments) {
    deptListEl.innerHTML = '';
    if (departments.length === 0) {
        deptListEl.innerHTML = '<p style="color: var(--text-secondary);">No hay datos por departamento</p>';
        return;
    }

    departments.forEach(dept => {
        const div = document.createElement('div');
        div.className = 'dept-item';
        div.innerHTML = `
            <span class="dept-name">${escapeHtml(dept.department)}</span>
            <span class="dept-count">${dept.count}</span>
        `;
        deptListEl.appendChild(div);
    });
}

// Conversion Analytics
async function loadConversionAnalytics() {
    try {
        const response = await fetch('/api/conversion-analytics');
        if (!response.ok) throw new Error('Failed to load conversion analytics');

        const data = await response.json();
        renderConversionAnalytics(data);
    } catch (error) {
        console.error('Conversion analytics error:', error);
    }
}

function renderConversionAnalytics(data) {
    const conversionStatsEl = document.getElementById('conversionStats');
    const conversionBandsEl = document.getElementById('conversionBands');
    const conversionInsightEl = document.getElementById('conversionInsight');

    // Stats
    conversionStatsEl.innerHTML = `
        <div class="conversion-stat">
            <div class="value">${data.overall_conversion_rate}%</div>
            <div class="label">Conversion Rate</div>
        </div>
        <div class="conversion-stat">
            <div class="value">${data.total_hired}</div>
            <div class="label">Contratados</div>
        </div>
        <div class="conversion-stat">
            <div class="value">${data.total_evaluated}</div>
            <div class="label">Evaluados</div>
        </div>
    `;

    // Bands
    conversionBandsEl.innerHTML = '';
    Object.entries(data.conversion_by_score_band).forEach(([band, stats]) => {
        const bandDiv = document.createElement('div');
        bandDiv.className = 'conversion-band';
        const percentage = stats.conversion_rate || 0;
        bandDiv.innerHTML = `
            <div class="band-header">
                <span class="band-name">${escapeHtml(band)}</span>
                <span class="band-rate">${stats.conversion_rate}%</span>
            </div>
            <div class="band-bar">
                <div class="band-fill" style="width: ${percentage}%"></div>
            </div>
            <div style="font-size: 0.8rem; color: var(--text-secondary); margin-top: 6px;">
                ${stats.hired} / ${stats.total} contratados
            </div>
        `;
        conversionBandsEl.appendChild(bandDiv);
    });

    // Insight
    const strongestBand = Object.entries(data.conversion_by_score_band)
        .sort((a, b) => b[1].conversion_rate - a[1].conversion_rate)[0];

    if (strongestBand) {
        const [band, stats] = strongestBand;
        conversionInsightEl.innerHTML = `
            <strong>💡 Insight:</strong> Los candidatos con score ${band} tienen ${stats.conversion_rate}%
            de probabilidad de ser contratados.
            ${stats.conversion_rate > data.overall_conversion_rate
                ? `Esto es ${(stats.conversion_rate - data.overall_conversion_rate).toFixed(1)}% mejor que el promedio.`
                : 'Debajo del promedio.'}
        `;
    }
}

// Google Sheets Export
async function exportToGoogleSheets() {
    const btn = document.getElementById('exportSheetsBtn');
    const originalText = btn.textContent;
    btn.disabled = true;
    btn.textContent = 'Exportando...';

    try {
        const response = await fetch('/api/export-google-sheets', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });

        if (!response.ok) throw new Error('Export failed');

        const data = await response.json();

        // Generate CSV from data
        const csv = generateCsvFromData(data.records);
        downloadCsv(csv, `sourcing-evaluator-${new Date().toISOString().split('T')[0]}.csv`);

        btn.textContent = '✓ Exportado';
        setTimeout(() => {
            btn.textContent = originalText;
            btn.disabled = false;
        }, 2000);

    } catch (error) {
        console.error('Export error:', error);
        btn.textContent = '❌ Error';
        setTimeout(() => {
            btn.textContent = originalText;
            btn.disabled = false;
        }, 2000);
    }
}

function generateCsvFromData(records) {
    if (records.length === 0) return '';

    const headers = Object.keys(records[0]);
    const csv = [headers.join(',')];

    records.forEach(record => {
        const row = headers.map(header => {
            const value = record[header] || '';
            const escaped = String(value).replace(/"/g, '""');
            return `"${escaped}"`;
        });
        csv.push(row.join(','));
    });

    return csv.join('\n');
}

function downloadCsv(csv, filename) {
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    window.URL.revokeObjectURL(url);
}

async function checkIfSharedEvaluation() {
    const params = new URLSearchParams(window.location.search);
    const shareToken = params.get('share');

    if (shareToken) {
        loadingEl.classList.remove('hidden');
        try {
            const response = await fetch(`/api/share/${shareToken}`);
            if (!response.ok) throw new Error('Evaluación no encontrada');

            const data = await response.json();
            jobDescriptionEl.value = data.job_description;
            jobDescriptionEl.disabled = true;

            // Load candidates
            candidatesListEl.innerHTML = '';
            candidateCount = 0;
            data.candidates.forEach(c => {
                const index = candidateCount++;
                const div = document.createElement('div');
                div.className = 'candidate-input';
                div.dataset.index = index;
                div.innerHTML = `
                    <div class="candidate-row">
                        <input type="text" class="candidate-name" value="${escapeHtml(c.name)}" disabled>
                        <textarea class="candidate-profile" disabled>${escapeHtml(c.profile)}</textarea>
                    </div>
                `;
                candidatesListEl.appendChild(div);
            });

            // Disable input section
            document.querySelectorAll('textarea, input[type="text"], button').forEach(el => {
                if (!el.matches('.modal-close, #newEvalBtn, #exportCsvBtn, #copyLinkBtn')) {
                    el.disabled = true;
                }
            });
            addCandidateBtnEl.disabled = true;
            evaluateBtnEl.disabled = true;
            clearBtnEl.disabled = true;

            currentResults = data.results;
            displayResults(data.results);
            resultsSection.classList.remove('hidden');

        } catch (error) {
            showError('No se pudo cargar la evaluación: ' + error.message);
        } finally {
            loadingEl.classList.add('hidden');
        }
    } else {
        addCandidate();
    }
}

// Admin Dashboard Logic
const adminTotalEvalsEl = document.getElementById('adminTotalEvals');
const adminUsersEl = document.getElementById('adminUsers');
const adminAvgScoreEl = document.getElementById('adminAvgScore');
const adminTimeSavedEl = document.getElementById('adminTimeSaved');
const adminConversionEl = document.getElementById('adminConversion');
const adminUsersListEl = document.getElementById('adminUsersList');
const adminScoreDistEl = document.getElementById('adminScoreDist');
const adminActivityChartEl = document.getElementById('adminActivityChart');
const exportAdminReportBtn = document.getElementById('exportAdminReportBtn');
const refreshAdminBtn = document.getElementById('refreshAdminBtn');

async function loadAdminMetrics() {
    try {
        const response = await fetch('/api/admin/metrics');
        const data = await response.json();
        displayAdminMetrics(data);
    } catch (error) {
        console.error('Error loading admin metrics:', error);
    }
}

function displayAdminMetrics(data) {
    const summary = data.summary;
    
    // Update summary cards
    adminTotalEvalsEl.textContent = summary.total_evaluations;
    adminUsersEl.textContent = summary.unique_users;
    adminAvgScoreEl.textContent = summary.avg_match_score + '%';
    adminTimeSavedEl.textContent = summary.time_saved_hours;
    adminConversionEl.textContent = summary.conversion_rate + '%';
    
    // Display users activity
    displayUsersActivity(data.by_user);
    
    // Display score distribution
    displayScoreDistribution(data.score_distribution);
    
    // Display activity chart
    displayActivityChart(data.by_date);
}

function displayUsersActivity(users) {
    adminUsersListEl.innerHTML = '';
    
    users.forEach(user => {
        const userDiv = document.createElement('div');
        userDiv.className = 'user-item';
        userDiv.innerHTML = `
            <div class="user-info">
                <div class="user-name">${escapeHtml(user.user)}</div>
                <div class="user-stats">${user.evals} evaluations</div>
            </div>
            <div class="user-evals">
                <div class="eval-count">${user.evals}</div>
                <div class="eval-avg">${user.avg_score}% avg</div>
            </div>
        `;
        adminUsersListEl.appendChild(userDiv);
    });
    
    if (users.length === 0) {
        adminUsersListEl.innerHTML = '<p style="color: var(--text-secondary);">No user data yet</p>';
    }
}

function displayScoreDistribution(scores) {
    adminScoreDistEl.innerHTML = '';
    
    const maxCount = Math.max(...Object.values(scores), 1);
    const bands = ['80-100', '60-79', '40-59', '0-39'];
    
    bands.forEach(band => {
        const count = scores[band] || 0;
        const percentage = (count / maxCount) * 100;
        
        const bandDiv = document.createElement('div');
        bandDiv.className = 'score-band';
        bandDiv.innerHTML = `
            <div class="band-label">${band}%</div>
            <div class="band-bar">
                <div class="band-fill" style="width: ${percentage}%">
                    ${count > 0 ? count : ''}
                </div>
            </div>
        `;
        adminScoreDistEl.appendChild(bandDiv);
    });
}

function displayActivityChart(activity) {
    adminActivityChartEl.innerHTML = '';
    
    if (activity.length === 0) {
        adminActivityChartEl.innerHTML = '<p style="color: var(--text-secondary);">No activity data</p>';
        return;
    }
    
    const maxCount = Math.max(...activity.map(a => a.count), 1);
    
    activity.forEach(day => {
        const height = (day.count / maxCount) * 100;
        const barDiv = document.createElement('div');
        barDiv.className = 'activity-bar';
        barDiv.style.height = Math.max(height, 5) + '%';
        barDiv.innerHTML = `<div class="activity-tooltip">${day.date}: ${day.count}</div>`;
        adminActivityChartEl.appendChild(barDiv);
    });
}

function exportAdminReport() {
    fetch('/api/admin/metrics')
        .then(r => r.json())
        .then(data => {
            const csv = generateAdminCSV(data);
            const blob = new Blob([csv], {type: 'text/csv'});
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `admin-report-${new Date().toISOString().split('T')[0]}.csv`;
            a.click();
        });
}

function generateAdminCSV(data) {
    let csv = 'ADMIN REPORT\n';
    csv += `Generated: ${new Date().toISOString()}\n\n`;
    
    csv += 'SUMMARY\n';
    const s = data.summary;
    csv += `Total Evaluations,${s.total_evaluations}\n`;
    csv += `Active Users,${s.unique_users}\n`;
    csv += `Avg Match Score,${s.avg_match_score}%\n`;
    csv += `Time Saved (hours),${s.time_saved_hours}\n`;
    csv += `Conversion Rate,${s.conversion_rate}%\n\n`;
    
    csv += 'USER ACTIVITY\n';
    csv += 'User,Evaluations,Avg Score\n';
    data.by_user.forEach(u => {
        csv += `${u.user},${u.evals},${u.avg_score}%\n`;
    });
    
    return csv;
}

if (exportAdminReportBtn) {
    exportAdminReportBtn.addEventListener('click', exportAdminReport);
}

if (refreshAdminBtn) {
    refreshAdminBtn.addEventListener('click', loadAdminMetrics);
}

// Load admin metrics when dashboard tab is opened
document.addEventListener('tabChange', (e) => {
    if (e.detail === 'admin') {
        loadAdminMetrics();
    }
});

// Admin Authentication
const adminTabBtn = document.getElementById('adminTabBtn');
const adminLoginModal = document.getElementById('adminLoginModal');
const adminLoginBtn = document.getElementById('adminLoginBtn');
const adminPassword = document.getElementById('adminPassword');
const adminErrorMsg = document.getElementById('adminErrorMsg');

// Admin password (change this to your secure password)
const ADMIN_PASSWORD = 'mambu2024'; // ⚠️ Change this!

function checkAdminAuth() {
    return sessionStorage.getItem('adminAuthenticated') === 'true';
}

function setAdminAuth(authenticated) {
    if (authenticated) {
        sessionStorage.setItem('adminAuthenticated', 'true');
        adminTabBtn.style.display = 'block';
        adminLoginModal.classList.add('hidden');
        return true;
    } else {
        sessionStorage.removeItem('adminAuthenticated');
        adminTabBtn.style.display = 'none';
        return false;
    }
}

function showAdminLogin() {
    adminLoginModal.classList.remove('hidden');
    adminPassword.value = '';
    adminPassword.focus();
    adminErrorMsg.style.display = 'none';
}

function verifyAdminPassword() {
    const pwd = adminPassword.value;
    
    if (pwd === ADMIN_PASSWORD) {
        setAdminAuth(true);
        loadAdminMetrics();
        switchTab('admin');
    } else {
        adminErrorMsg.textContent = 'Incorrect password';
        adminErrorMsg.style.display = 'block';
        adminPassword.value = '';
        adminPassword.focus();
    }
}

// Check if already authenticated on load
document.addEventListener('DOMContentLoaded', () => {
    if (checkAdminAuth()) {
        adminTabBtn.style.display = 'block';
    }
});

// Admin tab click - show login if not authenticated
if (adminTabBtn) {
    adminTabBtn.addEventListener('click', (e) => {
        if (!checkAdminAuth()) {
            e.preventDefault();
            showAdminLogin();
        }
    });
}

// Admin login button
if (adminLoginBtn) {
    adminLoginBtn.addEventListener('click', verifyAdminPassword);
}

// Enter key in password field
if (adminPassword) {
    adminPassword.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            verifyAdminPassword();
        }
    });
}

// Close login modal
const adminLoginClose = adminLoginModal ? adminLoginModal.querySelector('.modal-close') : null;
if (adminLoginClose) {
    adminLoginClose.addEventListener('click', () => {
        adminLoginModal.classList.add('hidden');
    });
}

// Close on backdrop click
if (adminLoginModal) {
    adminLoginModal.addEventListener('click', (e) => {
        if (e.target === adminLoginModal) {
            adminLoginModal.classList.add('hidden');
        }
    });
}
