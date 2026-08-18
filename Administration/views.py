from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password

from Authentification.models import Admin


def admin_login(request):

    if request.method == "POST":
        email = request.POST.get(
            "email",
            ""
        ).strip().lower()

        mot_de_passe = request.POST.get(
            "mot_de_passe",
            ""
        )

        admin = Admin.objects.filter(
            email=email
        ).first()

        if admin is None:
            messages.error(
                request,
                "Email ou mot de passe incorrect."
            )

            return render(
                request,
                "Administration/admin_login.html"
            )

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
                "Administration/admin_login.html"
            )

        if admin.statut_compte != "ACTIF":
            messages.error( request,"Ce compte administrateur est désactivé.")
            return render( request, "Administration/admin_login.html")
        request.session["admin_id"] = str( admin.id)
        request.session["role"] = "admin"
        return redirect("admin_dashboard")
    return render(request,"Administration/admin_login.html")


def admin_dashboard(request):
    if "admin_id" not in request.session:
        return redirect("admin_login")
    return render( request,"Administration/dashboard.html")


def admin_logout(request):
    request.session.flush()
    return redirect(
        "admin_login"
    )