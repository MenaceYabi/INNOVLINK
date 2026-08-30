
import json

from django.conf import settings
from google import genai
from google.genai import types


# ============================================================
# CLIENT GEMINI
# ============================================================

client = genai.Client(
    api_key=settings.SECRET_KEYS
)


# ============================================================
# ANALYSE GEMINI
# ============================================================

def tester_gemini(donnees_projet=None, fichier=None):

    # ========================================================
    # TEST SIMPLE
    # ========================================================

    if donnees_projet is None:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents="Réponds simplement : INNOVLINK fonctionne."
        )

        return response.text


    # ========================================================
    # INFORMATIONS DU PROJET
    # ========================================================

    nom = donnees_projet.get("nom", "")
    phase = donnees_projet.get("phase", "")
    description = donnees_projet.get("description", "")
    technologies = donnees_projet.get("technologies", "")
    domaines = donnees_projet.get("domaines_d_etude", "")
    collaboration = donnees_projet.get("type_collaboration", "")


    # ========================================================
    # PROMPT PRINCIPAL
    # ========================================================

    prompt = f"""
Tu es l'intelligence artificielle d'INNOVLINK.

Ta mission est d'analyser un projet informatique proposé
par un porteur de projet.

Tu dois évaluer le projet sur plusieurs critères et lui
attribuer un SCORE GLOBAL compris entre 0 et 100.

IMPORTANT :
Le score doit obligatoirement être écrit exactement sous
cette forme :

Score global : XX/100

Exemple :

Score global : 87/100

Ne mets jamais le score sous la forme 87%.
Utilise uniquement le format XX/100.

============================================================
INFORMATIONS DU PROJET
============================================================

Nom du projet :
{nom}

Phase :
{phase}

Description :
{description}

Technologies :
{technologies}

Domaines d'étude :
{domaines}

Type de collaboration souhaité :
{collaboration}


============================================================
CRITÈRES D'ÉVALUATION
============================================================

Analyse notamment :

1. Pertinence du problème
2. Clarté de la solution
3. Innovation
4. Faisabilité technique
5. Cohérence des technologies
6. Potentiel de développement
7. Potentiel de collaboration
8. Adéquation avec la phase du projet
9. Qualité globale du projet


============================================================
FORMAT DE TA RÉPONSE
============================================================

Ta réponse doit commencer obligatoirement par :

Score global : XX/100

Ensuite, fournis une analyse détaillée comprenant :

- Pertinence du problème
- Qualité de la solution
- Innovation
- Faisabilité technique
- Technologies
- Potentiel de développement
- Potentiel de collaboration
- Points forts
- Points faibles
- Recommandations
- Conclusion


============================================================
RÈGLE IMPORTANTE SUR LE SCORE
============================================================

Le score doit être un nombre entier entre 0 et 100.

0 = projet extrêmement faible
100 = projet exceptionnel

Évalue réellement le projet à partir des informations
fournies. Ne donne pas automatiquement une bonne note.
"""


    # ========================================================
    # CONTENU ENVOYÉ À GEMINI
    # ========================================================

    contents = [prompt]


    # ========================================================
    # ANALYSE DU ZIP
    # ========================================================

    if fichier:

        fichier.seek(0)

        fichier_bytes = fichier.read()

        contents.append(
            types.Part.from_bytes(
                data=fichier_bytes,
                mime_type="application/zip"
            )
        )

        contents.append(
            """
Analyse également le fichier ZIP fourni.

Lorsque tu analyses le code source, prends notamment
en compte :

- Organisation des fichiers
- Architecture du projet
- Qualité du code
- Lisibilité
- Cohérence entre le code et la description
- Technologies réellement utilisées
- Fonctionnalités présentes
- Niveau de maturité
- Faisabilité technique
- Qualité générale de l'implémentation

Intègre les résultats de cette analyse dans ton
évaluation globale.
"""
        )


    # ========================================================
    # APPEL GEMINI
    # ========================================================

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=contents,
        config=types.GenerateContentConfig(
            temperature=0.3
        )
    )


    # ========================================================
    # RÉCUPÉRATION DE LA RÉPONSE
    # ========================================================

    resultat = response.text.strip()


    # ========================================================
    # VÉRIFICATION
    # ========================================================

    if not resultat:

        raise Exception(
            "Gemini n'a retourné aucun résultat."
        )


    # ========================================================
    # VÉRIFICATION DU SCORE
    # ========================================================

    import re

    score_match = re.search(
        r"Score\s+global\s*:\s*(\d+(?:[.,]\d+)?)\s*/\s*100",
        resultat,
        re.IGNORECASE
    )


    if not score_match:

        # Tentative de récupérer un autre format
        score_match = re.search(
            r"(\d+(?:[.,]\d+)?)\s*/\s*100",
            resultat
        )


    if not score_match:

        raise Exception(
            "Gemini a retourné une analyse mais aucun score "
            "au format XX/100 n'a été trouvé."
        )


    score = float(
        score_match.group(1).replace(",", ".")
    )


    # ========================================================
    # SÉCURITÉ
    # ========================================================

    if score < 0 or score > 100:

        raise Exception(
            f"Score IA invalide : {score}/100"
        )


    # ========================================================
    # NORMALISATION DU SCORE
    # ========================================================

    # On force un affichage entier :
    score_entier = int(round(score))


    # Si Gemini avait écrit 87.5/100 par exemple,
    # on remplace par 88/100.

    resultat = re.sub(
        r"Score\s+global\s*:\s*\d+(?:[.,]\d+)?\s*/\s*100",
        f"Score global : {score_entier}/100",
        resultat,
        count=1,
        flags=re.IGNORECASE
    )


    # ========================================================
    # RETOUR
    # ========================================================

    return resultat
