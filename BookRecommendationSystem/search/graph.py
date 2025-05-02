from collections import defaultdict
from books.models import Book

def build_book_graph(limit=75000):
    books = Book.objects.all()[:limit]  # Limit the books fetched to avoid memory overload
    graph = {book.id: set() for book in books}
    
    for i, book1 in enumerate(books):
        for j, book2 in enumerate(books):
            if i != j:
                graph[book1.id].add(book2.id)
    
    return graph


from collections import deque
from books.models import Book

def bfs_recommendations(start_book_id, graph, depth=2, limit=10):
    visited = set()
    queue = deque([(start_book_id, 0)])
    recommendations = set()

    while queue:
        current_id, d = queue.popleft()
        if d > depth:
            continue
        visited.add(current_id)

        for neighbor in graph.get(current_id, []):
            if neighbor not in visited:
                if d < depth:
                    recommendations.add(neighbor)
                queue.append((neighbor, d + 1))
                visited.add(neighbor)

    books = Book.objects.filter(id__in=list(recommendations)[:limit])
    return books
