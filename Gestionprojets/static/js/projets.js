// ============================================================
// GESTION DES PROJETS - INNOVLINK
// Application Porteur de Projet
// ============================================================

// ============================================================
// DONNÉES MOCKÉES
// ------------------------------------------------------------
// Ces données servent uniquement pendant la phase de conception
// de l'interface.
//
// IMPORTANT :
// Dans la vraie base Django, le champ "resultats" contiendra
// le résultat de l'analyse IA.
//
// L'analyse de l'idée est obligatoire.
// L'analyse du code est facultative.
// ============================================================

const mockProjects = [
    {
        id: 1,

        nom: "AgriTech 2.0",

        description:
            "Solution intelligente destinée à optimiser la gestion agricole grâce aux technologies numériques et aux capteurs connectés.",

        phase: "MVP",

        statut: "actif",

        consultations: 450,

        favoris: 52,

        date_creation: "12 août 2026",

        ville: "Douala",

        pays: "Cameroun",

        technologies: "Python, Django, PostgreSQL, IoT",

        collaboration: {
            active: true,
            startup: "TechVision",
            nature: "Partenariat stratégique"
        },

        // =====================================================
        // CHAMP RÉEL PRÉVU DANS LE MODÈLE
        // =====================================================

        resultats: `
            Analyse globale du projet :

            Le projet présente une proposition de valeur claire
            et répond à un besoin réel dans le secteur agricole.

            Pertinence :
            Le projet est pertinent au regard des besoins
            d'optimisation de la production agricole.

            Faisabilité :
            La solution semble techniquement réalisable,
            notamment grâce aux technologies utilisées.

            Potentiel :
            Le marché présente des possibilités de développement
            importantes.

            Points forts :
            - Problème clairement identifié
            - Proposition de valeur pertinente
            - Potentiel de développement intéressant

            Points à améliorer :
            - Approfondir le modèle économique
            - Préciser la stratégie commerciale
            - Définir les coûts d'infrastructure

            Recommandations :
            - Renforcer la stratégie d'acquisition des utilisateurs
            - Étudier davantage la concurrence
            - Définir une stratégie de développement progressive
        `,

        // Analyse technique facultative.
        // Elle ne constitue PAS un champ séparé dans la BD.
        // Cette propriété sert uniquement à simuler le cas où
        // le porteur a fourni son code.
        analyseCodeDisponible: true
    },

    {
        id: 2,

        nom: "EduLearn",

        description:
            "Plateforme interactive destinée à accompagner les élèves dans leur apprentissage grâce à l'intelligence artificielle.",

        phase: "Prototype",

        statut: "en_analyse",

        consultations: 120,

        favoris: 15,

        date_creation: "05 juillet 2026",

        ville: "Yaoundé",

        pays: "Cameroun",

        technologies: "HTML, CSS, JavaScript, Python",

        collaboration: {
            active: false
        },

        resultats: `
            Analyse globale du projet :

            Le projet évolue dans un secteur porteur et répond
            à un besoin identifié dans le domaine de l'éducation.

            Points forts :
            - Secteur à fort potentiel
            - Solution accessible
            - Utilisation pertinente de l'intelligence artificielle

            Points à améliorer :
            - Différenciation insuffisante
            - Cible initiale à préciser
            - Faisabilité technique à approfondir

            Recommandations :
            - Définir une niche pour le lancement
            - Préciser les fonctionnalités principales
            - Définir précisément l'utilisation de l'IA
        `,

        analyseCodeDisponible: false
    },

    {
        id: 3,

        nom: "FinTrack",

        description:
            "Application destinée à faciliter le suivi financier des petites entreprises.",

        phase: "Idée",

        statut: "brouillon",

        consultations: 0,

        favoris: 0,

        date_creation: "22 août 2026",

        ville: "Libreville",

        pays: "Gabon",

        technologies: "Non défini",

        collaboration: {
            active: false
        },

        resultats: `
            Analyse globale du projet :

            Le projet répond à un besoin réel chez les petites
            entreprises concernant le suivi et la gestion financière.

            Points forts :
            - Besoin clairement identifié
            - Cible identifiable

            Points à améliorer :
            - Marché concurrentiel
            - Fonctionnalités encore générales

            Recommandations :
            - Définir un avantage concurrentiel
            - Identifier les fonctionnalités prioritaires
            - Étudier les solutions déjà présentes sur le marché
        `,

        analyseCodeDisponible: false
    }
];


