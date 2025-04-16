// Tab switching functionality
document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => {
        // Remove active class from all tabs and contents
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        
        // Add active class to clicked tab
        tab.classList.add('active');
        
        // Show corresponding content
        const tabId = tab.getAttribute('data-tab');
        document.getElementById(tabId).classList.add('active');
    });
});

// Funzione di filtro per la ricerca
function setupSearch(inputId, tableId, columns) {
    const input = document.getElementById(inputId);
    if (!input) return;
    
    input.addEventListener('keyup', function() {
        const filter = this.value.toLowerCase();
        const table = document.querySelector(`#${tableId} table`);
        const rows = table.getElementsByTagName('tr');
        
        for (let i = 1; i < rows.length; i++) { // Skip header row
            let match = false;
            const row = rows[i];
            
            for (let col of columns) {
                const cell = row.getElementsByTagName('td')[col];
                if (cell) {
                    const text = cell.textContent || cell.innerText;
                    if (text.toLowerCase().indexOf(filter) > -1) {
                        match = true;
                        break;
                    }
                }
            }
            
            if (match) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        }
    });
}

// Setup search functionality for each tab
document.addEventListener('DOMContentLoaded', function() {
    setupSearch('search-all', 'all', [1, 2, 3, 4]); // User, Service, Description, Date
    setupSearch('search-gym', 'gym', [1, 2, 3, 4]); // User, Course, Description, Date
    setupSearch('search-spa', 'spa', [1, 2, 3, 4]); // User, Treatment, Description, Date
    
    // Gestione bottoni azioni
    document.querySelectorAll('.btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const id = this.getAttribute('data-id');
            const type = this.getAttribute('data-type');
            const action = this.classList.contains('btn-view') ? 'view' : 
                          this.classList.contains('btn-edit') ? 'edit' : 'delete';
            
            console.log(`Azione: ${action}, ID: ${id}, Tipo: ${type}`);
            
            // Qui puoi implementare le azioni specifiche
            if (action === 'delete') {
                if (confirm('Sei sicuro di voler eliminare questa prenotazione?')) {
                    // Invia richiesta AJAX per eliminare
                    // Esempio: window.location.href = `/delete-booking/${type}/${id}/`;
                }
            } else if (action === 'edit') {
                // Reindirizza alla pagina di modifica
                // Esempio: window.location.href = `/edit-booking/${type}/${id}/`;
            } else if (action === 'view') {
                // Mostra dettagli
                // Esempio: window.location.href = `/view-booking/${type}/${id}/`;
            }
        });
    });
});