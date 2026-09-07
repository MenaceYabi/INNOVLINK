from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.db.models.deletion import ProtectedError
from django.urls import reverse

from Authentification.models import (
    Admin,
    PorteurProjet,
    Startup,
    StructureFinancement,
)

from Authentification.forms import (
    PorteurProjetForm,
    StartupForm,
    StructureFinancementForm,
)


# ==========================================================
# VÉRIFICATION ADMIN
# ==========================================================

def admin_required(request):
    """
    Vérifie que l'utilisateur connecté est bien un administrateur
    actif.
    """

    if request.session.get("role") != "admin":
        return False

    admin_id = request.session.get("user_id")

    if not admin_id:
        return False

    admin = Admin.objects.filter(id=admin_id).first()

    if not admin:
        return False

    if admin.statut_compte != "ACTIF":
        return False

    return True


# ==========================================================
# REDIRECTION VERS UN ONGLET DU DASHBOARD
# ==========================================================

def redirect_dashboard(tab="dashboard"):
    """
    Redirige vers le dashboard en conservant l'onglet actif.
    """

    return redirect(
        f"{reverse('admin_dashboard')}?tab={tab}"
    )


# ==========================================================
# DASHBOARD ADMINISTRATEUR
# ==========================================================

def admin_dashboard(request):

    if not admin_required(request):
        request.session.flush()
        return redirect("login")

    admin = Admin.objects.filter(
        id=request.session.get("user_id")
    ).first()

    # ------------------------------------------------------
    # STATISTIQUES
    # ------------------------------------------------------

    total_porteurs = PorteurProjet.objects.count()

    total_startups = Startup.objects.count()

    total_structures = StructureFinancement.objects.count()

    startups_en_attente = Startup.objects.filter(
        statut_validation="EN_ATTENTE"
    ).count()

    structures_en_attente = StructureFinancement.objects.filter(
        statut_validation="EN_ATTENTE"
    ).count()

    comptes_en_attente = (
        startups_en_attente
        + structures_en_attente
    )

    # ------------------------------------------------------
    # DONNÉES POUR LES TABLEAUX CRUD
    # ------------------------------------------------------

    porteurs = PorteurProjet.objects.all().order_by(
        "-date_inscription"
    )

    startups = Startup.objects.all().order_by(
        "-date_inscription"
    )

    structures = StructureFinancement.objects.all().order_by(
        "-date_inscription"
    )

    # ------------------------------------------------------
    # DEMANDES DE VALIDATION
    # ------------------------------------------------------

    demandes = []

    startups_en_attente_queryset = Startup.objects.filter(
        statut_validation="EN_ATTENTE"
    ).order_by("-date_inscription")

    for startup in startups_en_attente_queryset:

        demandes.append({
            "id": startup.id,
            "nom": startup.nom_startup,
            "type": "Startup",
            "email": startup.email,
            "date_inscription": startup.date_inscription,
            "objet": "startup",
        })

    structures_en_attente_queryset = StructureFinancement.objects.filter(
        statut_validation="EN_ATTENTE"
    ).order_by("-date_inscription")

    for structure in structures_en_attente_queryset:

        demandes.append({
            "id": structure.id,
            "nom": structure.nom_structure,
            "type": "Structure de financement",
            "email": structure.email,
            "date_inscription": structure.date_inscription,
            "objet": "structure",
        })

    demandes.sort(
        key=lambda demande: demande["date_inscription"],
        reverse=True
    )

    demandes = demandes[:10]

    # ------------------------------------------------------
    # CONTEXT
    # ------------------------------------------------------

    context = {
        "admin": admin,

        "total_porteurs": total_porteurs,
        "total_startups": total_startups,
        "total_structures": total_structures,
        "comptes_en_attente": comptes_en_attente,

        "porteurs": porteurs,
        "startups": startups,
        "structures": structures,

        "demandes": demandes,
        
    "types_collaboration": Startup.TYPES_COLLABORATION,
    "types_structure": StructureFinancement.TYPES_STRUCTURE,
    }

    return render(
        request,
        "Administration/dashboard.html",
        context
    )


