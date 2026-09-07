document.addEventListener("DOMContentLoaded", () => {

    // =====================================================
    // ELEMENTS
    // =====================================================

    const sidebar = document.getElementById("sidebar");
    const mobileToggle = document.getElementById("mobileToggle");
    const mobileCloseBtn = document.getElementById("mobileCloseBtn");
    const sidebarOverlay = document.getElementById("sidebarOverlay");
    const searchInput = document.getElementById("searchInput");

    const navItems = document.querySelectorAll(
        ".sidebar-nav .nav-item"
    );

    const tabContents = document.querySelectorAll(
        ".tab-content"
    );


    // =====================================================
    // SIDEBAR MOBILE
    // =====================================================

    function toggleSidebar() {

        if (!sidebar) return;

        sidebar.classList.toggle("open");

        if (sidebarOverlay) {
            sidebarOverlay.classList.toggle("open");
        }
    }


    if (mobileToggle) {
        mobileToggle.addEventListener(
            "click",
            toggleSidebar
        );
    }


    if (mobileCloseBtn) {
        mobileCloseBtn.addEventListener(
            "click",
            toggleSidebar
        );
    }


    if (sidebarOverlay) {
        sidebarOverlay.addEventListener(
            "click",
            toggleSidebar
        );
    }


    // =====================================================
    // CHANGEMENT D'ONGLET
    // =====================================================

    function showTab(tabName) {

        if (!tabName) {
            tabName = "dashboard";
        }


        // Cacher toutes les sections

        tabContents.forEach(section => {

            section.classList.remove("active");

        });


        // Retirer active de tous les liens

        navItems.forEach(item => {

            item.classList.remove("active");

        });


        // Afficher la section

        const selectedTab = document.getElementById(
            `tab-${tabName}`
        );

        if (selectedTab) {

            selectedTab.classList.add("active");

        } else {

            const dashboardTab =
                document.getElementById(
                    "tab-dashboard"
                );

            if (dashboardTab) {
                dashboardTab.classList.add("active");
            }

            tabName = "dashboard";
        }


        // Activer le lien correspondant

        const selectedNav = document.querySelector(
            `.nav-item[data-tab="${tabName}"]`
        );

        if (selectedNav) {

            selectedNav.classList.add("active");

        }


        // Fermer le menu mobile

        if (
            window.innerWidth <= 992 &&
            sidebar &&
            sidebar.classList.contains("open")
        ) {

            toggleSidebar();

        }


        // Mettre à jour l'URL

        const newUrl =
            `${window.location.pathname}?tab=${tabName}`;

        window.history.replaceState(
            {},
            "",
            newUrl
        );
    }


    // =====================================================
    // CLIC SIDEBAR
    // =====================================================

    navItems.forEach(item => {

        item.addEventListener("click", event => {

            event.preventDefault();

            const tabName =
                item.dataset.tab;

            showTab(tabName);

        });

    });


    // =====================================================
    // BOUTONS "VOIR TOUT"
    // =====================================================

    const tabButtons =
        document.querySelectorAll(
            "[data-tab-target]"
        );


    tabButtons.forEach(button => {

        button.addEventListener(
            "click",
            event => {

                event.preventDefault();

                const tabName =
                    button.dataset.tabTarget;

                showTab(tabName);

            }
        );

    });


    // =====================================================
    // ONGLET INITIAL
    // =====================================================

    const urlParams =
        new URLSearchParams(
            window.location.search
        );

    const initialTab =
        urlParams.get("tab") || "dashboard";

    showTab(initialTab);


    // =====================================================
    // MODALES
    // =====================================================

    function openModal(modalId) {

        const modal =
            document.getElementById(modalId);

        if (!modal) return;

        modal.classList.add("open");

        document.body.classList.add(
            "modal-open"
        );
    }


    function closeModal(modal) {

        if (!modal) return;

        modal.classList.remove("open");

        document.body.classList.remove(
            "modal-open"
        );
    }


    // Boutons d'ouverture

    const modalOpenButtons =
        document.querySelectorAll(
            "[data-modal]"
        );


    modalOpenButtons.forEach(button => {

        button.addEventListener(
            "click",
            () => {

                const modalId =
                    button.dataset.modal;

                openModal(modalId);

            }
        );

    });


    // Boutons de fermeture

    const modalCloseButtons =
        document.querySelectorAll(
            "[data-close-modal]"
        );


    modalCloseButtons.forEach(button => {

        button.addEventListener(
            "click",
            () => {

                const modal =
                    button.closest(".modal");

                closeModal(modal);

            }
        );

    });


    // Cliquer sur le fond de la modal

    document.querySelectorAll(
        ".modal"
    ).forEach(modal => {

        modal.addEventListener(
            "click",
            event => {

                if (
                    event.target === modal
                ) {

                    closeModal(modal);

                }

            }
        );

    });


    // =====================================================
    // ESCAPE
    // =====================================================

    document.addEventListener(
        "keydown",
        event => {

            if (event.key === "Escape") {

                document
                    .querySelectorAll(".modal.open")
                    .forEach(modal => {

                        closeModal(modal);

                    });

            }

        }
    );


    // =====================================================
    // CONFIRMATION SUPPRESSION
    // =====================================================

    const deleteForms =
        document.querySelectorAll(
            ".delete-form"
        );


    deleteForms.forEach(form => {

        form.addEventListener(
            "submit",
            event => {

                const confirmed =
                    window.confirm(
                        "Voulez-vous vraiment supprimer cet élément ? Cette action est irréversible."
                    );

                if (!confirmed) {

                    event.preventDefault();

                }

            }
        );

    });


    // =====================================================
    // RECHERCHE
    // =====================================================

    if (searchInput) {

        searchInput.addEventListener(
            "input",
            () => {

                const search =
                    searchInput.value
                        .toLowerCase()
                        .trim();


                const activeTab =
                    document.querySelector(
                        ".tab-content.active"
                    );


                if (!activeTab) return;


                const rows =
                    activeTab.querySelectorAll(
                        ".searchable-table tbody tr"
                    );


                rows.forEach(row => {

                    const text =
                        row.textContent
                            .toLowerCase();


                    if (
                        !search ||
                        text.includes(search)
                    ) {

                        row.style.display = "";

                    } else {

                        row.style.display =
                            "none";

                    }

                });

            }
        );

    }


    // =====================================================
    // CTRL + K
    // =====================================================

    document.addEventListener(
        "keydown",
        event => {

            if (
                (event.ctrlKey ||
                    event.metaKey) &&
                event.key.toLowerCase() === "k"
            ) {

                event.preventDefault();

                if (searchInput) {

                    searchInput.focus();

                }

            }

        }
    );

});