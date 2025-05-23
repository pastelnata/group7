from django.shortcuts import render

import json
from django.db.models.functions import Random
from django.http import JsonResponse
from django.shortcuts import render
from books.models import Book
from books.views import serialize_book, filter_books_by_criteria 
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def get_recommendations(request):
	if request.method != 'POST':
		return JsonResponse({'error': 'Invalid request method'}, status=405)
	try:
		data = json.loads(request.body)
		query = Book.objects.all()
		query = filter_books_by_criteria(data)
		results = query.order_by(Random())[:10]
		recommendations = [serialize_book(book) for book in results]
		return JsonResponse({'recommendations': recommendations})
	except Exception as e:
		return JsonResponse({'error': str(e)}, status=400)

def homepage_view(request):
	context = {
		'categories': Book.get_unique_categories(),
		'popular_books': Book.get_popular_books(limit=10),
		'best_sellers': Book.get_best_sellers()[:5],
		'editors_picks': Book.get_editors_picks()[:5],
		'goodreads_choices': Book.get_goodreads_choices()[:5],
	}
	return render(request, "homepage.html", context)
