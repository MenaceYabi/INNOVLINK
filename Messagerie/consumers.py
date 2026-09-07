import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Message
from Authentification.models import PorteurProjet, Startup


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        # ==================================================
        # IDENTITÉ RÉCUPÉRÉE DEPUIS LA SESSION DJANGO
        # ==================================================

        self.user_id = self.scope["session"].get("user_id")
        self.role = self.scope["session"].get("role")

        self.porteur_id = None
        self.startup_id = None
        self.room_group_name = None

        # ==================================================
        # VÉRIFICATION DE LA SESSION
        # ==================================================

        if not self.user_id:
            await self.close(code=4001)
            return

        if self.role not in ["porteur", "startup"]:
            await self.close(code=4002)
            return

        # ==================================================
        # CONNEXION ACCEPTÉE
        # ==================================================

        await self.accept()


    async def disconnect(self, close_code):

        # Si aucune conversation n'a encore été ouverte,
        # il n'y a aucun groupe à quitter.

        if self.room_group_name:

            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )


    async def receive(self, text_data):

        # ==================================================
        # LECTURE DU JSON
        # ==================================================

        try:

            data = json.loads(text_data)

        except json.JSONDecodeError:

            return


        # ==================================================
        # OUVERTURE D'UNE CONVERSATION
        # ==================================================

        action = data.get("action")

        if action == "ouvrir_conversation":

            await self.ouvrir_conversation(data)

            return


        # ==================================================
        # ENVOI D'UN MESSAGE
        # ==================================================

        contenu = data.get("message", "").strip()

        if not contenu:

            return


        # Impossible d'envoyer un message
        # sans conversation ouverte.

        if not self.room_group_name:

            return


        # ==================================================
        # ENREGISTREMENT DU MESSAGE
        # ==================================================

        message = await self.enregistrer_message(
            contenu
        )

        if not message:

            return


        # ==================================================
        # DIFFUSION DU MESSAGE
        # ==================================================

        await self.channel_layer.group_send(

            self.room_group_name,

            {
                "type": "chat_message",

                "message": contenu,

                "message_id": message.id,

                "date_envoi": (
                    message.date_envoi.isoformat()
                ),

                "role": self.role,
            }

        )


    async def ouvrir_conversation(self, data):

        # ==================================================
        # STARTUP
        # ==================================================

        if self.role == "startup":

            porteur_id = data.get("porteur_id")

            if not porteur_id:

                return


            # La startup connectée est automatiquement
            # l'expéditeur de départ.

            self.startup_id = self.user_id
            self.porteur_id = porteur_id


        # ==================================================
        # PORTEUR
        # ==================================================

        elif self.role == "porteur":

            startup_id = data.get("startup_id")

            if not startup_id:

                return


            # Le porteur connecté est automatiquement
            # identifié par sa session.

            self.porteur_id = self.user_id
            self.startup_id = startup_id


        # ==================================================
        # VÉRIFICATION DES UTILISATEURS
        # ==================================================

        utilisateurs_valides = (
            await self.verifier_utilisateurs()
        )

        if not utilisateurs_valides:

            await self.send(
                text_data=json.dumps({
                    "type": "erreur",
                    "message": (
                        "Les utilisateurs de cette "
                        "conversation sont invalides."
                    )
                })
            )

            return


        # ==================================================
        # NOM DU GROUPE
        # ==================================================

        self.room_group_name = (
            f"chat_{self.porteur_id}_{self.startup_id}"
        )


        # ==================================================
        # REJOINDRE LA CONVERSATION
        # ==================================================

        await self.channel_layer.group_add(

            self.room_group_name,

            self.channel_name
        )


        # ==================================================
        # ENVOYER L'HISTORIQUE
        # ==================================================

        historique = await self.get_historique()


        await self.send(

            text_data=json.dumps({

                "type": "historique",

                "messages": historique

            })

        )


    async def chat_message(self, event):

        await self.send(

            text_data=json.dumps({

                "type": "message",

                "message": event["message"],

                "message_id": event["message_id"],

                "date_envoi": event["date_envoi"],

                "role": event["role"],

            })

        )


    # ======================================================
    # VÉRIFICATION DES UTILISATEURS
    # ======================================================

    @database_sync_to_async
    def verifier_utilisateurs(self):

        porteur = (
            PorteurProjet.objects
            .filter(id=self.porteur_id)
            .first()
        )

        startup = (
            Startup.objects
            .filter(id=self.startup_id)
            .first()
        )

        return bool(
            porteur and startup
        )


    # ======================================================
    # ENREGISTRER LE MESSAGE
    # ======================================================

    @database_sync_to_async
    def enregistrer_message(self, contenu):

        # ==============================================
        # MESSAGE DU PORTEUR
        # ==============================================

        if self.role == "porteur":

            porteur = (
                PorteurProjet.objects
                .filter(id=self.porteur_id)
                .first()
            )

            startup = (
                Startup.objects
                .filter(id=self.startup_id)
                .first()
            )

            if not porteur or not startup:

                return None


            return Message.objects.create(

                expediteur_porteur=porteur,

                destinataire_startup=startup,

                contenu=contenu,

            )


        # ==============================================
        # MESSAGE DE LA STARTUP
        # ==============================================

        if self.role == "startup":

            startup = (
                Startup.objects
                .filter(id=self.startup_id)
                .first()
            )

            porteur = (
                PorteurProjet.objects
                .filter(id=self.porteur_id)
                .first()
            )

            if not startup or not porteur:

                return None


            return Message.objects.create(

                expediteur_startup=startup,

                destinataire_porteur=porteur,

                contenu=contenu,

            )


        return None


    # ======================================================
    # HISTORIQUE
    # ======================================================

    @database_sync_to_async
    def get_historique(self):

        messages = (

            Message.objects.filter(

                expediteur_porteur_id=self.porteur_id,

                destinataire_startup_id=self.startup_id

            )

            |

            Message.objects.filter(

                expediteur_startup_id=self.startup_id,

                destinataire_porteur_id=self.porteur_id

            )

        ).order_by("date_envoi")


        return [

            {

                "message_id": message.id,

                "message": message.contenu,

                "date_envoi": (
                    message.date_envoi.isoformat()
                ),

                "role": (

                    "porteur"

                    if message.expediteur_porteur_id

                    else "startup"

                ),

            }

            for message in messages

        ]