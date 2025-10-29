# Running the CIDE Web Application

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. **Install Flask** (if not already installed):
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Option 1: Direct Run
```bash
python app.py
```

### Option 2: Flask CLI
```bash
# On Windows PowerShell:
$env:FLASK_APP = "app.py"
flask run

# On Linux/Mac:
export FLASK_APP=app.py
flask run
```

## Accessing the Application

Once running, open your browser and navigate to:
```
http://localhost:5000
```

You should see the CIDE web interface!

## Features

### Home Page (/)
- **Upload Interface**: Drag & drop or click to upload two code files
- **Analysis Mode Selection**: 
  - Basic Text Analysis
  - Hybrid AST Analysis (Recommended for Python)
- **Real-time Analysis**: See results immediately after upload

### Results Page
After analysis, you'll see:

1. **Summary Cards**:
   - Overall Similarity Score
   - Structure Match Percentage
   - Plagiarism Detection Status

2. **Interactive Chart**:
   - Visual breakdown of similarity metrics
   - Color-coded bars for different aspects

3. **Code Features**:
   - Function count
   - Class count
   - Loop count
   - Conditional statements
   - Line count

4. **Side-by-Side Diff**:
   - Visual comparison of the two files
   - Highlighted differences
   - Toggle visibility

### About Page (/about)
- Detailed information about CIDE
- How it works
- Detection capabilities
- Use cases
- Technical details

## Supported File Types

- `.py` - Python
- `.java` - Java
- `.js` - JavaScript
- `.cpp`, `.c`, `.h` - C/C++
- `.txt` - Plain text

## Tips for Best Results

1. **Use Hybrid Mode for Python**: Get the most accurate results with AST-based analysis
2. **Check File Size**: Files should be under 16MB
3. **Use UTF-8 Encoding**: Ensure files are text-based and UTF-8 encoded
4. **Compare Similar Languages**: For best results, compare files in the same language

## Troubleshooting

### Port Already in Use
If port 5000 is already in use, change it in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change to 5001 or any available port
```

### Module Not Found Error
Make sure all dependencies are installed:
```bash
pip install Flask
```

### Upload Folder Issues
The app will automatically create an `uploads/` folder. If you encounter permission issues, create it manually:
```bash
mkdir uploads
```

## Security Notes

⚠️ **For Production Use**:
- Change the `app.secret_key` in `app.py`
- Set `debug=False`
- Use a production WSGI server (gunicorn, uWSGI)
- Implement proper authentication
- Add rate limiting
- Sanitize file uploads

## Development Mode

The app runs in debug mode by default, which:
- Auto-reloads on code changes
- Shows detailed error messages
- Enables debug toolbar

To disable debug mode:
```python
app.run(debug=False, host='0.0.0.0', port=5000)
```

## API Endpoints

### POST /analyze
Upload and analyze two code files.

**Form Data**:
- `file1`: First code file
- `file2`: Second code file
- `mode`: Analysis mode ('basic' or 'hybrid')

**Response**: JSON with analysis results

### GET /api/health
Health check endpoint.

**Response**: JSON with status and version info

## Next Steps

- Try uploading the example files from `examples/` folder
- Compare `original_code.py` with `plagiarized_renamed.py` to see plagiarism detection in action
- Experiment with different analysis modes
- Check the visual diff to see code differences highlighted

Enjoy using CIDE! 🚀