// ============================================================
// ÉTAT GLOBAL DE L'APPLICATION
// ============================================================

let projects = [];

let currentFilter = "all";

let currentSearch = "";

let projectToDelete = null;


// ============================================================
// INITIALISATION
// ============================================================

document.addEventListener("DOMContentLoaded", () => {

    initApp();

});


// ============================================================
// INITIALISATION DE L'APPLICATION
// ============================================================

async function initApp() {

    await loadProjects();

    setupEventListeners();

}


// ============================================================
// CHARGEMENT DES PROJETS
// ============================================================
//
// POUR LE MOMENT :
//     données mockées.
//
// PLUS TARD :
//     Django fournira les projets.
//
// Exemple futur :
//
// const response = await fetch("/api/projets/");
// projects = await response.json();
//
// ============================================================

async function loadProjects() {

    try {

        // ----------------------------------------------------
        // MODE MAQUETTE
        // ----------------------------------------------------

        projects = [...mockProjects];


        // ----------------------------------------------------
        // FUTURE VERSION DJANGO
        // ----------------------------------------------------

        /*
        const response = await fetch("/api/projets/");

        if (!response.ok) {
            throw new Error(
                "Impossible de récupérer les projets."
            );
        }

        projects = await response.json();
        */


        applyFiltersAndRender();

        updateDashboardStats();

    }

    catch (error) {

        console.error(
            "Erreur lors du chargement des projets :",
            error
        );

    }

}


// ============================================================
// ÉVÉNEMENTS
// ============================================================

function setupEventListeners() {


    // --------------------------------------------------------
    // FILTRES
    // --------------------------------------------------------

    const filterButtons =
        document.querySelectorAll(".filter-btn");


    filterButtons.forEach(button => {

        button.addEventListener("click", () => {

            filterButtons.forEach(btn => {

                btn.classList.remove("active");

            });


            button.classList.add("active");


            currentFilter =
                button.dataset.filter;


            applyFiltersAndRender();

        });

    });


    // --------------------------------------------------------
    // RECHERCHE
    // --------------------------------------------------------

    const searchInput =
        document.getElementById("search-input");


    if (searchInput) {

        searchInput.addEventListener("input", event => {

            currentSearch =
                event.target.value
                    .toLowerCase()
                    .trim();


            applyFiltersAndRender();

        });

    }

}


// ============================================================
// FILTRAGE + AFFICHAGE
// ============================================================

function applyFiltersAndRender() {

    let filteredProjects = [...projects];


    // --------------------------------------------------------
    // RECHERCHE
    // --------------------------------------------------------

    if (currentSearch) {

        filteredProjects =
            filteredProjects.filter(project => {

                const name =
                    project.nom?.toLowerCase() || "";

                const description =
                    project.description?.toLowerCase() || "";

                return (
                    name.includes(currentSearch) ||
                    description.includes(currentSearch)
                );

            });

    }


    // --------------------------------------------------------
    // FILTRE
    // --------------------------------------------------------

    switch (currentFilter) {

        case "active":

            filteredProjects =
                filteredProjects.filter(
                    project =>
                        project.statut === "actif"
                );

            break;


        case "analysis":

            filteredProjects =
                filteredProjects.filter(
                    project =>
                        project.statut === "en_analyse"
                );

            break;


        case "draft":

            filteredProjects =
                filteredProjects.filter(
                    project =>
                        project.statut === "brouillon"
                );

            break;


        case "collab":

            filteredProjects =
                filteredProjects.filter(
                    project =>
                        project.collaboration &&
                        project.collaboration.active
                );

            break;


        case "all":

        default:

            break;

    }


    renderProjects(filteredProjects);

}


