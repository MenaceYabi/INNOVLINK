document.addEventListener('DOMContentLoaded', () => {
    // 1. Gestion de la Sidebar (Responsive)
    const sidebar = document.getElementById('sidebar');
    const menuToggle = document.getElementById('menuToggle');
    const closeSidebar = document.getElementById('closeSidebar');
    const sidebarOverlay = document.getElementById('sidebarOverlay');

    function toggleSidebar() {
        sidebar.classList.toggle('active');
        sidebarOverlay.classList.toggle('active');
    }

    if (menuToggle && closeSidebar && sidebarOverlay) {
        menuToggle.addEventListener('click', toggleSidebar);
        closeSidebar.addEventListener('click', toggleSidebar);
        sidebarOverlay.addEventListener('click', toggleSidebar);
    }

    // 2. Raccourci Clavier pour la Recherche (Ctrl + K)
    const searchInput = document.getElementById('searchInput');
    document.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            searchInput.focus();
        }
    });

    // 3. Gestion simple de l'ajout aux favoris (changement visuel)
    const favorisBtns = document.querySelectorAll('.project-header .btn-icon');
    favorisBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const icon = this.querySelector('i');
            if (icon.classList.contains('fa-regular')) {
                icon.classList.replace('fa-regular', 'fa-solid');
                icon.style.color = 'var(--danger)';
            } else {
                icon.classList.replace('fa-solid', 'fa-regular');
                icon.style.color = '';
            }
        });
    });

    // 4. Préparation des modales / Dropdowns (Structure de base)
    // Les menus de profil et notifications pourront être développés ici
    const profileToggle = document.getElementById('profileToggle');
    const notifToggle = document.getElementById('notifToggle');

    if (profileToggle) {
        profileToggle.addEventListener('click', () => {
            // Logique de dropdown à implémenter si nécessaire
            console.log('Toggle profil dropdown');
        });
    }

    if (notifToggle) {
        notifToggle.addEventListener('click', () => {
            // Logique de dropdown notifications à implémenter si nécessaire
            console.log('Toggle notifications dropdown');
        });
    }
});