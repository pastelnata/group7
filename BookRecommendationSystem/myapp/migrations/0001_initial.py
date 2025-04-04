# Generated by Django 5.1.3 on 2025-03-13 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_id', models.IntegerField(unique=True)),
                ('title', models.CharField(max_length=255)),
                ('authors', models.CharField(max_length=255)),
                ('average_rating', models.FloatField()),
                ('isbn', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('language_code', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
    ]
