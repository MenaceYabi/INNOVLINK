
document.addEventListener("DOMContentLoaded", () => {


    /* ==================================================
       NAVIGATION
    ================================================== */

    const navLinks =
        document.querySelectorAll(
            "#mainNav .nav-link"
        );


    const sections =
        document.querySelectorAll(
            ".tab-section"
        );


    navLinks.forEach(link => {

        link.addEventListener(
            "click",
            function(event) {

                event.preventDefault();


                navLinks.forEach(item =>
                    item.classList.remove("active")
                );


                sections.forEach(section =>
                    section.classList.remove("active")
                );


                this.classList.add("active");


                const target =
                    this.dataset.target;


                const section =
                    document.getElementById(target);


                if (section) {

                    section.classList.add("active");

                }

            }
        );

    });



    /* ==================================================
       FAVORIS
    ================================================== */

    document
        .querySelectorAll(".btn-fav")
        .forEach(button => {

            button.addEventListener(
                "click",
                function() {

                    this.classList.toggle("active");

                }
            );

        });



    /* ==================================================
       CTRL + K
    ================================================== */

    const searchInput =
        document.getElementById("searchInput");


    document.addEventListener(
        "keydown",
        event => {

            if (
                (event.ctrlKey || event.metaKey) &&
                event.key.toLowerCase() === "k"
            ) {

                event.preventDefault();


                if (searchInput) {

                    searchInput.focus();

                }

            }

        }
    );



    /* ==================================================
       WEBSOCKET
    ================================================== */

    const startupId =
        "{{ startup.id }}";


    let socket = null;

    let currentPorteurId = null;



    /* ==================================================
       ELEMENTS
    ================================================== */

    const chatMessages =
        document.getElementById(
            "chatMessages"
        );


    const chatInput =
        document.getElementById(
            "chatInput"
        );


    const chatForm =
        document.getElementById(
            "chatForm"
        );


    const chatSendBtn =
        document.getElementById(
            "chatSendBtn"
        );


    const chatStatus =
        document.getElementById(
            "chatStatus"
        );


    const chatPartnerName =
        document.getElementById(
            "chatPartnerName"
        );


    const chatInfo =
        document.getElementById(
            "chatInfo"
        );


    const chatError =
        document.getElementById(
            "chatError"
        );



    /* ==================================================
       STATUT
    ================================================== */

    function setChatStatus(
        status,
        text
    ) {

        chatStatus.className =
            "chat-status " + status;


        chatStatus.innerHTML =
            `<i class="fa-solid fa-circle"></i> ${text}`;

    }



    /* ==================================================
       ERREUR
    ================================================== */

    function showChatError(message) {

        chatError.textContent =
            message;

        chatError.style.display =
            "block";

    }


    function hideChatError() {

        chatError.textContent =
            "";

        chatError.style.display =
            "none";

    }



    /* ==================================================
       NETTOYER
    ================================================== */

    function clearMessages() {

        chatMessages.innerHTML = "";

    }



    /* ==================================================
       AFFICHER MESSAGE
    ================================================== */

    function addMessage(
        message,
        role,
        dateEnvoi
    ) {

        const placeholder =
            chatMessages.querySelector(
                ".chat-placeholder"
            );


        if (placeholder) {

            placeholder.remove();

        }


        const element =
            document.createElement("div");


        element.className =
            role === "startup"
                ? "chat-message mine"
                : "chat-message theirs";


        const text =
            document.createElement("div");


        text.textContent =
            message;


        const time =
            document.createElement("span");


        time.className =
            "chat-message-time";


        if (dateEnvoi) {

            const date =
                new Date(dateEnvoi);


            if (!isNaN(date.getTime())) {

                time.textContent =
                    date.toLocaleTimeString(
                        "fr-FR",
                        {
                            hour: "2-digit",
                            minute: "2-digit"
                        }
                    );

            }

        }


        element.appendChild(text);

        element.appendChild(time);


        chatMessages.appendChild(element);


        chatMessages.scrollTop =
            chatMessages.scrollHeight;

    }



    /* ==================================================
       HISTORIQUE
    ================================================== */

    function afficherHistorique(messages) {

        clearMessages();


        if (
            !messages ||
            messages.length === 0
        ) {

            chatMessages.innerHTML = `

                <div class="chat-placeholder">

                    <i
                        class="fa-solid fa-comments"
                        style="
                            font-size:30px;
                            margin-bottom:10px;
                            display:block;
                        "
                    ></i>

                    Aucun message pour le moment.

                </div>

            `;

            return;

        }


        messages.forEach(message => {

            addMessage(
                message.message,
                message.role,
                message.date_envoi
            );

        });

    }



    /* ==================================================
       FERMER SOCKET
    ================================================== */

    function closeCurrentSocket() {

        if (socket) {

            try {

                socket.close();

            } catch (error) {

                console.error(error);

            }

            socket = null;

        }

    }



    /* ==================================================
       CONNECTER
    ================================================== */

    function connectWebSocket(
        porteurId,
        porteurNom
    ) {

        if (!porteurId) {

            showChatError(
                "Impossible de déterminer le porteur."
            );

            return;

        }


        currentPorteurId =
            String(porteurId);


        closeCurrentSocket();


        clearMessages();

        hideChatError();


        chatPartnerName.textContent =
            porteurNom ||
            "Porteur";


        chatInfo.textContent =
            `Conversation avec ${
                porteurNom || "le porteur"
            }.`;


        chatInput.disabled = true;

        chatSendBtn.disabled = true;


        setChatStatus(
            "connecting",
            "Connexion..."
        );


        /* ==============================================
           URL UNIQUE
        ============================================== */

        const protocol =
            window.location.protocol === "https:"
                ? "wss"
                : "ws";


        const wsUrl =
            `${protocol}://${window.location.host}/ws/chat/`;


        console.log(
            "Connexion WebSocket :",
            wsUrl
        );


        try {

            socket =
                new WebSocket(wsUrl);

        } catch (error) {

            console.error(error);


            setChatStatus(
                "offline",
                "Erreur"
            );


            showChatError(
                "Impossible de créer la connexion."
            );


            return;

        }



        /* ==============================================
           OUVERTURE
        ============================================== */

        socket.onopen = () => {

            console.log(
                "WebSocket connecté."
            );


            setChatStatus(
                "online",
                "Connecté"
            );


            /* ==========================================
               LA STARTUP OUVRE LA CONVERSATION
            ========================================== */

            socket.send(
                JSON.stringify({

                    action:
                        "ouvrir_conversation",

                    porteur_id:
                        String(porteurId)

                })
            );


        };



        /* ==============================================
           MESSAGE
        ============================================== */

        socket.onmessage = event => {

            try {

                const data =
                    JSON.parse(event.data);


                console.log(
                    "WebSocket reçu :",
                    data
                );


                if (
                    data.type ===
                    "historique"
                ) {

                    afficherHistorique(
                        data.messages
                    );

                    return;

                }


                if (
                    data.type ===
                    "message"
                ) {

                    addMessage(
                        data.message,
                        data.role,
                        data.date_envoi
                    );

                    return;

                }


                if (
                    data.type ===
                    "erreur"
                ) {

                    showChatError(
                        data.message
                    );

                }

            } catch (error) {

                console.error(
                    "Erreur lecture WebSocket :",
                    error
                );

            }

        };



        /* ==============================================
           ERREUR
        ============================================== */

        socket.onerror = error => {

            console.error(
                "Erreur WebSocket :",
                error
            );


            setChatStatus(
                "offline",
                "Erreur"
            );


            showChatError(
                "Erreur de connexion WebSocket."
            );

        };



        /* ==============================================
           FERMETURE
        ============================================== */

        socket.onclose = () => {

            console.log(
                "WebSocket fermé."
            );


            setChatStatus(
                "offline",
                "Déconnecté"
            );


            chatInput.disabled = true;

            chatSendBtn.disabled = true;

        };

    }



    /* ==================================================
       COLLABORER
    ================================================== */

    document
        .querySelectorAll(".btn-collaborer")
        .forEach(button => {

            button.addEventListener(
                "click",
                function() {

                    const porteurId =
                        this.dataset.porteurId;


                    const porteurNom =
                        this.dataset.porteurNom
                            .replace(/\s+/g, " ")
                            .trim();


                    console.log(
                        "Collaboration avec :",
                        porteurId,
                        porteurNom
                    );


                    if (!porteurId) {

                        alert(
                            "Porteur introuvable."
                        );

                        return;

                    }


                    /* Ouvrir l'onglet Messages */

                    navLinks.forEach(item =>
                        item.classList.remove(
                            "active"
                        )
                    );


                    sections.forEach(section =>
                        section.classList.remove(
                            "active"
                        )
                    );


                    const messagesLink =
                        document.querySelector(
                            '.nav-link[data-target="messages"]'
                        );


                    const messagesSection =
                        document.getElementById(
                            "messages"
                        );


                    if (messagesLink) {

                        messagesLink.classList.add(
                            "active"
                        );

                    }


                    if (messagesSection) {

                        messagesSection.classList.add(
                            "active"
                        );

                    }


                    /* Connexion */

                    connectWebSocket(
                        porteurId,
                        porteurNom
                    );

                }
            );

        });



    /* ==================================================
       ENVOYER MESSAGE
    ================================================== */

    chatForm.addEventListener(
        "submit",
        event => {

            event.preventDefault();


            if (
                !socket ||
                socket.readyState !==
                WebSocket.OPEN
            ) {

                showChatError(
                    "La connexion n'est pas active."
                );

                return;

            }


            const message =
                chatInput.value.trim();


            if (!message) {

                return;

            }


            /* ==========================================
               IMPORTANT
               Aucun role.
            ========================================== */

            socket.send(
                JSON.stringify({

                    message: message

                })
            );


            chatInput.value = "";

            chatInput.focus();

        }
    );



    /* ==================================================
       ENTER
    ================================================== */

    chatInput.addEventListener(
        "keydown",
        event => {

            if (
                event.key === "Enter" &&
                !event.shiftKey
            ) {

                event.preventDefault();

                chatForm.requestSubmit();

            }

        }
    );



    /* ==================================================
       FERMETURE PAGE
    ================================================== */

    window.addEventListener(
        "beforeunload",
        () => {

            if (socket) {

                socket.close();

            }

        }
    );


});
