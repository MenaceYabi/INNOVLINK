from django.urls import path
from . import views


urlpatterns = [

    path(
        "",
        views.Gestion,
        name="Gestion"
    ),

    path(
        "projet/<int:projet_id>/modifier/",
        views.modifier_projet,
        name="modifier_projet"
    ),

    path(
        "projet/<int:projet_id>/supprimer/",
        views.supprimer_projet,
        name="supprimer_projet"
    ),

]