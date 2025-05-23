import json

from django.db.models.functions import Random

from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from books.models import Book
from search.views import search_books

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .forms import SupportForm
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

def libraryview(request):
    event_list=Book.objects.all()
    random_books = event_list.order_by(Random())[:3]  
    return render(request, "libraryview.html", {'event_list': random_books})  

def autocomplete(request):
    if 'term' in request.GET:
        qs = Book.objects.filter(title__icontains=request.GET.get('term'))
        titles = list()
        for product in qs:
            titles.append(product.title)

        return JsonResponse(titles, safe=False)
    return render(request,"home.html")

def support_view(request):
    if request.method == 'POST':
        form = SupportForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            content = form.cleaned_data['content']
            
            full_message = f"From: {email}\n\n{content}"
            
            send_mail(
                subject,
                full_message,
                settings.DEFAULT_FROM_EMAIL,
                ['800.attari@gmail.com'], 
            )
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('support')
    else:
        form = SupportForm()
    
    return render(request, 'myapp/support.html', {'form': form})

def welcome(request):
    return render(request, 'myapp/welcome.html')

def about(request):
    return render(request, 'myapp/about.html')

@csrf_exempt
def get_recommendations(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            query = Book.objects.all()
            
            if data.get('tags'):
                if 'bestseller' in data['tags']:
                    query = query.filter(isBestSeller=True)
                if 'editors-pick' in data['tags']:
                    query = query.filter(isEditorsPick=True)
                if 'goodreads-choice' in data['tags']:
                    query = query.filter(isGoodReadsChoice=True)
                if 'highly-rated' in data['tags']:
                    query = query.filter(stars__gte=4.5)
                if 'new-releases' in data['tags']:
                    query = query.filter(published_date__isnull=False).order_by('-published_date')
                if 'kindle-unlimited' in data['tags']:
                    query = query.filter(isKindleUnlimited=True)
            
            if data.get('genres'):
                query = query.filter(category_name__in=data['genres'])
            
            if data.get('price'):
                if data['price'] == 'free':
                    query = query.filter(price=0)
                elif data['price'] == 'under5':
                    query = query.filter(price__lt=5)
                elif data['price'] == 'under10':
                    query = query.filter(price__lt=10)
                elif data['price'] == 'under15':
                    query = query.filter(price__lt=15)
            
            if data.get('rating') and data['rating'] != 'any':
                query = query.filter(stars__gte=float(data['rating']))
            
            results = query.order_by(Random())[:10]
            recommendations = []
            
            for book in results:
                recommendations.append({
                    'title': book.title,
                    'author': book.author,
                    'rating': book.stars,
                    'category': book.category_name,
                    'image': book.imgURL,
                    'product_url': book.productURL,
                    'is_bestseller': book.isBestSeller,
                    'is_editors_pick': book.isEditorsPick,
                    'is_goodreads_choice': book.isGoodReadsChoice
                })
            
            return JsonResponse({'recommendations': recommendations})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)
