"""
Code Similarity Analyzer
========================
A tool to compute similarity between two code files.

Features:
- Accepts two code inputs (via file path or text)
- Preprocesses code by stripping comments, whitespace, and normalizing casing
- Uses difflib.SequenceMatcher to compute similarity score
- AST-based structural analysis for detecting disguised plagiarism
- Weighted scoring model (70% structure + 30% sequence)
- Returns a percentage match
"""

import re
from difflib import SequenceMatcher
from typing import Union, Optional
from pathlib import Path

# Import AST analyzer if available
try:
    from ast_analyzer import HybridSimilarityAnalyzer
    AST_AVAILABLE = True
except ImportError:
    AST_AVAILABLE = False


class CodePreprocessor:
    """Handles preprocessing of code inputs."""
    
    @staticmethod
    def remove_comments(code: str, language: str = 'auto') -> str:
        """
        Remove comments from code.
        Supports common comment styles (C-style, Python-style).
        
        Args:
            code: The source code string
            language: Language hint ('auto', 'python', 'c', 'java', etc.)
        
        Returns:
            Code with comments removed
        """
        # Remove single-line comments (// and #)
        code = re.sub(r'//.*?$', '', code, flags=re.MULTILINE)
        code = re.sub(r'#.*?$', '', code, flags=re.MULTILINE)
        
        # Remove multi-line comments (/* */ and ''' ''')
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
        code = re.sub(r'""".*?"""', '', code, flags=re.DOTALL)
        code = re.sub(r"'''.*?'''", '', code, flags=re.DOTALL)
        
        return code
    
    @staticmethod
    def normalize_whitespace(code: str) -> str:
        """
        Normalize whitespace in code.
        - Removes leading/trailing whitespace from each line
        - Replaces multiple spaces with single space
        - Removes empty lines
        
        Args:
            code: The source code string
        
        Returns:
            Code with normalized whitespace
        """
        # Split into lines and strip each line
        lines = [line.strip() for line in code.split('\n')]
        
        # Remove empty lines
        lines = [line for line in lines if line]
        
        # Replace multiple spaces with single space in each line
        lines = [re.sub(r'\s+', ' ', line) for line in lines]
        
        return '\n'.join(lines)
    
    @staticmethod
    def normalize_casing(code: str) -> str:
        """
        Normalize casing to lowercase for comparison.
        
        Args:
            code: The source code string
        
        Returns:
            Lowercase code
        """
        return code.lower()
    
    @classmethod
    def preprocess(cls, code: str, language: str = 'auto') -> str:
        """
        Apply all preprocessing steps to code.
        
        Args:
            code: The source code string
            language: Language hint for comment removal
        
        Returns:
            Fully preprocessed code
        """
        code = cls.remove_comments(code, language)
        code = cls.normalize_whitespace(code)
        code = cls.normalize_casing(code)
        return code


