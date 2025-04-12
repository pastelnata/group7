#it does work
import csv
import heapq
import math
from collections import defaultdict
import os

def load_books_from_csv():
    # Adjust the path maybe
    csv_path = os.path.join(os.path.dirname(__file__), 'dataset', 'kindle_data-v2.csv')

    books = []

    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                stars = float(row['stars'])
                reviews = int(row['reviews'])
                category = row['category_name']
                title = row['title']
                author = row['author']

                # popularity formula so it include the number of reviews too, 
                popularity = stars * math.log(reviews + 1)

                books.append({
                    'title': title,
                    'author': author,
                    'category': category, #or category_name?
                    'stars': stars,
                    'reviews': reviews,
                    'popularity': popularity
                })

            except (ValueError, KeyError):
                continue  # Skip bad data

    return books


def get_top_k_books(books, k=10):
    global_heap = []
    category_heaps = defaultdict(list)

    for book in books:
        pop = book['popularity']
        category = book['category']

        # Global Top-K
        if len(global_heap) < k:
            heapq.heappush(global_heap, (pop, book['title'], book))
        else:
            if pop > global_heap[0][0]:
                heapq.heappushpop(global_heap, (pop, book['title'], book))

        # Category Top-K
        heap = category_heaps[category]
        if len(heap) < k:
            heapq.heappush(heap, (pop, book['title'], book))
        else:
            if pop > heap[0][0]:
                heapq.heappushpop(heap, (pop, book['title'], book))

    return {
        'global': [book for _, _, book in sorted(global_heap, reverse=True)],
        'categories': {
            cat: [book for _, _, book in sorted(h, reverse=True)]
            for cat, h in category_heaps.items()
        }
    }
