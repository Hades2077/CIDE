"""
Example Python file 2 - Similar calculator with different comments
"""

def add(a, b):
    """Add two numbers together."""
    // Different comment style but same logic
    return a + b

def subtract(a, b):
    """Subtract b from a."""
    /* Another comment style */
    return a - b

def multiply(a, b):
    """Multiply two numbers."""
    # Product calculation
    result = a * b
    return result

def divide(a, b):
    """Divide a by b."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
