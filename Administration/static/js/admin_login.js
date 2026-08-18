document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('loginForm');
    const btn = document.getElementById('submitBtn');
    const btnText = btn.querySelector('.btn-text');

    // Feedback visuel léger lors de la soumission
    form.addEventListener('submit', () => {
        btn.style.opacity = '0.7';
        btn.style.cursor = 'wait';
        btnText.textContent = 'Connexion en cours...';
        btn.disabled = true;
    });

    // Interaction simple : focus dynamique
    const inputs = document.querySelectorAll('input');
    inputs.forEach(input => {
        input.addEventListener('focus', () => {
            input.style.borderColor = '#666';
        });
        input.addEventListener('blur', () => {
            input.style.borderColor = '#222';
        });
    });
});