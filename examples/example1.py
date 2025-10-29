"""
Example Python file 1 - Calculator functions
"""

def add(a, b):
    """Add two numbers together."""
    # Return the sum
    return a + b

def subtract(a, b):
    """Subtract b from a."""
    # Return the difference
    return a - b

def multiply(a, b):
    """Multiply two numbers."""
    # Calculate product
    result = a * b
    return result

def divide(a, b):
    """Divide a by b."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