class CodeSimilarityAnalyzer:
    """Main analyzer for computing code similarity."""
    
    def __init__(self):
        self.preprocessor = CodePreprocessor()
    
    def read_code_input(self, input_data: Union[str, Path]) -> str:
        """
        Read code from file path or return text directly.
        
        Args:
            input_data: Either a file path (str/Path) or code text (str)
        
        Returns:
            Code content as string
        """
        # Check if input is a file path
        if isinstance(input_data, (str, Path)):
            path = Path(input_data)
            if path.exists() and path.is_file():
                with open(path, 'r', encoding='utf-8') as f:
                    return f.read()
        
        # Otherwise, treat as direct text input
        return str(input_data)
    
    def compute_similarity(self, code1: str, code2: str) -> float:
        """
        Compute similarity between two code strings using SequenceMatcher.
        
        Args:
            code1: First code string (preprocessed)
            code2: Second code string (preprocessed)
        
        Returns:
            Similarity ratio as float (0.0 to 1.0)
        """
        matcher = SequenceMatcher(None, code1, code2)
        return matcher.ratio()
    
    def analyze(self, input1: Union[str, Path], input2: Union[str, Path], 
                preprocess: bool = True, language: str = 'auto', 
                mode: str = 'basic') -> dict:
        """
        Analyze similarity between two code inputs.
        
        Args:
            input1: First code input (file path or text)
            input2: Second code input (file path or text)
            preprocess: Whether to preprocess code (default: True)
            language: Language hint for preprocessing (default: 'auto')
            mode: Analysis mode - 'basic', 'ast', or 'hybrid' (default: 'basic')
        
        Returns:
            Dictionary containing:
                - similarity_score: Float between 0.0 and 1.0
                - similarity_percentage: String formatted percentage
                - code1_length: Character count of first code
                - code2_length: Character count of second code
                - (additional fields for AST/hybrid modes)
        """
        # Read code inputs
        code1 = self.read_code_input(input1)
        code2 = self.read_code_input(input2)
        
        # Store original lengths
        original_length1 = len(code1)
        original_length2 = len(code2)
        
        # Use AST-based analysis if requested and available
        if mode in ['ast', 'hybrid'] and AST_AVAILABLE and language == 'python':
            return self._analyze_with_ast(code1, code2, mode, original_length1, original_length2)
        
        # Fall back to basic text-based analysis
        # Preprocess if requested
        if preprocess:
            code1 = self.preprocessor.preprocess(code1, language)
            code2 = self.preprocessor.preprocess(code2, language)
        
        # Compute similarity
        similarity = self.compute_similarity(code1, code2)
        
        return {
            'mode': 'basic',
            'similarity_score': similarity,
            'similarity_percentage': f"{similarity * 100:.1f}%",
            'code1_length': original_length1,
            'code2_length': original_length2,
            'preprocessed_code1_length': len(code1),
            'preprocessed_code2_length': len(code2)
        }
    
    def _analyze_with_ast(self, code1: str, code2: str, mode: str, 
                         len1: int, len2: int) -> dict:
        """
        Analyze using AST-based approach.
        
        Args:
            code1: First code string
            code2: Second code string
            mode: 'ast' or 'hybrid'
            len1: Original length of code1
            len2: Original length of code2
            
        Returns:
            Dictionary with analysis results
        """
        analyzer = HybridSimilarityAnalyzer()
        ast_result = analyzer.analyze(code1, code2)
        
        # Add basic info
        ast_result['mode'] = mode
        ast_result['code1_length'] = len1
        ast_result['code2_length'] = len2
        
        return ast_result


def main():
    """Example usage of the CodeSimilarityAnalyzer."""
    analyzer = CodeSimilarityAnalyzer()
    
    # Example 1: Compare two text strings
    code_a = """
    def hello_world():
        # This is a comment
        print("Hello, World!")
        return True
    """
    
    code_b = """
    def hello_world():
        // Different comment style
        print("Hello, World!")
        return True
    """
    
    print("=" * 60)
    print("Example 1: Comparing two code strings")
    print("=" * 60)
    result = analyzer.analyze(code_a, code_b)
    print(f"Similarity: {result['similarity_percentage']}")
    print(f"Code 1 length: {result['code1_length']} chars")
    print(f"Code 2 length: {result['code2_length']} chars")
    print(f"After preprocessing: {result['preprocessed_code1_length']} vs {result['preprocessed_code2_length']} chars")
    print()
    
    # Example 2: Compare with different code
    code_c = """
    def goodbye():
        print("Goodbye!")
        return False
    """
    
    print("=" * 60)
    print("Example 2: Comparing similar vs different code")
    print("=" * 60)
    result2 = analyzer.analyze(code_a, code_c)
    print(f"Similarity: {result2['similarity_percentage']}")
    print()
    
    # Example 3: Without preprocessing
    print("=" * 60)
    print("Example 3: Same comparison without preprocessing")
    print("=" * 60)
    result3 = analyzer.analyze(code_a, code_b, preprocess=False)
    print(f"Similarity (with comments/whitespace): {result3['similarity_percentage']}")
    result4 = analyzer.analyze(code_a, code_b, preprocess=True)
    print(f"Similarity (preprocessed): {result4['similarity_percentage']}")
    print()


if __name__ == "__main__":
    main()
