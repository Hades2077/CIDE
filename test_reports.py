"""
Test Report Generation
======================
Test the report generator with sample analysis data.
"""

from report_generator import generate_report

# Sample analysis result
sample_result = {
    'mode': 'hybrid',
    'language': 'python',
    'file1_name': 'original_code.py',
    'file2_name': 'plagiarized_renamed.py',
    'weighted_percentage': '87.2%',
    'weighted_score': 0.872,
    'structure_similarity': 1.0,
    'sequence_similarity': 0.689,
    'feature_similarity': 1.0,
    'identical_structure': True,
    'code1_lines': 50,
    'code2_lines': 52,
    'features1': {
        'functions': 3,
        'classes': 0,
        'loops': 4,
        'conditionals': 4
    },
    'features2': {
        'functions': 3,
        'classes': 0,
        'loops': 4,
        'conditionals': 4
    },
    'plagiarism': {
        'is_plagiarism': True,
        'confidence': 0.872,
        'confidence_percentage': '87.2%',
        'plagiarism_type': 'exact_copy'
    }
}

print("=" * 80)
print("TESTING REPORT GENERATION")
print("=" * 80)

# Test Text Report
print("\n1. Testing TEXT report generation...")
text_report = generate_report(sample_result, 'text')
print("✓ Text report generated successfully!")
print(f"   Length: {len(text_report)} characters")

# Test JSON Report
print("\n2. Testing JSON report generation...")
json_report = generate_report(sample_result, 'json')
print("✓ JSON report generated successfully!")
print(f"   Length: {len(json_report)} characters")

# Test HTML Report
print("\n3. Testing HTML report generation...")
html_report = generate_report(sample_result, 'html')
print("✓ HTML report generated successfully!")
print(f"   Length: {len(html_report)} characters")

print("\n" + "=" * 80)
print("ALL TESTS PASSED!")
print("=" * 80)

# Save sample reports
print("\nSaving sample reports to files...")

with open('sample_report.txt', 'w', encoding='utf-8') as f:
    f.write(text_report)
print("✓ Saved: sample_report.txt")

with open('sample_report.json', 'w', encoding='utf-8') as f:
    f.write(json_report)
print("✓ Saved: sample_report.json")

with open('sample_report.html', 'w', encoding='utf-8') as f:
    f.write(html_report)
print("✓ Saved: sample_report.html")

print("\n" + "=" * 80)
print("Preview of text report (first 500 characters):")
print("=" * 80)
print(text_report[:500] + "...")
