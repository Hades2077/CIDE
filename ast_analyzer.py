"""
AST-based Code Similarity Analyzer
===================================
Advanced analyzer that uses Abstract Syntax Trees to detect structural similarity,
resilient to variable renaming, comment changes, and formatting differences.
"""

import ast
import hashlib
from typing import Dict, List, Any, Tuple, Optional
from difflib import SequenceMatcher
import json


class ASTNormalizer(ast.NodeVisitor):
    """
    Normalizes AST by replacing variable names, function names,
    and constants with generic placeholders.
    """
    
    def __init__(self):
        self.var_counter = 0
        self.func_counter = 0
        self.const_counter = 0
        self.class_counter = 0
        self.var_map = {}
        self.func_map = {}
        self.const_map = {}
        self.class_map = {}
        self.structure = []
        
    def _get_var_placeholder(self, name: str) -> str:
        """Get or create placeholder for variable name."""
        if name not in self.var_map:
            self.var_map[name] = f"VAR_{self.var_counter}"
            self.var_counter += 1
        return self.var_map[name]
    
    def _get_func_placeholder(self, name: str) -> str:
        """Get or create placeholder for function name."""
        if name not in self.func_map:
            self.func_map[name] = f"FUNC_{self.func_counter}"
            self.func_counter += 1
        return self.func_map[name]
    
    def _get_const_placeholder(self, value: Any) -> str:
        """Get or create placeholder for constant value."""
        key = str(value)
        if key not in self.const_map:
            self.const_map[key] = f"CONST_{self.const_counter}"
            self.const_counter += 1
        return self.const_map[key]
    
    def _get_class_placeholder(self, name: str) -> str:
        """Get or create placeholder for class name."""
        if name not in self.class_map:
            self.class_map[name] = f"CLASS_{self.class_counter}"
            self.class_counter += 1
        return self.class_map[name]
    
    def visit_FunctionDef(self, node):
        """Visit function definition."""
        func_name = self._get_func_placeholder(node.name)
        args = [self._get_var_placeholder(arg.arg) for arg in node.args.args]
        self.structure.append(('FunctionDef', func_name, tuple(args)))
        self.generic_visit(node)
    
    def visit_AsyncFunctionDef(self, node):
        """Visit async function definition."""
        func_name = self._get_func_placeholder(node.name)
        args = [self._get_var_placeholder(arg.arg) for arg in node.args.args]
        self.structure.append(('AsyncFunctionDef', func_name, tuple(args)))
        self.generic_visit(node)
    
    def visit_ClassDef(self, node):
        """Visit class definition."""
        class_name = self._get_class_placeholder(node.name)
        bases = tuple(base.id if isinstance(base, ast.Name) else 'BASE' 
                     for base in node.bases)
        self.structure.append(('ClassDef', class_name, bases))
        self.generic_visit(node)
    
    def visit_Name(self, node):
        """Visit variable name."""
        placeholder = self._get_var_placeholder(node.id)
        self.structure.append(('Name', placeholder, type(node.ctx).__name__))
        self.generic_visit(node)
    
    def visit_Assign(self, node):
        """Visit assignment."""
        self.structure.append(('Assign',))
        self.generic_visit(node)
    
    def visit_AugAssign(self, node):
        """Visit augmented assignment (+=, -=, etc.)."""
        op = type(node.op).__name__
        self.structure.append(('AugAssign', op))
        self.generic_visit(node)
    
    def visit_If(self, node):
        """Visit if statement."""
        self.structure.append(('If',))
        self.generic_visit(node)
    
    def visit_For(self, node):
        """Visit for loop."""
        self.structure.append(('For',))
        self.generic_visit(node)
    
    def visit_While(self, node):
        """Visit while loop."""
        self.structure.append(('While',))
        self.generic_visit(node)
    
    def visit_Return(self, node):
        """Visit return statement."""
        self.structure.append(('Return',))
        self.generic_visit(node)
    
    def visit_Call(self, node):
        """Visit function call."""
        if isinstance(node.func, ast.Name):
            func_name = self._get_func_placeholder(node.func.id)
        elif isinstance(node.func, ast.Attribute):
            func_name = f"METHOD_{node.func.attr}"
        else:
            func_name = "CALL"
        self.structure.append(('Call', func_name))
        self.generic_visit(node)
    
    def visit_BinOp(self, node):
        """Visit binary operation."""
        op = type(node.op).__name__
        self.structure.append(('BinOp', op))
        self.generic_visit(node)
    
    def visit_UnaryOp(self, node):
        """Visit unary operation."""
        op = type(node.op).__name__
        self.structure.append(('UnaryOp', op))
        self.generic_visit(node)
    
    def visit_Compare(self, node):
        """Visit comparison."""
        ops = [type(op).__name__ for op in node.ops]
        self.structure.append(('Compare', tuple(ops)))
        self.generic_visit(node)
    
    def visit_Constant(self, node):
        """Visit constant value."""
        # Normalize constants by type, not value
        const_type = type(node.value).__name__
        self.structure.append(('Constant', const_type))
        # Don't visit children as constants are leaves
    
    def visit_Import(self, node):
        """Visit import statement."""
        self.structure.append(('Import',))
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node):
        """Visit from-import statement."""
        self.structure.append(('ImportFrom',))
        self.generic_visit(node)


