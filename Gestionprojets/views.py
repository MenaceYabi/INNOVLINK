from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
import re

from Authentification.models import PorteurProjet
from Gestionprojets.gemini_service import tester_gemini
from .models import Projet
from .forms import ProjetForm


# ============================================================
# EXTRACTION DU SCORE IA
# ============================================================

def extraire_score(resultat):

    """
    Extrait le score global depuis le résultat de Gemini.

    Exemple :
        Score global : 87/100

    Retourne :
        87.0
        ou None si aucun score trouvé.
    """

    if not resultat:
        return None

    # --------------------------------------------------------
    # Formats prioritaires
    # --------------------------------------------------------

    patterns = [

        r"score\s+global\s*[:\-]?\s*(\d+(?:[.,]\d+)?)\s*/\s*100",

        r"score\s+total\s*[:\-]?\s*(\d+(?:[.,]\d+)?)\s*/\s*100",

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
    # Dernier recours
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
# GESTION / CRÉATION DU PROJET
# ============================================================

def Gestion(request):

    # ========================================================
    # 1. VÉRIFICATION DE LA SESSION
    # ========================================================

    user_id = request.session.get("user_id")
    role = request.session.get("role")

    if not user_id:
        return redirect("login")

    if role != "porteur":
        return redirect("login")


    # ========================================================
    # 2. RÉCUPÉRER LE PORTEUR CONNECTÉ
    # ========================================================

    try:

        porteur = PorteurProjet.objects.get(
            id=user_id
        )

    except PorteurProjet.DoesNotExist:

        request.session.flush()

        return redirect("login")


    # ========================================================
    # 3. AFFICHAGE DU FORMULAIRE
    # ========================================================

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


    # ========================================================
    # 4. TRAITEMENT DU FORMULAIRE
    # ========================================================

    if request.method == "POST":

        form = ProjetForm(
            request.POST,
            request.FILES
        )


        # ====================================================
        # 5. VALIDATION DU FORMULAIRE
        # ====================================================

        if not form.is_valid():

            return render(
                request,
                "gestionprojets/projets.html",
                {
                    "form": form,
                    "porteur": porteur,
                }
            )


        # ====================================================
        # 6. RÉCUPÉRATION DES DONNÉES
        # ====================================================

        phase = form.cleaned_data["phase"]

        nom = form.cleaned_data["nom"]

        description = form.cleaned_data["description"]

        technologies = form.cleaned_data["technologies"]

        domaines_d_etude = form.cleaned_data[
            "domaines_d_etude"
        ]

        type_collaboration = form.cleaned_data[
            "type_collaboration"
        ]

        fichier_analyse = form.cleaned_data.get(
            "fichier_analyse"
        )


        # ====================================================
        # 7. DONNÉES POUR GEMINI
        # ====================================================

        donnees_projet = {

            "nom": nom,

            "phase": phase,

            "description": description,

            "technologies": technologies,

            "domaines_d_etude": domaines_d_etude,

            "type_collaboration": type_collaboration,
        }


        # ====================================================
        # 8. ANALYSE IA
        # ====================================================

        try:

            resultat_ia = tester_gemini(

                donnees_projet=donnees_projet,

                fichier=fichier_analyse
            )


        except Exception as e:

            form.add_error(
                None,
                f"L'analyse IA a échoué : {str(e)}"
            )

            return render(
                request,
                "gestionprojets/projets.html",
                {
                    "form": form,
                    "porteur": porteur,
                    "erreur_analyse": True,
                }
            )


        # ====================================================
        # 9. EXTRACTION DU SCORE
        # ====================================================

        score_ia = extraire_score(
            resultat_ia
        )


        # ====================================================
        # 10. VÉRIFICATION DU SCORE
        # ====================================================

        if score_ia is None:

            form.add_error(
                None,
                "L'analyse IA a été effectuée, "
                "mais aucun score valide n'a été trouvé."
            )

            return render(
                request,
                "gestionprojets/projets.html",
                {
                    "form": form,
                    "porteur": porteur,
                    "erreur_analyse": True,
                }
            )


        # ====================================================
        # 11. CRÉATION DU PROJET
        # ====================================================

        projet = Projet(

            porteur=porteur,

            phase=phase,

            nom=nom,

            description=description,

            technologies=technologies,

            domaines_d_etude=domaines_d_etude,

            type_collaboration=type_collaboration,

            resultat=resultat_ia
        )


        # ====================================================
        # 12. ENREGISTREMENT
        # ====================================================

        projet.save()


        # ====================================================
        # 13. REDIRECTION VERS LE DASHBOARD
        # ====================================================

        return redirect(
            "dashboard_porteur"
        )


# ============================================================
# TEST GEMINI
# ============================================================

def test_gemini(request):

    try:

        resultat = tester_gemini()

        return HttpResponse(
            f"""
            <h1>Test Gemini réussi ✅</h1>

            <p>{resultat}</p>
            """
        )

    except Exception as e:

        return HttpResponse(
            f"""
            <h1>Erreur Gemini ❌</h1>

            <p>{str(e)}</p>
            """,
            status=500
        )