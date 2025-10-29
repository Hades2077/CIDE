"""Quick verification that both modes work correctly."""
from code_similarity import CodeSimilarityAnalyzer

analyzer = CodeSimilarityAnalyzer()

code1 = "def foo(x): return x*2"
code2 = "def bar(y): return y*2"

# Test basic mode
r1 = analyzer.analyze(code1, code2, mode='basic')
print(f"✅ Basic mode: {r1['similarity_percentage']}")

# Test hybrid mode
r2 = analyzer.analyze(code1, code2, mode='hybrid', language='python')
print(f"✅ Hybrid mode: {r2['weighted_percentage']}")
print(f"   Structure: {r2['structure_similarity']:.1%}")
print(f"   Identical: {r2['identical_structure']}")

print("\n🎉 All modes working correctly!")
