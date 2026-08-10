document.addEventListener("DOMContentLoaded", () => {
    
    // 1. GESTION DE LA NAVBAR AU SCROLL
    const navbar = document.getElementById("navbar");
    
    window.addEventListener("scroll", () => {
        if (window.scrollY > 50) {
            navbar.classList.add("scrolled");
        } else {
            navbar.classList.remove("scrolled");
        }
    });

    // 2. MENU MOBILE
    const mobileBtn = document.getElementById("mobile-btn");
    const navLinks = document.querySelector(".nav-links");
    
    if (mobileBtn) {
        mobileBtn.addEventListener("click", () => {
            navLinks.classList.toggle("active");
            // Changement d'icône (hamburger / croix)
            const icon = mobileBtn.querySelector("i");
            if (navLinks.classList.contains("active")) {
                icon.classList.remove("fa-bars");
                icon.classList.add("fa-xmark");
            } else {
                icon.classList.remove("fa-xmark");
                icon.classList.add("fa-bars");
            }
        });
    }

    // 3. ANIMATION TYPING SUR LE SLOGAN (Page d'accueil)
    const sloganElement = document.getElementById("animated-slogan");
    
    if (sloganElement) {
        const sentences = [
            "Connecter les idées.",
            "Accélérer l'innovation.",
            "Construire les solutions de demain."
        ];
        
        let sentenceIndex = 0;
        let charIndex = 0;
        let isDeleting = false;
        let typingSpeed = 100;

        function typeWriter() {
            const currentSentence = sentences[sentenceIndex];
            
            if (isDeleting) {
                sloganElement.textContent = currentSentence.substring(0, charIndex - 1);
                charIndex--;
                typingSpeed = 50; // Plus rapide quand ça efface
            } else {
                sloganElement.textContent = currentSentence.substring(0, charIndex + 1);
                charIndex++;
                typingSpeed = 100;
            }

            // Gestion des pauses et changements de mots
            if (!isDeleting && charIndex === currentSentence.length) {
                // Mot terminé, faire une pause
                typingSpeed = 2000;
                isDeleting = true;
            } else if (isDeleting && charIndex === 0) {
                isDeleting = false;
                sentenceIndex = (sentenceIndex + 1) % sentences.length;
                typingSpeed = 500; // Pause avant le prochain mot
            }

            setTimeout(typeWriter, typingSpeed);
        }

        // Lancer l'animation
        setTimeout(typeWriter, 1000);
    }
});