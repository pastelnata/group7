from django.urls import path
from . import views 

urlpatterns = [
    path("",views.autocomplete,name="autocomplete"),
    path("top10/", views.top10_page, name="top10_page")
]