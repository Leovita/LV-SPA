document.addEventListener('DOMContentLoaded', function() {
    const addCourseBtn = document.getElementById('add-course-btn');
    const coursePopup = document.getElementById('course-popup');
    const courseForm = document.getElementById('course-form');

    addCourseBtn.addEventListener('click', function() {
        coursePopup.style.display = 'flex';
        document.getElementById('popup-title').textContent = 'Aggiungi Corso';
        courseForm.reset();
        courseForm.dataset.action = 'add';
    });

    courseForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(courseForm);
        const action = courseForm.dataset.action;
        const courseId = courseForm.dataset.id || null;

        fetch('/api/courses/' + (action === 'edit' ? courseId + '/' : ''), {
            method: action === 'add' ? 'POST' : 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(Object.fromEntries(formData))
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.reload();
            } else {
                alert('Errore: ' + (data.error || 'Operazione non riuscita'));
            }
        })
        .catch(error => {
            alert('Errore durante la richiesta.');
        });
    });

    document.querySelectorAll('.btn-edit').forEach(button => {
        button.addEventListener('click', function() {
            const courseId = this.dataset.id;
            fetch('/api/courses/' + courseId + '/')
            .then(response => response.json())
            .then(data => {
                coursePopup.style.display = 'flex';
                document.getElementById('popup-title').textContent = 'Modifica Corso';
                courseForm.dataset.action = 'edit';
                courseForm.dataset.id = courseId;
                document.getElementById('course-name').value = data.name;
                document.getElementById('course-description').value = data.description;
                document.getElementById('course-date').value = data.date;
                document.getElementById('course-available').value = data.available;
            });
        });
    });

    document.querySelectorAll('.btn-delete').forEach(button => {
        button.addEventListener('click', function() {
            const courseId = this.dataset.id;
            if (confirm('Sei sicuro di voler eliminare questo corso?')) {
                fetch('/api/courses/' + courseId + '/', {
                    method: 'DELETE',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken')
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        window.location.reload();
                    } else {
                        alert('Errore: ' + (data.error || 'Operazione non riuscita'));
                    }
                })
                .catch(error => {
                    alert('Errore durante la richiesta.');
                });
            }
        });
    });

    function closePopup() {
        coursePopup.style.display = 'none';
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});