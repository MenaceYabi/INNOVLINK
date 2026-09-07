from django.db import models
from Authentification.models import PorteurProjet, Startup


class Message(models.Model):

    id = models.BigAutoField(primary_key=True)

    expediteur_porteur = models.ForeignKey(
        PorteurProjet,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="messages_envoyes"
    )

    expediteur_startup = models.ForeignKey(
        Startup,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="messages_envoyes_startup"
    )

    destinataire_porteur = models.ForeignKey(
        PorteurProjet,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="messages_recus"
    )

    destinataire_startup = models.ForeignKey(
        Startup,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="messages_recus_startup"
    )

    contenu = models.TextField()

    date_envoi = models.DateTimeField(auto_now_add=True)

    lu = models.BooleanField(default=False)

    class Meta:
        ordering = ["date_envoi"]

    def __str__(self):
        if self.expediteur_porteur:
            return f"{self.expediteur_porteur.nom} → Startup"
        return f"Startup → {self.destinataire_porteur.nom}"