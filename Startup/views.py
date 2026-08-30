from django.shortcuts import render, redirect
from django.db.models import Q
import re

from Authentification.models import Startup
from Gestionprojets.models import Projet


# ============================================================
# EXTRACTION DU SCORE IA DEPUIS "resultat"
# ============================================================

def extraire_score(resultat):

    """
    Extrait le score total depuis le texte généré par l'IA.

    Exemples acceptés :

        Score total : 94/100
        Score global : 94/100
        Score : 94/100
        Note globale : 94/100
        94/100

    Retourne :
        float -> score trouvé
        None  -> aucun score trouvé
    """

    if not resultat:
        return None

    # --------------------------------------------------------
    # Recherche prioritaire des formats explicites
    # --------------------------------------------------------

    patterns = [

        r"score\s+total\s*[:\-]?\s*(\d+(?:[.,]\d+)?)\s*/\s*100",

        r"score\s+global\s*[:\-]?\s*(\d+(?:[.,]\d+)?)\s*/\s*100",

        r"score\s*[:\-]?\s*(\d+(?:[.,]\d+)?)\s*/\s*100",

        r"note\s+globale\s*[:\-]?\s*(\d+(?:[.,]\d+)?)\s*/\s*100",

        r"note\s+totale\s*[:\-]?\s*(\d+(?:[.,]\d+)?)\s*/\s*100",

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            resultat,
            re.IGNORECASE
        )

        if match:

            score = match.group(1).replace(",", ".")

            try:
                return float(score)
            except ValueError:
                pass


    # --------------------------------------------------------
    # Dernier recours : recherche d'un nombre /100
    # --------------------------------------------------------

    match = re.search(
        r"(\d+(?:[.,]\d+)?)\s*/\s*100",
        resultat
    )

    if match:

        score = match.group(1).replace(",", ".")

        try:
            return float(score)
        except ValueError:
            return None


    return None


# ============================================================
# DASHBOARD UNIQUE DE LA STARTUP
# ============================================================

def dashboard(request):

    # ========================================================
    # 1. VERIFICATION DE LA SESSION
    # ========================================================

    user_id = request.session.get("user_id")
    role = request.session.get("role")

    if not user_id:
        return redirect("login")

    if role != "startup":
        return redirect("login")


    # ========================================================
    # 2. RECUPERATION DE LA STARTUP CONNECTEE
    # ========================================================

    try:

        startup = Startup.objects.get(
            id=user_id
        )

    except Startup.DoesNotExist:

        request.session.flush()

        return redirect("login")


    # ========================================================
    # 3. VERIFICATION DU STATUT
    # ========================================================

    if startup.statut_compte != "ACTIF":
        return redirect("login")

    if startup.statut_validation != "VALIDE":
        return redirect("inscriptionattente")


    # ========================================================
    # 4. RECUPERATION DE TOUS LES PROJETS
    # ========================================================

    tous_les_projets = list(
        Projet.objects.select_related(
            "porteur"
        ).all()
    )


    # ========================================================
    # 5. EXTRACTION DU SCORE IA
    #
    # On ne modifie PAS le modèle.
    # Le score est calculé à partir de resultat.
    # ========================================================

    for projet in tous_les_projets:

        projet.score_ia = extraire_score(
            projet.resultat
        )


    # ========================================================
    # 6. RECHERCHE
    # ========================================================

    recherche = request.GET.get(
        "q",
        ""
    ).strip()


    projets_filtres = tous_les_projets


    if recherche:

        recherche_lower = recherche.lower()

        projets_filtres = [

            projet

            for projet in projets_filtres

            if (
                recherche_lower in projet.nom.lower()
                or
                recherche_lower in projet.description.lower()
                or
                recherche_lower in projet.technologies.lower()
                or
                recherche_lower in projet.domaines_d_etude.lower()
                or
                recherche_lower in projet.porteur.nom.lower()
                or
                recherche_lower in projet.porteur.prenom.lower()
            )

        ]


    # ========================================================
    # 7. FILTRE PAR PHASE
    # ========================================================

    phase = request.GET.get(
        "phase",
        ""
    )

    if phase:

        projets_filtres = [

            projet

            for projet in projets_filtres

            if projet.phase == phase

        ]


    # ========================================================
    # 8. TRI
    # ========================================================

    tri = request.GET.get(
        "tri",
        "recent"
    )


    if tri == "ancien":

        projets_filtres.sort(
            key=lambda projet: projet.id
        )

    else:

        projets_filtres.sort(
            key=lambda projet: projet.id,
            reverse=True
        )


    # ========================================================
    # 9. TOP 3 RECOMMANDATIONS IA
    #
    # Tous les projets de la plateforme
    # Score >= 90
    # Tri décroissant
    # Maximum 3
    # ========================================================

    projets_scores = [

        projet

        for projet in tous_les_projets

        if projet.score_ia is not None
        and projet.score_ia >= 90

    ]


    projets_scores.sort(
        key=lambda projet: projet.score_ia,
        reverse=True
    )


    recommandations = projets_scores[:3]


    # ========================================================
    # 10. PROJETS COMPATIBLES AVEC LE TYPE DE COLLABORATION
    #
    # Ce n'est PAS le filtre principal.
    # Cela pourra servir à personnaliser l'expérience.
    # ========================================================

    projets_compatibles = [

        projet

        for projet in tous_les_projets

        if projet.type_collaboration
        == startup.type_collaboration

    ]


    projets_compatibles.sort(
        key=lambda projet: (
            projet.score_ia
            if projet.score_ia is not None
            else -1
        ),
        reverse=True
    )


    # ========================================================
    # 11. STATISTIQUES
    # ========================================================

    nombre_projets = len(
        tous_les_projets
    )


    # Pour l'instant les modèles Favori /
    # Collaboration ne sont pas présents.

    nombre_favoris = 0

    nombre_collaborations = 0


    # ========================================================
    # 12. CONTEXT
    # ========================================================

    context = {

        "startup": startup,

        # Tous les projets après filtres
        "projets": projets_filtres,

        # Nombre total sur la plateforme
        "nombre_projets": nombre_projets,

        # Top 3 IA
        "recommandations": recommandations,

        # Projets correspondant au profil
        "projets_compatibles": projets_compatibles,

        # Filtres
        "recherche": recherche,

        "phase_selectionnee": phase,

        "tri": tri,

        # Choix des phases
        "phases": Projet.PHASE_CHOICES,

        # Type de collaboration de la startup
        "type_collaboration": (
            startup.get_type_collaboration_display()
        ),

    }


    # ========================================================
    # 13. UNIQUE PAGE
    # ========================================================

    return render(
        request,
        "Startup/dashboard.html",
        context
    )