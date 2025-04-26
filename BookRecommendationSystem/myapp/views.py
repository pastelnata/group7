import json

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
from .forms import SupportForm
from django.conf import settings
# Create your views here.





def libraryview(request):
    event_list=Book.objects.all()
    # random books since loading whole database makes the system loads for at least 5 min or it is breaking 
    random_books = event_list.order_by(Random())[:10]  
    return render(request, "libraryview.html", {'event_list': random_books})  

def autocomplete(request):
    if 'term' in request.GET:
        qs = Book.objects.filter(title__icontains=request.GET.get('term'))
        titles = list()
        for product in qs:
            titles.append(product.title)

        # titles = [product.title for product in qs]
        return JsonResponse(titles, safe=False)
    return render(request,"home.html")

def top10_page(request):
    # dummy data
    top10s = {
        "Top 10 fiction": [f"Book {i}" for i in range(1, 11)],
        "Top 10 non-fiction": [f"Book {i}" for i in range(1, 11)],
        "Top 10 science": [f"Book {i}" for i in range(1, 11)],
        "Top 10 history": [f"Book {i}" for i in range(1, 11)],
        "Top 10 fantasy": [f"Book {i}" for i in range(1, 11)],
        "Top 10 biography": [f"Book {i}" for i in range(1, 11)],
        "Top 10 mystery": [f"Book {i}" for i in range(1, 11)],
        "Top 10 romance": [f"Book {i}" for i in range(1, 11)],
    }
    return render(request,"top10.html", {"top10s": top10s})

def homepage(request):
    return render(request, "homepage.html")

def support_view(request):
    if request.method == 'POST':
        form = SupportForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            content = form.cleaned_data['content']
            
            full_message = f"From: {email}\n\n{content}"
            
            send_mail(
                subject,
                full_message,
                settings.DEFAULT_FROM_EMAIL,
                ['800.attari@gmail.com'], 
            )
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('support')
    else:
        form = SupportForm()
    
    return render(request, 'myapp/support.html', {'form': form})



## build_graph() function is preparing dataset in a way that makes it usable as a graph.
#  it is needed to perform graph-based algorithms like Breadth-First Search (BFS).


# put this outside of any function in your views.py


def build_graph():
    book_qs = Book.objects.all().values()
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
