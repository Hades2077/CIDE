"""
Test script for Code Similarity Analyzer
Demonstrates various use cases
"""

from code_similarity import CodeSimilarityAnalyzer
from pathlib import Path


def test_file_comparison():
    """Test comparing code files."""
    analyzer = CodeSimilarityAnalyzer()
    
    print("=" * 70)
    print("TEST 1: Comparing example1.py and example2.py (similar with different comments)")
    print("=" * 70)
    
    result = analyzer.analyze(
        'examples/example1.py',
        'examples/example2.py',
        preprocess=True
    )
    
    print(f"✓ Similarity Score: {result['similarity_percentage']}")
    print(f"  - Original lengths: {result['code1_length']} vs {result['code2_length']} chars")
    print(f"  - After preprocessing: {result['preprocessed_code1_length']} vs {result['preprocessed_code2_length']} chars")
    print()
    
    print("=" * 70)
    print("TEST 2: Comparing example1.py and example3.py (different implementations)")
    print("=" * 70)
    
    result = analyzer.analyze(
        'examples/example1.py',
        'examples/example3.py',
        preprocess=True
    )
    
    print(f"✓ Similarity Score: {result['similarity_percentage']}")
    print(f"  - Original lengths: {result['code1_length']} vs {result['code2_length']} chars")
    print(f"  - After preprocessing: {result['preprocessed_code1_length']} vs {result['preprocessed_code2_length']} chars")
    print()


def test_text_comparison():
    """Test comparing code strings directly."""
    analyzer = CodeSimilarityAnalyzer()
    
    print("=" * 70)
    print("TEST 3: Comparing code strings directly")
    print("=" * 70)
    
    code1 = """
    function calculateSum(a, b) {
        // Add two numbers
        return a + b;
    }
    """
    
    code2 = """
    function calculateSum(a, b) {
        /* Add two numbers */
        return a + b;
    }
    """
    
    result = analyzer.analyze(code1, code2, preprocess=True)
    print(f"✓ Similarity Score: {result['similarity_percentage']}")
    print(f"  (Same code with different comment styles)")
    print()
    
    code3 = """
    function sumTwoNumbers(x, y) {
        return x + y;
    }
    """
    
    result = analyzer.analyze(code1, code3, preprocess=True)
    print(f"✓ Similarity Score: {result['similarity_percentage']}")
    print(f"  (Different function name and parameters)")
    print()


def test_preprocessing_impact():
    """Test the impact of preprocessing on similarity."""
    analyzer = CodeSimilarityAnalyzer()
    
    print("=" * 70)
    print("TEST 4: Preprocessing impact demonstration")
    print("=" * 70)
    
    code1 = """
def hello():
    # This is a comment
    print("Hello")
    """
    
    code2 = """
def HELLO():
    /* Different comment */
    print("Hello")
    """
    
    result_no_preprocess = analyzer.analyze(code1, code2, preprocess=False)
    result_with_preprocess = analyzer.analyze(code1, code2, preprocess=True)
    
    print(f"✓ Without preprocessing: {result_no_preprocess['similarity_percentage']}")
    print(f"✓ With preprocessing: {result_with_preprocess['similarity_percentage']}")
    print(f"  Preprocessing improved similarity by {(result_with_preprocess['similarity_score'] - result_no_preprocess['similarity_score']) * 100:.1f} percentage points")
    print()


def test_identical_code():
    """Test with identical code."""
    analyzer = CodeSimilarityAnalyzer()
    
    print("=" * 70)
    print("TEST 5: Identical code comparison")
    print("=" * 70)
    
    code = """
    class Calculator:
        def add(self, a, b):
            return a + b
    """
    
    result = analyzer.analyze(code, code, preprocess=True)
    print(f"✓ Similarity Score: {result['similarity_percentage']}")
    print(f"  (Should be 100% for identical code)")
    print()


def main():
    """Run all tests."""
    print("\n")
    print("🔍 CODE SIMILARITY ANALYZER - TEST SUITE")
    print("=" * 70)
    print()
    
    try:
        test_file_comparison()
        test_text_comparison()
        test_preprocessing_impact()
        test_identical_code()
        
        print("=" * 70)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        print()
        
    except FileNotFoundError as e:
        print(f"❌ Error: Could not find example files. Please ensure they exist.")
        print(f"   {e}")
    except Exception as e:
        print(f"❌ Error during testing: {e}")


if __name__ == "__main__":
    main()
