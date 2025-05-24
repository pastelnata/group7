import time

def safe_float_conversion(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0
    
def calculate_relevance_score(book, search_query: str) -> float:
    if not search_query:
        return 0.0
    
    score = 0.0
    query_lower = search_query.lower()
    
    title = str(book.get('title', '')).lower()
    if title == query_lower:
        score += 100  
    elif query_lower in title:
        score += 50   
    
    author = str(book.get('author', '')).lower()
    if query_lower in author:
        score += 30
    
    category = str(book.get('category_name', '')).lower()
    if query_lower in category:
        score += 20
    
    stars = safe_float_conversion(book.get('stars'))
    score += stars * 2

    if book.get('isBestSeller'): score += 10
    if book.get('isEditorsPick'): score += 8
    if book.get('isGoodReadsChoice'): score += 6
    
    return score

def get_sort_key(book, sort_by):
    def get_value(obj, key, default=0.0):
        if isinstance(obj, dict):
            return obj.get(key, default)
        return getattr(obj, key, default)

    if sort_by == 'rating':
        return safe_float_conversion(get_value(book, 'stars', 0.0))
    elif sort_by == 'price_high':
        return safe_float_conversion(get_value(book, 'price', 0.0))
    elif sort_by == 'price_low':
        return -safe_float_conversion(get_value(book, 'price', 0.0))
    elif sort_by == 'relevance':
        return calculate_relevance_score(book, book.get('search_query', '') if isinstance(book, dict) else getattr(book, 'search_query', ''))

def merge_sort(books, sort_by='relevance'):
    if not isinstance(books, list) or len(books) <= 1:
        return books

    mid = len(books) // 2
    left = merge_sort(books[:mid], sort_by)
    right = merge_sort(books[mid:], sort_by)
    merge_sort_end = time.time()
    return merge(left, right, sort_by)

def merge(left, right, sort_by):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if get_sort_key(left[i], sort_by) >= get_sort_key(right[j], sort_by):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result