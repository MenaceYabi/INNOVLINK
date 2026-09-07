from django import forms

from .models import (
    PorteurProjet,
    Startup,
    StructureFinancement,
)


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
            "mot_de_passe": forms.PasswordInput(
                attrs={
                    "placeholder": "Mot de passe"
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "Adresse email"
                }
            ),
            "nom": forms.TextInput(
                attrs={
                    "placeholder": "Nom"
                }
            ),
            "prenom": forms.TextInput(
                attrs={
                    "placeholder": "Prénom"
                }
            ),
            "ville": forms.TextInput(
                attrs={
                    "placeholder": "Ville"
                }
            ),
            "pays": forms.TextInput(
                attrs={
                    "placeholder": "Pays"
                }
            ),
            "telephone": forms.TextInput(
                attrs={
                    "placeholder": "Numéro de téléphone"
                }
            ),
            "diplome": forms.TextInput(
                attrs={
                    "placeholder": "Diplôme obtenu"
                }
            ),
            "annee_obtention": forms.NumberInput(
                attrs={
                    "placeholder": "Année d'obtention"
                }
            ),
            "etablissement": forms.TextInput(
                attrs={
                    "placeholder": "École ou université"
                }
            ),
            "langues": forms.TextInput(
                attrs={
                    "placeholder": "Langues maîtrisées"
                }
            ),
            "github": forms.URLInput(
                attrs={
                    "placeholder": "Lien GitHub (optionnel)"
                }
            ),
            "linkedin": forms.URLInput(
                attrs={
                    "placeholder": "Lien LinkedIn (optionnel)"
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ancien_mot_de_passe = None

        if self.instance and self.instance.pk:
            self.ancien_mot_de_passe = self.instance.mot_de_passe

            self.fields["mot_de_passe"].required = False

            self.fields["mot_de_passe"].widget.attrs[
                "placeholder"
            ] = "Laisser vide pour conserver le mot de passe"

    def clean_email(self):
        email = self.cleaned_data["email"].lower().strip()

        queryset = PorteurProjet.objects.filter(
            email=email
        )

        if self.instance and self.instance.pk:
            queryset = queryset.exclude(
                pk=self.instance.pk
            )

        if queryset.exists():
            raise forms.ValidationError(
                "Un compte porteur de projet utilise déjà cet email."
            )

        return email

    def save(self, commit=True):
        instance = super().save(commit=False)

        nouveau_mot_de_passe = self.cleaned_data.get(
            "mot_de_passe"
        )

        if (
            self.instance
            and self.instance.pk
            and not nouveau_mot_de_passe
        ):
            instance.mot_de_passe = self.ancien_mot_de_passe

        if commit:
            instance.save()

        return instance


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
            "mot_de_passe": forms.PasswordInput(
                attrs={
                    "placeholder": "Mot de passe"
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "Adresse email"
                }
            ),
            "nom_startup": forms.TextInput(
                attrs={
                    "placeholder": "Nom de la startup"
                }
            ),
            "secteur": forms.TextInput(
                attrs={
                    "placeholder": "Secteur d'activité"
                }
            ),
            "annee_creation": forms.NumberInput(
                attrs={
                    "placeholder": "Année de création"
                }
            ),
            "numero_nu": forms.TextInput(
                attrs={
                    "placeholder": "Numéro NU"
                }
            ),
            "type_startup": forms.TextInput(
                attrs={
                    "placeholder": "Type de startup"
                }
            ),
            "type_collaboration": forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ancien_mot_de_passe = None

        if self.instance and self.instance.pk:
            self.ancien_mot_de_passe = self.instance.mot_de_passe

            self.fields["mot_de_passe"].required = False

            self.fields["mot_de_passe"].widget.attrs[
                "placeholder"
            ] = "Laisser vide pour conserver le mot de passe"

    def clean_email(self):
        email = self.cleaned_data["email"].lower().strip()

        queryset = Startup.objects.filter(
            email=email
        )

        if self.instance and self.instance.pk:
            queryset = queryset.exclude(
                pk=self.instance.pk
            )

        if queryset.exists():
            raise forms.ValidationError(
                "Une startup utilise déjà cet email."
            )

        return email

    def save(self, commit=True):
        instance = super().save(commit=False)

        nouveau_mot_de_passe = self.cleaned_data.get(
            "mot_de_passe"
        )

        if (
            self.instance
            and self.instance.pk
            and not nouveau_mot_de_passe
        ):
            instance.mot_de_passe = self.ancien_mot_de_passe

        if commit:
            instance.save()

        return instance


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
            "mot_de_passe": forms.PasswordInput(
                attrs={
                    "placeholder": "Mot de passe"
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "Adresse email"
                }
            ),
            "nom_structure": forms.TextInput(
                attrs={
                    "placeholder": "Nom de la structure"
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "placeholder": "Description de la structure",
                    "rows": 4,
                }
            ),
            "pays": forms.TextInput(
                attrs={
                    "placeholder": "Pays"
                }
            ),
            "ville": forms.TextInput(
                attrs={
                    "placeholder": "Ville"
                }
            ),
            "numero_nu": forms.TextInput(
                attrs={
                    "placeholder": "Numéro NU"
                }
            ),
            "type_structure": forms.Select(),
            "type_collaboration": forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ancien_mot_de_passe = None

        if self.instance and self.instance.pk:
            self.ancien_mot_de_passe = self.instance.mot_de_passe

            self.fields["mot_de_passe"].required = False

            self.fields["mot_de_passe"].widget.attrs[
                "placeholder"
            ] = "Laisser vide pour conserver le mot de passe"

    def clean_email(self):
        email = self.cleaned_data["email"].lower().strip()

        queryset = StructureFinancement.objects.filter(
            email=email
        )

        if self.instance and self.instance.pk:
            queryset = queryset.exclude(
                pk=self.instance.pk
            )

        if queryset.exists():
            raise forms.ValidationError(
                "Une structure de financement utilise déjà cet email."
            )

        return email

    def save(self, commit=True):
        instance = super().save(commit=False)

        nouveau_mot_de_passe = self.cleaned_data.get(
            "mot_de_passe"
        )

        if (
            self.instance
            and self.instance.pk
            and not nouveau_mot_de_passe
        ):
            instance.mot_de_passe = self.ancien_mot_de_passe

        if commit:
            instance.save()

        return instance