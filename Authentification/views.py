from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password

from .forms import (
    PorteurProjetForm,
    StartupForm,
    StructureFinancementForm
)

from .models import (
    Admin,
    PorteurProjet,
    Startup,
    StructureFinancement
)


# ============================================================
# CHOIX DU ROLE POUR L'INSCRIPTION
# ============================================================

def role_choice(request):

    return render(
        request,
        "authentification/role.html"
    )


# ============================================================
# INSCRIPTION
# ============================================================

def register_view(request):
    """
    Inscription selon le rôle choisi.

    Porteur :
        - compte créé
        - connexion automatique
        - accès au dashboard

    Startup / Structure :
        - compte créé
        - statut_validation = EN_ATTENTE
        - redirection vers la page d'attente
    """

    role = request.GET.get("role", "porteur")

    # ========================================================
    # PORTEUR DE PROJET
    # ========================================================

    if role == "porteur":

        if request.method == "POST":

            form = PorteurProjetForm(request.POST)

            if form.is_valid():

                utilisateur = form.save()

                request.session["user_id"] = str(
                    utilisateur.pk
                )

                request.session["role"] = "porteur"

                return redirect(
                    "dashboard_porteur"
                )

        else:
            form = PorteurProjetForm()


    # ========================================================
    # STARTUP
    # ========================================================

    elif role == "startup":

        if request.method == "POST":

            form = StartupForm(request.POST)

            if form.is_valid():

                utilisateur = form.save()

                # Session temporaire pour la page d'attente
                request.session["user_id"] = str(
                    utilisateur.id
                )

                request.session["role"] = "startup"

                messages.success(
                    request,
                    "Votre inscription a été enregistrée avec succès."
                )

                return redirect(
                    "inscriptionattente"
                )

        else:
            form = StartupForm()


    # ========================================================
    # STRUCTURE DE FINANCEMENT
    # ========================================================

    elif role == "structure":

        if request.method == "POST":

            form = StructureFinancementForm(request.POST)

            if form.is_valid():

                utilisateur = form.save()

                # Session temporaire pour la page d'attente
                request.session["user_id"] = str(
                    utilisateur.id
                )

                request.session["role"] = "structure"

                messages.success(
                    request,
                    "Votre inscription a été enregistrée avec succès."
                )

                return redirect(
                    "inscriptionattente"
                )

        else:
            form = StructureFinancementForm()


    # ========================================================
    # ROLE INVALIDE
    # ========================================================

    else:

        messages.error(
            request,
            "Rôle invalide."
        )

        return redirect(
            "role"
        )


    # ========================================================
    # AFFICHAGE DU FORMULAIRE
    # ========================================================

    return render(
        request,
        "authentification/register.html",
        {
            "form": form,
            "role": role
        }
    )


# ============================================================
# PAGE D'ATTENTE DE VALIDATION
# ============================================================

def inscription_attente(request):

    role = request.session.get("role")
    user_id = request.session.get("user_id")

    if not role or not user_id:
        return redirect("login")

    compte = None
    type_compte = ""

    if role == "startup":

        compte = Startup.objects.filter(
            id=user_id
        ).first()

        type_compte = "Startup"

    elif role == "structure":

        compte = StructureFinancement.objects.filter(
            id=user_id
        ).first()

        type_compte = "Structure de financement"

    else:

        return redirect("login")

    if not compte:
        return redirect("login")

    # ========================================================
    # COMPTE VALIDÉ PAR L'ADMINISTRATION
    # ========================================================

    if (
        compte.statut_validation == "VALIDE"
        and compte.statut_compte == "ACTIF"
    ):

        if role == "startup":
            return redirect("dashboard_startup")

        if role == "structure":
            return redirect("dashboard_structure")


    # ========================================================
    # AFFICHAGE DE LA PAGE D'ATTENTE
    # ========================================================

    return render(
        request,
        "authentification/inscriptionattente.html",
        {
            "type_compte": type_compte,
            "email": compte.email,
            "statut": compte.statut_validation,
            "motif_rejet": compte.motif_rejet,
        }
    )


# ============================================================
# CONNEXION UNIQUE POUR TOUS LES UTILISATEURS
# ============================================================

