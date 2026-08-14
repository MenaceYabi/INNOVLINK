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


def role_choice(request):
    return render(
        request,
        "authentification/role.html"
    )


def register_view(request):
    """
    Inscription selon le rôle choisi.
    """
    role = request.GET.get("role", "porteur")
    if role == "porteur":
        if request.method == "POST":
            form = PorteurProjetForm(request.POST)
            if form.is_valid():
                utilisateur = form.save()
                request.session["user_id"] = str(utilisateur.pk)
                request.session["role"] = "porteur"
                return redirect("dashboard_porteur")
        else:
            form = PorteurProjetForm()

    elif role == "startup":
        if request.method == "POST":
            form = StartupForm(request.POST)
            if form.is_valid():
              utilisateur = form.save()
            request.session["user_id"] = str(
                    utilisateur.id
                )
            request.session["role"] = "startup"
            return redirect("dashboard_startup")
        else:
            form = StartupForm()



    elif role == "structure":
        if request.method == "POST":
            form = StructureFinancementForm(request.POST)
            if form.is_valid():
               utilisateur = form.save()
            request.session["user_id"] = str(
                    utilisateur.id
                )
            request.session["role"] = "structure"
            return redirect("dashboard_structure")
               
        else:
            form = StructureFinancementForm()
    else:
        messages.error(
            request,
            "Rôle invalide."
        )
        return redirect("role_choice")
    return render(
        request,
        "authentification/register.html",
        {
            "form": form,
            "role": role
        }
    )


def login_view(request):

    role = request.GET.get("role", "porteur")

    if request.method == "POST":
        email = request.POST.get(
            "email",
            ""
        ).strip().lower()
        mot_de_passe = request.POST.get(
            "mot_de_passe",
            ""
        )
        utilisateur = None
        if role == "porteur":
            utilisateur = PorteurProjet.objects.filter(
                email=email
            ).first()
            dashboard = "dashboard_porteur"
        elif role == "startup":
            utilisateur = Startup.objects.filter(
                email=email
            ).first()
            dashboard = "dashboard_startup"
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
            return redirect("role_choice")
        if utilisateur is None:
            messages.error(
                request,
                "Aucun compte ne correspond à cet email."
            )
            return render(
                request,
                "authentification/login.html",
                {"role": role}
            )
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
                "authentification/login.html",
                {"role": role}
            )
        if utilisateur.statut_compte != "ACTIF":
            messages.error(
                request,
                "Votre compte n'est pas actif."
            )
            return render(
                request,
                "authentification/login.html",
                {"role": role}
            )
        if role in ["startup", "structure"]:
            if utilisateur.statut_validation != "VALIDE":
                messages.warning(
                    request,
                    "Votre compte est encore en attente "
                    "de validation par l'administration."
                )
                return render(
                    request,
                    "authentification/login.html",
                    {"role": role}
                )
        request.session["user_id"] = str(
            utilisateur.id
        )
        request.session["role"] = role
        return redirect(dashboard)
    return render(
        request,
        "authentification/login.html",
        {
            "role": role
        }
    )


def logout_view(request):

    request.session.flush()

    return redirect("role")