from datetime import datetime, time, timezone
import json
import re
from django.contrib import messages
from django.core.validators import validate_email
from django.forms import ValidationError
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as auth_login, logout
from spa.models import SpaBooking, SpaService
from users.models import User
from palestra.models import GymBooking, GymClass
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_http_methods
from users.models import ProfileUpdateForm, ProfilePictureForm
from django.contrib.auth.models import Group


def gest_corsi(request):
    gym_courses = GymClass.objects.all()
    spa_services = SpaService.objects.all()
    all_courses = list(gym_courses) + list(spa_services)
    total_gym_courses = gym_courses.count()
    total_spa_services = spa_services.count()

    return render(request, 'users/gest_corsi.html', {
        'gym_courses': gym_courses,
        'spa_services': spa_services,
        'all_courses': all_courses,
        'total_gym_courses': total_gym_courses,
        'total_spa_services': total_spa_services,
    })

def profile(request):
    if not request.user.is_authenticated:
        return redirect('login') 
    return render(request, 'users/profile.html')

def login(request): 
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("login-password")

        if not email or not password:
            messages.error(request, "Inserisci email e password.")
            return render(request, "users/login.html")

        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, "Login effettuato con successo!")
            return redirect('home')
        else:
            messages.error(request, "Email o password non validi.")
    
    return render(request, "users/login.html")

def home(request):
    gym_services = GymClass.objects.all()
    spa_services = SpaService.objects.all()

    gym_dates = {}
    spa_dates = {}

    # date gym calss
    for service in gym_services:
        booking_date = GymBooking.objects.filter(class_id=service).values_list('date', flat=True).first()
        gym_dates[service.id] = booking_date
    # date servizi spa
    for service in spa_services:
        booking_date = SpaBooking.objects.filter(service_id=service).values_list('date', flat=True).first()
        spa_dates[service.id] = booking_date

    return render(request, 'users/home.html', {
        'gym_services': gym_services,
        'spa_services': spa_services,
        'gym_service_booking_dates': gym_dates,
        'spa_service_booking_dates': spa_dates,
        'timestamp': datetime.now().timestamp(),  
    })

def validate_password(password):
    errors = []
    if len(password) < 8:
        errors.append("La password deve avere almeno 8 caratteri.")
    if not re.search(r'[A-Z]', password):
        errors.append("La password deve contenere almeno una lettera maiuscola.")
    if not re.search(r'[a-z]', password):
        errors.append("La password deve contenere almeno una lettera minuscola.")
    if not re.search(r'[0-9]', password):
        errors.append("La password deve contenere almeno un numero.")
    if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
        errors.append("La password deve contenere almeno un carattere speciale (!@#$%^&* etc.).")
    return errors

def register(request):
    if request.method == "POST":
        full_name = request.POST.get("register-name", "").strip()
        email = request.POST.get("register-email", "").strip().lower()
        password = request.POST.get("register-password", "")
        password_confirm = request.POST.get("register-confirm", "")

        if not all([full_name, email, password, password_confirm]):
            messages.error(request, "Tutti i campi devono essere compilati.")
            return redirect('/login/?tab=register')

        if password != password_confirm:
            messages.error(request, "Le password non coincidono.")
            return redirect('/login/?tab=register')

        if User.objects.filter(email__iexact=email).exists():
            messages.error(request, "Un utente con questa email esiste già.")
            return redirect('/login/?tab=register')

        password_errors = validate_password(password)
        if password_errors:
            for error in password_errors:
                messages.error(request, error)
            return redirect('/login/?tab=register')
        try:
            user = User.objects.create_user(
                email=email,
                password=password,
                full_name=full_name
            )
            messages.success(request, "Registrazione completata! Ora puoi effettuare il login.")
            return redirect("login")
        except Exception as e:
            messages.error(request, f"Errore durante la registrazione. Riprova più tardi.")
            print(f"[Register Error]: {e}")
            return redirect('/login/?tab=register')


    return redirect('/login/?tab=register')

def user_logout(request):
    """Effettua il logout dell'utente e lo reindirizza alla homepage."""
    logout(request)
    return redirect('home')

@login_required
def profile_view(request):
    """
    Visualizza la pagina del profilo utente.
    """
    return redirect('profile')

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


