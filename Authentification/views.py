from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password

from .forms import (
    PorteurProjetForm,
    StartupForm,
    StructureFinancementForm
)

from .models import (
    PorteurProjet,
    Startup,
    StructureFinancement
)


def role(request):
    """
    Page de choix du rôle.
    """
    return render(
        request,
        "Authentification/role.html"
    )


def register(request, role):
    """
    Inscription selon le rôle choisi.
    """

    if role == "porteur":

        if request.method == "POST":
            form = PorteurProjetForm(request.POST)

            if form.is_valid():
                form.save()

                messages.success(
                    request,
                    "Votre compte a été créé avec succès."
                )

                return redirect(
                    "login",
                    role="porteur"
                )

        else:
            form = PorteurProjetForm()

    elif role == "startup":

        if request.method == "POST":
            form = StartupForm(request.POST)

            if form.is_valid():
                form.save()

                messages.success(
                    request,
                    "Votre compte startup a été créé. "
                    "Il doit maintenant être validé."
                )

                return redirect(
                    "login",
                    role="startup"
                )

        else:
            form = StartupForm()

    elif role == "structure":

        if request.method == "POST":
            form = StructureFinancementForm(request.POST)

            if form.is_valid():
                form.save()

                messages.success(
                    request,
                    "Votre compte a été créé. "
                    "Il doit maintenant être validé."
                )

                return redirect(
                    "login",
                    role="structure"
                )

        else:
            form = StructureFinancementForm()

    else:
        messages.error(
            request,
            "Rôle invalide."
        )

        return redirect("profil")

    return render(
        request,
        "Authentification/register.html",
        {
            "form": form,
            "role": role
        }
    )


def login_view(request, role):
    """
    Connexion selon le rôle choisi.
    """

    if request.method == "POST":

        email = request.POST.get("email", "").strip().lower()
        mot_de_passe = request.POST.get(
            "mot_de_passe",
            ""
        )

        utilisateur = None

        # Porteur de projet
        if role == "porteur":

            utilisateur = PorteurProjet.objects.filter(
                email=email
            ).first()

            dashboard = "dashboard_porteur"

        # Startup
        elif role == "startup":

            utilisateur = Startup.objects.filter(
                email=email
            ).first()

            dashboard = "dashboard_startup"

        # Structure de financement
        elif role == "structure":

            utilisateur = StructureFinancement.objects.filter(
                email=email
            ).first()

            dashboard = "dashboard_structure"

        else:
            messages.error(
                request,
                "Rôle invalide."
            )

            return redirect("profil")

        # Vérification du compte
        if utilisateur is None:

            messages.error(
                request,
                "Aucun compte ne correspond à cet email."
            )

            return render(
                request,
                "Authentification/login.html",
                {
                    "role": role
                }
            )

        # Vérification du mot de passe
        if not check_password(
            mot_de_passe,
            utilisateur.mot_de_passe
        ):

            messages.error(
                request,
                "Mot de passe incorrect."
            )

            return render(
                request,
                "Authentification/login.html",
                {
                    "role": role
                }
            )

        # Vérification du statut
        if utilisateur.statut_compte != "ACTIF":

            messages.error(
                request,
                "Votre compte n'est pas actif."
            )

            return render(
                request,
                "Authentification/login.html",
                {
                    "role": role
                }
            )

        # Pour startup et structure :
        # le compte doit être validé par l'administration.
        if role in ["startup", "structure"]:

            if utilisateur.statut_validation != "VALIDE":

                messages.warning(
                    request,
                    "Votre compte est encore en attente "
                    "de validation par l'administration."
                )

                return render(
                    request,
                    "Authentification/login.html",
                    {
                        "role": role
                    }
                )

        # Création de la session Django
        request.session["user_id"] = str(
            utilisateur.id
        )

        request.session["role"] = role

        return redirect(dashboard)

    return render(
        request,
        "Authentification/login.html",
        {
            "role": role
        }
    )


def logout_view(request):
    """
    Déconnexion.
    """

    request.session.flush()

    return redirect("role")