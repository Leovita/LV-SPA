from datetime import time, timezone
import re
from django.contrib import messages
from django.core.validators import validate_email
from django.forms import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login as auth_login, logout
from subscriptions.models import SubscriptionPlan
from spa.models import SpaService
from users.models import User
from palestra.models import GymClass
from django.contrib.auth.decorators import login_required
from users.models import ProfileUpdateForm, ProfilePictureForm

def profile(request):
    if not request.user.is_authenticated:
        return redirect('register')  # oppure puoi aggiungere ?tab=register se hai i tab

    return render(request, 'users/profile.html')

def login(request): 
    if request.method == "POST":
        print("post request")
        email = request.POST["email"]
        password = request.POST["login-password"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            print("user non esiste")
            user = None

        if user is not None:
            authenticated_user = authenticate(request, username=email, password=password)
            if authenticated_user is not None:
                print("OTTIMO SEI DENTRO!!")
                auth_login(request, authenticated_user)  
                messages.success(request, "Login effettuato con successo!")
                return redirect('home')
            else:
                print("Credenziali non valide")
                messages.error(request, "Credenziali non valide. Riprova.")
        else:
            print("User non esiste")
            messages.error(request, "Credenziali non valide. Riprova.")

    return render(request, "users/login.html")

def home(request):
    gym_services = GymClass.objects.all()
    spa_services = SpaService.objects.all()
    
    return render(request, 'users/home.html', {
        'gym_services': gym_services,
        'spa_services': spa_services,
    })

def register(request):
    if request.method == "POST":
        full_name = request.POST.get("register-name")
        email = request.POST.get("register-email")
        password = request.POST.get("register-password")
        password_confirm = request.POST.get("register-confirm")

        print(full_name, email, password, password_confirm)
        if not full_name or not email or not password or not password_confirm:
            return render(request, "login.html/tab=register", {"error": "Tutti i campi devono essere compilati."})

        if User.objects.filter(email=email).exists():
            return render(request, "login.html/tab=register", {"error": "Un utente con questa email esiste già."})

        if password != password_confirm:
            return render(request, "register.html", {"error": "Le password non coincidono."})
   
        user = User.objects.create_user(email=email, password=password, full_name=full_name)

        return redirect('login') 
    return render(request, "users/login.html")


def user_logout(request):
    """Effettua il logout dell'utente e lo reindirizza alla homepage."""
    logout(request)
    return redirect('home')

@login_required
def profile_view(request):
    """
    Visualizza la pagina del profilo utente.
    """
    return render(request, 'users/profile.html')

@login_required
def update_profile(request):
    """
    Gestisce l'aggiornamento dei dati personali dell'utente con validazione.
    """
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        
        if form.is_valid():
            cleaned_data = form.cleaned_data
            full_name = cleaned_data.get('full_name', '').strip()
            phone = cleaned_data.get('phone', '').strip()
            email = cleaned_data.get('email', '').strip()

            # Controllo nome completo (almeno 2 parole, solo lettere/spazi)
            if not re.match(r'^[A-Za-zÀ-ÿ\s]{3,}$', full_name) or len(full_name.split()) < 2:
                messages.error(request, "Il nome completo deve contenere almeno nome e cognome (solo lettere).")
                return redirect('profile')

            if phone and (not phone.isdigit() or len(phone) < 9) or len(phone) > 10:
                messages.error(request, "Il numero di telefono deve contenere almeno 8 cifre numeriche.")
                return redirect('profile')
            try:
                validate_email(email)
            except ValidationError:
                messages.error(request, "L'email inserita non è valida.")
                return redirect('profile')

            form.save()
            messages.success(request, 'Il tuo profilo è stato aggiornato con successo!')
            return redirect('profile')
        
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

    return redirect('profile')
@login_required
def update_profile_picture(request):
    """
    Gestisce l'aggiornamento dell'immagine del profilo.
    """
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid()  :
            form.save()
            messages.success(request, 'La tua immagine del profilo è stata aggiornata con successo!')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    
    return redirect('profile')

@login_required
def change_password_view(request):
    """
    Visualizza la pagina per il cambio della password.
    """
    return render(request, 'users/change_password.html')

@login_required
def delete_account(request):
    """
    Mostra una pagina di conferma per l'eliminazione dell'account.
    Esegue l'eliminazione solo dopo la conferma (POST).
    """
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, 'Il tuo account è stato eliminato con successo.')
        return redirect('home')

    return render(request, 'users/delete_account.html')



