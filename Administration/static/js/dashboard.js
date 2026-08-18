document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.getElementById('sidebar');
    const mobileToggle = document.getElementById('mobileToggle');
    const mobileCloseBtn = document.getElementById('mobileCloseBtn');
    const sidebarOverlay = document.getElementById('sidebarOverlay');
    const searchInput = document.getElementById('searchInput');

    // Gestion de l'affichage de la sidebar sur mobile
    function toggleSidebar() {
        sidebar.classList.toggle('open');
        sidebarOverlay.classList.toggle('open');
    }

    if (mobileToggle) {
        mobileToggle.addEventListener('click', toggleSidebar);
    }

    if (mobileCloseBtn) {
        mobileCloseBtn.addEventListener('click', toggleSidebar);
    }

    if (sidebarOverlay) {
        sidebarOverlay.addEventListener('click', toggleSidebar);
    }

    // Raccourci clavier (Ctrl + K) pour cibler la barre de recherche
    document.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
            e.preventDefault();
            if (searchInput) {
                searchInput.focus();
            }
        }
    });

    // Gestion interactive des liens de navigation actifs
    const navItems = document.querySelectorAll('.sidebar-nav .nav-item');
    navItems.forEach(item => {
        item.addEventListener('click', function() {
            navItems.forEach(nav => nav.classList.remove('active'));
            this.classList.add('active');
        });
    });
});