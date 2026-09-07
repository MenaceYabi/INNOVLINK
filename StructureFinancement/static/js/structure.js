
        /* ============================================================
           NAVIGATION ENTRE LES ONGLETS
        ============================================================= */

        function switchTab(tabId, clickedElement) {

            document
                .querySelectorAll(".nav-item")
                .forEach(item => {

                    item.classList.remove("active");

                });


            if (clickedElement) {

                clickedElement.classList.add("active");

            }


            document
                .querySelectorAll(".tab-pane")
                .forEach(pane => {

                    pane.classList.remove("active");

                });


            const target = document.getElementById(tabId);


            if (target) {

                target.classList.add("active");

            }


            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });
        }



        /* ============================================================
           RECHERCHE + FILTRE PHASE + TRI DATE
        ============================================================= */

        function filterProjects() {

            const searchInput =
                document.getElementById("search-projets");

            const phaseSelect =
                document.getElementById("filter-phase");

            const dateSelect =
                document.getElementById("filter-date");

            const container =
                document.getElementById("projects-container");


            if (
                !searchInput ||
                !phaseSelect ||
                !dateSelect ||
                !container
            ) {
                return;
            }


            const search =
                searchInput.value
                    .toLowerCase()
                    .trim();


            const phase =
                phaseSelect.value;


            const cards =
                Array.from(
                    container.querySelectorAll(".project-item")
                );


            cards.forEach(card => {

                const searchableText =
                    card
                        .getAttribute("data-search")
                        .toLowerCase();


                const cardPhase =
                    card.getAttribute("data-phase");


                const matchesSearch =
                    searchableText.includes(search);


                const matchesPhase =
                    phase === "all" ||
                    cardPhase === phase;


                card.style.display =
                    matchesSearch && matchesPhase
                        ? "flex"
                        : "none";

            });


            /* TRI */

            cards.sort((a, b) => {

                const idA =
                    parseInt(
                        a.getAttribute("data-id")
                    ) || 0;


                const idB =
                    parseInt(
                        b.getAttribute("data-id")
                    ) || 0;


                if (dateSelect.value === "ancien") {

                    return idA - idB;

                }


                return idB - idA;

            });


            cards.forEach(card => {

                container.appendChild(card);

            });
        }



        /* ============================================================
           EVENEMENTS FILTRES
        ============================================================= */

        document.addEventListener(
            "DOMContentLoaded",
            function () {

                const search =
                    document.getElementById(
                        "search-projets"
                    );

                const phase =
                    document.getElementById(
                        "filter-phase"
                    );

                const date =
                    document.getElementById(
                        "filter-date"
                    );


                if (search) {

                    search.addEventListener(
                        "input",
                        filterProjects
                    );

                }


                if (phase) {

                    phase.addEventListener(
                        "change",
                        filterProjects
                    );

                }


                if (date) {

                    date.addEventListener(
                        "change",
                        filterProjects
                    );

                }


                filterProjects();

            }
        );



        /* ============================================================
           RECHERCHE RAPIDE TOPBAR
        ============================================================= */

        const globalSearch =
            document.getElementById(
                "globalSearch"
            );


        if (globalSearch) {

            globalSearch.addEventListener(
                "input",
                function () {

                    const value =
                        this.value
                            .toLowerCase()
                            .trim();


                    if (!value) {
                        return;
                    }


                    const projectTab =
                        document.querySelector(
                            '[data-tab="projets"]'
                        );


                    if (projectTab) {

                        switchTab(
                            "projets",
                            projectTab
                        );

                    }


                    const projectSearch =
                        document.getElementById(
                            "search-projets"
                        );


                    if (projectSearch) {

                        projectSearch.value =
                            value;

                        filterProjects();

                    }

                }
            );

        }



        /* ============================================================
           FAVORIS — INTERFACE LOCALE
        ============================================================= */

        function toggleFavorite(button) {

            button.classList.toggle(
                "favorite-active"
            );


            const icon =
                button.querySelector("i");


            if (
                button.classList.contains(
                    "favorite-active"
                )
            ) {

                icon.classList.remove(
                    "fa-regular"
                );

                icon.classList.add(
                    "fa-solid"
                );

                button.style.color =
                    "var(--color-red)";

            } else {

                icon.classList.remove(
                    "fa-solid"
                );

                icon.classList.add(
                    "fa-regular"
                );

                button.style.color =
                    "var(--color-blue)";

            }

        }



        /* ============================================================
           MODALE DETAIL PROJET
        ============================================================= */

        function showProjectDetails(
            name,
            description,
            score,
            phase,
            technologies,
            domaine,
            collaboration
        ) {

            const modal =
                document.getElementById(
                    "projectModal"
                );


            const nameElement =
                document.getElementById(
                    "modalProjectName"
                );


            const content =
                document.getElementById(
                    "modalProjectContent"
                );


            const scoreElement =
                document.getElementById(
                    "modalScore"
                );


            nameElement.textContent =
                name;


            content.innerHTML = `

        <p>
            <strong style="color:var(--text-main);">
                Description
            </strong>
        </p>

        <p style="margin-bottom:15px;">
            ${escapeHtml(description)}
        </p>

        <p>
            <strong style="color:var(--text-main);">
                Phase :
            </strong>

            ${escapeHtml(phase)}
        </p>

        <p>
            <strong style="color:var(--text-main);">
                Technologies :
            </strong>

            ${escapeHtml(technologies)}
        </p>

        <p>
            <strong style="color:var(--text-main);">
                Domaine :
            </strong>

            ${escapeHtml(domaine)}
        </p>

        <p>
            <strong style="color:var(--text-main);">
                Type de collaboration :
            </strong>

            ${escapeHtml(collaboration)}
        </p>
    `;


            scoreElement.textContent =
                score + "/100";


            modal.style.display =
                "flex";
        }



        /* ============================================================
           FERMER MODALE
        ============================================================= */

        function closeProjectDetails() {

            document
                .getElementById(
                    "projectModal"
                )
                .style.display = "none";
        }



        /* ============================================================
           FERMER MODALE EN CLIQUANT A L'EXTERIEUR
        ============================================================= */

        document
            .getElementById("projectModal")
            .addEventListener(
                "click",
                function (event) {

                    if (
                        event.target === this
                    ) {

                        closeProjectDetails();

                    }

                }
            );



        /* ============================================================
           PROTECTION CONTRE L'INJECTION HTML
        ============================================================= */

        function escapeHtml(text) {

            if (!text) {
                return "";
            }


            return text
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;")
                .replace(/"/g, "&quot;")
                .replace(/'/g, "&#039;");
        }
