from django.urls import path
from . import views

urlpatterns =[
    path('' , views.Gestion , name="Gestion"),
        path("TEST/", views.test_gemini, name="test_gemini"),
]