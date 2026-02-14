// BENYAMIN BATAU JOURNAL APP - Frontend JavaScript

let selectedFiles = [];

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeDropZone();
    initializeForm();
});

// Initialize drop zone functionality
function initializeDropZone() {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');

    // Click to select files
    dropZone.addEventListener('click', () => {
        fileInput.click();
    });

    // Drag and drop events
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        
        const files = Array.from(e.dataTransfer.files);
        handleFiles(files);
    });

    // File input change
    fileInput.addEventListener('change', (e) => {
        const files = Array.from(e.target.files);
        handleFiles(files);
    });
}

// Handle selected files
function handleFiles(files) {
    // Filter valid files
    const validFiles = files.filter(file => {
        const ext = file.name.split('.').pop().toLowerCase();
        return ['pdf', 'docx', 'doc'].includes(ext) && file.size <= 50 * 1024 * 1024;
    });

    // Add to selected files
    validFiles.forEach(file => {
        if (!selectedFiles.find(f => f.name === file.name)) {
            selectedFiles.push(file);
        }
    });

    // Update UI
    updateFileList();
}

// Update file list display
function updateFileList() {
    const fileList = document.getElementById('fileList');
    
    if (selectedFiles.length === 0) {
        fileList.innerHTML = '';
        return;
    }

    let html = '<div class="mt-3"><h5>File yang Dipilih:</h5>';
    
    selectedFiles.forEach((file, index) => {
        const ext = file.name.split('.').pop().toLowerCase();
        const icon = ext === 'pdf' ? 'fa-file-pdf text-danger' : 'fa-file-word text-primary';
        const size = formatFileSize(file.size);
        
        html += `
            <div class="file-item">
                <div>
                    <i class="fas ${icon} me-2"></i>
                    <strong>${file.name}</strong>
                    <span class="badge bg-secondary ms-2">${size}</span>
                </div>
                <button type="button" class="btn btn-sm btn-outline-danger" onclick="removeFile(${index})">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
    });
    
    html += '</div>';
    fileList.innerHTML = html;
}

// Remove file from selection
function removeFile(index) {
    selectedFiles.splice(index, 1);
    updateFileList();
}

// Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Initialize form submission
function initializeForm() {
    const form = document.getElementById('settingsForm');
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Validate files
        if (selectedFiles.length === 0) {
            showAlert('error', 'Silakan upload minimal 1 file tesis!');
            return;
        }

        // Process files
        await processThesis();
    });
}

// Process thesis files
async function processThesis() {
    try {
        // Show progress
        showProgress();
        updateProgress(10, 'Mengunggah file...');

        // Prepare form data
        const formData = new FormData();
        
        // Add files
        selectedFiles.forEach(file => {
            formData.append('files[]', file);
        });

        // Add settings
        formData.append('author_name', document.getElementById('authorName').value);
        formData.append('coauthors', document.getElementById('coauthors').value);
        formData.append('affiliation', document.getElementById('affiliation').value);
        formData.append('email', document.getElementById('email').value);
        formData.append('output_format', document.getElementById('outputFormat').value);
        formData.append('ai_provider', document.getElementById('aiProvider').value);
        formData.append('min_references', document.getElementById('minReferences').value);
        formData.append('use_ai', document.getElementById('useAI').checked);
        formData.append('include_abstract', document.getElementById('includeAbstract').checked);
        formData.append('template', 'unm');

        updateProgress(30, 'Mengekstrak konten dari dokumen...');

        // Upload and process
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        updateProgress(70, 'Memproses dengan AI...');

        const result = await response.json();

        if (result.success) {
            updateProgress(100, 'Selesai!');
            setTimeout(() => {
                showResult(result);
            }, 500);
        } else {
            throw new Error(result.error || 'Terjadi kesalahan saat memproses');
        }

    } catch (error) {
        hideProgress();
        showAlert('error', error.message);
    }
}

// Show progress section
function showProgress() {
    document.getElementById('progressSection').style.display = 'block';
    document.getElementById('resultSection').style.display = 'none';
    
    // Scroll to progress
    document.getElementById('progressSection').scrollIntoView({ behavior: 'smooth' });
}

// Update progress
function updateProgress(percent, text) {
    document.getElementById('progressBar').style.width = percent + '%';
    document.getElementById('progressText').textContent = text;
}

// Hide progress
function hideProgress() {
    document.getElementById('progressSection').style.display = 'none';
}

// Show result section
function showResult(result) {
    hideProgress();
    
    const resultSection = document.getElementById('resultSection');
    resultSection.style.display = 'block';
    resultSection.classList.add('animate-in');

    // Update statistics
    document.getElementById('wordCount').textContent = result.preview_data.word_count.toLocaleString();
    document.getElementById('refCount').textContent = result.preview_data.reference_count;
    document.getElementById('pageCount').textContent = Math.ceil(result.preview_data.word_count / 500);
    document.getElementById('abstractPreview').textContent = result.preview_data.abstract;

    // Scroll to result
    resultSection.scrollIntoView({ behavior: 'smooth' });
}

// Show alert message
function showAlert(type, message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type === 'error' ? 'danger' : 'success'} alert-dismissible fade show alert-custom`;
    alertDiv.innerHTML = `
        <i class="fas fa-${type === 'error' ? 'exclamation-circle' : 'check-circle'}"></i>
        <strong>${type === 'error' ? 'Error!' : 'Success!'}</strong> ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.querySelector('.upload-section').insertAdjacentElement('afterbegin', alertDiv);
    
    // Auto dismiss after 5 seconds
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// Helper: Detect chapter type from filename
function detectChapterType(filename) {
    const lower = filename.toLowerCase();
    
    if (lower.includes('sampul') || lower.includes('cover')) return 'Sampul';
    if (lower.includes('bab_i') || lower.includes('bab_1') || lower.includes('chapter_1')) return 'BAB I';
    if (lower.includes('bab_ii') || lower.includes('bab_2') || lower.includes('chapter_2')) return 'BAB II';
    if (lower.includes('bab_iii') || lower.includes('bab_3') || lower.includes('chapter_3')) return 'BAB III';
    if (lower.includes('bab_iv') || lower.includes('bab_4') || lower.includes('chapter_4')) return 'BAB IV';
    if (lower.includes('bab_v') || lower.includes('bab_5') || lower.includes('chapter_5')) return 'BAB V';
    if (lower.includes('daftar') || lower.includes('pustaka') || lower.includes('reference')) return 'Daftar Pustaka';
    
    return 'Unknown';
}

// Preview enhancement (optional feature)
async function enhanceAbstract() {
    const abstractText = prompt('Masukkan teks abstract yang ingin ditingkatkan:');
    
    if (!abstractText) return;
    
    try {
        const response = await fetch('/api/enhance-abstract', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: abstractText,
                provider: document.getElementById('aiProvider').value
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert('Enhanced Abstract:\n\n' + result.enhanced_text);
        } else {
            showAlert('error', result.error);
        }
    } catch (error) {
        showAlert('error', error.message);
    }
}
