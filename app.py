"""
CIDE Web Application
====================
Flask-based web interface for Code Integrity Detection Engine.
Provides visual interface for code similarity analysis and plagiarism detection.
"""

from flask import Flask, render_template, request, jsonify, session
from werkzeug.utils import secure_filename
import os
import difflib
from pathlib import Path
import json
from datetime import datetime

# Import our analyzers
from code_similarity import CodeSimilarityAnalyzer
from ast_analyzer import HybridSimilarityAnalyzer

app = Flask(__name__)
app.secret_key = 'cide-secret-key-change-in-production'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'py', 'java', 'js', 'cpp', 'c', 'h', 'txt'}

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def get_file_language(filename):
    """Detect programming language from file extension."""
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else 'txt'
    language_map = {
        'py': 'python',
        'java': 'java',
        'js': 'javascript',
        'cpp': 'cpp',
        'c': 'c',
        'h': 'c',
        'txt': 'text'
    }
    return language_map.get(ext, 'text')


def generate_diff_html(code1, code2, filename1='File 1', filename2='File 2'):
    """Generate HTML for side-by-side diff view."""
    differ = difflib.HtmlDiff(wrapcolumn=80)
    code1_lines = code1.splitlines()
    code2_lines = code2.splitlines()
    
    diff_html = differ.make_table(
        code1_lines,
        code2_lines,
        fromdesc=filename1,
        todesc=filename2,
        context=True,
        numlines=3
    )
    
    return diff_html


@app.route('/')
def index():
    """Home page with file upload form."""
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze uploaded files for similarity."""
    try:
        # Check if files were uploaded
        if 'file1' not in request.files or 'file2' not in request.files:
            return jsonify({'error': 'Both files are required'}), 400
        
        file1 = request.files['file1']
        file2 = request.files['file2']
        
        # Check if files have names
        if file1.filename == '' or file2.filename == '':
            return jsonify({'error': 'Both files must be selected'}), 400
        
        # Validate file types
        if not (allowed_file(file1.filename) and allowed_file(file2.filename)):
            return jsonify({'error': f'Allowed file types: {", ".join(app.config["ALLOWED_EXTENSIONS"])}'}), 400
        
        # Read file contents
        code1 = file1.read().decode('utf-8')
        code2 = file2.read().decode('utf-8')
        
        # Get analysis mode from form
        mode = request.form.get('mode', 'hybrid')
        
        # Detect language
        language = get_file_language(file1.filename)
        
        # Initialize analyzers
        basic_analyzer = CodeSimilarityAnalyzer()
        
        # Perform analysis based on mode
        if mode == 'hybrid' and language == 'python':
            # Use hybrid analyzer for Python
            hybrid_analyzer = HybridSimilarityAnalyzer()
            ast_result = hybrid_analyzer.analyze(code1, code2)
            
            result = {
                'mode': 'hybrid',
                'language': language,
                'weighted_score': ast_result['weighted_score'],
                'weighted_percentage': ast_result['weighted_percentage'],
                'structure_similarity': ast_result['structure_similarity'],
                'sequence_similarity': ast_result['sequence_similarity'],
                'feature_similarity': ast_result['feature_similarity'],
                'identical_structure': ast_result['identical_structure'],
                'features1': ast_result['features1'],
                'features2': ast_result['features2'],
                'error': ast_result.get('error')
            }
            
            # Check for plagiarism
            plagiarism_result = hybrid_analyzer.detect_plagiarism(code1, code2, threshold=0.75)
            result['plagiarism'] = {
                'is_plagiarism': plagiarism_result['is_plagiarism'],
                'confidence': plagiarism_result['confidence'],
                'confidence_percentage': plagiarism_result['confidence_percentage'],
                'plagiarism_type': plagiarism_result['plagiarism_type']
            }
        else:
            # Use basic analyzer
            basic_result = basic_analyzer.analyze(code1, code2, mode='basic', language=language)
            
            result = {
                'mode': 'basic',
                'language': language,
                'similarity_score': basic_result['similarity_score'],
                'similarity_percentage': basic_result['similarity_percentage'],
                'code1_length': basic_result['code1_length'],
                'code2_length': basic_result['code2_length']
            }
        
        # Generate diff view
        diff_html = generate_diff_html(code1, code2, file1.filename, file2.filename)
        
        # Add metadata
        result['file1_name'] = file1.filename
        result['file2_name'] = file2.filename
        result['code1_lines'] = len(code1.splitlines())
        result['code2_lines'] = len(code2.splitlines())
        result['timestamp'] = datetime.now().isoformat()
        result['diff_html'] = diff_html
        
        return jsonify(result)
    
    except UnicodeDecodeError:
        return jsonify({'error': 'Unable to decode file. Please ensure files are text-based.'}), 400
    except Exception as e:
        return jsonify({'error': f'Analysis error: {str(e)}'}), 500


@app.route('/about')
def about():
    """About page with information about the tool."""
    return render_template('about.html')


@app.route('/api/health')
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'version': '2.0.0',
        'features': ['basic', 'ast', 'hybrid', 'plagiarism_detection']
    })


if __name__ == '__main__':
    print("=" * 70)
    print("🚀 CIDE - Code Integrity Detection Engine")
    print("=" * 70)
    print("Starting web server...")
    print("Access the application at: http://localhost:5000")
    print("=" * 70)
    app.run(debug=True, host='0.0.0.0', port=5000)
