# CIDE Milestone 4 - Quick Start Guide

## 🚀 Getting Started with New Features

### Prerequisites
```bash
# Ensure you have Python 3.6+ and Flask installed
python --version
pip install -r requirements.txt
```

### Starting the Application
```bash
# Start the Flask development server
python app.py

# Or use the interactive startup script
python start_web_app.py
```

The server will start at: **http://localhost:5000**

---

## 📄 Feature 1: Report Generation

### How to Use

1. **Analyze Files**
   - Go to http://localhost:5000
   - Upload two code files
   - Click "Analyze Files"

2. **Download Reports**
   - Scroll to the "Download Report" section
   - Choose your preferred format:
     - **Text (.txt)** - Best for terminal viewing
     - **JSON (.json)** - Best for API integration
     - **HTML (.html)** - Best for printing/sharing

3. **Report Contents**
   - File information and metadata
   - Similarity metrics (structure, sequence, weighted)
   - Plagiarism detection results
   - Code features comparison
   - Professional conclusions

### Example: Downloading a Text Report

```bash
# After analysis, click "Text Report (.txt)"
# File downloads as: cide_report_20251029_231235.txt
```

### Sample Report Preview

```
================================================================================
CODE SIMILARITY ANALYSIS REPORT
================================================================================
Generated: 2025-10-29 23:12:35

FILE INFORMATION
File 1: original_code.py
File 2: plagiarized_renamed.py
Analysis Mode: HYBRID

SIMILARITY ANALYSIS RESULTS
Overall Similarity: 87.2%
  - Structure Similarity: 100.0%
  - Sequence Similarity: 68.9%
  - Feature Similarity: 100.0%
Identical Structure: YES

PLAGIARISM DETECTION
Status: DETECTED
Confidence: 87.2%
Type: Exact Copy

CONCLUSION
⚠️  PLAGIARISM DETECTED
The analysis indicates a high degree of similarity between the submitted files.
================================================================================
```

---

## 📊 Feature 2: Batch Comparison

### How to Use

1. **Navigate to Batch Page**
   - Click "Batch Compare" in the navigation
   - Or go to http://localhost:5000/batch

2. **Select Multiple Files**
   - Click "Select Files"
   - Use Ctrl+Click (Windows) or Cmd+Click (Mac) to select multiple files
   - Or Shift+Click to select a range
   - Minimum: 2 files
   - Recommended: 3-10 files for best results

3. **Choose Analysis Mode**
   - **Hybrid** (Recommended) - AST + Text analysis
   - **Basic** - Text-only analysis

4. **Analyze**
   - Click "Analyze All Files"
   - Wait for processing (shows loading spinner)
   - View comprehensive results

### Understanding Results

#### 1. Summary Statistics
```
Files Analyzed: 5
Comparisons: 10 (all pairs)
Average Similarity: 62.3%
Max Similarity: 94.1% (file1.py <-> file2.py)
```

#### 2. Similarity Matrix
```
           file1  file2  file3  file4  file5
file1      100%   94%    45%    38%    52%
file2      94%    100%   42%    35%    49%
file3      45%    42%    100%   88%    91%
file4      38%    35%    88%    100%   85%
file5      52%    49%    91%    85%    100%
```

**Color Code:**
- 🟥 Red (75%+): High similarity - investigate for plagiarism
- 🟨 Yellow (50-75%): Moderate similarity - review recommended
- 🟩 Green (<50%): Low similarity - likely original

#### 3. File Rankings
Shows which files are most similar to others overall:

```
🥇 file1.py - 75.5%  (Most similar overall)
🥈 file3.py - 74.2%
🥉 file2.py - 68.9%
4. file5.py - 65.3%
5. file4.py - 61.5%  (Most unique)
```

**Interpretation:**
- Files at the top might be "template" or "source" files
- Files at the bottom are more original/unique

#### 4. Pairwise Comparisons
Detailed breakdown of each file pair, sorted by similarity:

```
file1.py ↔ file2.py: 94.1% (HIGH SIMILARITY) 🟥
file3.py ↔ file5.py: 91.0% (HIGH SIMILARITY) 🟥
file3.py ↔ file4.py: 88.0% (HIGH SIMILARITY) 🟥
file1.py ↔ file5.py: 52.0% (MODERATE) 🟨
...
```

### Use Cases

#### Academic Setting
```
# Check 20 student submissions for plagiarism
1. Upload all 20 Python files
2. Use Hybrid mode for accurate detection
3. Look for clusters in similarity matrix
4. Investigate pairs with 75%+ similarity
```

#### Code Review
```
# Find duplicate code across project modules
1. Upload all .py files from src/
2. Identify high similarity pairs
3. Refactor common code into shared modules
```

