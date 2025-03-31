// Funzione per inviare il modulo di contatto (per esempio, solo una simulazione)
document.getElementById('contact-form').addEventListener('submit', function(event) {
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

document.addEventListener('DOMContentLoaded', function() {
    // Select the "Scopri i Nostri Servizi" button in the hero section
    const discoverServicesBtn = document.querySelector('.hero .btn');
    
    // Select the services section
    const servicesSection = document.getElementById('services');
    
    // Add click event listener to the button
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