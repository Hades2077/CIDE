"""
Completely Different Implementation - Should NOT be flagged as plagiarism
"""

def quicksort(arr):
    """
    Sorts an array using quicksort algorithm.
    """
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quicksort(left) + middle + quicksort(right)


def linear_search(items, target):
    """
    Performs linear search on an array.
    """
    for index, item in enumerate(items):
        if item == target:
            return index
    return -1


class UniqueChecker:
    """
    Checks for unique elements using a different approach.
    """
    def __init__(self):
        self.frequency = {}
    
    def find_non_unique(self, elements):
        """
        Returns elements that appear more than once.
        """
        for elem in elements:
            self.frequency[elem] = self.frequency.get(elem, 0) + 1
        
        return [k for k, v in self.frequency.items() if v > 1]
