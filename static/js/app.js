/* ===== ClearSpeak AI — Frontend Logic ===== */

// ---- State ----
let selectedFile = null;
let capturedImageBlob = null;
let cameraStream = null;
let currentQuiz = [];
let currentDocText = '';
let userQuizAnswers = {};

// ---- Toast ----
function showToast(message, isError = false) {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = isError ? 'toast error show' : 'toast show';
    setTimeout(() => { toast.className = toast.className.replace(' show', ''); }, 3500);
}

// ---- Spinner ----
function showSpinner(show) {
    const spinner = document.getElementById('spinner');
    if (spinner) spinner.classList.toggle('active', show);
}

// ---- File Handling ----
function handleFileSelect(event) {
    const file = event.target.files[0];
    if (!file) return;
    selectedFile = file;
    capturedImageBlob = null;
    showFileChip(file.name);
    showToast('File selected: ' + file.name);
}

function showFileChip(name) {
    const chip = document.getElementById('fileChip');
    if (!chip) return;
    chip.style.display = 'inline-flex';
    chip.className = 'file-chip';
    chip.innerHTML = '📄 ' + name + ' <span class="remove" onclick="removeFile()">✕</span>';
}

function removeFile() {
    selectedFile = null;
    capturedImageBlob = null;
    const chip = document.getElementById('fileChip');
    if (chip) chip.style.display = 'none';
    const fileInput = document.getElementById('fileInput');
    if (fileInput) fileInput.value = '';
}

// ---- Camera ----
async function openCamera() {
    const modal = document.getElementById('cameraModal');
    const video = document.getElementById('cameraVideo');
    const preview = document.getElementById('cameraPreview');
    const captureBtn = document.getElementById('captureBtn');
    const retakeBtn = document.getElementById('retakeBtn');
    const useBtn = document.getElementById('useCapturedBtn');

    // Reset state
    if (preview) preview.style.display = 'none';
    if (video) video.style.display = 'block';
    if (captureBtn) captureBtn.style.display = '';
    if (retakeBtn) retakeBtn.style.display = 'none';
    if (useBtn) useBtn.style.display = 'none';

    try {
        cameraStream = await navigator.mediaDevices.getUserMedia({
            video: { facingMode: 'environment', width: { ideal: 1280 }, height: { ideal: 720 } }
        });
        video.srcObject = cameraStream;
        modal.classList.add('active');
    } catch (err) {
        showToast('Camera access denied. Please allow camera permissions.', true);
    }
}

function capturePhoto() {
    const video = document.getElementById('cameraVideo');
    const canvas = document.getElementById('cameraCanvas');
    const preview = document.getElementById('cameraPreview');
    const captureBtn = document.getElementById('captureBtn');
    const retakeBtn = document.getElementById('retakeBtn');
    const useBtn = document.getElementById('useCapturedBtn');

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);

    const dataUrl = canvas.toDataURL('image/jpeg', 0.9);
    preview.src = dataUrl;
    preview.style.display = 'block';
    video.style.display = 'none';
    captureBtn.style.display = 'none';
    retakeBtn.style.display = '';
    useBtn.style.display = '';
}

function retakePhoto() {
    const video = document.getElementById('cameraVideo');
    const preview = document.getElementById('cameraPreview');
    const captureBtn = document.getElementById('captureBtn');
    const retakeBtn = document.getElementById('retakeBtn');
    const useBtn = document.getElementById('useCapturedBtn');

    preview.style.display = 'none';
    video.style.display = 'block';
    captureBtn.style.display = '';
    retakeBtn.style.display = 'none';
    useBtn.style.display = 'none';
}

function useCapturedImage() {
    const canvas = document.getElementById('cameraCanvas');
    canvas.toBlob(function (blob) {
        capturedImageBlob = blob;
        selectedFile = null;
        showFileChip('captured_document.jpg');
        closeCamera();
        showToast('Document captured successfully!');
    }, 'image/jpeg', 0.9);
}

function closeCamera() {
    const modal = document.getElementById('cameraModal');
    modal.classList.remove('active');
    if (cameraStream) {
        cameraStream.getTracks().forEach(track => track.stop());
        cameraStream = null;
    }
}

// ---- Simplify / Explain ----
async function simplifyDocument() {
    const textarea = document.getElementById('documentInput');
    const text = textarea ? textarea.value.trim() : '';

    if (!text && !selectedFile && !capturedImageBlob) {
        showToast('Please paste text, upload a file, or capture a document.', true);
        return;
    }

    showSpinner(true);

    try {
        const formData = new FormData();

        if (selectedFile) {
            formData.append('file', selectedFile);
        } else if (capturedImageBlob) {
            formData.append('file', capturedImageBlob, 'captured_document.jpg');
        } else {
            const blob = new Blob([text], { type: 'text/plain' });
            formData.append('file', blob, 'input.txt');
        }

        const response = await fetch('/api/explain', { method: 'POST', body: formData });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || 'Analysis failed');
        }

        const data = await response.json();
        currentDocText = text || 'Uploaded file content';
        currentQuiz = data.quiz || [];

        renderResults(data);
        showToast('Analysis complete!');
    } catch (error) {
        showToast('Error: ' + error.message, true);
    } finally {
        showSpinner(false);
    }
}

