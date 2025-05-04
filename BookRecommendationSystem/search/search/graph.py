import networkx as nx
from collections import defaultdict
from books.models import Book
from collections import deque, defaultdict
from books.models import Book

def build_graph_adj_list():
    """
    Builds an adjacency list where books are connected if they share the same category.
    """
    books = list(Book.objects.all())
    adj = defaultdict(list)
    category_groups = defaultdict(list)

    # Group books by category
    for book in books:
        category_groups[book.category_id].append(book)

    # Create edges between all books in the same category
    for group in category_groups.values():
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                b1, b2 = group[i], group[j]
                adj[b1.id].append(b2.id)
                adj[b2.id].append(b1.id)

    return adj, {book.id: book for book in books}  # Return ID-to-object mapping too


def build_graph():
    G = nx.Graph()

    # Get all books
    books = list(Book.objects.all())

    # Add nodes
    for book in books:
        G.add_node(book.id, title=book.title, category=book.category_id)

    # Group books by category
    category_groups = defaultdict(list)
    for book in books:
        category_groups[book.category_id].append(book)

    # Add edges within same category
    for group in category_groups.values():
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                G.add_edge(group[i].id, group[j].id, weight=1)

    return G

