from collections import deque
from .graph import build_graph_adj_list

def bfs(start_node_id, return_books=False):
    """
    Performs real BFS from the given book ID.
    If return_books=True, returns a list of Book objects.
    Otherwise, returns a list of visited book IDs.
    """
    adj, book_lookup = build_graph_adj_list()

    if start_node_id not in book_lookup:
        raise ValueError("Start node does not exist in the database.")

    visited = set()
    queue = deque([start_node_id])
    order = []

    while queue:
        current = queue.popleft()
        if current in visited:
            continue
        visited.add(current)
        order.append(current)

        for neighbor in adj[current]:
            if neighbor not in visited:
                queue.append(neighbor)

    if return_books:
        return [book_lookup[bid] for bid in order]
    return order
