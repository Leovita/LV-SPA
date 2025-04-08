document.addEventListener('DOMContentLoaded', function() {
    // Profile picture upload functionality
    const profilePicInput = document.getElementById('profile-pic-input');
    const changePhotoBtn = document.getElementById('change-photo-btn');
    const uploadPhotoBtn = document.getElementById('upload-photo-btn');
    const profilePicContainer = document.querySelector('.profile-picture-container');
    const currentProfilePic = document.querySelector('.current-profile-pic');
    
    changePhotoBtn.addEventListener('click', function() {
        profilePicInput.click();
    }); 
    
    profilePicInput.addEventListener('change', function() {
        if (this.files && this.files[0]) {
            const reader = new FileReader();
            
            reader.onload = function(e) {
                currentProfilePic.src = e.target.result;
                uploadPhotoBtn.disabled = false;
            }
            
            reader.readAsDataURL(this.files[0]);
        }
    });
    
    profilePicContainer.addEventListener('click', function() {
        profilePicInput.click();
    });
    
    const personalInfoForm = document.querySelector('.personal-info-section form');
    
    personalInfoForm.addEventListener('submit', function(e) {
        const emailInput = document.getElementById('email');
        const phoneInput = document.getElementById('phone');
        // validazione mail 
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailPattern.test(emailInput.value)) {
            e.preventDefault();
            showFormError(emailInput, 'Inserisci un indirizzo email valido');
            return;
        }
        
        // validazione telefono
        if (phoneInput.value.trim() !== '') {
            const phonePattern = /^[0-9+\s()-]{6,20}$/;
            if (!phonePattern.test(phoneInput.value)) {
                e.preventDefault();
                showFormError(phoneInput, 'Inserisci un numero di telefono valido');
                return;
            }
        }
    });
    
    function showFormError(inputElement, message) {
        const existingError = inputElement.parentElement.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }
        
        inputElement.classList.add('error');
        const errorSpan = document.createElement('span');
        errorSpan.className = 'error-message';
        errorSpan.textContent = message;
        inputElement.parentElement.appendChild(errorSpan);
        
        errorSpan.style.color = '#e74c3c';
        errorSpan.style.fontSize = '0.85rem';
        errorSpan.style.display = 'block';
        errorSpan.style.marginTop = '5px';
        
        inputElement.addEventListener('input', function() {
            inputElement.classList.remove('error');
            errorSpan.remove();
        }, { once: true });
    }
    
    const messages = document.querySelectorAll('.message');
    if (messages.length > 0) {
        setTimeout(() => {
            messages.forEach(msg => {
                msg.style.transition = 'opacity 0.5s ease';
                msg.style.opacity = '0';
                setTimeout(() => {
                    msg.remove();
                }, 500);
            });
        }, 5000);
    }
});

function toggleDropdown() {
    const dropdown = document.querySelector('.dropdown');
    dropdown.classList.toggle('active');
    
    if (dropdown.classList.contains('active')) {
        document.addEventListener('click', function closeDropdown(e) {
            if (!dropdown.contains(e.target)) {
                dropdown.classList.remove('active');
                document.removeEventListener('click', closeDropdown);
            }
        });
    }
}