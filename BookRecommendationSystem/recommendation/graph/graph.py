import random
import time
from collections import defaultdict
from books.models import Book
from django.core.cache import cache
from books.filter_books import group_by_category

def get_cached_graph():
    """Get or build the graph from cache."""
    cache_key = 'book_recommendation_graph'
    cached_data = cache.get(cache_key)
    if cached_data is None:
        adj, book_lookup = build_graph_adj_list()
        cache.set(cache_key, (adj, book_lookup), 3600)
        return adj, book_lookup
    return cached_data

def build_graph_adj_list():
    """
    Builds an optimized adjacency list where books are connected if they share the same category.
    """
    cached_graph = cache.get('book_recommendation_graph')
    if cached_graph is not None:
        return cached_graph

    start_time = time.time()
    books = list(Book.objects.only('id', 'category_id'))
    
    adj = {}
    book_lookup = {}

    # Build book_lookup and initialize adjacency sets
    for book in books:
        if book.category_id:
            book_lookup[book.id] = book
            adj[book.id] = set()

    category_groups = group_by_category()

    # Build adjacency sets in a single pass per category
    MAX_NEIGHBORS = 700
    for group in category_groups.values():
        if len(group) > 1:
            if len(group) > MAX_NEIGHBORS + 1:
                # Sample once for the group
                sampled = set(random.sample(group, MAX_NEIGHBORS + 1))
                for book_id in group:
                    neighbors = sampled - {book_id}
                    adj[book_id].update(neighbors)
            else:
                group_set = set(group)
                for book_id in group:
                    adj[book_id].update(group_set - {book_id})

    # Convert sets to lists
    adj = {book_id: list(neighbors) for book_id, neighbors in adj.items()}
    
    end_time = time.time()
    print(f"Graph built in {end_time - start_time:.2f} seconds")

    cache.set('book_recommendation_graph', (adj, book_lookup), 3600)

    return adj, book_lookup