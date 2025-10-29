# CIDE
Code Integrity Detection Engine

## Overview

A Python tool for computing similarity between two code files.

## Milestone 1: Foundation - Similarity Computation ✅

### Features

- ✅ Accepts two code inputs (via file path or direct text)
- ✅ Preprocesses code by:
  - Stripping comments (C-style `//`, `/* */` and Python-style `#`, `''' '''`)
  - Normalizing whitespace
  - Normalizing casing
- ✅ Uses `difflib.SequenceMatcher` to compute similarity score
- ✅ Returns percentage match (e.g., "Similarity: 78.2%")

## Milestone 2: AST-Based Structural Analysis ✅

### Advanced Features

- 🧠 **AST (Abstract Syntax Tree) Parsing** - Parses Python code into structural representation
- 🔄 **Variable Normalization** - Replaces variable names, function names, and constants with generic placeholders
- 🏗️ **Structural Comparison** - Compares code structure rather than raw text
- ⚖️ **Weighted Scoring Model** - 70% structure similarity + 30% sequence similarity
- 🚨 **Plagiarism Detection** - Detects "disguised plagiarism" through:
  - Variable/function renaming
  - Comment additions/removals
  - Whitespace/formatting changes
  - Code reordering (partial detection)

## Milestone 3: Web UI & Visualization ✅

### User Interface Features

- 🌐 **Flask Web Application** - Clean, modern web interface
- 🎨 **Tailwind CSS Design** - Responsive, beautiful UI
- 📤 **File Upload** - Drag & drop or click to upload code files
- 📊 **Interactive Charts** - Visual breakdown of similarity metrics using Chart.js
- 🔍 **Side-by-Side Diff** - Visual code comparison with highlighting
- 📈 **Results Dashboard** - Comprehensive analysis with:
  - Overall similarity score
  - Structure match percentage
  - Plagiarism detection status
  - Feature comparison (functions, classes, loops, etc.)
  - Code metrics and statistics
- ⚡ **Real-time Analysis** - Instant results after upload
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile

## Installation

### For Command-Line Use
No external dependencies required! Uses Python standard library only.

```bash
# Python 3.6+ required
python --version
```

### For Web Application
Install Flask to run the web interface:

```bash
# Install dependencies
pip install -r requirements.txt

# Or install Flask directly
pip install Flask
```

## Quick Start

### Option 1: Web Interface (Recommended) 🌐

```bash
# Start the Flask server
python app.py

# Open browser to http://localhost:5000
# Upload two files and see results instantly!
```

See [WEB_APP_GUIDE.md](WEB_APP_GUIDE.md) for detailed instructions.

### Option 2: Command-Line / Python Script

#### Basic Text-Based Analysis

```python
from code_similarity import CodeSimilarityAnalyzer

# Create analyzer instance
analyzer = CodeSimilarityAnalyzer()

# Compare two code strings
code1 = """
def hello():
    print("Hello World")
"""

code2 = """
def hello():
    # Comment here
    print("Hello World")
"""

# Basic mode (text-based)
result = analyzer.analyze(code1, code2, mode='basic')
print(f"Similarity: {result['similarity_percentage']}")
```

### AST-Based Structural Analysis

```python
# Hybrid mode (70% structure + 30% text) - RECOMMENDED
result = analyzer.analyze(code1, code2, mode='hybrid', language='python')
print(f"Structure Similarity: {result['structure_similarity']:.1%}")
print(f"Weighted Score: {result['weighted_percentage']}")
print(f"Identical Structure: {result['identical_structure']}")
```

### Detect Disguised Plagiarism

```python
from ast_analyzer import HybridSimilarityAnalyzer

analyzer = HybridSimilarityAnalyzer()

original = """
def calculate_sum(numbers):
    total = 0
    for num in numbers:
        total += num
    return total
"""

# Code with renamed variables (disguised plagiarism)
suspicious = """
def calculate_sum(data):
    result = 0
    for value in data:
        result += value
    return result
"""

# Detect plagiarism
result = analyzer.detect_plagiarism(original, suspicious, threshold=0.75)
print(f"Is Plagiarism: {result['is_plagiarism']}")
print(f"Confidence: {result['confidence_percentage']}")
print(f"Type: {result['plagiarism_type']}")
# Output: Is Plagiarism: True, Type: exact_copy (100% structure match!)
```

