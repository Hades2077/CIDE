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

## Installation

No external dependencies required! Uses Python standard library only.

```bash
# Python 3.6+ required
python --version
```

## Quick Start

### Basic Usage

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

result = analyzer.analyze(code1, code2)
print(f"Similarity: {result['similarity_percentage']}")
# Output: Similarity: 100.0% (after preprocessing removes comments)
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

```bash
# Run the built-in examples
python code_similarity.py

# Run the test suite
python test_similarity.py
```

## Project Structure

```
CIDE/
├── code_similarity.py      # Main module with analyzer logic
├── test_similarity.py      # Test suite
├── examples/
│   ├── example1.py        # Sample code file 1
│   ├── example2.py        # Sample code file 2 (similar to 1)
│   └── example3.py        # Sample code file 3 (different)
├── LICENSE
└── README.md
```

## API Reference

### CodeSimilarityAnalyzer

Main class for analyzing code similarity.

#### `analyze(input1, input2, preprocess=True, language='auto')`

Analyze similarity between two code inputs.

**Parameters:**
- `input1`: First code input (file path or text string)
- `input2`: Second code input (file path or text string)  
- `preprocess`: Whether to preprocess code (default: True)
- `language`: Language hint for preprocessing (default: 'auto')

**Returns:**
Dictionary containing:
- `similarity_score`: Float between 0.0 and 1.0
- `similarity_percentage`: String formatted percentage (e.g., "78.2%")
- `code1_length`: Character count of first code
- `code2_length`: Character count of second code
- `preprocessed_code1_length`: Character count after preprocessing
- `preprocessed_code2_length`: Character count after preprocessing

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

## Future Enhancements

Potential additions for future milestones:
- [ ] UI for file upload and comparison
- [ ] Support for more languages and comment styles
- [ ] AST-based comparison for semantic similarity
- [ ] Plagiarism detection features
- [ ] Batch comparison of multiple files
- [ ] Export results to JSON/CSV