class ASTStructureAnalyzer:
    """
    Analyzes code structure using Abstract Syntax Trees.
    """
    
    def __init__(self):
        pass
    
    def parse_python(self, code: str) -> Optional[ast.AST]:
        """
        Parse Python code into AST.
        
        Args:
            code: Python source code string
            
        Returns:
            AST tree or None if parsing fails
        """
        try:
            return ast.parse(code)
        except SyntaxError as e:
            print(f"Syntax error while parsing: {e}")
            return None
    
    def normalize_ast(self, tree: ast.AST) -> Tuple[List[Tuple], Dict]:
        """
        Normalize AST by replacing names with placeholders.
        
        Args:
            tree: AST tree
            
        Returns:
            Tuple of (structure list, mapping dictionaries)
        """
        normalizer = ASTNormalizer()
        normalizer.visit(tree)
        
        mappings = {
            'variables': normalizer.var_map,
            'functions': normalizer.func_map,
            'constants': normalizer.const_map,
            'classes': normalizer.class_map
        }
        
        return normalizer.structure, mappings
    
    def structure_to_string(self, structure: List[Tuple]) -> str:
        """
        Convert structure list to string for comparison.
        
        Args:
            structure: List of structure tuples
            
        Returns:
            String representation
        """
        return '\n'.join(str(item) for item in structure)
    
    def compute_structure_similarity(self, struct1: List[Tuple], 
                                     struct2: List[Tuple]) -> float:
        """
        Compute similarity between two normalized structures.
        
        Args:
            struct1: First structure
            struct2: Second structure
            
        Returns:
            Similarity score (0.0 to 1.0)
        """
        str1 = self.structure_to_string(struct1)
        str2 = self.structure_to_string(struct2)
        
        matcher = SequenceMatcher(None, str1, str2)
        return matcher.ratio()
    
    def get_structure_hash(self, structure: List[Tuple]) -> str:
        """
        Get hash of structure for quick comparison.
        
        Args:
            structure: Structure list
            
        Returns:
            Hash string
        """
        struct_str = self.structure_to_string(structure)
        return hashlib.md5(struct_str.encode()).hexdigest()
    
    def analyze_code_features(self, tree: ast.AST) -> Dict[str, int]:
        """
        Extract code features from AST.
        
        Args:
            tree: AST tree
            
        Returns:
            Dictionary of feature counts
        """
        features = {
            'functions': 0,
            'classes': 0,
            'loops': 0,
            'conditionals': 0,
            'assignments': 0,
            'calls': 0,
            'returns': 0,
            'imports': 0
        }
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                features['functions'] += 1
            elif isinstance(node, ast.ClassDef):
                features['classes'] += 1
            elif isinstance(node, (ast.For, ast.While)):
                features['loops'] += 1
            elif isinstance(node, ast.If):
                features['conditionals'] += 1
            elif isinstance(node, (ast.Assign, ast.AugAssign)):
                features['assignments'] += 1
            elif isinstance(node, ast.Call):
                features['calls'] += 1
            elif isinstance(node, ast.Return):
                features['returns'] += 1
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                features['imports'] += 1
        
        return features
    
    def compute_feature_similarity(self, features1: Dict[str, int], 
                                   features2: Dict[str, int]) -> float:
        """
        Compute similarity based on code features.
        
        Args:
            features1: First code features
            features2: Second code features
            
        Returns:
            Similarity score (0.0 to 1.0)
        """
        if not features1 or not features2:
            return 0.0
        
        # Calculate weighted similarity for each feature
        total_weight = 0
        weighted_similarity = 0
        
        for feature in features1.keys():
            count1 = features1.get(feature, 0)
            count2 = features2.get(feature, 0)
            
            if count1 == 0 and count2 == 0:
                similarity = 1.0
            else:
                max_count = max(count1, count2)
                min_count = min(count1, count2)
                similarity = min_count / max_count if max_count > 0 else 0.0
            
            # Weight based on importance
            weight = 2 if feature in ['functions', 'classes'] else 1
            weighted_similarity += similarity * weight
            total_weight += weight
        
        return weighted_similarity / total_weight if total_weight > 0 else 0.0


