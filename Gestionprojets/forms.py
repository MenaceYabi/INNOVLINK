from django import forms
from .models import Projet


class ProjetForm(forms.ModelForm):

    # Fichier utilisé uniquement pour l'analyse IA
    fichier_analyse = forms.FileField(
        required=False,
        label="Fichier du projet",
        widget=forms.ClearableFileInput(
            attrs={
                "class": "form-control",
                "accept": ".zip"
            }
        )
    )

    class Meta:
        model = Projet

        fields = [
            "phase",
            "nom",
            "description",
            "technologies",
            "domaines_d_etude",
            "type_collaboration",
        ]

        widgets = {

            "phase": forms.Select(
                attrs={
                    "class": "form-control",
                    "id": "id_phase"
                }
            ),

            "nom": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nom du projet"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Décrivez votre projet...",
                    "rows": 6
                }
            ),

            "technologies": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex : Python, Django, Flutter..."
                }
            ),

            "domaines_d_etude": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex : Informatique, Agriculture..."
                }
            ),

            "type_collaboration": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),
        }

    def clean_fichier_analyse(self):
        fichier = self.cleaned_data.get("fichier_analyse")

        if fichier:
            # Vérification de l'extension
            if not fichier.name.lower().endswith(".zip"):
                raise forms.ValidationError(
                    "Veuillez sélectionner un fichier ZIP."
                )

            # Limite de 50 Mo
            if fichier.size > 50 * 1024 * 1024:
                raise forms.ValidationError(
                    "Le fichier ZIP ne doit pas dépasser 50 Mo."
                )

        return fichier

    def clean(self):
        cleaned_data = super().clean()

        phase = cleaned_data.get("phase")
        fichier = cleaned_data.get("fichier_analyse")

        # Le ZIP est obligatoire sauf pour la phase Idée
        if phase in ["PROTOTYPE", "MVP", "CROISSANCE"] and not fichier:
            self.add_error(
                "fichier_analyse",
                "Un fichier ZIP du projet est obligatoire pour cette phase."
            )

        # Pour Idée, aucun ZIP n'est nécessaire
        if phase == "IDEE":
            cleaned_data["fichier_analyse"] = None

        return cleaned_data