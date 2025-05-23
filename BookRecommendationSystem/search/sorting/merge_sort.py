from typing import List, Dict, Any, Union
from decimal import Decimal

def safe_float_conversion(value: Any) -> float:
    if value is None:
        return 0.0
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0

def calculate_relevance_score(book: Dict[str, Any], search_query: str) -> float:
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

def merge_sort(books: List[Dict[str, Any]], search_query: str, 
               sort_by: str = 'relevance') -> List[Dict[str, Any]]:
    
    if not isinstance(books, list) or len(books) <= 1:
        return books
        
    mid = len(books) // 2
    left = merge_sort(books[:mid], search_query, sort_by)
    right = merge_sort(books[mid:], search_query, sort_by)
    
    return merge(left, right, sort_by, search_query)

def merge(left: List[Dict[str, Any]], right: List[Dict[str, Any]], 
         sort_by: str, search_query: str = '') -> List[Dict[str, Any]]:
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        left_key = get_sort_key(left[i], sort_by, search_query)
        right_key = get_sort_key(right[j], sort_by, search_query)
        
        if left_key >= right_key:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def get_sort_key(book: Dict[str, Any], sort_by: str, search_query: str = '') -> float:
    
    if sort_by == 'relevance':
        return calculate_relevance_score(book, search_query)
    elif sort_by == 'rating':
        return safe_float_conversion(book.get('stars', 0.0))
    elif sort_by == 'price_low':
        return -safe_float_conversion(book.get('price', 0.0))  
    elif sort_by == 'price_high':
        return safe_float_conversion(book.get('price', 0.0))   
    return 0.0