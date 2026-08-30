from django.urls import path
from . import views


urlpatterns = [
    # Choix du rôle
    path(
        "role/",
        views.role_choice,
        name="role"
    ),

    # Inscription selon le rôle
    path(
        "register/",
        views.register_view,
        name="register"
    ),

    # Connexion selon le rôle
    path(
        "login/",
        views.login_view,
        name="login"
    ),

    # Déconnexion
    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),
    
    path(
    "inscription-attente/",
    views.inscription_attente,
    name="inscriptionattente"
),
]
