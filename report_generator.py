"""
Report Generator for CIDE
=========================
Generates professional PDF and text reports for code similarity analysis.
"""

from datetime import datetime
from typing import Dict, Any, List
import json


class ReportGenerator:
    """Generates analysis reports in various formats."""
    
    def __init__(self):
        self.timestamp = datetime.now()
    
    def generate_text_report(self, analysis_result: Dict[str, Any]) -> str:
        """
        Generate a text-based report.
        
        Args:
            analysis_result: Dictionary containing analysis results
            
        Returns:
            Formatted text report
        """
        report = []
        report.append("=" * 80)
        report.append("CODE SIMILARITY ANALYSIS REPORT")
        report.append("=" * 80)
        report.append(f"Generated: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # File Information
        report.append("-" * 80)
        report.append("FILE INFORMATION")
        report.append("-" * 80)
        report.append(f"File 1: {analysis_result.get('file1_name', 'Unknown')}")
        report.append(f"File 2: {analysis_result.get('file2_name', 'Unknown')}")
        report.append(f"Analysis Mode: {analysis_result.get('mode', 'Unknown').upper()}")
        report.append(f"Language: {analysis_result.get('language', 'Unknown')}")
        report.append("")
        
        # Overall Results
        report.append("-" * 80)
        report.append("SIMILARITY ANALYSIS RESULTS")
        report.append("-" * 80)
        
        if analysis_result.get('mode') == 'hybrid':
            report.append(f"Overall Similarity: {analysis_result.get('weighted_percentage', 'N/A')}")
            report.append(f"  - Structure Similarity: {analysis_result.get('structure_similarity', 0) * 100:.1f}%")
            report.append(f"  - Sequence Similarity: {analysis_result.get('sequence_similarity', 0) * 100:.1f}%")
            report.append(f"  - Feature Similarity: {analysis_result.get('feature_similarity', 0) * 100:.1f}%")
            report.append(f"Identical Structure: {'YES' if analysis_result.get('identical_structure') else 'NO'}")
        else:
            report.append(f"Text Similarity: {analysis_result.get('similarity_percentage', 'N/A')}")
        
        report.append("")
        
        # Plagiarism Detection
        if 'plagiarism' in analysis_result:
            report.append("-" * 80)
            report.append("PLAGIARISM DETECTION")
            report.append("-" * 80)
            plag = analysis_result['plagiarism']
            status = "DETECTED" if plag['is_plagiarism'] else "NOT DETECTED"
            report.append(f"Status: {status}")
            report.append(f"Confidence: {plag['confidence_percentage']}")
            report.append(f"Type: {plag['plagiarism_type'].replace('_', ' ').title()}")
            report.append("")
        
        # Code Features
        if 'features1' in analysis_result and 'features2' in analysis_result:
            report.append("-" * 80)
            report.append("CODE FEATURES COMPARISON")
            report.append("-" * 80)
            
            f1 = analysis_result['features1']
            f2 = analysis_result['features2']
            
            report.append(f"{'Feature':<20} {'File 1':>15} {'File 2':>15} {'Match':>10}")
            report.append("-" * 65)
            
            for feature in f1.keys():
                count1 = f1.get(feature, 0)
                count2 = f2.get(feature, 0)
                match = "✓" if count1 == count2 else "✗"
                report.append(f"{feature.title():<20} {count1:>15} {count2:>15} {match:>10}")
            
            report.append("")
        
        # Code Metrics
        report.append("-" * 80)
        report.append("CODE METRICS")
        report.append("-" * 80)
        report.append(f"File 1 Lines: {analysis_result.get('code1_lines', 'N/A')}")
        report.append(f"File 2 Lines: {analysis_result.get('code2_lines', 'N/A')}")
        report.append("")
        
        # Conclusion
        report.append("-" * 80)
        report.append("CONCLUSION")
        report.append("-" * 80)
        
        if 'plagiarism' in analysis_result:
            if analysis_result['plagiarism']['is_plagiarism']:
                report.append("⚠️  PLAGIARISM DETECTED")
                report.append("")
                report.append("The analysis indicates a high degree of similarity between the")
                report.append("submitted files. The code structure and logic are substantially")
                report.append("similar, suggesting potential plagiarism.")
            else:
                report.append("✓ NO PLAGIARISM DETECTED")
                report.append("")
                report.append("The analysis indicates the files are sufficiently different.")
                report.append("The code appears to be original work.")
        else:
            similarity = analysis_result.get('similarity_score', 0) * 100
            if similarity > 75:
                report.append("⚠️  HIGH SIMILARITY")
            elif similarity > 50:
                report.append("⚠️  MODERATE SIMILARITY")
            else:
                report.append("✓ LOW SIMILARITY")
        
        report.append("")
        report.append("=" * 80)
        report.append("End of Report")
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def generate_json_report(self, analysis_result: Dict[str, Any]) -> str:
        """
        Generate a JSON report.
        
        Args:
            analysis_result: Dictionary containing analysis results
            
        Returns:
            JSON formatted report
        """
        report = {
            'report_metadata': {
                'generated_at': self.timestamp.isoformat(),
                'tool': 'CIDE - Code Integrity Detection Engine',
                'version': '2.0.0'
            },
            'analysis_result': analysis_result
        }
        
        return json.dumps(report, indent=2)
    
    def generate_html_report(self, analysis_result: Dict[str, Any]) -> str:
        """
        Generate an HTML report suitable for PDF conversion.
        
        Args:
            analysis_result: Dictionary containing analysis results
            
        Returns:
            HTML formatted report
        """
        
        # Determine status and color
        if 'plagiarism' in analysis_result:
            is_plagiarism = analysis_result['plagiarism']['is_plagiarism']
            status = "PLAGIARISM DETECTED" if is_plagiarism else "NO PLAGIARISM"
            status_color = "#dc2626" if is_plagiarism else "#16a34a"
        else:
            similarity = analysis_result.get('similarity_score', 0) * 100
            status = f"{similarity:.1f}% SIMILAR"
            status_color = "#dc2626" if similarity > 75 else "#16a34a"
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>CIDE Analysis Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
            background: #f9fafb;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}
        .header h1 {{
            margin: 0 0 10px 0;
            font-size: 32px;
        }}
        .header p {{
            margin: 5px 0;
            opacity: 0.9;
        }}
        .section {{
            background: white;
            padding: 25px;
            margin-bottom: 20px;
            border-radius: 10px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        .section h2 {{
            color: #667eea;
            margin-top: 0;
            padding-bottom: 10px;
            border-bottom: 2px solid #e5e7eb;
        }}
        .status-badge {{
            display: inline-block;
            padding: 10px 20px;
            background: {status_color};
            color: white;
            border-radius: 5px;
            font-weight: bold;
            font-size: 18px;
            margin: 10px 0;
        }}
        .metric {{
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #f3f4f6;
        }}
        .metric:last-child {{
            border-bottom: none;
        }}
        .metric-label {{
            font-weight: 600;
            color: #374151;
        }}
        .metric-value {{
            color: #6b7280;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e5e7eb;
        }}
        th {{
            background: #f9fafb;
            font-weight: 600;
            color: #374151;
        }}
        .footer {{
            text-align: center;
            color: #6b7280;
            margin-top: 30px;
            padding: 20px;
            border-top: 2px solid #e5e7eb;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Code Similarity Analysis Report</h1>
        <p>Generated: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>CIDE - Code Integrity Detection Engine v2.0</p>
    </div>
    
    <div class="section">
        <h2>📁 File Information</h2>
        <div class="metric">
            <span class="metric-label">File 1:</span>
            <span class="metric-value">{analysis_result.get('file1_name', 'Unknown')}</span>
        </div>
        <div class="metric">
            <span class="metric-label">File 2:</span>
            <span class="metric-value">{analysis_result.get('file2_name', 'Unknown')}</span>
        </div>
        <div class="metric">
            <span class="metric-label">Analysis Mode:</span>
            <span class="metric-value">{analysis_result.get('mode', 'Unknown').upper()}</span>
        </div>
        <div class="metric">
            <span class="metric-label">Language:</span>
            <span class="metric-value">{analysis_result.get('language', 'Unknown')}</span>
        </div>
    </div>
    
    <div class="section">
        <h2>📈 Similarity Analysis</h2>
        <div style="text-align: center;">
            <div class="status-badge">{status}</div>
        </div>
"""
        
        if analysis_result.get('mode') == 'hybrid':
            html += f"""
        <div class="metric">
            <span class="metric-label">Overall Similarity (Weighted):</span>
            <span class="metric-value">{analysis_result.get('weighted_percentage', 'N/A')}</span>
        </div>
        <div class="metric">
            <span class="metric-label">Structure Similarity:</span>
            <span class="metric-value">{analysis_result.get('structure_similarity', 0) * 100:.1f}%</span>
        </div>
        <div class="metric">
            <span class="metric-label">Sequence Similarity:</span>
            <span class="metric-value">{analysis_result.get('sequence_similarity', 0) * 100:.1f}%</span>
        </div>
        <div class="metric">
            <span class="metric-label">Feature Similarity:</span>
            <span class="metric-value">{analysis_result.get('feature_similarity', 0) * 100:.1f}%</span>
        </div>
        <div class="metric">
            <span class="metric-label">Identical Structure:</span>
            <span class="metric-value">{'YES' if analysis_result.get('identical_structure') else 'NO'}</span>
        </div>
"""
        else:
            html += f"""
        <div class="metric">
            <span class="metric-label">Text Similarity:</span>
            <span class="metric-value">{analysis_result.get('similarity_percentage', 'N/A')}</span>
        </div>
"""
        
        html += """
    </div>
"""
        
        # Plagiarism section
        if 'plagiarism' in analysis_result:
            plag = analysis_result['plagiarism']
            html += f"""
    <div class="section">
        <h2>🚨 Plagiarism Detection</h2>
        <div class="metric">
            <span class="metric-label">Detection Status:</span>
            <span class="metric-value">{'DETECTED' if plag['is_plagiarism'] else 'NOT DETECTED'}</span>
        </div>
        <div class="metric">
            <span class="metric-label">Confidence:</span>
            <span class="metric-value">{plag['confidence_percentage']}</span>
        </div>
        <div class="metric">
            <span class="metric-label">Type:</span>
            <span class="metric-value">{plag['plagiarism_type'].replace('_', ' ').title()}</span>
        </div>
    </div>
"""
        
        # Features comparison
        if 'features1' in analysis_result and 'features2' in analysis_result:
            f1 = analysis_result['features1']
            f2 = analysis_result['features2']
            
            html += """
    <div class="section">
        <h2>🔍 Code Features Comparison</h2>
        <table>
            <tr>
                <th>Feature</th>
                <th>File 1</th>
                <th>File 2</th>
                <th>Match</th>
            </tr>
"""
            
            for feature in f1.keys():
                count1 = f1.get(feature, 0)
                count2 = f2.get(feature, 0)
                match = "✓" if count1 == count2 else "✗"
                html += f"""
            <tr>
                <td>{feature.title()}</td>
                <td>{count1}</td>
                <td>{count2}</td>
                <td>{match}</td>
            </tr>
"""
            
            html += """
        </table>
    </div>
"""
        
        # Conclusion
        html += """
    <div class="section">
        <h2>📝 Conclusion</h2>
        <p>
"""
        
        if 'plagiarism' in analysis_result:
            if analysis_result['plagiarism']['is_plagiarism']:
                html += """
            <strong style="color: #dc2626;">⚠️ PLAGIARISM DETECTED</strong><br><br>
            The analysis indicates a high degree of similarity between the submitted files. 
            The code structure and logic are substantially similar, suggesting potential plagiarism.
"""
            else:
                html += """
            <strong style="color: #16a34a;">✓ NO PLAGIARISM DETECTED</strong><br><br>
            The analysis indicates the files are sufficiently different. 
            The code appears to be original work.
"""
        
        html += """
        </p>
    </div>
    
    <div class="footer">
        <p><strong>CIDE - Code Integrity Detection Engine</strong></p>
        <p>AST-based structural analysis for intelligent plagiarism detection</p>
    </div>
</body>
</html>
"""
        
        return html


def generate_report(analysis_result: Dict[str, Any], format_type: str = 'text') -> str:
    """
    Convenience function to generate reports.
    
    Args:
        analysis_result: Analysis results dictionary
        format_type: 'text', 'json', or 'html'
        
    Returns:
        Formatted report string
    """
    generator = ReportGenerator()
    
    if format_type == 'json':
        return generator.generate_json_report(analysis_result)
    elif format_type == 'html':
        return generator.generate_html_report(analysis_result)
    else:
        return generator.generate_text_report(analysis_result)


if __name__ == "__main__":
    # Example usage
    example_result = {
        'mode': 'hybrid',
        'language': 'python',
        'file1_name': 'original.py',
        'file2_name': 'suspicious.py',
        'weighted_percentage': '87.2%',
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
    
    print("Generating sample reports...\n")
    
    # Text report
    text_report = generate_report(example_result, 'text')
    print(text_report)
    
    print("\n" + "=" * 80)
    print("Report generation module ready!")
    print("=" * 80)
