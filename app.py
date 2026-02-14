"""
BENYAMIN BATAU JOURNAL APP
Aplikasi untuk mengonversi Tesis menjadi Artikel Jurnal
Developed by: Benyamin Batau
Version: 1.0.0
"""

from flask import Flask, render_template, request, send_file, jsonify, session
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import json
import tempfile
import traceback
from datetime import datetime
from pathlib import Path

# Import modules
from utils.document_processor import DocumentProcessor
from utils.ai_processor import AIProcessor
from utils.journal_generator import JournalGenerator
from utils.reference_manager import ReferenceManager

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'benyamin-batau-journal-secret-key-2026')
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Create folders if not exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Homepage with upload form"""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_files():
    """Handle file uploads and process thesis"""
    try:
        # Validate files
        if 'files[]' not in request.files:
            return jsonify({'error': 'No files uploaded'}), 400
        
        files = request.files.getlist('files[]')
        
        if not files or files[0].filename == '':
            return jsonify({'error': 'No selected files'}), 400
        
        # Get settings
        settings = {
            'template': request.form.get('template', 'unm'),  # UNM template
            'output_format': request.form.get('output_format', 'docx'),  # docx or pdf
            'use_ai': request.form.get('use_ai', 'true') == 'true',
            'ai_provider': request.form.get('ai_provider', 'claude'),  # claude or gpt4
            'max_pages': int(request.form.get('max_pages', '10')),
            'include_abstract': request.form.get('include_abstract', 'true') == 'true',
            'min_references': int(request.form.get('min_references', '15')),
            'author_name': request.form.get('author_name', ''),
            'coauthors': request.form.get('coauthors', ''),
            'affiliation': request.form.get('affiliation', ''),
            'email': request.form.get('email', ''),
        }
        
        # Save uploaded files
        uploaded_files = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                unique_filename = f"{timestamp}_{filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(filepath)
                uploaded_files.append({
                    'filename': filename,
                    'filepath': filepath,
                    'type': filename.rsplit('.', 1)[1].lower()
                })
        
        # Process documents
        processor = DocumentProcessor()
        thesis_content = processor.extract_thesis_content(uploaded_files)
        
        # Enhance with AI if enabled
        if settings['use_ai']:
            ai_processor = AIProcessor(provider=settings['ai_provider'])
            thesis_content = ai_processor.enhance_content(thesis_content, settings)
        
        # Generate journal article
        generator = JournalGenerator(template=settings['template'])
        journal_data = generator.create_journal_article(thesis_content, settings)
        
        # Process references
        ref_manager = ReferenceManager()
        journal_data['references'] = ref_manager.format_references(
            thesis_content.get('references', []),
            min_count=settings['min_references']
        )
        
        # Generate output file
        output_filename = f"artikel_jurnal_{timestamp}.{settings['output_format']}"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
        if settings['output_format'] == 'docx':
            generator.generate_docx(journal_data, output_path)
        else:
            generator.generate_pdf(journal_data, output_path)
        
        # Store in session for download
        session['output_file'] = output_path
        session['output_filename'] = output_filename
        
        return jsonify({
            'success': True,
            'message': 'Artikel jurnal berhasil dibuat!',
            'filename': output_filename,
            'download_url': '/download',
            'preview_data': {
                'title': journal_data.get('title', ''),
                'abstract': journal_data.get('abstract', '')[:300] + '...',
                'word_count': len(journal_data.get('body', '').split()),
                'reference_count': len(journal_data.get('references', []))
            }
        })
        
    except Exception as e:
        app.logger.error(f"Error processing files: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            'error': f'Error processing files: {str(e)}'
        }), 500


@app.route('/download')
def download_file():
    """Download generated journal article"""
    try:
        output_file = session.get('output_file')
        output_filename = session.get('output_filename')
        
        if not output_file or not os.path.exists(output_file):
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(
            output_file,
            as_attachment=True,
            download_name=output_filename,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        
    except Exception as e:
        app.logger.error(f"Error downloading file: {str(e)}")
        return jsonify({'error': 'Download failed'}), 500


@app.route('/preview', methods=['POST'])
def preview():
    """Preview journal article before download"""
    try:
        data = request.get_json()
        # Generate preview HTML
        preview_html = f"""
        <div class="preview-container">
            <h1>{data.get('title', 'Judul Artikel')}</h1>
            <p class="authors">{data.get('authors', '')}</p>
            <h2>ABSTRACT</h2>
            <p>{data.get('abstract', '')}</p>
            <h2>ABSTRAK</h2>
            <p>{data.get('abstrak', '')}</p>
        </div>
        """
        return jsonify({'success': True, 'html': preview_html})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/check-references', methods=['POST'])
def check_references():
    """Check and validate references"""
    try:
        data = request.get_json()
        references = data.get('references', [])
        
        ref_manager = ReferenceManager()
        validation_result = ref_manager.validate_references(references)
        
        return jsonify({
            'success': True,
            'validation': validation_result
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/enhance-abstract', methods=['POST'])
def enhance_abstract():
    """Enhance abstract using AI"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        provider = data.get('provider', 'claude')
        
        ai_processor = AIProcessor(provider=provider)
        enhanced = ai_processor.enhance_abstract(text)
        
        return jsonify({
            'success': True,
            'enhanced_text': enhanced
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    })


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error"""
    return jsonify({
        'error': 'File terlalu besar. Maksimal 50MB per file.'
    }), 413


@app.errorhandler(500)
def internal_server_error(error):
    """Handle internal server error"""
    app.logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        'error': 'Terjadi kesalahan server. Silakan coba lagi.'
    }), 500


if __name__ == '__main__':
    # Development server
    app.run(debug=True, host='0.0.0.0', port=5000)
