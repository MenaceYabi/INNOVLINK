
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.utils import timezone

from Authentification.models import (
    Admin,
    PorteurProjet,
    Startup,
    StructureFinancement,
)


# ==========================================================
# CONNEXION ADMINISTRATEUR
# ==========================================================

def admin_login(request):

    if request.method == "POST":

        email = request.POST.get("email", "").strip().lower()
        mot_de_passe = request.POST.get("mot_de_passe", "")

        # Recherche de l'administrateur
        admin = Admin.objects.filter(email=email).first()

        # Vérification du compte
        if admin is None:
            messages.error(
                request,
                "Email ou mot de passe incorrect."
            )
            return render(
                request,
                "Administration/admin_login.html"
            )

        # Vérification du mot de passe
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

        # Vérification du statut
        if admin.statut_compte != "ACTIF":
            messages.error(
                request,
                "Ce compte administrateur est désactivé."
            )
            return render(
                request,
                "Administration/admin_login.html"
            )

        # Création de la session
        request.session["admin_id"] = str(admin.id)
        request.session["role"] = "admin"

        return redirect("admin_dashboard")

    return render(
        request,
        "Administration/admin_login.html"
    )


# ==========================================================
# DASHBOARD ADMINISTRATEUR
# ==========================================================

def admin_dashboard(request):

    # Vérification de la connexion
    if "admin_id" not in request.session:
        return redirect("admin_login")

    # Récupération de l'administrateur connecté
    admin = Admin.objects.filter(
        id=request.session["admin_id"]
    ).first()

    # Si l'administrateur n'existe plus
    if admin is None:
        request.session.flush()
        return redirect("admin_login")

    # Vérification du statut
    if admin.statut_compte != "ACTIF":

        request.session.flush()

        messages.error(
            request,
            "Votre compte administrateur est désactivé."
        )

        return redirect("admin_login")

    # ======================================================
    # STATISTIQUES
    # ======================================================

    total_porteurs = PorteurProjet.objects.count()

    total_startups = Startup.objects.count()

    total_structures = StructureFinancement.objects.count()

    # Comptes actuellement en attente
    startups_en_attente = Startup.objects.filter(
        statut_validation="EN_ATTENTE"
    ).count()

    structures_en_attente = StructureFinancement.objects.filter(
        statut_validation="EN_ATTENTE"
    ).count()

    comptes_en_attente = (
        startups_en_attente +
        structures_en_attente
    )

    # ======================================================
    # DEMANDES DE VALIDATION
    # ======================================================

    demandes = []

    # Startups en attente
    startups = Startup.objects.filter(
        statut_validation="EN_ATTENTE"
    ).order_by("-date_inscription")

    for startup in startups:

        demandes.append({
            "id": startup.id,
            "nom": startup.nom_startup,
            "type": "Startup",
            "email": startup.email,
            "date_inscription": startup.date_inscription,
            "objet": "startup",
        })

    # Structures en attente
    structures = StructureFinancement.objects.filter(
        statut_validation="EN_ATTENTE"
    ).order_by("-date_inscription")

    for structure in structures:

        demandes.append({
            "id": structure.id,
            "nom": structure.nom_structure,
            "type": "Structure de financement",
            "email": structure.email,
            "date_inscription": structure.date_inscription,
            "objet": "structure",
        })

    # Tri des demandes par date
    demandes.sort(
        key=lambda demande: demande["date_inscription"],
        reverse=True
    )

    # On affiche uniquement les 10 dernières demandes
    demandes = demandes[:10]

    # ======================================================
    # CONTEXTE ENVOYÉ AU TEMPLATE
    # ======================================================

    context = {
        "admin": admin,

        "total_porteurs": total_porteurs,
        "total_startups": total_startups,
        "total_structures": total_structures,
        "comptes_en_attente": comptes_en_attente,

        "demandes": demandes,
    }

    return render(
        request,
        "Administration/dashboard.html",
        context
    )


# ==========================================================
# VALIDATION D'UNE STARTUP
# ==========================================================

def valider_startup(request, startup_id):

    # Vérification de la session admin
    if "admin_id" not in request.session:
        return redirect("admin_login")

    if request.method != "POST":
        return redirect("admin_dashboard")

    startup = get_object_or_404(
        Startup,
        id=startup_id
    )

    startup.statut_validation = "VALIDE"
    startup.statut_compte = "ACTIF"
    startup.date_validation = timezone.now()
    startup.motif_rejet = None

    startup.save()

    messages.success(
        request,
        f"La startup « {startup.nom_startup} » a été validée."
    )

    return redirect("admin_dashboard")


# ==========================================================
# REJET D'UNE STARTUP
# ==========================================================

def rejeter_startup(request, startup_id):

    # Vérification de la session admin
    if "admin_id" not in request.session:
        return redirect("admin_login")

    if request.method != "POST":
        return redirect("admin_dashboard")

    startup = get_object_or_404(
        Startup,
        id=startup_id
    )

    startup.statut_validation = "REJETE"
    startup.statut_compte = "DESACTIVE"
    startup.date_validation = timezone.now()

    startup.save()

    messages.warning(
        request,
        f"La startup « {startup.nom_startup} » a été rejetée."
    )

    return redirect("admin_dashboard")


# ==========================================================
# VALIDATION D'UNE STRUCTURE
# ==========================================================

def valider_structure(request, structure_id):

    # Vérification de la session admin
    if "admin_id" not in request.session:
        return redirect("admin_login")

    if request.method != "POST":
        return redirect("admin_dashboard")

    structure = get_object_or_404(
        StructureFinancement,
        id=structure_id
    )

    structure.statut_validation = "VALIDE"
    structure.statut_compte = "ACTIF"
    structure.date_validation = timezone.now()
    structure.motif_rejet = None

    structure.save()

    messages.success(
        request,
        f"La structure « {structure.nom_structure} » a été validée."
    )

    return redirect("admin_dashboard")


# ==========================================================
# REJET D'UNE STRUCTURE
# ==========================================================

def rejeter_structure(request, structure_id):

    # Vérification de la session admin
    if "admin_id" not in request.session:
        return redirect("admin_login")

    if request.method != "POST":
        return redirect("admin_dashboard")

    structure = get_object_or_404(
        StructureFinancement,
        id=structure_id
    )

    structure.statut_validation = "REJETE"
    structure.statut_compte = "DESACTIVE"
    structure.date_validation = timezone.now()

    structure.save()

    messages.warning(
        request,
        f"La structure « {structure.nom_structure} » a été rejetée."
    )

    return redirect("admin_dashboard")


# ==========================================================
# DECONNEXION ADMINISTRATEUR
# ==========================================================

def admin_logout(request):

    request.session.flush()

    return redirect("admin_login")
