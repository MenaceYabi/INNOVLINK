from django.shortcuts import render, redirect

from Authentification.models import PorteurProjet
from .models import Projet
from .forms import ProjetForm


def Gestion(request):

    # ==========================================
    # 1. RÉCUPÉRER L'UTILISATEUR CONNECTÉ
    # ==========================================
    user_id = request.session.get("user_id")
    role = request.session.get("role")

    # Si personne n'est connecté
    if not user_id:
        return redirect("login")

    # Vérifier qu'il s'agit bien d'un porteur
    if role != "porteur":
        return redirect("login")

    # ==========================================
    # 2. RÉCUPÉRER LE PORTEUR
    # ==========================================
    try:
        porteur = PorteurProjet.objects.get(id=user_id)
    except PorteurProjet.DoesNotExist:
        return redirect("login")

    # ==========================================
    # 3. AFFICHAGE DU FORMULAIRE
    # ==========================================
    if request.method == "GET":

        form = ProjetForm()

        return render(
            request,
            "gestionprojets/projets.html",
            {
                "form": form,
                "porteur": porteur,
            }
        )

    # ==========================================
    # 4. TRAITEMENT DU FORMULAIRE
    # ==========================================
    if request.method == "POST":

        form = ProjetForm(
            request.POST,
            request.FILES
        )

        # ======================================
        # 5. VALIDATION DU FORMULAIRE
        # ======================================
        if form.is_valid():

            # Ne pas enregistrer directement
            # avant d'avoir associé le porteur
            projet = form.save(commit=False)

            # Association automatique au porteur connecté
            projet.porteur = porteur

            # Pour l'instant resultat reste vide.
            # Il sera rempli plus tard par l'IA.
            projet.resultat = None

            # Enregistrement en BD
            projet.save()

            # ==================================
            # 6. RETOUR AU DASHBOARD
            # ==================================
            return redirect("dashboard")

        # ======================================
        # 7. EN CAS D'ERREUR
        # ======================================
        return render(
            request,
            "gestionprojets/projets.html",
            {
                "form": form,
                "porteur": porteur,
            }
        )