#### Quality Assurance
```
# Verify code originality in team project
1. Upload all team member contributions
2. Check for unusual similarity patterns
3. Review rankings to identify outliers
```

---

## 🧪 Testing Your Setup

### Test Report Generation
```bash
python test_reports.py
```

**Expected Output:**
```
✓ Text report generated successfully!
✓ JSON report generated successfully!
✓ HTML report generated successfully!
✓ Saved: sample_report.txt
✓ Saved: sample_report.json
✓ Saved: sample_report.html
```

### Test Batch Comparison
```bash
python batch_comparator.py
```

**Expected Output:**
```
Analyzed 3 files
Performed 3 comparisons
Average similarity: 74.5%
Most similar pair: file1.py <-> file2.py (88.8%)
```

### Run Comprehensive Tests
```bash
python test_milestone4.py
```

**Expected Output:**
```
✅ [TEST 1] Report Generator Module ............ PASSED
✅ [TEST 2] Batch Comparator Module ............ PASSED
✅ [TEST 3] Flask App Integration .............. PASSED
✅ [TEST 4] Template Files ..................... PASSED
✅ [TEST 5] Core Analysis Modules .............. PASSED
✅ [TEST 6] Sample Reports ..................... PASSED
🎉 ALL TESTS PASSED!
```

---

## 💡 Pro Tips

### Report Generation
- **Use HTML reports** for presentations or documentation
- **Use JSON reports** for automated processing or APIs
- **Use Text reports** for quick terminal viewing or logs

### Batch Comparison
- **Start with 3-5 files** to understand the interface
- **Use Hybrid mode** for Python files (more accurate)
- **Look for clusters** in the matrix - diagonal blocks indicate similar groups
- **Check rankings** to find potential "source" files

### Performance
- **Batch mode works best** with 2-50 files
- **Processing time:** ~200ms per file pair (Hybrid mode)
- **For 10 files:** ~9 seconds (45 comparisons)
- **For 20 files:** ~38 seconds (190 comparisons)

### Interpreting Results
- **Structure similarity 100% + Sequence 60-80%** = Renamed variables (plagiarism)
- **Structure similarity 80-90%** = Modified logic (possible plagiarism)
- **Structure similarity < 50%** = Different implementations (likely original)

---

## 🔧 Troubleshooting

### Issue: "No analysis result available"
**Solution:** Perform an analysis first before downloading reports

### Issue: Files not uploading
**Solutions:**
- Check file size (16MB limit)
- Verify file extension (.py, .java, .js, .cpp, .c, .h, .txt)
- Ensure files are text-based (not binary)

### Issue: Batch comparison taking too long
**Solutions:**
- Reduce number of files
- Use Basic mode instead of Hybrid
- Wait for MinHash implementation (coming soon)

### Issue: Syntax errors during analysis
**Solution:** Some test files intentionally have syntax errors - this is normal for testing edge cases

---

## 📚 Additional Resources

### Documentation
- [README.md](README.md) - Main project documentation
- [MILESTONE4_SUMMARY.md](MILESTONE4_SUMMARY.md) - Detailed feature documentation
- [MILESTONE4_COMPLETE.md](MILESTONE4_COMPLETE.md) - Implementation summary

### Example Files
- `examples/original_code.py` - Original implementations
- `examples/plagiarized_renamed.py` - Renamed variables example
- `examples/different_code.py` - Different implementation
- `sample_report.txt/json/html` - Example reports

### Test Files
- `test_milestone4.py` - Comprehensive feature tests
- `test_reports.py` - Report generation tests
- `test_ast_analyzer.py` - AST analysis tests

---

## 🎯 Quick Reference

### Navigation
```
Home Page:          http://localhost:5000/
Batch Comparison:   http://localhost:5000/batch
About:              http://localhost:5000/about
Health Check:       http://localhost:5000/api/health
```

### Keyboard Shortcuts
- **Ctrl+Click** (Windows) / **Cmd+Click** (Mac): Select multiple files
- **Shift+Click**: Select range of files
- **Ctrl+C**: Stop Flask server in terminal

### File Limits
- **Min files:** 2 (for any comparison)
- **Max file size:** 16MB per file
- **Recommended batch size:** 3-10 files
- **Supported extensions:** .py, .java, .js, .cpp, .c, .h, .txt

---

## 🚀 What's Next?

### Coming Soon
- **MinHash Algorithm** - Fast similarity estimation for large batches
- **Admin Dashboard** - Track all analyses and statistics
- **Database Storage** - Persistent analysis history
- **Production Features** - Rate limiting, API docs, authentication

### Stay Updated
Check the [README.md](README.md) for the latest features and updates!

---

**Happy Analyzing! 🎉**

Need help? Open an issue on GitHub or check the documentation files listed above.