### Compare Files

```python
# Compare two files
result = analyzer.analyze('file1.py', 'file2.py')
print(f"Similarity: {result['similarity_percentage']}")
```

### Without Preprocessing

```python
# Compare without preprocessing (keeps comments, whitespace, casing)
result = analyzer.analyze(code1, code2, preprocess=False)
print(f"Similarity: {result['similarity_percentage']}")
```

## Running Examples

### Web Interface
```bash
# Start the web server
python app.py
# Then open http://localhost:5000 in your browser
```

### Command-Line Examples
```bash
# Run basic text-based examples
python code_similarity.py

# Run basic test suite
python test_similarity.py

# Run AST-based analyzer examples
python ast_analyzer.py

# Run comprehensive plagiarism detection tests
python test_ast_analyzer.py

# Run interactive demonstration
python demo_plagiarism_detection.py

# Test Flask app configuration
python test_flask_app.py
```

## Project Structure

```
CIDE/
├── app.py                          # Flask web application
├── code_similarity.py              # Main module with basic & hybrid analyzers
├── ast_analyzer.py                 # AST-based structural analyzer
├── templates/
│   ├── index.html                 # Main web interface
│   └── about.html                 # About page
├── uploads/                        # Upload directory (auto-created)
├── test_similarity.py              # Basic analysis test suite
├── test_ast_analyzer.py            # AST analysis comprehensive tests
├── test_flask_app.py               # Flask app configuration test
├── demo_plagiarism_detection.py    # Interactive CLI demonstration
├── examples/
│   ├── example1.py                # Basic sample 1
│   ├── example2.py                # Basic sample 2 (similar)
│   ├── example3.py                # Basic sample 3 (different)
│   ├── original_code.py           # Original implementation
│   ├── plagiarized_renamed.py     # Plagiarized (renamed variables)
│   └── different_code.py          # Completely different code
├── requirements.txt                # Python dependencies
├── WEB_APP_GUIDE.md               # Web app usage guide
├── MILESTONE2_SUMMARY.md          # Milestone 2 documentation
├── LICENSE
└── README.md
```

## API Reference

### CodeSimilarityAnalyzer

Main class for analyzing code similarity.

#### `analyze(input1, input2, preprocess=True, language='auto', mode='basic')`

Analyze similarity between two code inputs.

**Parameters:**
- `input1`: First code input (file path or text string)
- `input2`: Second code input (file path or text string)  
- `preprocess`: Whether to preprocess code (default: True)
- `language`: Language hint for preprocessing (default: 'auto')
- `mode`: Analysis mode - 'basic', 'ast', or 'hybrid' (default: 'basic')

**Returns (Basic Mode):**
- `mode`: 'basic'
- `similarity_score`: Float between 0.0 and 1.0
- `similarity_percentage`: String formatted percentage
- `code1_length`: Character count of first code
- `code2_length`: Character count of second code

**Returns (Hybrid/AST Mode):**
- `mode`: 'hybrid' or 'ast'
- `structure_similarity`: Structural similarity (0.0 to 1.0)
- `sequence_similarity`: Text sequence similarity (0.0 to 1.0)
- `weighted_score`: Weighted overall score (0.0 to 1.0)
- `weighted_percentage`: Formatted percentage
- `identical_structure`: Boolean - true if AST structures are identical
- `features1` / `features2`: Code feature counts (functions, classes, loops, etc.)
- `feature_similarity`: Similarity of feature counts (0.0 to 1.0)

### CodePreprocessor

Handles preprocessing of code inputs.

#### `preprocess(code, language='auto')`

Apply all preprocessing steps to code.

**Steps:**
1. Remove comments
2. Normalize whitespace
3. Normalize casing (lowercase)

## How It Works

1. **Input Reading**: Accepts either file paths or direct code strings
2. **Preprocessing** (optional):
   - Removes all comments (supports `//, /* */, #, ''' '''`)
   - Strips extra whitespace and empty lines
   - Converts to lowercase for case-insensitive comparison
3. **Similarity Computation**: Uses Python's `difflib.SequenceMatcher` to compute similarity ratio
4. **Output**: Returns detailed results including percentage match

