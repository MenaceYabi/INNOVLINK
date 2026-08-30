from django.urls import path

from . import views


urlpatterns = [

    # Authentification
    path(
        "login/",
        views.admin_login,
        name="admin_login"
    ),

    # Dashboard
    path(
        "dashboard/",
        views.admin_dashboard,
        name="admin_dashboard"
    ),

    # Validations startups
    path(
        "startup/<uuid:startup_id>/valider/",
        views.valider_startup,
        name="valider_startup"
    ),

    path(
        "startup/<uuid:startup_id>/rejeter/",
        views.rejeter_startup,
        name="rejeter_startup"
    ),

    # Validations structures
    path(
        "structure/<uuid:structure_id>/valider/",
        views.valider_structure,
        name="valider_structure"
    ),

    path(
        "structure/<uuid:structure_id>/rejeter/",
        views.rejeter_structure,
        name="rejeter_structure"
    ),

    # Déconnexion
    path(
        "logout/",
        views.admin_logout,
        name="admin_logout"
    ),
]