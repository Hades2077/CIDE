"""
Web App Quick Start Demo
========================
This script demonstrates how easy it is to start the CIDE web application.
"""

import sys
import os

def print_header(text):
    print("\n" + "=" * 70)
    print(text.center(70))
    print("=" * 70)

def check_prerequisites():
    """Check if all prerequisites are met."""
    print_header("🔍 Checking Prerequisites")
    
    issues = []
    
    # Check Flask
    try:
        import flask
        print(f"✅ Flask {flask.__version__} installed")
    except ImportError:
        print("❌ Flask not installed")
        issues.append("Flask")
    
    # Check code_similarity module
    try:
        from code_similarity import CodeSimilarityAnalyzer
        print("✅ CodeSimilarityAnalyzer available")
    except ImportError:
        print("❌ code_similarity.py not found")
        issues.append("code_similarity")
    
    # Check ast_analyzer module
    try:
        from ast_analyzer import HybridSimilarityAnalyzer
        print("✅ HybridSimilarityAnalyzer available")
    except ImportError:
        print("❌ ast_analyzer.py not found")
        issues.append("ast_analyzer")
    
    # Check templates
    if os.path.exists('templates'):
        if os.path.exists('templates/index.html'):
            print("✅ templates/index.html found")
        else:
            print("❌ templates/index.html missing")
            issues.append("index.html")
        
        if os.path.exists('templates/about.html'):
            print("✅ templates/about.html found")
        else:
            print("❌ templates/about.html missing")
            issues.append("about.html")
    else:
        print("❌ templates/ directory missing")
        issues.append("templates directory")
    
    return issues

def print_instructions():
    """Print instructions for running the app."""
    print_header("🚀 Starting CIDE Web Application")
    
    print("\n📋 What the web app provides:")
    print("   • Beautiful, modern interface")
    print("   • Drag & drop file upload")
    print("   • Interactive charts and visualizations")
    print("   • Side-by-side code comparison")
    print("   • Real-time plagiarism detection")
    print("   • Comprehensive analysis results")
    
    print("\n🌐 Access Methods:")
    print("   1. http://localhost:5000")
    print("   2. http://127.0.0.1:5000")
    
    print("\n📄 Available Pages:")
    print("   • Home (/) - Upload and analyze files")
    print("   • About (/about) - Documentation and info")
    
    print("\n💡 Quick Demo:")
    print("   1. Go to http://localhost:5000")
    print("   2. Upload examples/original_code.py as File 1")
    print("   3. Upload examples/plagiarized_renamed.py as File 2")
    print("   4. Select 'Hybrid AST Analysis' mode")
    print("   5. Click 'Analyze Code Similarity'")
    print("   6. See plagiarism detected with 87.2% similarity!")
    
    print("\n⚠️  To stop the server:")
    print("   Press Ctrl+C in this terminal")

def main():
    """Main function."""
    print_header("🎉 CIDE Web Application Quick Start")
    
    # Check prerequisites
    issues = check_prerequisites()
    
    if issues:
        print("\n" + "=" * 70)
        print("❌ Prerequisites not met! Please fix the following:")
        for issue in issues:
            print(f"   • {issue}")
        print("\nTo install Flask: pip install Flask")
        print("=" * 70)
        return
    
    # Print instructions
    print_instructions()
    
    print("\n" + "=" * 70)
    print("✅ All checks passed! Ready to start server.")
    print("=" * 70)
    
    # Ask user if they want to start
    print("\n🚀 Start the Flask server now? (yes/no): ", end="")
    response = input().lower().strip()
    
    if response in ['yes', 'y']:
        print("\n" + "=" * 70)
        print("Starting Flask server...")
        print("=" * 70)
        print()
        
        try:
            from app import app
            app.run(debug=True, host='0.0.0.0', port=5000)
        except KeyboardInterrupt:
            print("\n\n" + "=" * 70)
            print("🛑 Server stopped by user")
            print("=" * 70)
        except Exception as e:
            print(f"\n❌ Error starting server: {e}")
    else:
        print("\n💡 When ready to start, run:")
        print("   python app.py")
        print("\n   Or run this script again:")
        print("   python start_web_app.py")

if __name__ == "__main__":
    main()
