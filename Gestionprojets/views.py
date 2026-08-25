from django.shortcuts import render

# Create your views here.
def Gestion(request):
    return render (  request  , 'gestionprojets/projets.html')