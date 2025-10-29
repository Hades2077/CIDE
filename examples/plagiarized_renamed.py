"""
Plagiarized Code - Variables Renamed
This is the SAME code with renamed variables and slightly different comments.
"""

def bubble_sort(data):
    """
    Implementation of bubble sort.
    """
    size = len(data)
    
    # Loop through entire array
    for idx in range(size):
        # Already sorted elements don't need checking
        for pos in range(0, size - idx - 1):
            # Exchange elements if out of order
            if data[pos] > data[pos + 1]:
                data[pos], data[pos + 1] = data[pos + 1], data[pos]
    
    return data


def binary_search(sorted_list, value):
    """
    Binary search implementation.
    """
    start = 0
    end = len(sorted_list) - 1
    
    while start <= end:
        middle = (start + end) // 2
        
        if sorted_list[middle] == value:
            return middle
        elif sorted_list[middle] < value:
            start = middle + 1
        else:
            end = middle - 1
    
    return -1


def find_duplicates(values):
    """
    Locate duplicate values in list.
    """
    checked = set()
    dupes = []
    
    for val in values:
        if val in checked:
            dupes.append(val)
        else:
            checked.add(val)
    
    return dupes