// ============================================================
// AFFICHAGE DES PROJETS
// ============================================================

function renderProjects(projectList) {

    const grid =
        document.getElementById("projects-grid");


    if (!grid) return;


    grid.innerHTML = "";


    // --------------------------------------------------------
    // AUCUN PROJET
    // --------------------------------------------------------

    if (projectList.length === 0) {

        grid.innerHTML = `

            <div
                class="empty-state"
                style="grid-column: 1 / -1;"
            >

                <h3>Aucun projet trouvé</h3>

                <p>
                    Aucun projet ne correspond à votre recherche.
                </p>

                <button
                    class="btn btn-primary"
                    onclick="goToCreateProject()"
                >
                    + Créer un projet
                </button>

            </div>

        `;

        return;

    }


    // --------------------------------------------------------
    // AFFICHAGE DES CARTES
    // --------------------------------------------------------

    projectList.forEach(project => {

        grid.appendChild(
            createProjectCard(project)
        );

    });

}


// ============================================================
// CRÉATION D'UNE CARTE PROJET
// ============================================================

function createProjectCard(project) {

    const card =
        document.createElement("div");


    card.className = "card";


    const statusBadge =
        getStatusBadge(project.statut);


    let collaborationHTML = "";


    if (
        project.collaboration &&
        project.collaboration.active
    ) {

        collaborationHTML = `

            <div
                class="project-collaboration"
                style="
                    color: var(--success);
                    font-size: 0.85rem;
                    margin-top: 8px;
                "
            >

                <strong>
                    Collaboration effective
                </strong>

                <br>

                Startup :
                ${escapeHTML(
                    project.collaboration.startup
                )}

                <br>

                Nature :
                ${escapeHTML(
                    project.collaboration.nature
                )}

            </div>

        `;

    }

    else {

        collaborationHTML = `

            <div
                style="
                    color: var(--text-muted);
                    font-size: 0.85rem;
                    margin-top: 8px;
                "
            >

                Aucune collaboration

            </div>

        `;

    }


    card.innerHTML = `

        <div class="card-header">

            <div>

                <h3 class="card-title">

                    ${escapeHTML(project.nom)}

                </h3>

                <span
                    class="badge badge-primary"
                    style="
                        margin-top: 4px;
                        display:inline-block;
                    "
                >

                    ${escapeHTML(project.phase)}

                </span>

            </div>

            ${statusBadge}

        </div>


        <p class="card-desc">

            ${escapeHTML(project.description)}

        </p>


        <div class="card-stats">

            <span title="Consultations">

                👁 ${project.consultations ?? 0}

            </span>


            <span title="Favoris">

                ⭐ ${project.favoris ?? 0}

            </span>

        </div>


        <div class="card-meta">

            ${collaborationHTML}


            <span>

                Créé le
                ${escapeHTML(project.date_creation)}

            </span>

        </div>


        <div class="card-actions">

            <button
                class="btn btn-secondary flex-1"
                onclick="viewProjectDetails(${project.id})"
            >

                Voir le projet

            </button>


            <button
                class="btn btn-secondary btn-sm"
                onclick="editProject(${project.id})"
                title="Modifier"
            >

                ✏️

            </button>


            <button
                class="btn btn-danger btn-sm"
                onclick="openDeleteModal(${project.id})"
                title="Supprimer"
            >

                🗑️

            </button>

        </div>

    `;


    return card;

}


// ============================================================
// BADGE STATUT
// ============================================================

