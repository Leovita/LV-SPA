from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.models import User, ProfileUpdateForm, ProfilePictureForm
from django.conf import settings
import re

def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'users/profile.html', {'MEDIA_URL': settings.MEDIA_URL})

def login(req):
    if req.method == "POST":
        mail = req.POST.get("email")
        pwd = req.POST.get("login-password")

        if not mail or not pwd:
            messages.error(req, "Inserisci email e password.")
            return render(req, "users/login.html")

        user = authenticate(req, username=mail, password=pwd)
        if user:
            auth_login(req, user)
            messages.success(req, "Login effettuato!")
            return redirect('home')
        else:
            messages.error(req, "Email o password errati.")

    return render(req, "users/login.html")

def register(req):
    if req.method == "POST":
        name = req.POST.get("register-name", "").strip()
        mail = req.POST.get("register-email", "").strip().lower()
        pwd = req.POST.get("register-password", "")
        pwd2 = req.POST.get("register-confirm", "")

        if not all([name, mail, pwd, pwd2]):
            messages.error(req, "Compila tutti i campi.")
            return render(req, "users/login.html", {'tab': 'register', 'form_data': req.POST})

        # Validazione email
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, mail):
            messages.error(req, "Email non valida.")
            return render(req, "users/login.html", {'tab': 'register', 'form_data': req.POST})

        if pwd != pwd2:
            messages.error(req, "Le password non coincidono.")
            return render(req, "users/login.html", {'tab': 'register', 'form_data': req.POST})

        if User.objects.filter(email__iexact=mail).exists():
            messages.error(req, "Utente già esistente con questa email.")
            return render(req, "users/login.html", {'tab': 'register', 'form_data': req.POST})

        # Validazione nome completo
        if len(name) < 3 or len(name.split()) < 2:
            messages.error(req, "Il nome completo deve contenere almeno nome e cognome (minimo 3 caratteri e almeno due parole).")
            return render(req, "users/login.html", {'tab': 'register', 'form_data': req.POST})

        pwd_err = User.validate_password(pwd)
        if pwd_err:
            for err in pwd_err:
                messages.error(req, err)
            return render(req, "users/login.html", {'tab': 'register', 'form_data': req.POST})
        try:
            user = User.objects.create_user(email=mail, password=pwd, full_name=name)
            messages.success(req, "Registrazione completata! Ora puoi effettuare il login.")
            return redirect('login')
        except Exception as e:
            messages.error(req, "Errore durante la registrazione.")
            print(f"[Register Error]: {e}")
            return render(req, "users/login.html", {'tab': 'register', 'form_data': req.POST})

    return render(req, "users/login.html", {'tab': 'register'})

def user_logout(request):
    """Effettua il logout dell'utente e lo reindirizza alla homepage."""
    logout(request)
    return redirect('home')

@login_required
def change_password_view(request):
    """
    Visualizza la pagina per il cambio della password.
    """
    return render(request, 'users/change_password.html') 