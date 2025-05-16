// Dropdown universale per la navbar

document.addEventListener('DOMContentLoaded', function() {
    const dropdown = document.querySelector('.dropdown');
    const profilePic = document.querySelector('.user-profile-pic');
    const dropdownMenu = document.querySelector('.dropdown-menu');

    if (!dropdown || !profilePic) return;

    // Chiudi dropdown
    function closeDropdown() {
        dropdown.classList.remove('active');
    }

    // Toggle dropdown
    profilePic.addEventListener('click', function(e) {
        e.stopPropagation();
        dropdown.classList.toggle('active');
    });

    // Chiudi cliccando fuori
    document.addEventListener('click', function(e) {
        if (!dropdown.contains(e.target)) {
            closeDropdown();
        }
    });

    // Chiudi con ESC
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeDropdown();
        }
    });

    // Non chiudere cliccando dentro il menu
    if (dropdownMenu) {
        dropdownMenu.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    }
}); 