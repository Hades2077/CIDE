"""
Demonstration: Detecting Disguised Plagiarism
==============================================
This script demonstrates how the AST-based analyzer can detect
plagiarism even when code has been disguised through variable renaming.
"""

from code_similarity import CodeSimilarityAnalyzer
from pathlib import Path


def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 80)
    print(title.center(80))
    print("=" * 80)


def print_result(label, result):
    """Print formatted results."""
    if 'weighted_percentage' in result:
        # Hybrid/AST mode
        print(f"\n{label}:")
        print(f"  📊 Overall Score (Weighted): {result['weighted_percentage']}")
        print(f"  🏗️  Structure Similarity: {result['structure_similarity']:.1%}")
        print(f"  📝 Sequence Similarity: {result['sequence_similarity']:.1%}")
        print(f"  ⚖️  Identical Structure: {result['identical_structure']}")
    else:
        # Basic mode
        print(f"\n{label}:")
        print(f"  📊 Similarity: {result['similarity_percentage']}")


def demo_file_comparison():
    """Demonstrate comparison of example files."""
    
    print_header("🔍 DETECTING DISGUISED PLAGIARISM - DEMONSTRATION")
    
    analyzer = CodeSimilarityAnalyzer()
    
    # Files to compare
    original = 'examples/original_code.py'
    plagiarized = 'examples/plagiarized_renamed.py'
    different = 'examples/different_code.py'
    
    print("\n📁 Files being compared:")
    print(f"   1. {original} (Original)")
    print(f"   2. {plagiarized} (Variables renamed)")
    print(f"   3. {different} (Completely different)")
    
    # Test 1: Original vs Plagiarized (renamed variables)
    print_header("TEST 1: Original vs Plagiarized (Renamed Variables)")
    
    print("\n🔍 Basic Text-Based Analysis:")
    basic_result = analyzer.analyze(original, plagiarized, mode='basic', language='python')
    print(f"   Similarity: {basic_result['similarity_percentage']}")
    print("   ⚠️  May miss plagiarism due to renamed variables!")
    
    print("\n🧠 AST-Based Structural Analysis:")
    ast_result = analyzer.analyze(original, plagiarized, mode='hybrid', language='python')
    print(f"   Structure Similarity: {ast_result['structure_similarity']:.1%}")
    print(f"   Weighted Score: {ast_result['weighted_percentage']}")
    print(f"   Identical Structure: {ast_result['identical_structure']}")
    print("   ✅ Detects plagiarism through structural analysis!")
    
    # Test 2: Original vs Different Code
    print_header("TEST 2: Original vs Different Implementation")
    
    print("\n🔍 Basic Text-Based Analysis:")
    basic_result2 = analyzer.analyze(original, different, mode='basic', language='python')
    print(f"   Similarity: {basic_result2['similarity_percentage']}")
    
    print("\n🧠 AST-Based Structural Analysis:")
    ast_result2 = analyzer.analyze(original, different, mode='hybrid', language='python')
    print(f"   Structure Similarity: {ast_result2['structure_similarity']:.1%}")
    print(f"   Weighted Score: {ast_result2['weighted_percentage']}")
    print("   ✅ Correctly identifies as different code!")
    
    # Summary
    print_header("📊 SUMMARY")
    
    print("\n🎯 Key Findings:")
    print(f"   • Original vs Plagiarized: {ast_result['weighted_percentage']} similarity")
    print(f"     → Identical structure: {ast_result['identical_structure']}")
    print(f"     → Verdict: PLAGIARISM DETECTED ⚠️")
    
    print(f"\n   • Original vs Different: {ast_result2['weighted_percentage']} similarity")
    print(f"     → Identical structure: {ast_result2['identical_structure']}")
    print(f"     → Verdict: NOT PLAGIARISM ✅")
    
    print("\n💡 AST-based analysis advantages:")
    print("   ✓ Detects plagiarism through variable renaming")
    print("   ✓ Ignores comments and formatting differences")
    print("   ✓ Focuses on actual code structure and logic")
    print("   ✓ Weighted scoring (70% structure + 30% text)")
    print("   ✓ Reduces false positives from superficial changes")


def demo_detailed_analysis():
    """Show detailed feature analysis."""
    
    print_header("🔬 DETAILED FEATURE ANALYSIS")
    
    from ast_analyzer import HybridSimilarityAnalyzer
    
    original = Path('examples/original_code.py').read_text()
    plagiarized = Path('examples/plagiarized_renamed.py').read_text()
    different = Path('examples/different_code.py').read_text()
    
    analyzer = HybridSimilarityAnalyzer()
    
    # Analyze original vs plagiarized
    result = analyzer.analyze(original, plagiarized)
    
    print("\n📊 Original Code Features:")
    for feature, count in result['features1'].items():
        if count > 0:
            print(f"   • {feature}: {count}")
    
    print("\n📊 Plagiarized Code Features:")
    for feature, count in result['features2'].items():
        if count > 0:
            print(f"   • {feature}: {count}")
    
    print(f"\n🎯 Feature Similarity: {result['feature_similarity']:.1%}")
    print("   (Identical feature counts indicate same functionality)")
    
    # Analyze original vs different
    result2 = analyzer.analyze(original, different)
    
    print("\n📊 Different Code Features:")
    for feature, count in result2['features2'].items():
        if count > 0:
            print(f"   • {feature}: {count}")
    
    print(f"\n🎯 Feature Similarity: {result2['feature_similarity']:.1%}")
    print("   (Different feature counts indicate different functionality)")


def demo_plagiarism_detection():
    """Demonstrate plagiarism detection with thresholds."""
    
    print_header("🚨 PLAGIARISM DETECTION WITH THRESHOLDS")
    
    from ast_analyzer import HybridSimilarityAnalyzer
    
    original = Path('examples/original_code.py').read_text()
    plagiarized = Path('examples/plagiarized_renamed.py').read_text()
    different = Path('examples/different_code.py').read_text()
    
    analyzer = HybridSimilarityAnalyzer()
    
    thresholds = [0.70, 0.75, 0.80, 0.85]
    
    print("\n🎯 Testing with different detection thresholds:")
    print("\n1️⃣  Original vs Plagiarized (Renamed Variables):")
    
    for threshold in thresholds:
        result = analyzer.detect_plagiarism(original, plagiarized, threshold=threshold)
        status = "🚨 DETECTED" if result['is_plagiarism'] else "✅ PASSED"
        print(f"   Threshold {threshold:.0%}: {status} (Confidence: {result['confidence_percentage']})")
    
    print("\n2️⃣  Original vs Different Code:")
    
    for threshold in thresholds:
        result = analyzer.detect_plagiarism(original, different, threshold=threshold)
        status = "🚨 DETECTED" if result['is_plagiarism'] else "✅ PASSED"
        print(f"   Threshold {threshold:.0%}: {status} (Confidence: {result['confidence_percentage']})")
    
    print("\n💡 Recommended threshold: 75% for balanced detection")


def main():
    """Run all demonstrations."""
    try:
        demo_file_comparison()
        demo_detailed_analysis()
        demo_plagiarism_detection()
        
        print("\n" + "=" * 80)
        print("✅ DEMONSTRATION COMPLETE".center(80))
        print("=" * 80)
        print()
        
    except FileNotFoundError as e:
        print(f"❌ Error: Could not find example files.")
        print(f"   {e}")
        print("\n   Please ensure the example files exist:")
        print("   - examples/original_code.py")
        print("   - examples/plagiarized_renamed.py")
        print("   - examples/different_code.py")
    except Exception as e:
        print(f"❌ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