### HybridSimilarityAnalyzer

Advanced analyzer combining structural and sequence-based analysis.

#### `analyze(code1, code2, language='python')`

Perform hybrid analysis on two code samples.

**Parameters:**
- `code1`: First code string
- `code2`: Second code string
- `language`: Programming language (currently only 'python' supported)

**Returns:**
Dictionary with detailed metrics (see above)

#### `detect_plagiarism(code1, code2, threshold=0.75)`

Detect potential plagiarism between code samples.

**Parameters:**
- `code1`: First code string
- `code2`: Second code string
- `threshold`: Similarity threshold for detection (default: 0.75)

**Returns:**
- `is_plagiarism`: Boolean
- `confidence`: Confidence score (0.0 to 1.0)
- `confidence_percentage`: Formatted percentage
- `plagiarism_type`: 'exact_copy', 'renamed_variables', 'restructured_code', or 'none'
- `analysis`: Full analysis results

## How It Works

### Basic Mode
1. **Input Reading**: File paths or direct code strings
2. **Preprocessing**: Remove comments, normalize whitespace/casing
3. **Text Comparison**: Use `difflib.SequenceMatcher`
4. **Output**: Similarity percentage

### AST/Hybrid Mode
1. **Parse**: Convert code to Abstract Syntax Tree
2. **Normalize**: Replace names with placeholders (VAR_0, FUNC_0, etc.)
3. **Structure Extraction**: Extract code patterns and features
4. **Comparison**: Compare normalized structures
5. **Weighted Scoring**: 70% structure + 30% text sequence
6. **Output**: Detailed metrics including plagiarism detection

### Why AST-Based Analysis?

Traditional text-based comparison can be fooled by:
- ✗ Renaming variables/functions
- ✗ Adding/removing comments
- ✗ Changing formatting/whitespace
- ✗ Reordering code blocks

AST-based analysis detects:
- ✓ **Identical structure** despite variable renaming
- ✓ **Same logic flow** regardless of formatting
- ✓ **Feature similarity** (loops, conditionals, functions)
- ✓ **Semantic equivalence** through structural patterns

**Real-world example from tests:**
- Basic text comparison: **10.5%** similarity
- AST-based comparison: **100%** structure match (87.2% weighted)
- Verdict: **Plagiarism detected!** 🚨

## Milestone 4: Professional Features (In Progress) 🚧

### Production-Ready Enhancements

- ✅ **Report Generation** - Download analysis reports in 3 formats:
  - 📄 Text reports (.txt) - Terminal-friendly
  - 📊 JSON reports (.json) - API integration
  - 🌐 HTML reports (.html) - Printable/shareable
- ✅ **Batch Comparison** - Compare multiple files simultaneously:
  - All-pairs similarity matrix (NxN comparison)
  - Statistical analysis (avg, min, max similarity)
  - File rankings by average similarity
  - Color-coded visualization (red/yellow/green)
  - Pairwise detailed comparisons
- 🚧 **MinHash Algorithm** - Fast similarity estimation (In Progress)
  - LSH (Locality-Sensitive Hashing)
  - O(1) similarity checks for scalability
  - Pre-filtering for large batches
- ⏳ **Admin Dashboard** - Track all analyses (Planned)
- ⏳ **Database Storage** - Analysis history with SQLite/PostgreSQL (Planned)
- ⏳ **Production Features** - Rate limiting, API docs, user sessions (Planned)

See [MILESTONE4_SUMMARY.md](MILESTONE4_SUMMARY.md) for detailed documentation.

## Future Enhancements

Potential additions for future milestones:
- [x] ~~UI for file upload and comparison~~ ✅
- [ ] Support for more languages (JavaScript, Java, C++, etc.)
- [x] ~~AST-based comparison for semantic similarity~~ ✅
- [x] ~~Plagiarism detection features~~ ✅
- [x] ~~Batch comparison of multiple files~~ ✅
- [x] ~~Export results to JSON/CSV~~ ✅
- [x] ~~Code diff visualization~~ ✅
- [ ] Machine learning-based similarity detection
- [ ] GitHub integration for repository scanning
- [ ] Real-time collaboration features
