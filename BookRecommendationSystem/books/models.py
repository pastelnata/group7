from django.db import models

# Create your models here.
class Book(models.Model):
    asin = models.CharField(max_length=20, unique=True, null=True, blank=True)
    title = models.CharField(max_length=255, db_index=True)
    author = models.CharField(max_length=255, db_index=True)
    soldBy = models.CharField(max_length=255, null=True, blank=True)
    productURL = models.URLField(max_length=500, null=True, blank=True)
    imgURL = models.URLField(max_length=500, null=True, blank=True)
    stars = models.FloatField(null=True, blank=True, db_index=True)
    reviews = models.IntegerField(null=True, blank=True, db_index=True)
    price = models.FloatField(null=True, blank=True, db_index=True)
    isKindleUnlimited = models.BooleanField(default=False, db_index=True)
    category_id = models.IntegerField(null=True, blank=True, db_index=True)
    isBestSeller = models.BooleanField(default=False, db_index=True)
    isEditorsPick = models.BooleanField(default=False, db_index=True)
    isGoodReadsChoice = models.BooleanField(default=False, db_index=True)
    published_date = models.DateField(null=True, blank=True)
    category_name = models.CharField(max_length=255, null=True, blank=True, db_index=True)

    def __str__(self):
        return self.title

    @classmethod
    def get_unique_categories(cls):
        """Get all unique categories from the database"""
        return cls.objects.exclude(category_name__isnull=True).values_list('category_name', flat=True).distinct()

    @classmethod
    def get_popular_books(cls, limit=10):
        """Get popular books based on ratings and reviews"""
        return cls.objects.exclude(stars__isnull=True).order_by('-stars', '-reviews')[:limit]

    @classmethod
    def get_best_sellers(cls):
        """Get all bestseller books"""
        return cls.objects.filter(isBestSeller=True)

    @classmethod
    def get_editors_picks(cls):
        """Get all editor's pick books"""
        return cls.objects.filter(isEditorsPick=True)

    @classmethod
    def get_goodreads_choices(cls):
        """Get all Goodreads Choice winners"""
        return cls.objects.filter(isGoodReadsChoice=True)

    def get_similar_books(self, limit=5):
        """Get similar books based on category and author"""
        similar_books = set()
        
        category_matches = Book.objects.filter(
            category_name=self.category_name
        ).exclude(id=self.id)
        
        author_matches = Book.objects.filter(
            author=self.author
        ).exclude(id=self.id)
        
        for book in category_matches:
            similar_books.add((book, 1))
        
        for book in author_matches:
            similar_books.add((book, 2))
        
        return sorted(similar_books, key=lambda x: x[1], reverse=True)[:limit]

    class Meta:
        indexes = [
            models.Index(fields=['category_name', 'stars']),
            models.Index(fields=['price', 'stars']),
            models.Index(fields=['isBestSeller', 'stars']),
            models.Index(fields=['isEditorsPick', 'stars']),
            models.Index(fields=['isGoodReadsChoice', 'stars']),
            models.Index(fields=['isKindleUnlimited', 'stars']),
        ]
