from django.urls import path
from . import views


urlpatterns = [

    # ======================================================
    # DASHBOARD
    # ======================================================

    path(
        "dashboard/",
        views.admin_dashboard,
        name="admin_dashboard"
    ),


    # ======================================================
    # PORTEURS DE PROJETS
    # ======================================================

    path(
        "porteur/ajouter/",
        views.ajouter_porteur,
        name="ajouter_porteur"
    ),

    path(
        "porteur/<uuid:porteur_id>/modifier/",
        views.modifier_porteur,
        name="modifier_porteur"
    ),

    path(
        "porteur/<uuid:porteur_id>/supprimer/",
        views.supprimer_porteur,
        name="supprimer_porteur"
    ),


    # ======================================================
    # STARTUPS
    # ======================================================

    path(
        "startup/ajouter/",
        views.ajouter_startup,
        name="ajouter_startup"
    ),

    path(
        "startup/<uuid:startup_id>/modifier/",
        views.modifier_startup,
        name="modifier_startup"
    ),

    path(
        "startup/<uuid:startup_id>/supprimer/",
        views.supprimer_startup,
        name="supprimer_startup"
    ),


    # ======================================================
    # STRUCTURES DE FINANCEMENT
    # ======================================================

    path(
        "structure/ajouter/",
        views.ajouter_structure,
        name="ajouter_structure"
    ),

    path(
        "structure/<uuid:structure_id>/modifier/",
        views.modifier_structure,
        name="modifier_structure"
    ),

    path(
        "structure/<uuid:structure_id>/supprimer/",
        views.supprimer_structure,
        name="supprimer_structure"
    ),


    # ======================================================
    # VALIDATION STARTUP
    # ======================================================

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


    # ======================================================
    # VALIDATION STRUCTURE
    # ======================================================

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


    # ======================================================
    # LOGOUT
    # ======================================================

    path(
        "logout/",
        views.admin_logout,
        name="admin_logout"
    ),
]