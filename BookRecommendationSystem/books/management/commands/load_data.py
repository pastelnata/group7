from django.core.management.base import BaseCommand
import pandas as pd
from books.models import Book
import os
from datetime import datetime

class Command(BaseCommand):
    help = 'Loads book data from CSV into the database'

    def handle(self, *args, **kwargs):
        books_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        csv_path = os.path.join(books_dir, 'dataset', 'kindle_data-v2.csv')

        self.stdout.write(f"Attempting to read file from: {csv_path}")

        try:
            df = pd.read_csv(csv_path)
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            exit()

        df.columns = df.columns.str.strip()

        string_columns = ['asin', 'title', 'author', 'soldBy', 'imgURL', 'productURL', 'category_name']
        for col in string_columns:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()

        df = df.rename(columns={
            'imgUrl': 'imgURL',
            'publishedDate': 'published_date'
        })

        boolean_columns = ['isKindleUnlimited', 'isBestSeller', 'isEditorsPick', 'isGoodReadsChoice']
        for col in boolean_columns:
            if col in df.columns:
                df[col] = df[col].astype(str).str.lower() == 'true'

        df['stars'] = pd.to_numeric(df['stars'], errors='coerce')
        df['reviews'] = pd.to_numeric(df['reviews'], errors='coerce')
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        df['category_id'] = pd.to_numeric(df['category_id'], errors='coerce')

        def convert_date(date_str):
            try:
                if pd.isna(date_str):
                    return None
                date_str = str(date_str)
                return datetime.strptime(date_str, '%Y-%m-%d').date()
            except (ValueError, TypeError):
                return None

        df['published_date'] = df['published_date'].apply(convert_date)

        unique_fields = ['asin', 'soldBy', 'productURL', 'imgURL', 'stars', 'reviews', 'price', 'category_id']
        df = df.drop_duplicates(subset=unique_fields, keep='first')

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
                category_name=row['category_name']
            )
            for _, row in df.iterrows()
        ]

        Book.objects.bulk_create(books)
        print("Data imported successfully!")