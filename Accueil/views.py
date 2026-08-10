from django.http import HttpResponse # type: ignore
from django.shortcuts import render # type: ignore

# Create your views here.

def home(request):
    return render( request , 'accueil/home.html')

def Contact(request):
    return render( request , 'accueil/contact.html')
