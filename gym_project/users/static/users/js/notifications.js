function updateCourseCounters() {
    // Get counts from each tab, excluding the "no-data" rows
    const gymRows = document.querySelectorAll('#gym tbody tr:not(.no-data)');
    const spaRows = document.querySelectorAll('#spa tbody tr:not(.no-data)');
    
    const totalGym = gymRows.length;
    const totalSpa = spaRows.length;
    const total = totalGym + totalSpa;

    // Update the stat cards with animation
    const statCards = document.querySelectorAll('.stat-cards .stat-card p');
    if (statCards.length >= 3) {
        // Animate the number changes
        animateCounter(statCards[1], parseInt(statCards[1].textContent), totalGym); // Totale Corsi Palestra
        animateCounter(statCards[0], parseInt(statCards[0].textContent), totalSpa); // Totale Servizi Spa
        animateCounter(statCards[2], parseInt(statCards[2].textContent), total);    // Corsi Totali
    }
}

// Simple function to update course counters without animation
function simpleUpdateCounters() {
    const gymRows = document.querySelectorAll('#gym tbody tr:not(.no-data)');
    const spaRows = document.querySelectorAll('#spa tbody tr:not(.no-data)');
    
    const totalGym = gymRows.length;
    const totalSpa = spaRows.length;
    const total = totalGym + totalSpa;

    // Direct update without animation
    const statCards = document.querySelectorAll('.stat-cards .stat-card p');
    if (statCards.length >= 3) {
        statCards[1].textContent = totalGym;  // Totale Corsi Palestra
        statCards[0].textContent = totalSpa;  // Totale Servizi Spa
        statCards[2].textContent = total;     // Corsi Totali
    }
}

// Function to animate counter from old to new value
function animateCounter(element, oldValue, newValue) {
    const duration = 300; // Animation duration in ms
    const start = performance.now();
    
    // Ensure we have valid numbers
    oldValue = isNaN(oldValue) ? 0 : oldValue;
    newValue = isNaN(newValue) ? 0 : newValue;
    
    function updateNumber(currentTime) {
        const elapsed = currentTime - start;
        const progress = Math.min(elapsed / duration, 1);
        
        // Easing function for smooth animation
        const easeProgress = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress);
        
        const currentValue = Math.round(oldValue + (newValue - oldValue) * easeProgress);
        element.textContent = currentValue;
        
        if (progress < 1) {
            requestAnimationFrame(updateNumber);
        }
    }
    
    requestAnimationFrame(updateNumber);
}

// Function to update booking counters
function updateBookingCounters() {
    const gymRows = document.querySelectorAll('#gym tbody tr:not(.no-data)');
    const spaRows = document.querySelectorAll('#spa tbody tr:not(.no-data)');
    
    const totalGym = gymRows.length;
    const totalSpa = spaRows.length;
    const total = totalGym + totalSpa;

    // Update the stat cards with animation
    const statCards = document.querySelectorAll('.stat-cards .stat-card p');
    if (statCards.length >= 3) {
        animateCounter(statCards[1], parseInt(statCards[1].textContent), totalGym); // Totale Prenotazioni Palestra
        animateCounter(statCards[0], parseInt(statCards[0].textContent), totalSpa); // Totale Prenotazioni Spa
        animateCounter(statCards[2], parseInt(statCards[2].textContent), total);    // Prenotazioni Totali
    }
}

function showNotification(message, type = 'success', shouldUpdateCounters = false, counterType = null) {
    let notification = document.getElementById('notification');
    if (!notification) {
        notification = document.createElement('div');
        notification.id = 'notification';
        document.body.appendChild(notification);
    }

    notification.textContent = message;
    notification.className = `notification ${type}`;
    notification.style.display = 'flex';
    
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);

    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.style.display = 'none';
        }, 300);
    }, 3000);

    if (shouldUpdateCounters) {
        if (counterType === 'courses') {
            updateCourseCounters();
        } else if (counterType === 'bookings') {
            updateBookingCounters();
        }
    }
}

function showSuccess(message, shouldUpdateCounters = false, counterType = null) {
    showNotification(message, 'success', shouldUpdateCounters, counterType);
}

function showError(message, shouldUpdateCounters = false, counterType = null) {
    showNotification(message, 'error', shouldUpdateCounters, counterType);
}

function showWarning(message, shouldUpdateCounters = false, counterType = null) {
    showNotification(message, 'warning', shouldUpdateCounters, counterType);
}

function showInfo(message, shouldUpdateCounters = false, counterType = null) {
    showNotification(message, 'info', shouldUpdateCounters, counterType);
} 