#fix groups!
def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_admin)
def gest_prenotazioni(request):
    print(request.user)
    gym_bookings = GymBooking.objects.select_related('user', 'class_id').all()    
    spa_bookings = SpaBooking.objects.select_related('user', 'service_id').all()    

    # print(gym_bookings, spa_bookings)
    gym_count = gym_bookings.count()
    spa_count = spa_bookings.count()
    
    all_bookings = []
    
    for booking in gym_bookings:
        all_bookings.append({
            'id': booking.id,
            'user': f"{booking.user.full_name}",
            'service': f"{booking.class_id.name} (Palestra)",
            'description': booking.description if booking.description else booking.class_id.description,
            'date': booking.date,
            'status': 'confirmed',  
            'type': 'gym'
        })
    
    for booking in spa_bookings:
        all_bookings.append({
            'id': booking.id,
            'user': f"{booking.user.full_name}",
            'service': f"{booking.service_id.name} (Spa)",
            'description': booking.description if booking.description else booking.service_id.description,
            'date': booking.date,
            'status': 'confirmed',
            'type': 'spa'
        })
    
    #sort
    all_bookings.sort(key=lambda x: x['date'])
    
    gym_bookings_data = []
    for booking in gym_bookings:
        gym_bookings_data.append({
            'id': booking.id,
            'user': f"{booking.user.full_name}",
            'course': booking.class_id.name,
            'description': booking.description if booking.description else booking.class_id.description,
            'date': booking.date,
            'status': 'confirmed', 
        })
    
    spa_bookings_data = []
    for booking in spa_bookings:
        spa_bookings_data.append({
            'id': booking.id,
            'user': f"{booking.user.full_name}",
            'treatment': booking.service_id.name,
            'description': booking.description if booking.description else booking.service_id.description,
            'date': booking.date,
            'status': 'confirmed',  
        })
    
    context = {
        'total_gym_bookings': gym_count,
        'total_spa_bookings': spa_count,
        'all_bookings': all_bookings,
        'gym_bookings': gym_bookings_data,
        'spa_bookings': spa_bookings_data,
        'timestamp': datetime.now().timestamp(),  
    }
    
    return render(request, 'users/gest_prenotazioni.html', context)


@login_required
@require_http_methods(["POST"])
def book_gym_class(request, class_id):
    try:
        gym_class = GymClass.objects.get(id=class_id)
        
        if not gym_class.check_availability:
            return JsonResponse({'success': False, 'error': 'Classe esaurita. Non ci sono posti disponibili.'})
        
        data = json.loads(request.body)
        date_time_str = data.get('date_time')
        
        if not date_time_str:
            return JsonResponse({'success': False, 'error': 'Data/ora mancante.'})
        
        try:
            date_time = datetime.fromisoformat(date_time_str)
        except ValueError:
            return JsonResponse({'success': False, 'error': 'Formato data/ora non valido.'})
        
        # Create booking object
        booking = GymBooking.objects.create(
            user=request.user,
            class_id=gym_class,
            date=date_time,
        )
        
        return JsonResponse({
            'success': True, 
            'booking_id': booking.id,
            'message': f'Prenotazione per {gym_class.name} confermata!'
        })
    
    except GymClass.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Classe non trovata.'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
@require_http_methods(["POST"])
def book_spa_service(request, service_id):
    try:
        spa_service = SpaService.objects.get(id=service_id)
        
        if not spa_service.check_availability:
            return JsonResponse({'success': False, 'error': 'Servizio non disponibile al momento.'})
        
        data = json.loads(request.body)
        date_time_str = data.get('date_time')
        
        if not date_time_str:
            return JsonResponse({'success': False, 'error': 'Data/ora mancante.'})
        
        try:
            date_time = datetime.fromisoformat(date_time_str)
        except ValueError:
            return JsonResponse({'success': False, 'error': 'Formato data/ora non valido.'})
        
        notes = data.get('notes', '')
        
        booking = SpaBooking.objects.create(
            user=request.user,
            service_id=spa_service,
            date=date_time,
            description=notes
        )
        
        return JsonResponse({
            'success': True, 
            'booking_id': booking.id,
            'message': f'Prenotazione per {spa_service.name} confermata!'
        })
    except SpaService.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Servizio non trovato.'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def my_bookings(request):
    gym_bookings = GymBooking.objects.filter(user=request.user).order_by('-date')
    spa_bookings = SpaBooking.objects.filter(user=request.user).order_by('-date')
    
    context = {
        'gym_bookings': gym_bookings,
        'spa_bookings': spa_bookings,
    }
    
    return render(request, 'users/my_bookings.html', context)

@login_required
def cancel_gym_booking(request, booking_id):
    try:
        booking = GymBooking.objects.get(id=booking_id, user_id=request.user.id)
        booking.delete()
        return JsonResponse({'success': True})
    except GymBooking.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Prenotazione non trovata'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
def cancel_spa_booking(request, booking_id):
    try:
        booking = SpaBooking.objects.get(id=booking_id, user_id=request.user.id)
        booking.delete()
        return JsonResponse({'success': True})
    except SpaBooking.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Prenotazione non trovata'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})