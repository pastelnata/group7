from django.urls import path
from . import views
from django.http import JsonResponse

#def search_view(request):
#    query = request.GET.get('q', '')
#    limit = int(request.GET.get('limit', 25))
#    results = views.search_books(query, limit)
#    return JsonResponse({
#        'results': [
#            {
#                'title': book.title,
#                'author': book.author,
#                'stars': book.stars,
#                'reviews': book.reviews,
#                'price': book.price,
#            } for book in results
#        ]
#    })

#def search_bar(request):
#    return

urlpatterns = [
    path('', views.search_results, name='bst-search'),
] 