# ==========================================================
# PORTEURS DE PROJETS — CRÉATION
# ==========================================================

def ajouter_porteur(request):

    if not admin_required(request):
        return redirect("login")

    if request.method != "POST":
        return redirect_dashboard("porteurs")

    form = PorteurProjetForm(request.POST)

    if form.is_valid():

        porteur = form.save()

        messages.success(
            request,
            f"Le porteur de projet « {porteur.prenom} "
            f"{porteur.nom} » a été ajouté avec succès."
        )

        return redirect_dashboard("porteurs")

    messages.error(
        request,
        "Impossible d'ajouter le porteur de projet. "
        "Veuillez vérifier les informations saisies."
    )

    return redirect_dashboard("porteurs")


# ==========================================================
# PORTEURS DE PROJETS — MODIFICATION
# ==========================================================

def modifier_porteur(request, porteur_id):

    if not admin_required(request):
        return redirect("login")

    porteur = get_object_or_404(
        PorteurProjet,
        id=porteur_id
    )

    if request.method != "POST":
        return redirect_dashboard("porteurs")

    form = PorteurProjetForm(
        request.POST,
        instance=porteur
    )

    if form.is_valid():

        porteur = form.save()

        messages.success(
            request,
            f"Le porteur « {porteur.prenom} "
            f"{porteur.nom} » a été modifié avec succès."
        )

    else:

        messages.error(
            request,
            "Impossible de modifier ce porteur. "
            "Veuillez vérifier les informations saisies."
        )

    return redirect_dashboard("porteurs")


# ==========================================================
# PORTEURS DE PROJETS — SUPPRESSION
# ==========================================================

def supprimer_porteur(request, porteur_id):

    if not admin_required(request):
        return redirect("login")

    if request.method != "POST":
        return redirect_dashboard("porteurs")

    porteur = get_object_or_404(
        PorteurProjet,
        id=porteur_id
    )

    nom_porteur = f"{porteur.prenom} {porteur.nom}"

    try:

        porteur.delete()

        messages.success(
            request,
            f"Le porteur « {nom_porteur} » "
            "a été supprimé avec succès."
        )

    except ProtectedError:

        messages.error(
            request,
            "Impossible de supprimer ce porteur car "
            "des données liées à son compte existent encore."
        )

    return redirect_dashboard("porteurs")


# ==========================================================
# STARTUPS — CRÉATION
# ==========================================================

def ajouter_startup(request):

    if not admin_required(request):
        return redirect("login")

    if request.method != "POST":
        return redirect_dashboard("startups")

    form = StartupForm(request.POST)

    if form.is_valid():

        startup = form.save()

        messages.success(
            request,
            f"La startup « {startup.nom_startup} » "
            "a été ajoutée avec succès."
        )

        return redirect_dashboard("startups")

    messages.error(
        request,
        "Impossible d'ajouter la startup. "
        "Veuillez vérifier les informations saisies."
    )

    return redirect_dashboard("startups")


# ==========================================================
# STARTUPS — MODIFICATION
# ==========================================================

def modifier_startup(request, startup_id):

    if not admin_required(request):
        return redirect("login")

    startup = get_object_or_404(
        Startup,
        id=startup_id
    )

    if request.method != "POST":
        return redirect_dashboard("startups")

    form = StartupForm(
        request.POST,
        instance=startup
    )

    if form.is_valid():

        startup = form.save()

        messages.success(
            request,
            f"La startup « {startup.nom_startup} » "
            "a été modifiée avec succès."
        )

    else:

        messages.error(
            request,
            "Impossible de modifier cette startup. "
            "Veuillez vérifier les informations saisies."
        )

    return redirect_dashboard("startups")


# ==========================================================
# STARTUPS — SUPPRESSION
# ==========================================================