function getStatusBadge(status) {

    switch (status) {

        case "actif":

            return `
                <span class="badge badge-active">
                    🟢 Actif
                </span>
            `;


        case "en_analyse":

            return `
                <span class="badge badge-analysis">
                    🟡 En analyse
                </span>
            `;


        case "brouillon":

            return `
                <span class="badge badge-draft">
                    ⚪ Brouillon
                </span>
            `;


        default:

            return `
                <span class="badge">
                    Non défini
                </span>
            `;

    }

}


// ============================================================
// STATISTIQUES
// ============================================================

function updateDashboardStats() {

    const total =
        document.getElementById("stat-total");

    const actifs =
        document.getElementById("stat-actifs");

    const collaborations =
        document.getElementById("stat-collab");

    const analyses =
        document.getElementById("stat-analyse");


    if (total) {

        total.innerText =
            projects.length;

    }


    if (actifs) {

        actifs.innerText =
            projects.filter(
                project =>
                    project.statut === "actif"
            ).length;

    }


    if (collaborations) {

        collaborations.innerText =
            projects.filter(
                project =>
                    project.collaboration &&
                    project.collaboration.active
            ).length;

    }


    if (analyses) {

        analyses.innerText =
            projects.filter(
                project =>
                    project.statut === "en_analyse"
            ).length;

    }

}


// ============================================================
// AFFICHAGE DES DÉTAILS D'UN PROJET
// ============================================================