class HybridSimilarityAnalyzer:
    """
    Combines AST-based structural analysis with sequence-based text analysis.
    Uses weighted scoring: 70% structure + 30% sequence.
    """
    
    def __init__(self, structure_weight: float = 0.7, sequence_weight: float = 0.3):
        """
        Initialize hybrid analyzer.
        
        Args:
            structure_weight: Weight for structural similarity (default: 0.7)
            sequence_weight: Weight for sequence similarity (default: 0.3)
        """
        self.structure_weight = structure_weight
        self.sequence_weight = sequence_weight
        self.ast_analyzer = ASTStructureAnalyzer()
    
    def analyze(self, code1: str, code2: str, language: str = 'python') -> Dict[str, Any]:
        """
        Perform hybrid analysis on two code samples.
        
        Args:
            code1: First code string
            code2: Second code string
            language: Programming language (currently only 'python' supported)
            
        Returns:
            Dictionary with detailed similarity metrics
        """
        result = {
            'language': language,
            'structure_similarity': 0.0,
            'sequence_similarity': 0.0,
            'feature_similarity': 0.0,
            'weighted_score': 0.0,
            'weighted_percentage': '0.0%',
            'identical_structure': False,
            'features1': {},
            'features2': {},
            'structure1': [],
            'structure2': [],
            'error': None
        }
        
        try:
            # Parse both code samples
            tree1 = self.ast_analyzer.parse_python(code1)
            tree2 = self.ast_analyzer.parse_python(code2)
            
            if tree1 is None or tree2 is None:
                result['error'] = 'Failed to parse one or both code samples'
                return result
            
            # Normalize ASTs
            struct1, mappings1 = self.ast_analyzer.normalize_ast(tree1)
            struct2, mappings2 = self.ast_analyzer.normalize_ast(tree2)
            
            result['structure1'] = struct1
            result['structure2'] = struct2
            
            # Compute structural similarity
            structure_similarity = self.ast_analyzer.compute_structure_similarity(struct1, struct2)
            result['structure_similarity'] = structure_similarity
            
            # Check if structures are identical
            hash1 = self.ast_analyzer.get_structure_hash(struct1)
            hash2 = self.ast_analyzer.get_structure_hash(struct2)
            result['identical_structure'] = (hash1 == hash2)
            
            # Extract and compare features
            features1 = self.ast_analyzer.analyze_code_features(tree1)
            features2 = self.ast_analyzer.analyze_code_features(tree2)
            result['features1'] = features1
            result['features2'] = features2
            
            feature_similarity = self.ast_analyzer.compute_feature_similarity(features1, features2)
            result['feature_similarity'] = feature_similarity
            
            # Compute sequence similarity (basic text comparison)
            matcher = SequenceMatcher(None, code1, code2)
            sequence_similarity = matcher.ratio()
            result['sequence_similarity'] = sequence_similarity
            
            # Calculate weighted score
            weighted_score = (
                structure_similarity * self.structure_weight +
                sequence_similarity * self.sequence_weight
            )
            result['weighted_score'] = weighted_score
            result['weighted_percentage'] = f"{weighted_score * 100:.1f}%"
            
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def detect_plagiarism(self, code1: str, code2: str, 
                         threshold: float = 0.75) -> Dict[str, Any]:
        """
        Detect potential plagiarism between two code samples.
        
        Args:
            code1: First code string
            code2: Second code string
            threshold: Similarity threshold for plagiarism detection (default: 0.75)
            
        Returns:
            Dictionary with plagiarism detection results
        """
        analysis = self.analyze(code1, code2)
        
        is_plagiarism = analysis['weighted_score'] >= threshold
        confidence = analysis['weighted_score']
        
        # Determine plagiarism type
        plagiarism_type = 'none'
        if is_plagiarism:
            if analysis['identical_structure']:
                plagiarism_type = 'exact_copy'
            elif analysis['structure_similarity'] > 0.9:
                plagiarism_type = 'renamed_variables'
            elif analysis['structure_similarity'] > threshold:
                plagiarism_type = 'restructured_code'
        
        return {
            'is_plagiarism': is_plagiarism,
            'confidence': confidence,
            'confidence_percentage': f"{confidence * 100:.1f}%",
            'plagiarism_type': plagiarism_type,
            'threshold': threshold,
            'analysis': analysis
        }


