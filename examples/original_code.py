"""
Original Code - Sorting Algorithm Implementation
"""

def bubble_sort(array):
    """
    Sorts an array using bubble sort algorithm.
    """
    length = len(array)
    
    # Traverse through all array elements
    for i in range(length):
        # Last i elements are already in place
        for j in range(0, length - i - 1):
            # Swap if the element found is greater than the next element
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
    
    return array


def binary_search(sorted_array, target):
    """
    Performs binary search on a sorted array.
    """
    left = 0
    right = len(sorted_array) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if sorted_array[mid] == target:
            return mid
        elif sorted_array[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1


def find_duplicates(numbers):
    """
    Finds duplicate numbers in a list.
    """
    seen = set()
    duplicates = []
    
    for num in numbers:
        if num in seen:
            duplicates.append(num)
        else:
            seen.add(num)
    
    return duplicates
