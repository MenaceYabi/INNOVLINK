document.addEventListener("DOMContentLoaded", () => {
    /* ==========================================================
       NAVIGATION
    ========================================================== */
    const menuItems =
        document.querySelectorAll(
            ".sidebar-menu .menu-item[data-target]"
        );
    const sections =
        document.querySelectorAll(
            ".content-section"
        );
    const menuBtn =
        document.getElementById("menuBtn");
    const sidebar =
        document.getElementById("sidebar");
    const overlay =
        document.getElementById("sidebarOverlay");
    menuItems.forEach(item => {
        item.addEventListener("click", () => {
            menuItems.forEach(btn =>
                btn.classList.remove("active")
            );
            sections.forEach(section =>
                section.classList.remove("active")
            );
            item.classList.add("active");
            const targetId =
                item.getAttribute(
                    "data-target"
                );
            const targetSection =
                document.getElementById(
                    targetId
                );
            if (targetSection) {
                targetSection.classList.add(
                    "active"
                );

            }
            closeSidebar();
        });

    });



    /* ==========================================================
       MENU MOBILE
    ========================================================== */
    function openSidebar() {

        if (sidebar) {

            sidebar.classList.add("open");

        }


        if (overlay) {

            overlay.classList.add("active");

        }

    }


    function closeSidebar() {

        if (sidebar) {

            sidebar.classList.remove("open");

        }


        if (overlay) {

            overlay.classList.remove("active");

        }

    }


    if (menuBtn) {

        menuBtn.addEventListener(
            "click",
            () => {

                if (
                    sidebar.classList.contains(
                        "open"
                    )
                ) {

                    closeSidebar();

                } else {

                    openSidebar();

                }

            }
        );

    }


    if (overlay) {

        overlay.addEventListener(
            "click",
            closeSidebar
        );

    }



    /* ==========================================================
       WEBSOCKET
    ========================================================== */

    let socket = null;

    let startupActive = null;



    /* ==========================================================
       ELEMENTS
    ========================================================== */

    const conversationItems =
        document.querySelectorAll(
            ".conversation-item"
        );


    const chatMessages =
        document.getElementById(
            "chatMessages"
        );


    const chatForm =
        document.getElementById(
            "chatForm"
        );


    const chatInput =
        document.getElementById(
            "chatInput"
        );


    const chatStatus =
        document.getElementById(
            "chatStatus"
        );


    const chatUserName =
        document.getElementById(
            "chatUserName"
        );


    const chatSend =
        document.getElementById(
            "chatSend"
        );



    /* ==========================================================
       STATUT
    ========================================================== */

    function afficherStatut(
        texte,
        classe
    ) {

        if (!chatStatus) {

            return;

        }


        chatStatus.textContent =
            texte;


        chatStatus.className =
            `chat-status ${classe}`;

    }



    /* ==========================================================
       VIDER CHAT
    ========================================================== */

    function viderMessages() {

        if (chatMessages) {

            chatMessages.innerHTML = "";

        }

    }



    /* ==========================================================
       MESSAGE VIDE
    ========================================================== */

    function afficherMessageVide() {

        if (!chatMessages) {

            return;

        }


        chatMessages.innerHTML = `

            <div class="chat-empty">

                <i class="fas fa-comments"></i>

                <p>
                    Aucun message pour le moment.
                </p>

                <small>
                    Cette startup n'a encore envoyé
                    aucun message.
                </small>

            </div>

        `;

    }



    /* ==========================================================
       AFFICHER HISTORIQUE
    ========================================================== */

    function afficherHistorique(messages) {

        viderMessages();


        if (
            !messages ||
            messages.length === 0
        ) {

            afficherMessageVide();

            return;

        }


        messages.forEach(message => {

            afficherMessage(message);

        });

    }



    /* ==========================================================
       AFFICHER MESSAGE
    ========================================================== */

    function afficherMessage(data) {

        if (!chatMessages) {

            return;

        }


        const empty =
            chatMessages.querySelector(
                ".chat-empty"
            );


        if (empty) {

            empty.remove();

        }


        const row =
            document.createElement(
                "div"
            );


        /*
         * Le serveur nous indique le rôle.
         *
         * porteur  = notre message
         * startup  = message reçu
         */

        const role =
            data.role === "porteur"
                ? "porteur"
                : "startup";


        row.className =
            `message-row ${role}`;


        const bubble =
            document.createElement(
                "div"
            );


        bubble.className =
            "message-bubble";


        const contenu =
            document.createElement(
                "div"
            );


        contenu.textContent =
            data.message || "";


        bubble.appendChild(
            contenu
        );


        if (data.date_envoi) {

            const date =
                document.createElement(
                    "span"
                );


            date.className =
                "message-time";


            date.textContent =
                formaterDate(
                    data.date_envoi
                );


            bubble.appendChild(
                date
            );

        }


        row.appendChild(
            bubble
        );


        chatMessages.appendChild(
            row
        );


        chatMessages.scrollTop =
            chatMessages.scrollHeight;

    }



    /* ==========================================================
       DATE
    ========================================================== */

    function formaterDate(
        dateString
    ) {

        try {

            const date =
                new Date(
                    dateString
                );


            if (
                isNaN(
                    date.getTime()
                )
            ) {

                return "";

            }


            return date.toLocaleString(
                "fr-FR",
                {
                    day: "2-digit",
                    month: "2-digit",
                    hour: "2-digit",
                    minute: "2-digit"
                }
            );

        } catch (error) {

            return "";

        }

    }



    /* ==========================================================
       FERMER SOCKET
    ========================================================== */

    function fermerSocket() {

        if (socket) {

            try {

                socket.close();

            } catch (error) {

                console.error(
                    error
                );

            }


            socket = null;

        }

    }



    /* ==========================================================
       CONNECTER PORTEUR
    ========================================================== */

    function connecterWebSocket(
        startupId
    ) {

        if (!startupId) {

            console.error(
                "Startup ID manquant."
            );

            return;

        }


        startupActive =
            String(startupId);


        fermerSocket();


        viderMessages();


        if (chatSend) {

            chatSend.disabled =
                true;

        }


        if (chatInput) {

            chatInput.disabled =
                true;

        }


        afficherStatut(
            "Connexion...",
            "connecting"
        );


        /* ==================================================
           URL UNIQUE
        ================================================== */

        const protocole =
            window.location.protocol === "https:"
                ? "wss"
                : "ws";


        const url =
            `${protocole}://${window.location.host}/ws/chat/`;


        console.log(
            "Connexion WebSocket :",
            url
        );


        socket =
            new WebSocket(url);



        /* ==================================================
           OUVERTURE
        ================================================== */

        socket.onopen = () => {

            console.log(
                "WebSocket connecté."
            );


            afficherStatut(
                "Connecté",
                "connected"
            );


            /*
             * Le porteur ouvre une conversation
             * qu'il a reçue.
             *
             * Le serveur connaît déjà
             * le porteur grâce à la session.
             */

            socket.send(
                JSON.stringify({

                    action:
                        "ouvrir_conversation",

                    startup_id:
                        String(startupId)

                })
            );

        };



        /* ==================================================
           MESSAGE
        ================================================== */

        socket.onmessage = event => {

            try {

                const data =
                    JSON.parse(
                        event.data
                    );


                console.log(
                    "Message WebSocket reçu :",
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

                    afficherMessage(
                        data
                    );

                    return;

                }


                if (
                    data.type ===
                    "erreur"
                ) {

                    console.error(
                        data.message
                    );

                    return;

                }

            } catch (error) {

                console.error(
                    "Erreur lecture WebSocket :",
                    error
                );

            }

        };



        /* ==================================================
           ERREUR
        ================================================== */

        socket.onerror = error => {

            console.error(
                "Erreur WebSocket :",
                error
            );


            afficherStatut(
                "Erreur",
                "disconnected"
            );


            if (chatSend) {

                chatSend.disabled =
                    true;

            }

        };



        /* ==================================================
           FERMETURE
        ================================================== */

        socket.onclose = () => {

            console.log(
                "WebSocket fermé."
            );


            afficherStatut(
                "Déconnecté",
                "disconnected"
            );


            if (chatSend) {

                chatSend.disabled =
                    true;

            }


            if (chatInput) {

                chatInput.disabled =
                    true;

            }

        };

    }



    /* ==========================================================
       SÉLECTION CONVERSATION
    ========================================================== */

    conversationItems.forEach(item => {

        item.addEventListener(
            "click",
            () => {

                conversationItems.forEach(
                    button =>
                        button.classList.remove(
                            "active"
                        )
                );


                item.classList.add(
                    "active"
                );


                const startupId =
                    item.dataset.startupId;


                const startupName =
                    item.dataset.startupName ||
                    "Startup";


                if (chatUserName) {

                    chatUserName.textContent =
                        startupName;

                }


                connecterWebSocket(
                    startupId
                );

            }
        );

    });



    /* ==========================================================
       ENVOYER MESSAGE
    ========================================================== */

    if (chatForm) {

        chatForm.addEventListener(
            "submit",
            event => {

                event.preventDefault();


                if (
                    !socket ||
                    socket.readyState !==
                    WebSocket.OPEN
                ) {

                    console.error(
                        "WebSocket non connecté."
                    );

                    return;

                }


                const contenu =
                    chatInput.value.trim();


                if (!contenu) {

                    return;

                }


                /*
                 * IMPORTANT :
                 *
                 * Le porteur n'envoie PAS son rôle.
                 *
                 * Le serveur sait que c'est
                 * un porteur grâce à la session.
                 */

                socket.send(
                    JSON.stringify({

                        message:
                            contenu

                    })
                );


                chatInput.value =
                    "";


                chatInput.focus();

            }
        );

    }



    /* ==========================================================
       ENTER
    ========================================================== */

    if (chatInput) {

        chatInput.addEventListener(
            "keydown",
            event => {

                if (
                    event.key === "Enter" &&
                    !event.shiftKey
                ) {

                    event.preventDefault();


                    if (chatForm) {

                        chatForm.requestSubmit();

                    }

                }

            }
        );

    }



    /* ==========================================================
       FERMETURE PAGE
    ========================================================== */

    window.addEventListener(
        "beforeunload",
        () => {

            fermerSocket();

        }
    );

});