// ---- Render Results ----
function renderResults(data) {
    const explanation = data.explanation || {};

    // Check if we're on the dashboard page
    const dashboardResults = document.getElementById('dashboardResults');
    if (dashboardResults) {
        renderDashboardResults(dashboardResults, explanation, data);
        return;
    }

    // Home page results
    const resultsSection = document.getElementById('resultsSection');
    if (resultsSection) {
        resultsSection.classList.add('active');
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    // Summary
    setTextContent('summaryText', explanation.summary || 'No summary available.');

    // Verdict + risk badge
    setTextContent('verdictText', explanation.one_line_verdict || '');
    const riskBadge = document.getElementById('riskBadge');
    if (riskBadge && explanation.overall_risk_level) {
        const level = explanation.overall_risk_level.toLowerCase();
        riskBadge.innerHTML = '<span class="risk-badge risk-' + level + '">' + explanation.overall_risk_level + ' Risk</span>';
    }

    // Key terms
    const termsList = document.getElementById('termsList');
    if (termsList && explanation.key_terms) {
        termsList.innerHTML = explanation.key_terms.map(t =>
            '<div class="term-item"><strong>' + escHtml(t.term) + '</strong><span>' + escHtml(t.explanation) + '</span></div>'
        ).join('');
    }

    // Risk flags
    const risksList = document.getElementById('risksList');
    if (risksList && explanation.risk_flags) {
        risksList.innerHTML = explanation.risk_flags.map(r =>
            '<div class="risk-item"><strong>⚠️ ' + escHtml(r.risk) + '</strong><span>' + escHtml(r.why_it_matters) + '</span></div>'
        ).join('');
    }

    // Action items
    const actionsList = document.getElementById('actionsList');
    if (actionsList && explanation.action_items) {
        actionsList.innerHTML = explanation.action_items.map(a =>
            '<li>' + escHtml(a) + '</li>'
        ).join('');
    }

    // Quiz
    if (currentQuiz.length > 0) {
        renderQuiz(currentQuiz);
    }
}

function renderDashboardResults(container, explanation, data) {
    let html = '';

    // Summary
    if (explanation.summary) {
        html += '<div style="margin-bottom:20px"><h3 style="font-size:1rem; font-weight:700; color:var(--navy); margin-bottom:8px;">📋 Summary</h3>';
        html += '<p style="font-size:0.92rem; color:var(--gray-600); line-height:1.7;">' + escHtml(explanation.summary) + '</p></div>';
    }

    // Verdict + Risk
    if (explanation.one_line_verdict) {
        const level = (explanation.overall_risk_level || 'low').toLowerCase();
        html += '<div style="margin-bottom:20px; padding:16px; background:var(--gray-50); border-radius:var(--radius);">';
        html += '<h3 style="font-size:1rem; font-weight:700; color:var(--navy); margin-bottom:8px;">⚖️ Verdict</h3>';
        html += '<p style="font-size:0.92rem; color:var(--gray-600); margin-bottom:8px;">' + escHtml(explanation.one_line_verdict) + '</p>';
        html += '<span class="risk-badge risk-' + level + '">' + escHtml(explanation.overall_risk_level || 'Unknown') + ' Risk</span>';
        html += '</div>';
    }

    // Key terms
    if (explanation.key_terms && explanation.key_terms.length) {
        html += '<div style="margin-bottom:20px"><h3 style="font-size:1rem; font-weight:700; color:var(--navy); margin-bottom:8px;">📖 Key Terms</h3>';
        explanation.key_terms.forEach(t => {
            html += '<div class="term-item"><strong>' + escHtml(t.term) + '</strong><span>' + escHtml(t.explanation) + '</span></div>';
        });
        html += '</div>';
    }

    // Risks
    if (explanation.risk_flags && explanation.risk_flags.length) {
        html += '<div style="margin-bottom:20px"><h3 style="font-size:1rem; font-weight:700; color:var(--navy); margin-bottom:8px;">🚩 Risk Flags</h3>';
        explanation.risk_flags.forEach(r => {
            html += '<div class="risk-item"><strong>⚠️ ' + escHtml(r.risk) + '</strong><span>' + escHtml(r.why_it_matters) + '</span></div>';
        });
        html += '</div>';
    }

    // Action items
    if (explanation.action_items && explanation.action_items.length) {
        html += '<div style="margin-bottom:20px"><h3 style="font-size:1rem; font-weight:700; color:var(--navy); margin-bottom:8px;">✅ Action Items</h3>';
        html += '<ul class="action-list">';
        explanation.action_items.forEach(a => {
            html += '<li>' + escHtml(a) + '</li>';
        });
        html += '</ul></div>';
    }

    // Quiz
    if (data.quiz && data.quiz.length) {
        html += '<div style="margin-bottom:20px"><h3 style="font-size:1rem; font-weight:700; color:var(--navy); margin-bottom:12px;">🧠 Test Your Understanding</h3>';
        html += '<div id="quizContent"></div>';
        html += '<button class="btn btn-primary" id="submitQuizBtn" onclick="submitQuiz()" style="margin-top:12px; display:none">Submit Answers</button>';
        html += '<div id="quizResults" style="margin-top:12px"></div>';
        html += '</div>';
    }

    container.innerHTML = html;

    // Render quiz if present
    if (data.quiz && data.quiz.length) {
        currentQuiz = data.quiz;
        renderQuiz(currentQuiz);
    }
}

// ---- Quiz ----
function renderQuiz(quiz) {
    const quizCard = document.getElementById('quizCard');
    if (quizCard) quizCard.style.display = 'block';

    const container = document.getElementById('quizContent');
    if (!container) return;

    const submitBtn = document.getElementById('submitQuizBtn');
    if (submitBtn) submitBtn.style.display = '';

    userQuizAnswers = {};

    container.innerHTML = quiz.map((q, i) =>
        '<div class="quiz-card" id="quiz-' + i + '"><h4>Q' + (i + 1) + ': ' + escHtml(q.question) + '</h4>' +
        q.options.map((opt, j) =>
            '<div class="quiz-option" data-qi="' + i + '" data-oi="' + j + '" onclick="selectQuizOption(this, ' + i + ', ' + j + ')">' + escHtml(opt) + '</div>'
        ).join('') +
        '</div>'
    ).join('');
}

function selectQuizOption(el, qi, oi) {
    // Deselect siblings
    const siblings = el.parentElement.querySelectorAll('.quiz-option');
    siblings.forEach(s => s.classList.remove('selected'));
    el.classList.add('selected');

    // Store answer: extract letter (A, B, C, D)
    const optText = currentQuiz[qi].options[oi];
    userQuizAnswers[qi] = optText.charAt(0);
}

async function submitQuiz() {
    if (Object.keys(userQuizAnswers).length !== currentQuiz.length) {
        showToast('Please answer all questions before submitting.', true);
        return;
    }

    const answers = currentQuiz.map((_, i) => userQuizAnswers[i]);

    // Show correct/incorrect visually
    currentQuiz.forEach((q, i) => {
        const card = document.getElementById('quiz-' + i);
        if (!card) return;
        const options = card.querySelectorAll('.quiz-option');
        options.forEach((opt, j) => {
            const letter = q.options[j].charAt(0);
            opt.classList.remove('selected');
            if (letter === q.correct) {
                opt.classList.add('correct');
            } else if (letter === userQuizAnswers[i] && letter !== q.correct) {
                opt.classList.add('incorrect');
            }
        });
    });

    // Calculate score
    let correct = 0;
    currentQuiz.forEach((q, i) => {
        if (userQuizAnswers[i] === q.correct) correct++;
    });

    const resultsDiv = document.getElementById('quizResults');
    if (resultsDiv) {
        resultsDiv.innerHTML = '<div style="padding:16px; background:var(--primary-light); border-radius:var(--radius); text-align:center;">' +
            '<p style="font-size:1.1rem; font-weight:700; color:var(--primary-dark);">Score: ' + correct + ' / ' + currentQuiz.length + '</p>' +
            '</div>';
    }

    const submitBtn = document.getElementById('submitQuizBtn');
    if (submitBtn) submitBtn.style.display = 'none';

    // Also try to validate via backend
    try {
        const response = await fetch('/api/validate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                document_text: currentDocText,
                quiz: currentQuiz,
                user_answers: answers
            })
        });
        if (response.ok) {
            const validation = await response.json();
            if (validation && resultsDiv) {
                let vHtml = resultsDiv.innerHTML;
                if (validation.feedback) {
                    vHtml += '<div style="margin-top:12px; padding:14px; background:var(--gray-50); border-radius:var(--radius-sm); font-size:0.88rem; color:var(--gray-600); text-align:left;">' + escHtml(typeof validation.feedback === 'string' ? validation.feedback : JSON.stringify(validation.feedback)) + '</div>';
                }
                resultsDiv.innerHTML = vHtml;
            }
        }
    } catch (e) {
        // Validation API call is optional
    }
}

// ---- Utilities ----
function setTextContent(id, text) {
    const el = document.getElementById(id);
    if (el) el.textContent = text;
}

function escHtml(str) {
    if (!str) return '';
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

// ---- Smooth scroll for anchor links ----
document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
});
