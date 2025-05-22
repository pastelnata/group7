from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Book
import logging
from search.search.graph import build_graph_adj_list
from collections import defaultdict
import traceback
from django.core.cache import cache
from django.conf import settings

logger = logging.getLogger(__name__)

def get_cached_graph():
    """Get or build the graph from cache"""
    cache_key = 'book_recommendation_graph'
    cached_data = cache.get(cache_key)
    
    if cached_data is None:
        logger.debug("Building new graph...")
        adj, book_lookup = build_graph_adj_list()
        cache.set(cache_key, (adj, book_lookup), 3600)
        return adj, book_lookup
    
    return cached_data


@csrf_exempt
def get_recommendations(request):
    if request.method == 'POST':
        try:
            logger.debug(f"Request body: {request.body}")
            
            data = json.loads(request.body)
            tags = data.get('tags', [])
            genres = data.get('genres', [])
            price = data.get('price')
            rating = data.get('rating')
            
            logger.debug(f"Parsed data: tags={tags}, genres={genres}, price={price}, rating={rating}")
            
            adj, book_lookup = get_cached_graph()
            logger.debug(f"Using graph with {len(adj)} nodes")
            
            books = Book.objects.all()
            logger.debug(f"Initial book count: {books.count()}")
            
            if genres:
                books = books.filter(category_name__in=genres)
                logger.debug(f"After genre filter: {books.count()} books")
            
            if price and price != 'any':
                if price == 'free':
                    books = books.filter(price=0)
                elif price == 'under5':
                    books = books.filter(price__lt=500)
                elif price == 'under10':
                    books = books.filter(price__lt=1000)
                elif price == 'under15':
                    books = books.filter(price__lt=1500)
                logger.debug(f"After price filter: {books.count()} books")
            
            if rating and rating != 'any':
                try:
                    rating_value = int(rating)
                    books = books.filter(stars__gte=rating_value)
                    logger.debug(f"After rating filter: {books.count()} books")
                except ValueError:
                    logger.error(f"Invalid rating value: {rating}")
            
            if 'bestseller' in tags:
                books = books.filter(isBestSeller=True)
            if 'editors-pick' in tags:
                books = books.filter(isEditorsPick=True)
            if 'goodreads-choice' in tags:
                books = books.filter(isGoodReadsChoice=True)
            if 'kindle-unlimited' in tags:
                books = books.filter(isKindleUnlimited=True)
            if 'highly-rated' in tags:
                books = books.filter(stars__gte=4)
            logger.debug(f"After tag filters: {books.count()} books")
            
            filtered_book_ids = set(book.id for book in books)
            logger.debug(f"Filtered book IDs count: {len(filtered_book_ids)}")
            
            recommendation_scores = defaultdict(float)
            
            for book_id in filtered_book_ids:
                if book_id in adj:
                    for neighbor_id in adj[book_id]:
                        if neighbor_id in book_lookup:
                            neighbor = book_lookup[neighbor_id]
                            score = (neighbor.stars or 0) * (neighbor.reviews or 1)
                            recommendation_scores[neighbor_id] += score
            
            logger.debug(f"Recommendation scores calculated for {len(recommendation_scores)} books")
            
            recommended_books = []
            for book_id, score in sorted(recommendation_scores.items(), key=lambda x: x[1], reverse=True):
                if book_id in book_lookup and book_id not in filtered_book_ids:
                    book = book_lookup[book_id]
                    recommended_books.append({
                        'id': book.id,
                        'title': book.title,
                        'author': book.author,
                        'rating': float(book.stars) if book.stars is not None else None,
                        'price': book.price,
                        'category': book.category_name,
                        'is_bestseller': book.isBestSeller,
                        'is_editors_pick': book.isEditorsPick,
                        'is_goodreads_choice': book.isGoodReadsChoice,
                        'is_kindle_unlimited': book.isKindleUnlimited,
                        'image': book.imgURL if book.imgURL else None,
                        'product_url': book.productURL if book.productURL else None
                    })
                    if len(recommended_books) >= 20:
                        break
            
            logger.debug(f"Graph-based recommendations count: {len(recommended_books)}")
            
            if len(recommended_books) < 20:
                remaining_slots = 20 - len(recommended_books)
                for book in books.order_by('-stars', '-reviews')[:remaining_slots]:
                    recommended_books.append({
                        'id': book.id,
                        'title': book.title,
                        'author': book.author,
                        'rating': float(book.stars) if book.stars is not None else None,
                        'price': book.price,
                        'category': book.category_name,
                        'is_bestseller': book.isBestSeller,
                        'is_editors_pick': book.isEditorsPick,
                        'is_goodreads_choice': book.isGoodReadsChoice,
                        'is_kindle_unlimited': book.isKindleUnlimited,
                        'image': book.imgURL if book.imgURL else None,
                        'product_url': book.productURL if book.productURL else None
                    })
            
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

@csrf_exempt
def get_filtered_books(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            tags = data.get('tags', [])
            genres = data.get('genres', [])
            price = data.get('price')
            rating = data.get('rating')
            
            books = Book.objects.all()
            
            if genres:
                books = books.filter(category_name__in=genres)
            
            if price and price != 'any':
                if price == 'free':
                    books = books.filter(price=0)
                elif price == 'under5':
                    books = books.filter(price__lt=500)  # Assuming price is in cents
                elif price == 'under10':
                    books = books.filter(price__lt=1000)
                elif price == 'under15':
                    books = books.filter(price__lt=1500)
            
            if rating and rating != 'any':
                books = books.filter(stars__gte=int(rating))
            
            if 'bestseller' in tags:
                books = books.filter(isBestSeller=True)
            if 'editors-pick' in tags:
                books = books.filter(isEditorsPick=True)
            if 'goodreads-choice' in tags:
                books = books.filter(isGoodReadsChoice=True)
            if 'kindle-unlimited' in tags:
                books = books.filter(isKindleUnlimited=True)
            if 'highly-rated' in tags:
                books = books.filter(stars__gte=4)
            
            books = books.order_by('-stars', '-reviews')[:20]  # Limit to 20 books
            
            response_data = [{
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'rating': book.stars,
                'price': book.price,
                'category': book.category_name,
                'is_bestseller': book.isBestSeller,
                'is_editors_pick': book.isEditorsPick,
                'is_goodreads_choice': book.isGoodReadsChoice,
                'is_kindle_unlimited': book.isKindleUnlimited
            } for book in books]
            
            return JsonResponse({'books': response_data})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)
