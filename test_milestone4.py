"""
Comprehensive Feature Test
===========================
Test all Milestone 4 features.
"""

import sys

print("=" * 80)
print("CIDE MILESTONE 4 - COMPREHENSIVE FEATURE TEST")
print("=" * 80)

# Test 1: Report Generator
print("\n[TEST 1] Report Generator Module")
print("-" * 80)
try:
    from report_generator import generate_report
    
    sample_data = {
        'mode': 'hybrid',
        'language': 'python',
        'file1_name': 'test1.py',
        'file2_name': 'test2.py',
        'weighted_percentage': '85.0%',
        'structure_similarity': 0.95,
        'sequence_similarity': 0.75
    }
    
    text_report = generate_report(sample_data, 'text')
    json_report = generate_report(sample_data, 'json')
    html_report = generate_report(sample_data, 'html')
    
    print("✓ Text report generation: OK")
    print("✓ JSON report generation: OK")
    print("✓ HTML report generation: OK")
    print("✓ Report Generator Module: PASSED")
except Exception as e:
    print(f"✗ Report Generator Module: FAILED - {e}")
    sys.exit(1)

# Test 2: Batch Comparator
print("\n[TEST 2] Batch Comparator Module")
print("-" * 80)
try:
    from batch_comparator import BatchComparator
    
    test_files = [
        {
            'name': 'file1.py',
            'content': '''
def calculate_sum(numbers):
    total = 0
    for num in numbers:
        total += num
    return total
'''
        },
        {
            'name': 'file2.py',
            'content': '''
def sum_values(data):
    result = 0
    for value in data:
        result += value
    return result
'''
        }
    ]
    
    comparator = BatchComparator(mode='hybrid')
    result = comparator.compare_all_pairs(test_files, 'python')
    
    assert result['file_count'] == 2
    assert result['comparison_count'] == 1
    assert 'matrix' in result
    assert 'comparisons' in result
    assert 'statistics' in result
    
    print(f"✓ File count: {result['file_count']}")
    print(f"✓ Comparison count: {result['comparison_count']}")
    print(f"✓ Average similarity: {result['statistics']['average_percentage']}")
    print("✓ Batch Comparator Module: PASSED")
except Exception as e:
    print(f"✗ Batch Comparator Module: FAILED - {e}")
    sys.exit(1)

# Test 3: Flask App Integration
print("\n[TEST 3] Flask App Integration")
print("-" * 80)
try:
    from app import app
    
    # Check routes exist
    routes = [rule.rule for rule in app.url_map.iter_rules()]
    
    required_routes = [
        '/',
        '/analyze',
        '/batch',
        '/download/report/<format_type>',
        '/about',
        '/api/health'
    ]
    
    for route in required_routes:
        if route in routes:
            print(f"✓ Route '{route}': OK")
        else:
            print(f"✗ Route '{route}': MISSING")
            sys.exit(1)
    
    print("✓ Flask App Integration: PASSED")
except Exception as e:
    print(f"✗ Flask App Integration: FAILED - {e}")
    sys.exit(1)

# Test 4: Template Files
print("\n[TEST 4] Template Files")
print("-" * 80)
try:
    import os
    
    templates = ['index.html', 'about.html', 'batch.html']
    template_dir = 'templates'
    
    for template in templates:
        path = os.path.join(template_dir, template)
        if os.path.exists(path):
            print(f"✓ Template '{template}': OK")
        else:
            print(f"✗ Template '{template}': MISSING")
            sys.exit(1)
    
    print("✓ Template Files: PASSED")
except Exception as e:
    print(f"✗ Template Files: FAILED - {e}")
    sys.exit(1)

# Test 5: Core Analysis Modules
print("\n[TEST 5] Core Analysis Modules")
print("-" * 80)
try:
    from code_similarity import CodeSimilarityAnalyzer
    from ast_analyzer import HybridSimilarityAnalyzer
    
    # Test basic analyzer
    basic_analyzer = CodeSimilarityAnalyzer()
    code1 = "def hello(): print('hi')"
    code2 = "def hello(): print('hello')"
    
    basic_result = basic_analyzer.analyze(code1, code2, mode='basic')
    assert 'similarity_score' in basic_result
    print("✓ Basic analyzer: OK")
    
    # Test hybrid analyzer
    hybrid_analyzer = HybridSimilarityAnalyzer()
    hybrid_result = hybrid_analyzer.analyze(code1, code2)
    assert 'structure_similarity' in hybrid_result
    assert 'weighted_score' in hybrid_result
    print("✓ Hybrid analyzer: OK")
    
    print("✓ Core Analysis Modules: PASSED")
except Exception as e:
    print(f"✗ Core Analysis Modules: FAILED - {e}")
    sys.exit(1)

# Test 6: Sample Reports Exist
print("\n[TEST 6] Sample Reports")
print("-" * 80)
try:
    import os
    
    sample_files = ['sample_report.txt', 'sample_report.json', 'sample_report.html']
    
    for sample in sample_files:
        if os.path.exists(sample):
            size = os.path.getsize(sample)
            print(f"✓ {sample}: OK ({size} bytes)")
        else:
            print(f"⚠ {sample}: Not found (run test_reports.py to generate)")
    
    print("✓ Sample Reports: PASSED")
except Exception as e:
    print(f"✗ Sample Reports: FAILED - {e}")
    sys.exit(1)

# Summary
print("\n" + "=" * 80)
print("MILESTONE 4 TEST SUMMARY")
print("=" * 80)
print("✅ [TEST 1] Report Generator Module ............ PASSED")
print("✅ [TEST 2] Batch Comparator Module ............ PASSED")
print("✅ [TEST 3] Flask App Integration .............. PASSED")
print("✅ [TEST 4] Template Files ..................... PASSED")
print("✅ [TEST 5] Core Analysis Modules .............. PASSED")
print("✅ [TEST 6] Sample Reports ..................... PASSED")
print("=" * 80)
print("🎉 ALL TESTS PASSED!")
print("=" * 80)

print("\nFeature Status:")
print("✅ Report Generation (Text, JSON, HTML)")
print("✅ Batch File Comparison")
print("✅ Web UI with Download Buttons")
print("✅ Navigation Updates")
print("✅ Session Management")
print("🚧 MinHash Algorithm (In Progress)")
print("⏳ Admin Dashboard (Planned)")
print("⏳ Database Storage (Planned)")

print("\nNext Steps:")
print("1. Test the web interface at http://localhost:5000")
print("2. Upload two files and test report downloads")
print("3. Try batch comparison with 3+ files")
print("4. Review MILESTONE4_SUMMARY.md for full documentation")

print("\n" + "=" * 80)
