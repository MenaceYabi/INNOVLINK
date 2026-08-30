from django.shortcuts import render, redirect
from django.contrib import messages
from Authentification.models import StructureFinancement
from Gestionprojets.models import Projet
import re


# ============================================================
# OUTIL : EXTRAIRE LE SCORE IA DEPUIS resultat
# ============================================================

def extraire_score(resultat):
    """
    Extrait le score global depuis le champ Projet.resultat.

    Exemples acceptés :
        Score global : 95/100
        Score : 92
        score_global = 91
        Score IA : 94/100

    Si aucun score n'est trouvé :
        retourne 0
    """

    if not resultat:
        return 0

    texte = str(resultat)

    patterns = [
        r"score\s*global\s*[:=]\s*(\d+(?:[.,]\d+)?)",
        r"score\s*ia\s*[:=]\s*(\d+(?:[.,]\d+)?)",
        r"score\s*[:=]\s*(\d+(?:[.,]\d+)?)",
        r"score\s*global\s*[-:]?\s*(\d+(?:[.,]\d+)?)\s*/\s*100",
        r"score\s*[-:]?\s*(\d+(?:[.,]\d+)?)\s*/\s*100",
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            texte,
            re.IGNORECASE
        )

        if match:
            try:
                score = float(
                    match.group(1).replace(",", ".")
                )

                return min(
                    max(score, 0),
                    100
                )

            except (ValueError, TypeError):
                pass

    return 0


# ============================================================
# DASHBOARD STRUCTURE DE FINANCEMENT
# ============================================================

def dashboard(request):

    # ========================================================
    # 1. VERIFICATION DE LA SESSION
    # ========================================================

    user_id = request.session.get("user_id")
    role = request.session.get("role")

    if not user_id:
        return redirect("login")


    # ========================================================
    # 2. VERIFICATION DU ROLE
    # ========================================================

    if role != "structure":
        return redirect("login")


    # ========================================================
    # 3. RECUPERATION DE LA STRUCTURE CONNECTEE
    # ========================================================

    try:

        structure = StructureFinancement.objects.get(
            id=user_id
        )

    except StructureFinancement.DoesNotExist:

        request.session.flush()

        return redirect("login")


    # ========================================================
    # 4. VERIFICATION DU COMPTE
    # ========================================================

    if structure.statut_compte != "ACTIF":

        messages.error(
            request,
            "Votre compte est désactivé."
        )

        request.session.flush()

        return redirect("login")


    # ========================================================
    # 5. VERIFICATION DE LA VALIDATION
    # ========================================================

    if structure.statut_validation != "VALIDE":

        return redirect(
            "inscriptionattente"
        )


    # ========================================================
    # 6. RECUPERATION DE TOUS LES PROJETS
    # ========================================================
    #
    # L'onglet "Projets" doit afficher TOUS les projets
    # présents sur la plateforme.
    #

    projets = Projet.objects.select_related(
        "porteur"
    ).all().order_by(
        "-id"
    )


    # ========================================================
    # 7. PREPARATION DU SCORE IA
    # ========================================================

    projets_avec_score = []

    for projet in projets:

        score = extraire_score(
            projet.resultat
        )

        # On ajoute dynamiquement le score
        # sans modifier le modèle.
        projet.score_global = score

        projets_avec_score.append(
            projet
        )


    # ========================================================
    # 8. RECOMMANDATIONS IA
    # ========================================================
    #
    # Top 3 des meilleurs projets ayant au minimum 90/100.
    #

    projets_recommandes = sorted(
        [
            projet
            for projet in projets_avec_score
            if projet.score_global >= 90
        ],
        key=lambda projet: projet.score_global,
        reverse=True
    )[:3]


    # ========================================================
    # 9. PROJETS CORRESPONDANT AU TYPE DE COLLABORATION
    # ========================================================
    #
    # Exemple :
    #
    # Structure :
    # type_collaboration = INVESTISSEMENT
    #
    # Elle pourra retrouver les projets ayant :
    # type_collaboration = INVESTISSEMENT
    #
    # IMPORTANT :
    # On conserve aussi TOUS les projets dans "projets".
    #

    projets_compatibles = [
        projet
        for projet in projets_avec_score
        if projet.type_collaboration
        == structure.type_collaboration
    ]


    # ========================================================
    # 10. STATISTIQUES
    # ========================================================

    projets_count = len(
        projets_avec_score
    )

    projets_compatibles_count = len(
        projets_compatibles
    )

    recommandations_count = len(
        projets_recommandes
    )


    # ========================================================
    # 11. CONTEXTE ENVOYE AU HTML
    # ========================================================

    context = {

        # Structure connectée
        "structure": structure,

        # Tous les projets
        "projets": projets_avec_score,

        # Projets correspondant au type de collaboration
        "projets_compatibles": projets_compatibles,

        # Recommandations IA
        "projets_recommandes": projets_recommandes,

        # Statistiques
        "projets_count": projets_count,

        "projets_compatibles_count":
            projets_compatibles_count,

        "recommandations_count":
            recommandations_count,

        # Informations de la structure
        "type_collaboration":
            structure.get_type_collaboration_display(),

        "type_structure":
            structure.get_type_structure_display(),

        # Pour l'instant, aucune relation de financement
        # n'existe dans ton modèle.
        "favoris_count": 0,

        "collaborations_count": 0,

        "projets_suivis_count": 0,
    }


    # ========================================================
    # 12. AFFICHAGE
    # ========================================================

    return render(
        request,
        "StructureFinancement/dashboard.html",
        context
    )