def main():
    """Example usage and demonstrations."""
    
    print("=" * 70)
    print("AST-BASED CODE SIMILARITY ANALYZER")
    print("=" * 70)
    print()
    
    analyzer = HybridSimilarityAnalyzer()
    
    # Example 1: Same code with renamed variables
    print("Example 1: Same logic with renamed variables")
    print("-" * 70)
    
    code1 = """
def calculate_sum(numbers):
    total = 0
    for num in numbers:
        total += num
    return total
"""
    
    code2 = """
def compute_total(values):
    result = 0
    for val in values:
        result += val
    return result
"""
    
    result = analyzer.analyze(code1, code2)
    print(f"Structure similarity: {result['structure_similarity']:.1%}")
    print(f"Sequence similarity: {result['sequence_similarity']:.1%}")
    print(f"Weighted score (70/30): {result['weighted_percentage']}")
    print(f"Identical structure: {result['identical_structure']}")
    print()
    
    # Example 2: Plagiarism detection
    print("Example 2: Plagiarism detection")
    print("-" * 70)
    
    plagiarism_result = analyzer.detect_plagiarism(code1, code2, threshold=0.75)
    print(f"Is plagiarism: {plagiarism_result['is_plagiarism']}")
    print(f"Confidence: {plagiarism_result['confidence_percentage']}")
    print(f"Type: {plagiarism_result['plagiarism_type']}")
    print()
    
    # Example 3: Completely different code
    print("Example 3: Completely different code")
    print("-" * 70)
    
    code3 = """
class Person:
    def __init__(self, name):
        self.name = name
    
    def greet(self):
        print(f"Hello, {self.name}")
"""
    
    result2 = analyzer.analyze(code1, code3)
    print(f"Structure similarity: {result2['structure_similarity']:.1%}")
    print(f"Sequence similarity: {result2['sequence_similarity']:.1%}")
    print(f"Weighted score (70/30): {result2['weighted_percentage']}")
    print()
    
    # Example 4: Feature analysis
    print("Example 4: Code feature comparison")
    print("-" * 70)
    print(f"Code 1 features: {result['features1']}")
    print(f"Code 2 features: {result['features2']}")
    print(f"Feature similarity: {result['feature_similarity']:.1%}")
    print()


if __name__ == "__main__":
    main()
