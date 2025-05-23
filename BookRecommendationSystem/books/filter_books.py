from django.views.decorators.csrf import csrf_exempt
from recommendation.graph.graph import get_cached_graph
from .models import Book
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)

def filter_books_by_criteria(data):
	tags = data.get('tags', [])
	genres = data.get('genres', [])
	price = data.get('price')
	rating = data.get('rating')
	books = Book.objects.all()
	books = filter_by_genres(books, genres)
	books = filter_by_price(books, price)
	books = filter_by_rating(books, rating)
	books = filter_by_tags(books, tags)
	return books

def filter_by_genres(books, genres):
	if genres:
		books = books.filter(category_name__in=genres)
	return books

def filter_by_price(books, price):
	if price and price != 'any':
		if price == 'free':
			books = books.filter(price=0)
		elif price == 'under5':
			books = books.filter(price__lt=500)
		elif price == 'under10':
			books = books.filter(price__lt=1000)
		elif price == 'under15':
			books = books.filter(price__lt=1500)
	return books

def filter_by_rating(books, rating):
	if rating and rating != 'any':
		try:
			rating_value = int(rating)
			books = books.filter(stars__gte=rating_value)
		except ValueError:
			pass
	return books

def filter_by_tags(books, tags):
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
	return books

def serialize_book(book):
	return {
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
		'image': book.imgURL if hasattr(book, 'imgURL') else None,
		'product_url': book.productURL if hasattr(book, 'productURL') else None
	}
