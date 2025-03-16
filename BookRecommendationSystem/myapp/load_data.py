import pandas as pd
from myapp.models import Book

df = pd.read_csv('BookRecommendationSystem/myapp/dataset/kindle_data-v2.csv')


books = [
    Book(
        asin=row['asin'],
        title=row['title'],
        author=row['author'],
        soldBy=row['soldBy'],
        imgURL=row['imgURL'],
        productURL=row['productURL'],
        stars=row['stars'],
        reviews=row['reviews'],
        price=row['price'],
        isKindleUnlimited=row['isKindleUnlimited'],
        category_id=row['category_id'],
        isBestSeller=row['isBestSeller'],
        isEditorsPick=row['isEditorsPick'],
        isGoodReadsChoice=row['isGoodReadsChoice'],
        published_date=row['published_date'],
        category_name=row['category_name'],
    )
    for _, row in df.iterrows()
]

Book.objects.bulk_create(books)
print("Data imported successfully!")
