from django.urls import path
from . import views


urlpatterns = [

    path(
        "role/",
        views.role,
        name="role"
    ),

    path(
        "register/<str:role>/",
        views.register,
        name="register"
    ),

    path(
        "login/<str:role>/",
        views.login_view,
        name="login"
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),
]