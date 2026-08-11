
from django import forms
from .models import PorteurProjet, Startup, StructureFinancement


# ============================================================
# PORTEUR DE PROJET
# ============================================================

class PorteurProjetForm(forms.ModelForm):

    class Meta:
        model = PorteurProjet

        fields = [
            "email",
            "mot_de_passe",
            "nom",
            "prenom",
            "ville",
            "pays",
            "telephone",
            "diplome",
            "annee_obtention",
            "etablissement",
            "langues",
            "github",
            "linkedin",
        ]

        widgets = {
            "mot_de_passe": forms.PasswordInput(),

            "email": forms.EmailInput(attrs={
                "placeholder": "Adresse email"
            }),

            "nom": forms.TextInput(attrs={
                "placeholder": "Nom"
            }),

            "prenom": forms.TextInput(attrs={
                "placeholder": "Prénom"
            }),

            "ville": forms.TextInput(attrs={
                "placeholder": "Ville"
            }),

            "pays": forms.TextInput(attrs={
                "placeholder": "Pays"
            }),

            "telephone": forms.TextInput(attrs={
                "placeholder": "Numéro de téléphone"
            }),

            "diplome": forms.TextInput(attrs={
                "placeholder": "Diplôme obtenu"
            }),

            "annee_obtention": forms.NumberInput(attrs={
                "placeholder": "Année d'obtention"
            }),

            "etablissement": forms.TextInput(attrs={
                "placeholder": "École ou université"
            }),

            "langues": forms.TextInput(attrs={
                "placeholder": "Langues maîtrisées"
            }),

            "github": forms.URLInput(attrs={
                "placeholder": "Lien GitHub (optionnel)"
            }),

            "linkedin": forms.URLInput(attrs={
                "placeholder": "Lien LinkedIn (optionnel)"
            }),
        }

    def clean_email(self):
        email = self.cleaned_data["email"].lower().strip()

        if PorteurProjet.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Un compte porteur de projet utilise déjà cet email."
            )

        return email


# ============================================================
# STARTUP
# ============================================================

class StartupForm(forms.ModelForm):

    class Meta:
        model = Startup

        fields = [
            "email",
            "mot_de_passe",
            "nom_startup",
            "secteur",
            "annee_creation",
            "numero_nu",
            "type_startup",
            "type_collaboration",
        ]

        widgets = {
            "mot_de_passe": forms.PasswordInput(),

            "email": forms.EmailInput(attrs={
                "placeholder": "Adresse email"
            }),

            "nom_startup": forms.TextInput(attrs={
                "placeholder": "Nom de la startup"
            }),

            "secteur": forms.TextInput(attrs={
                "placeholder": "Secteur d'activité"
            }),

            "annee_creation": forms.NumberInput(attrs={
                "placeholder": "Année de création"
            }),

            "numero_nu": forms.TextInput(attrs={
                "placeholder": "Numéro NU / numéro d'organisation"
            }),

            "type_startup": forms.TextInput(attrs={
                "placeholder": "Type de startup"
            }),

            "type_collaboration": forms.Select(),
        }

    def clean_email(self):
        email = self.cleaned_data["email"].lower().strip()

        if Startup.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Une startup utilise déjà cet email."
            )

        return email


# ============================================================
# STRUCTURE DE FINANCEMENT
# ============================================================

class StructureFinancementForm(forms.ModelForm):

    class Meta:
        model = StructureFinancement

        fields = [
            "email",
            "mot_de_passe",
            "nom_structure",
            "description",
            "pays",
            "ville",
            "numero_nu",
            "type_structure",
            "type_collaboration",
        ]

        widgets = {
            "mot_de_passe": forms.PasswordInput(),

            "email": forms.EmailInput(attrs={
                "placeholder": "Adresse email"
            }),

            "nom_structure": forms.TextInput(attrs={
                "placeholder": "Nom de la structure"
            }),

            "description": forms.Textarea(attrs={
                "placeholder": "Présentez votre structure",
                "rows": 4
            }),

            "pays": forms.TextInput(attrs={
                "placeholder": "Pays"
            }),

            "ville": forms.TextInput(attrs={
                "placeholder": "Ville"
            }),

            "numero_nu": forms.TextInput(attrs={
                "placeholder": "Numéro NU / numéro d'organisation"
            }),

            "type_structure": forms.Select(),

            "type_collaboration": forms.Select(),
        }

    def clean_email(self):
        email = self.cleaned_data["email"].lower().strip()

        if StructureFinancement.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Une structure utilise déjà cet email."
            )

        return email
