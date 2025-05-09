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
# Create your views here.

def libraryview(request):
    event_list=Book.objects.all()
    # random books since loading whole database makes the system loads for at least 5 min or it is breaking 
    random_books = event_list.order_by(Random())[:3]  
    return render(request, "libraryview.html", {'event_list': random_books})  

def autocomplete(request):
    if 'term' in request.GET:
        qs = Book.objects.filter(title__icontains=request.GET.get('term'))
        titles = list()
        for product in qs:
            titles.append(product.title)

        # titles = [product.title for product in qs]
        return JsonResponse(titles, safe=False)
    return render(request,"home.html")

def homepage(request):
    return render(request, "homepage.html")

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
