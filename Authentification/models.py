import uuid

from django.db import models
from django.contrib.auth.hashers import make_password


class PorteurProjet(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    email = models.EmailField(unique=True)
    mot_de_passe = models.CharField(max_length=128)

    date_inscription = models.DateTimeField(auto_now_add=True)
    statut_compte = models.CharField(
        max_length=20,
        default="ACTIF"
    )

    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    ville = models.CharField(max_length=100)
    pays = models.CharField(max_length=100, default="Cameroun")

    telephone = models.CharField(max_length=30)

    diplome = models.CharField(max_length=150)
    annee_obtention = models.PositiveIntegerField()
    etablissement = models.CharField(max_length=200)

    langues = models.CharField(max_length=255)

    github = models.URLField(
        blank=True,
        null=True
    )

    linkedin = models.URLField(
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):
        if not self.mot_de_passe.startswith("pbkdf2_"):
            self.mot_de_passe = make_password(self.mot_de_passe)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.prenom} {self.nom}"


class Startup(models.Model):

    TYPES_COLLABORATION = [
        ("INVESTISSEMENT", "Investissement"),
        ("PARTENARIAT_STRATEGIQUE", "Partenariat stratégique"),
        ("ACQUISITION_SOLUTION", "Acquisition de solution"),
        ("LICENCE_UTILISATION", "Licence d'utilisation"),
        ("INCUBATION", "Incubation"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    email = models.EmailField(unique=True)
    mot_de_passe = models.CharField(max_length=128)

    date_inscription = models.DateTimeField(auto_now_add=True)
    statut_compte = models.CharField(
        max_length=20,
        default="ACTIF"
    )

    nom_startup = models.CharField(max_length=150)
    secteur = models.CharField(max_length=150)
    annee_creation = models.PositiveIntegerField()

    numero_nu = models.CharField(
        max_length=100,
        unique=True
    )

    type_startup = models.CharField(max_length=100)

    type_collaboration = models.CharField(
        max_length=40,
        choices=TYPES_COLLABORATION
    )



    statut_validation = models.CharField(
        max_length=20,
        default="EN_ATTENTE"
    )

    date_validation = models.DateTimeField(
        blank=True,
        null=True
    )

    motif_rejet = models.TextField(
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):
        if not self.mot_de_passe.startswith("pbkdf2_"):
            self.mot_de_passe = make_password(self.mot_de_passe)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom_startup


class StructureFinancement(models.Model):

    TYPES_STRUCTURE = [
        ("INCUBATEUR", "Incubateur"),
        ("BANQUE", "Banque"),
        ("FONDS_INVESTISSEMENT", "Fonds d'investissement"),
        ("ACCELERATEUR", "Accélérateur"),
        ("ONG", "ONG"),
        ("INSTITUTION_PUBLIQUE", "Institution publique"),
        ("AUTRE", "Autre"),
    ]

    TYPES_COLLABORATION = Startup.TYPES_COLLABORATION

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    email = models.EmailField(unique=True)
    mot_de_passe = models.CharField(max_length=128)

    date_inscription = models.DateTimeField(auto_now_add=True)
    statut_compte = models.CharField(
        max_length=20,
        default="ACTIF"
    )

    nom_structure = models.CharField(max_length=150)
    description = models.TextField()

    pays = models.CharField(max_length=100)
    ville = models.CharField(max_length=100)

    numero_nu = models.CharField(
        max_length=100,
        unique=True
    )

    type_structure = models.CharField(
        max_length=50,
        choices=TYPES_STRUCTURE
    )

    type_collaboration = models.CharField(
        max_length=40,
        choices=TYPES_COLLABORATION
    )

    statut_validation = models.CharField(
        max_length=20,
        default="EN_ATTENTE"
    )

    date_validation = models.DateTimeField(
        blank=True,
        null=True
    )

    motif_rejet = models.TextField(
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):
        if not self.mot_de_passe.startswith("pbkdf2_"):
            self.mot_de_passe = make_password(self.mot_de_passe)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom_structure


class Admin(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    email = models.EmailField(unique=True)
    mot_de_passe = models.CharField(max_length=128)

    date_inscription = models.DateTimeField(auto_now_add=True)

    statut_compte = models.CharField(
        max_length=20,
        default="ACTIF"
    )

    niveau_acces = models.CharField(
        max_length=50,
        default="ADMIN"
    )

    def save(self, *args, **kwargs):
        if not self.mot_de_passe.startswith("pbkdf2_"):
            self.mot_de_passe = make_password(self.mot_de_passe)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.email