from django.shortcuts import render, redirect

from Authentification.models import PorteurProjet
from Gestionprojets.models import Projet


def dashboard(request):

    # 1. Vérification de la session
    user_id = request.session.get("user_id")
    role = request.session.get("role")

    # 2. Vérification de l'authentification
    if not user_id:
        return redirect("login")

    # 3. Vérification du rôle
    if role != "porteur":
        return redirect("login")

    # 4. Récupération du véritable porteur connecté
    try:
        porteur = PorteurProjet.objects.get(id=user_id)
    except PorteurProjet.DoesNotExist:
        return redirect("login")

    # 5. Récupération uniquement des projets de ce porteur
    projets = porteur.projets.all()

    # 6. Données envoyées au template
    context = {
        "porteur": porteur,
        "projets": projets,
    }

    # 7. Affichage du dashboard
    return render(
        request,
        "poteur/dashboard.html",
        context
    )