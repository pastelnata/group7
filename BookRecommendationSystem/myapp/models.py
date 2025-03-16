from django.db import models

class Book(models.Model):
    asin = models.CharField(max_length=20, unique=True, null=True, blank=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    soldBy = models.CharField(max_length=255, unique=True, null=True, blank=True)
    productURL = models.CharField(max_length=255, unique=True, null=True, blank=True)
    imgURL = models.CharField(max_length=255, unique=True, null=True, blank=True)
    stars = models.IntegerField(null=True, blank=True, unique=True)
    reviews = models.IntegerField(null=True, blank=True, unique=True)
    price = models.IntegerField(null=True, blank=True, unique=True)
    isKindleUnlimited = models.BooleanField(default=False)
    category_id = models.IntegerField(null=True, blank=True, unique=True)
    isBestSeller = models.BooleanField(default=False)
    isEditorsPick = models.BooleanField(default=False)
    isGoodReadsChoice = models.BooleanField(default=False)
    published_date = models.DateField(null=True, blank=True)
    category_name = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.title

#DON'T FORGET TO CHANGE FIELDS
#ALSO MAKE MIGRATIONS 
#python3 manage.py makemigrations myapp
#python3 manage.py migrate

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