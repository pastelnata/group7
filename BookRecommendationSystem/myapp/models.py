from django.db import models

class Book(models.Model):
    asin = models.CharField(max_length=20, unique=True, null=True, blank=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    soldBy = models.CharField(max_length=255, null=True, blank=True)
    productURL = models.CharField(max_length=255, unique=True, null=True, blank=True)
    imgURL = models.CharField(max_length=255, null=True, blank=True)
    stars = models.IntegerField(null=True, blank=True)
    reviews = models.IntegerField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    isKindleUnlimited = models.BooleanField(default=False)
    category_id = models.IntegerField(null=True, blank=True)
    isBestSeller = models.BooleanField(default=False)
    isEditorsPick = models.BooleanField(default=False)
    isGoodReadsChoice = models.BooleanField(default=False)
    published_date = models.DateField(null=True, blank=True)
    category_name = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.title