function viewProjectDetails(id) {

    const project =
        projects.find(
            project =>
                project.id === id
        );


    if (!project) return;


    // --------------------------------------------------------
    // TITRE
    // --------------------------------------------------------

    const title =
        document.getElementById("detail-title");


    if (title) {

        title.innerText =
            project.nom;

    }


    // --------------------------------------------------------
    // INFORMATIONS DU PROJET
    // --------------------------------------------------------

    const info =
        document.getElementById("detail-info");


    if (info) {

        info.innerHTML = `

            <p>
                <strong>Description :</strong>
                ${escapeHTML(project.description)}
            </p>

            <p>
                <strong>Phase :</strong>
                ${escapeHTML(project.phase)}
            </p>

            <p>
                <strong>Technologies :</strong>
                ${escapeHTML(project.technologies)}
            </p>

            <p>
                <strong>Localisation :</strong>
                ${escapeHTML(project.ville)},
                ${escapeHTML(project.pays)}
            </p>

            <p>
                <strong>Date de création :</strong>
                ${escapeHTML(project.date_creation)}
            </p>

        `;

    }


    // --------------------------------------------------------
    // STATISTIQUES
    // --------------------------------------------------------

    const stats =
        document.getElementById("detail-stats");


    if (stats) {

        stats.innerHTML = `

            <div class="info-list">

                <p>
                    <strong>Consultations :</strong>
                    ${project.consultations ?? 0}
                </p>

                <p>
                    <strong>Favoris :</strong>
                    ${project.favoris ?? 0}
                </p>

                <p>
                    <strong>Statut :</strong>
                    ${getStatusBadge(project.statut)}
                </p>

            </div>

        `;

    }


    // --------------------------------------------------------
    // COLLABORATION
    // --------------------------------------------------------

    const collaboration =
        document.getElementById(
            "detail-collab"
        );


    if (collaboration) {

        if (
            project.collaboration &&
            project.collaboration.active
        ) {

            collaboration.innerHTML = `

                <div class="info-list">

                    <p>
                        <strong>
                            Statut :
                        </strong>

                        🟢 Collaboration effective
                    </p>

                    <p>
                        <strong>
                            Startup :
                        </strong>

                        ${escapeHTML(
                            project.collaboration.startup
                        )}
                    </p>

                    <p>
                        <strong>
                            Nature :
                        </strong>

                        ${escapeHTML(
                            project.collaboration.nature
                        )}
                    </p>

                </div>

            `;

        }

        else {

            collaboration.innerHTML = `

                <p
                    style="
                        color: var(--text-muted);
                    "
                >

                    Ce projet ne fait actuellement
                    l'objet d'aucune collaboration.

                </p>

            `;

        }

    }


    // ========================================================
    // ANALYSE IA
    // ========================================================
    //
    // IMPORTANT :
    // On utilise UNIQUEMENT le champ "resultats".
    //
    // Le JS ne suppose pas que la BD contient :
    // score
    // pertinence
    // innovation
    // faisabilité
    // etc.
    //
    // Gemini pourra enregistrer son analyse complète
    // dans "resultats".
    //
    // ========================================================

    const aiContainer =
        document.getElementById(
            "detail-ai-idea"
        );


    if (aiContainer) {

        if (
            project.resultats &&
            project.resultats.trim() !== ""
        ) {

            aiContainer.innerHTML = `

                <div class="ai-header">

                    <h3>
                        🤖 Analyse IA du projet
                    </h3>

                    <span class="badge badge-readonly">
                        🔒 Lecture seule
                    </span>

                </div>


                <div
                    class="ai-result"
                    style="
                        white-space: pre-line;
                        line-height: 1.7;
                        color: var(--text-main);
                    "
                >

                    ${escapeHTML(
                        project.resultats
                    )}

                </div>

            `;

        }

        else {

            aiContainer.innerHTML = `

                <div class="empty-state">

                    <h3>
                        Analyse IA indisponible
                    </h3>

                    <p>

                        L'analyse IA de ce projet
                        n'est pas encore disponible.

                    </p>

                </div>

            `;

        }

    }


    // ========================================================
    // ANALYSE TECHNIQUE DU CODE
    // ========================================================
    //
    // L'analyse du code est FACULTATIVE.
    //
    // Elle ne doit donc pas être présentée comme obligatoire.
    //
    // Comme ton modèle possède uniquement "resultats",
    // si une analyse technique existe, elle peut être
    // intégrée au même champ "resultats".
    //
    // ========================================================

    const codeContainer =
        document.getElementById(
            "detail-ai-code-container"
        );


    if (codeContainer) {

        if (project.analyseCodeDisponible) {

            codeContainer.innerHTML = `

                <div class="ai-header">

                    <h3>
                        💻 Analyse technique du code
                    </h3>

                    <span class="badge badge-readonly">
                        🔒 Lecture seule
                    </span>

                </div>


                <p
                    style="
                        color: var(--text-muted);
                        line-height: 1.6;
                    "
                >

                    Une analyse technique du code
                    a été prise en compte dans
                    l'analyse IA globale du projet.

                </p>


                <div
                    style="
                        margin-top: 16px;
                        padding: 14px;
                        border-radius: 8px;
                        background: var(--bg-main);
                        border: 1px solid var(--border-color);
                    "
                >

                    <strong>
                        Analyse facultative
                    </strong>

                    <p
                        style="
                            margin-top: 6px;
                            color: var(--text-muted);
                        "
                    >

                        Le porteur peut fournir un dépôt
                        GitHub ou les fichiers de son projet
                        afin d'obtenir une analyse technique
                        complémentaire.

                    </p>

                </div>

            `;

        }

        else {

            codeContainer.innerHTML = `

                <div class="empty-state">

                    <h3>
                        Analyse technique du code
                    </h3>

                    <p>

                        Aucune analyse technique du code
                        n'est disponible pour ce projet.

                    </p>

                    <p
                        style="
                            font-size: 0.85rem;
                            margin-top: 8px;
                        "
                    >

                        Cette analyse est facultative.

                        Le porteur pourra fournir
                        ultérieurement un dépôt GitHub
                        ou les fichiers du projet.

                    </p>

                </div>

            `;

        }

    }


    // ========================================================
    // CHANGEMENT DE VUE
    // ========================================================

    const listView =
        document.getElementById(
            "view-projects-list"
        );


    const detailView =
        document.getElementById(
            "view-project-detail"
        );


    if (listView) {

        listView.classList.add("hidden");

    }


    if (detailView) {

        detailView.classList.remove("hidden");

    }

}


