import networkx as nx
from collections import defaultdict
from books.models import Book
from collections import defaultdict
from django.core.cache import cache

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
    books = list(Book.objects.all())
    
    adj = defaultdict(list)
    category_groups = defaultdict(list)
    book_lookup = {}

    for book in books:
        if book.category_id:  
            category_groups[book.category_id].append(book)
            book_lookup[book.id] = book
            adj[book.id] = []  
    for group in category_groups.values():
        if len(group) > 1:
            for i in range(len(group)):
                for j in range(i + 1, len(group)):
                    b1, b2 = group[i], group[j]
                    adj[b1.id].append(b2.id)
                    adj[b2.id].append(b1.id)

    return adj, book_lookup

def build_graph():
    """
    Builds an optimized NetworkX graph where books are connected if they share the same category.
    """
    G = nx.Graph()

    books = list(Book.objects.all())

    for book in books:
        if book.category_id: 
            G.add_node(book.id, 
                      title=book.title, 
                      category=book.category_id,
                      stars=book.stars or 0,
                      reviews=book.reviews or 0)

    category_groups = defaultdict(list)
    for book in books:
        if book.category_id: 
            category_groups[book.category_id].append(book)

    for group in category_groups.values():
        if len(group) > 1:  
            for i in range(len(group)):
                for j in range(i + 1, len(group)):
                    G.add_edge(group[i].id, group[j].id, weight=1)

    return G

