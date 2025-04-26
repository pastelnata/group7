from django.shortcuts import render
from .bst_manager import search_books


from django.db.models.functions import Random
import pandas as pd # type: ignore
import itertools
import numpy as np # type: ignore
from collections import deque

from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from books.models import Book
from search.views import search_books

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings




GRAPH_DATA = None

def get_graph():
    global GRAPH_DATA
    if GRAPH_DATA is None:
        GRAPH_DATA = build_graph()
    return GRAPH_DATA

def get_suggested_books(query):
    x, edge_index, sorted_df = get_graph()
    
    if not query:
        return []

    try:
        book_row = sorted_df[sorted_df['title'].str.contains(query, case=False, na=False)].iloc[0]
        start_node = book_row['node_id']
        traversal = bfs(start_node, edge_index, len(sorted_df))
        suggested = sorted_df[sorted_df['node_id'].isin(traversal[1:6])]  # skip first node
        return suggested
    except IndexError:
        return []
    
def search_results(request):
    query = request.GET.get('query', '')
    results = search_books(query)

    # NEW: Get suggestions
    suggested_books = get_suggested_books(query)

    return render(request, 'search_results.html', {
        'results': results,
        'query': query,
        'suggested_books': suggested_books,  # <-- pass to template
    })




def build_graph():
    book_qs = Book.objects.all().values()[:100]
    book_df = pd.DataFrame(list(book_qs))
    sorted_df = book_df.sort_values(by="asin")
    node_features = sorted_df[[
        "category_name",  
        "stars",
        "reviews",
        "price",
        "isKindleUnlimited",
        "isBestSeller",
        "isEditorsPick",
        "isGoodReadsChoice"
    ]]
    pd.set_option('mode.chained_assignment', None)
    node_features["category"] = node_features["category_name"].fillna("Unknown")
    category_dummies = pd.get_dummies(node_features["category"], prefix="genre")
    node_features = pd.concat([node_features, category_dummies], axis=1)
    node_features.drop(["category_name", "category"], axis=1, inplace=True)

    x = node_features.to_numpy()
    sorted_df = sorted_df.reset_index(drop=True)
    sorted_df["node_id"] = sorted_df.index

    all_edges = np.array([], dtype=np.int32).reshape((0, 2))
    authors = sorted_df["author"].unique()
    for author in authors:
        author_books = sorted_df[sorted_df["author"] == author]
        nodes = author_books["node_id"].values
        if len(nodes) < 2:
            continue
        combinations = list(itertools.combinations(nodes, 2))
        source = [e[0] for e in combinations]
        target = [e[1] for e in combinations]
        edges = np.column_stack([source, target])
        all_edges = np.vstack([all_edges, edges])

    edge_index = all_edges.transpose()

    return x, edge_index, sorted_df

def bfs(start_node, edge_index, num_nodes):
    adj_list = [[] for _ in range(num_nodes)]
    for src, tgt in edge_index.T:
        adj_list[src].append(tgt)
        adj_list[tgt].append(src)

    visited = [False] * num_nodes
    queue = deque([start_node])  
    visited[start_node] = True
    traversal_order = []

    while queue:
        current = queue.popleft()
        traversal_order.append(current)
        for neighbor in adj_list[current]:
            if not visited[neighbor]:
                visited[neighbor] = True
                queue.append(neighbor)

    return traversal_order

def bfs_suggestions(request):
    query = request.GET.get('query', '')  
    x, edge_index, sorted_df = get_graph()  # <-- use cached graph

    suggested_books = []

    if query:
        try:
            book_row = sorted_df[sorted_df['title'].str.contains(query, case=False, na=False)].iloc[0]
            start_node = book_row['node_id']

            traversal = bfs(start_node, edge_index, len(sorted_df))
            suggested_books = sorted_df[sorted_df['node_id'].isin(traversal[1:6])]

        except IndexError:
            pass  # no matching book

    context = {
        'suggested_books': suggested_books
    }
    return render(request, "test.html", context)
