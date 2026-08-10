from django.shortcuts import render
from django.http import HttpResponse # type: ignore

# Create your views here.
def role_choice(request):
    return render(request, "authentification/role.html")


def login_view(request):
    role = request.GET.get("role", "porteur")
    context = {'role': role}
    return render(request, "authentification/login.html", context)


def register_view(request):
    role = request.GET.get("role", "porteur")
    context = {'role': role}
    return render(request, "authentification/register.html", context)