// ============================================================
// RETOUR À LA LISTE
// ============================================================

function showListView() {

    const listView =
        document.getElementById(
            "view-projects-list"
        );


    const detailView =
        document.getElementById(
            "view-project-detail"
        );


    if (detailView) {

        detailView.classList.add("hidden");

    }


    if (listView) {

        listView.classList.remove("hidden");

    }

}


// ============================================================
// CRÉATION D'UN PROJET
// ============================================================

function goToCreateProject() {

    /*
     * Route Django prévue.
     *
     * À adapter au nom réel de ta route.
     */

    window.location.href =
        "/gestion-projets/creer/";

}


// ============================================================
// MODIFICATION D'UN PROJET
// ============================================================

function editProject(id) {

    /*
     * Route Django prévue.
     */

    window.location.href =
        `/gestion-projets/${id}/modifier/`;

}


// ============================================================
// OUVERTURE DE LA MODALE DE SUPPRESSION
// ============================================================

function openDeleteModal(id) {

    projectToDelete = id;


    const modal =
        document.getElementById(
            "delete-modal"
        );


    if (modal) {

        modal.classList.remove("hidden");

    }

}


// ============================================================
// FERMETURE DE LA MODALE
// ============================================================

function closeDeleteModal() {

    projectToDelete = null;


    const modal =
        document.getElementById(
            "delete-modal"
        );


    if (modal) {

        modal.classList.add("hidden");

    }

}


// ============================================================
// SUPPRESSION D'UN PROJET
// ============================================================
//
// POUR LA MAQUETTE :
// suppression locale.
//
// PLUS TARD :
// requête DELETE vers Django.
// ============================================================

async function executeDelete() {

    if (!projectToDelete) return;


    try {

        // ====================================================
        // VERSION MAQUETTE
        // ====================================================

        projects =
            projects.filter(
                project =>
                    project.id !== projectToDelete
            );


        applyFiltersAndRender();

        updateDashboardStats();

        closeDeleteModal();


        // ====================================================
        // FUTURE VERSION DJANGO
        // ====================================================

        /*
        const response = await fetch(
            `/api/projets/${projectToDelete}/`,
            {
                method: "DELETE",
                headers: {
                    "X-CSRFToken":
                        getCookie("csrftoken")
                }
            }
        );

        if (!response.ok) {
            throw new Error(
                "Erreur lors de la suppression."
            );
        }
        */


    }

    catch (error) {

        console.error(
            "Erreur suppression :",
            error
        );

    }

}


// ============================================================
// PROTECTION CONTRE L'INJECTION HTML
// ============================================================
//
// Très important puisque les informations des projets
// viendront plus tard de la base de données.
//
// ============================================================

function escapeHTML(value) {

    if (value === null || value === undefined) {

        return "";

    }


    return String(value)

        .replace(/&/g, "&amp;")

        .replace(/</g, "&lt;")

        .replace(/>/g, "&gt;")

        .replace(/"/g, "&quot;")

        .replace(/'/g, "&#039;");

}


// ============================================================
// RÉCUPÉRATION DU CSRF DJANGO
// ------------------------------------------------------------
// À utiliser lorsque les requêtes POST / PUT / DELETE
// seront réellement connectées à Django.
// ============================================================

function getCookie(name) {

    const cookies =
        document.cookie
            .split(";")
            .map(cookie => cookie.trim());


    for (const cookie of cookies) {

        if (
            cookie.startsWith(
                name + "="
            )
        ) {

            return decodeURIComponent(
                cookie.substring(
                    name.length + 1
                )
            );

        }

    }


    return null;

}


// ============================================================
// FIN DU FICHIER
// ============================================================