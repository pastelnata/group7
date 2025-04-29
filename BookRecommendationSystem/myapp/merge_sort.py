
def merge_sort(book, sort_key='stars', order='desc'):
    """
    Implements merge sort algorithm to sort books by the specified key.
    
    Parameters:
    books (list): List of book objects to sort
    sort_key (str): The attribute to sort by ('stars', 'ratings_count', 'reviews', 'published_date')
    order (str): Sort order - 'asc' for ascending, 'desc' for descending
    
    Returns:
    list: Sorted list of books
    """
    if len(book) <= 1:
        return book
    
    # Split the list into two halves
    mid = len(book) // 2
    left_half = book[:mid]
    right_half = book[mid:]
    
    # Recursively sort both halves
    left_half = merge_sort(left_half, sort_key, order)
    right_half = merge_sort(right_half, sort_key, order)
    
    # Merge the sorted halves
    return merge(left_half, right_half, sort_key, order)

def merge(left, right, sort_key, order):
    """
    Merges two sorted lists into a single sorted list based on the sort key.
    
    Parameters:
    left (list): First sorted list
    right (list): Second sorted list
    sort_key (str): The attribute to sort by
    order (str): Sort order - 'asc' for ascending, 'desc' for descending
    
    Returns:
    list: Merged sorted list
    """
    result = []
    i = j = 0
    
    # Compare elements from both lists and merge them in sorted order
    while i < len(left) and j < len(right):
        # Get the values to compare based on the sort key
        left_value = getattr(left[i], sort_key, None)  # Default to 0 if attribute doesn't exist
        right_value = getattr(right[j], sort_key, None)  # Default to 0 if attribute doesn't exist
        
         # Handle None values - consider None as lowest value
        if left_value is None and right_value is None:
            comparison = True  # Arbitrary choice when both are None
        elif left_value is None:
            comparison = False if order == 'desc' else True
        elif right_value is None:
            comparison = True if order == 'desc' else False
        # Handle specific comparison logic based on data type
        elif sort_key == 'published_date':
            # For dates: newer dates first for desc, older dates first for asc
            if order == 'desc':
                comparison = left_value >= right_value
            else:
                comparison = left_value <= right_value
        else:
            # For numeric values: higher values first for desc, lower first for asc
            if order == 'desc':
                comparison = left_value >= right_value
            else:
                comparison = left_value <= right_value
        
        if comparison:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    # Add any remaining elements
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result