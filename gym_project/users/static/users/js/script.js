// Funzione per inviare il modulo di contatto (per esempio, solo una simulazione)
const contactForm = document.getElementById('contact-form');
if (contactForm) {
    contactForm.addEventListener('submit', function(event) {
        event.preventDefault();  // Previene il comportamento predefinito del modulo (invio)

        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const message = document.getElementById('message').value;

        if (name && email && message) {
            alert('Grazie per il tuo messaggio, ' + name + '! Ti risponderemo presto.');
        } else {
            alert('Per favore, compila tutti i campi del modulo.');
        }
    });
}

const loginBtn = document.querySelector(".login-btn");
if (loginBtn) {
    loginBtn.addEventListener("click", function() {
        window.location.href = "/login/";
    });
}

const registerBtn = document.querySelector(".register-btn");
if (registerBtn) {
    registerBtn.addEventListener("click", function() {
        console.log("register premuto!");
        // Assicurati che showTab sia definito se usato qui, altrimenti commenta o rimuovi
        // showTab('register');
    });
}

document.addEventListener('DOMContentLoaded', function() {
    const discoverServicesBtn = document.querySelector('.hero .btn');
    const servicesSection = document.getElementById('services');

    if (discoverServicesBtn && servicesSection) {
        discoverServicesBtn.addEventListener('click', function(event) {
            event.preventDefault();

            function smoothScroll(target) {
                const targetPosition = target.getBoundingClientRect().top + window.pageYOffset;
                const startPosition = window.pageYOffset;
                const distance = targetPosition - startPosition;
                const duration = 1000; 
                let start = null;
                
                window.requestAnimationFrame(step);
                
                function step(timestamp) {
                    if (!start) start = timestamp;
                    const progress = timestamp - start;
                    // Use easing function for more natural scroll
                    const progressPercentage = Math.min(progress / duration, 1);
                    const easeInOutCubic = progressPercentage < 0.5 
                        ? 4 * progressPercentage ** 3 
                        : 1 - Math.pow(-2 * progressPercentage + 2, 3) / 2;
                    
                    window.scrollTo(0, startPosition + distance * easeInOutCubic);
                    
                    if (progress < duration) {
                        window.requestAnimationFrame(step);
                    }
                }
            }
            
            // Call the custom smooth scroll function
            smoothScroll(servicesSection);
        });
    }
});