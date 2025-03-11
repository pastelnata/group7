from django.db import models


# Create your models here.

""" when Library is name of the database
class Library(models.Model):
    book_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=500)
    authors = models.CharField(max_length=500)
    average_rating = models.FloatField()
    isbn = models.CharField(max_length=20, unique=True)
    isbn13 = models.CharField(max_length=30, unique=True)
    language_code = models.CharField(max_length=10)
    num_pages = models.IntegerField()
    ratings_count = models.IntegerField()
    text_reviews_count = models.IntegerField()
    publication_date = models.DateField()
    publisher = models.CharField(max_length=255)

    def __str__(self):
        return self.title"
        
        """