def supprimer_startup(request, startup_id):

    if not admin_required(request):
        return redirect("login")

    if request.method != "POST":
        return redirect_dashboard("startups")

    startup = get_object_or_404(
        Startup,
        id=startup_id
    )

    nom_startup = startup.nom_startup

    try:

        startup.delete()

        messages.success(
            request,
            f"La startup « {nom_startup} » "
            "a été supprimée avec succès."
        )

    except ProtectedError:

        messages.error(
            request,
            "Impossible de supprimer cette startup car "
            "des données liées à son compte existent encore."
        )

    return redirect_dashboard("startups")


# ==========================================================
# STRUCTURES DE FINANCEMENT — CRÉATION
# ==========================================================

def ajouter_structure(request):

    if not admin_required(request):
        return redirect("login")

    if request.method != "POST":
        return redirect_dashboard("structures")

    form = StructureFinancementForm(request.POST)

    if form.is_valid():

        structure = form.save()

        messages.success(
            request,
            f"La structure « {structure.nom_structure} » "
            "a été ajoutée avec succès."
        )

        return redirect_dashboard("structures")

    messages.error(
        request,
        "Impossible d'ajouter la structure. "
        "Veuillez vérifier les informations saisies."
    )

    return redirect_dashboard("structures")


# ==========================================================
# STRUCTURES DE FINANCEMENT — MODIFICATION
# ==========================================================

def modifier_structure(request, structure_id):

    if not admin_required(request):
        return redirect("login")

    structure = get_object_or_404(
        StructureFinancement,
        id=structure_id
    )

    if request.method != "POST":
        return redirect_dashboard("structures")

    form = StructureFinancementForm(
        request.POST,
        instance=structure
    )

    if form.is_valid():

        structure = form.save()

        messages.success(
            request,
            f"La structure « {structure.nom_structure} » "
            "a été modifiée avec succès."
        )

    else:

        messages.error(
            request,
            "Impossible de modifier cette structure. "
            "Veuillez vérifier les informations saisies."
        )

    return redirect_dashboard("structures")


# ==========================================================
# STRUCTURES DE FINANCEMENT — SUPPRESSION
# ==========================================================

def supprimer_structure(request, structure_id):

    if not admin_required(request):
        return redirect("login")

    if request.method != "POST":
        return redirect_dashboard("structures")

    structure = get_object_or_404(
        StructureFinancement,
        id=structure_id
    )

    nom_structure = structure.nom_structure

    try:

        structure.delete()

        messages.success(
            request,
            f"La structure « {nom_structure} » "
            "a été supprimée avec succès."
        )

    except ProtectedError:

        messages.error(
            request,
            "Impossible de supprimer cette structure car "
            "des données liées à son compte existent encore."
        )

    return redirect_dashboard("structures")


# ==========================================================
# VALIDATION STARTUP
# ==========================================================

def valider_startup(request, startup_id):

    if not admin_required(request):
        return redirect("login")

    if request.method != "POST":
        return redirect_dashboard("validations")

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
        f"La startup « {startup.nom_startup} » "
        "a été validée."
    )

    return redirect_dashboard("validations")


# ==========================================================
# REJET STARTUP
# ==========================================================

def rejeter_startup(request, startup_id):

    if not admin_required(request):
        return redirect("login")

    if request.method != "POST":
        return redirect_dashboard("validations")

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
        f"La startup « {startup.nom_startup} » "
        "a été rejetée."
    )

    return redirect_dashboard("validations")


# ==========================================================
# VALIDATION STRUCTURE
# ==========================================================

def valider_structure(request, structure_id):

    if not admin_required(request):
        return redirect("login")

    if request.method != "POST":
        return redirect_dashboard("validations")

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
        f"La structure « {structure.nom_structure} » "
        "a été validée."
    )

    return redirect_dashboard("validations")


# ==========================================================
# REJET STRUCTURE
# ==========================================================

def rejeter_structure(request, structure_id):

    if not admin_required(request):
        return redirect("login")

    if request.method != "POST":
        return redirect_dashboard("validations")

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
        f"La structure « {structure.nom_structure} » "
        "a été rejetée."
    )

    return redirect_dashboard("validations")


# ==========================================================
# DÉCONNEXION ADMIN
# ==========================================================

def admin_logout(request):

    request.session.flush()

    return redirect("home")