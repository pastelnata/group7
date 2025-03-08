from django.shortcuts import render, HttpResponse

# Create your views here.
def autocomplete(request):
    return render(request,"home.html") 