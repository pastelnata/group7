import json
import traceback
from collections import defaultdict
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from books.filter_books import filter_books_by_criteria
from books.filter_books import serialize_book
from recommendation.graph.graph import get_cached_graph
import logging

logger = logging.getLogger(__name__)

def get_graph_recommendations(recommendation_scores, book_lookup, filtered_book_ids, limit=20):
	recommended_books = []
	for book_id, score in sorted(recommendation_scores.items(), key=lambda x: x[1], reverse=True):
		if book_id in book_lookup and book_id not in filtered_book_ids:
			book = book_lookup[book_id]
			recommended_books.append(serialize_book(book))
			if len(recommended_books) >= limit:
				break
	return recommended_books

def calculate_recommendation_scores(filtered_book_ids, adj, book_lookup):
	recommendation_scores = defaultdict(float)
	for book_id in filtered_book_ids:
		if book_id in adj:
			for neighbor_id in adj[book_id]:
				if neighbor_id in book_lookup:
					neighbor = book_lookup[neighbor_id]
					score = (neighbor.stars or 0) * (neighbor.reviews or 1)
					recommendation_scores[neighbor_id] += score
	return recommendation_scores
