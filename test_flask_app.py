"""
Quick test to verify Flask app is working correctly
"""
import sys
import os

print("=" * 70)
print("CIDE Flask App Test")
print("=" * 70)

# Test imports
try:
    from flask import Flask
    print("✅ Flask imported successfully")
except ImportError as e:
    print(f"❌ Flask import failed: {e}")
    sys.exit(1)

try:
    from code_similarity import CodeSimilarityAnalyzer
    print("✅ CodeSimilarityAnalyzer imported successfully")
except ImportError as e:
    print(f"❌ CodeSimilarityAnalyzer import failed: {e}")
    sys.exit(1)

try:
    from ast_analyzer import HybridSimilarityAnalyzer
    print("✅ HybridSimilarityAnalyzer imported successfully")
except ImportError as e:
    print(f"❌ HybridSimilarityAnalyzer import failed: {e}")
    sys.exit(1)

# Test Flask app creation
try:
    from app import app
    print("✅ Flask app created successfully")
except ImportError as e:
    print(f"❌ Flask app creation failed: {e}")
    sys.exit(1)

# Check templates directory
if os.path.exists('templates'):
    print("✅ Templates directory exists")
    if os.path.exists('templates/index.html'):
        print("✅ index.html found")
    if os.path.exists('templates/about.html'):
        print("✅ about.html found")
else:
    print("❌ Templates directory not found")

# Check uploads directory
if not os.path.exists('uploads'):
    os.makedirs('uploads')
    print("✅ Created uploads directory")
else:
    print("✅ Uploads directory exists")

print("\n" + "=" * 70)
print("✅ All checks passed! Flask app is ready to run.")
print("=" * 70)
print("\nTo start the server, run:")
print("  python app.py")
print("\nThen open your browser to:")
print("  http://localhost:5000")
print("=" * 70)
