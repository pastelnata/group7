import json
import traceback
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from books.filter_books import filter_books_by_criteria
from books.filter_books import serialize_book
from recommendation.graph.graph import get_cached_graph
from .recommendation import get_graph_recommendations, calculate_recommendation_scores
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def get_recommendations(request):
	if request.method == 'POST':
		try:
			data = json.loads(request.body)
			adj, book_lookup = get_cached_graph()
			books = filter_books_by_criteria(data)
			filtered_book_ids = set(book.id for book in books)
			recommendation_scores = calculate_recommendation_scores(filtered_book_ids, adj, book_lookup)
			recommended_books = get_graph_recommendations(recommendation_scores, book_lookup, filtered_book_ids, limit=20)
			if len(recommended_books) < 20:
				remaining_slots = 20 - len(recommended_books)
				for book in books.order_by('-stars', '-reviews')[:remaining_slots]:
					recommended_books.append(serialize_book(book))
			logger.debug(f"Final recommendations count: {len(recommended_books)}")
			return JsonResponse({'recommendations': recommended_books})
		except json.JSONDecodeError as e:
			logger.error(f"JSON decode error: {str(e)}")
			return JsonResponse({'error': 'Invalid JSON data'}, status=400)
		except Exception as e:
			logger.error(f"Unexpected error: {str(e)}")
			logger.error(f"Traceback: {traceback.format_exc()}")
			return JsonResponse({'error': str(e)}, status=400)
	return JsonResponse({'error': 'Invalid request method'}, status=400)