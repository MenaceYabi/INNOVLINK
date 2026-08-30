from django.db import models
from Authentification.models import PorteurProjet


class Projet(models.Model):

    PHASE_CHOICES = [
        ("IDEE", "Idée"),
        ("PROTOTYPE", "Prototype"),
        ("MVP", "MVP"),
        ("CROISSANCE", "Croissance"),
    ]

    TYPE_COLLABORATION_CHOICES = [
        ("INVESTISSEMENT", "Investissement"),
        ("PARTENARIAT_STRATEGIQUE", "Partenariat stratégique"),
        ("ACQUISITION_SOLUTION", "Acquisition de solution"),
        ("LICENCE_UTILISATION", "Licence d'utilisation"),
        ("INCUBATION", "Incubation"),
    ]

    id = models.AutoField(primary_key=True)
    porteur = models.ForeignKey(
        PorteurProjet,
        on_delete=models.CASCADE,
        related_name="projets"
    )

    phase = models.CharField(
        max_length=20,
        choices=PHASE_CHOICES
    )

    nom = models.CharField(max_length=255)

    description = models.TextField()

    technologies = models.CharField(max_length=255)

    domaines_d_etude = models.CharField(max_length=255)

    type_collaboration = models.CharField(
        max_length=50,
        choices=TYPE_COLLABORATION_CHOICES
    )

    resultat = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return self.nom