def login_view(request):

    if request.method == "POST":

        # ====================================================
        # RECUPERATION DES DONNEES
        # ====================================================

        email = request.POST.get(
            "email",
            ""
        ).strip().lower()

        mot_de_passe = request.POST.get(
            "mot_de_passe",
            ""
        )

        utilisateur = None
        role = None
        dashboard = None


        # ====================================================
        # 1. RECHERCHE ADMINISTRATEUR
        # ====================================================

        admin = Admin.objects.filter(
            email=email
        ).first()

        if admin:

            if not check_password(
                mot_de_passe,
                admin.mot_de_passe
            ):

                messages.error(
                    request,
                    "Email ou mot de passe incorrect."
                )

                return render(
                    request,
                    "authentification/login.html"
                )


            if admin.statut_compte != "ACTIF":

                messages.error(
                    request,
                    "Ce compte administrateur est désactivé."
                )

                return render(
                    request,
                    "authentification/login.html"
                )


            # Session administrateur
            request.session["user_id"] = str(
                admin.id
            )

            request.session["role"] = "admin"

            return redirect(
                "admin_dashboard"
            )


        # ====================================================
        # 2. RECHERCHE PORTEUR DE PROJET
        # ====================================================

        utilisateur = PorteurProjet.objects.filter(
            email=email
        ).first()

        if utilisateur:

            role = "porteur"
            dashboard = "dashboard_porteur"


        # ====================================================
        # 3. RECHERCHE STARTUP
        # ====================================================

        else:

            utilisateur = Startup.objects.filter(
                email=email
            ).first()

            if utilisateur:

                role = "startup"
                dashboard = "dashboard_startup"


        # ====================================================
        # 4. RECHERCHE STRUCTURE DE FINANCEMENT
        # ====================================================

        if utilisateur is None:

            utilisateur = StructureFinancement.objects.filter(
                email=email
            ).first()

            if utilisateur:

                role = "structure"
                dashboard = "dashboard_structure"


        # ====================================================
        # AUCUN COMPTE TROUVE
        # ====================================================

        if utilisateur is None:

            messages.error(
                request,
                "Email ou mot de passe incorrect."
            )

            return render(
                request,
                "authentification/login.html"
            )


        # ====================================================
        # VERIFICATION DU MOT DE PASSE
        # ====================================================

        if not check_password(
            mot_de_passe,
            utilisateur.mot_de_passe
        ):

            messages.error(
                request,
                "Email ou mot de passe incorrect."
            )

            return render(
                request,
                "authentification/login.html"
            )


        # ====================================================
        # VERIFICATION DU STATUT DU COMPTE
        # ====================================================

        if utilisateur.statut_compte != "ACTIF":

            messages.error(
                request,
                "Votre compte est désactivé."
            )

            return render(
                request,
                "authentification/login.html"
            )


        # ====================================================
        # VERIFICATION DE LA VALIDATION
        # STARTUP + STRUCTURE
        # ====================================================

        if role in ["startup", "structure"]:

            # ------------------------------------------------
            # COMPTE EN ATTENTE
            # ------------------------------------------------

            if utilisateur.statut_validation == "EN_ATTENTE":

                messages.warning(
                    request,
                    "Votre compte est encore en attente "
                    "de validation par l'administration."
                )

                return render(
                    request,
                    "authentification/login.html"
                )


            # ------------------------------------------------
            # COMPTE REFUSE
            # ------------------------------------------------

            if utilisateur.statut_validation == "REJETE":

                motif = utilisateur.motif_rejet

                if motif:

                    messages.error(
                        request,
                        f"Votre inscription a été refusée. "
                        f"Motif : {motif}"
                    )

                else:

                    messages.error(
                        request,
                        "Votre inscription a été refusée "
                        "par l'administration."
                    )

                return render(
                    request,
                    "authentification/login.html"
                )


            # ------------------------------------------------
            # COMPTE NON VALIDE
            # ------------------------------------------------

            if utilisateur.statut_validation != "VALIDE":

                messages.error(
                    request,
                    "Votre compte n'est pas encore autorisé "
                    "à accéder à la plateforme."
                )

                return render(
                    request,
                    "authentification/login.html"
                )


        # ====================================================
        # CREATION DE LA SESSION
        # ====================================================

        request.session["user_id"] = str(
            utilisateur.id
        )

        request.session["role"] = role


        # ====================================================
        # REDIRECTION SELON LE ROLE
        # ====================================================

        return redirect(
            dashboard
        )


    # ========================================================
    # AFFICHAGE DE LA PAGE DE CONNEXION
    # ========================================================

    return render(
        request,
        "authentification/login.html"
    )


# ============================================================
# DECONNEXION
# ============================================================

def logout_view(request):

    request.session.flush()

    return redirect(
        "home"
    )