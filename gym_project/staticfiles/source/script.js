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
