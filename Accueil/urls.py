
from django.urls import path # type: ignore
from . import views # type: ignore

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.Contact, name='contact'),
]