// ==========================================================
// SUPPRESSION D'UN PROJET
// ==========================================================

const deleteModal = document.getElementById("deleteModal");
const deleteForm = document.getElementById("deleteForm");
const deleteMessage = document.getElementById("deleteMessage");


// ----------------------------------------------------------
// OUVRIR LA MODALE
// ----------------------------------------------------------

function ouvrirSuppression(button) {

    const deleteUrl = button.dataset.deleteUrl;
    const projectName = button.dataset.projectName;

    deleteForm.action = deleteUrl;

    deleteMessage.textContent =
        `Voulez-vous vraiment supprimer le projet « ${projectName} » ?`;

    deleteModal.classList.add("open");

    deleteModal.setAttribute(
        "aria-hidden",
        "false"
    );
}


// ----------------------------------------------------------
// FERMER LA MODALE
// ----------------------------------------------------------

function fermerSuppression() {

    deleteModal.classList.remove("open");

    deleteModal.setAttribute(
        "aria-hidden",
        "true"
    );
}


// ----------------------------------------------------------
// FERMER EN CLIQUANT À L'EXTÉRIEUR
// ----------------------------------------------------------

if (deleteModal) {

    deleteModal.addEventListener(
        "click",
        function(event) {

            if (event.target === deleteModal) {

                fermerSuppression();

            }

        }
    );

}