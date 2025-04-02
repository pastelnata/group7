from django.urls import path
from . import views
from django.http import JsonResponse

def search_view(request):
    query = request.GET.get('q', '')
    limit = int(request.GET.get('limit', 25))
    results = views.search_books(query, limit)
    return JsonResponse({
        'results': [
            {
                'title': book.title,
                'author': book.author,
                'stars': book.stars,
                'reviews': book.reviews,
                'price': book.price,
            } for book in results
        ]
    })

urlpatterns = [
    path('', search_view, name='bst-search'),
] 