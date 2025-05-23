from curses import window
import json
import re
from datetime import datetime
from django.contrib import messages
from django.core.validators import validate_email
from django.forms import ValidationError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_http_methods, require_POST
from django.utils import timezone
from users.models import User, ProfileUpdateForm, ProfilePictureForm
from palestra.models import GymBooking, GymClass
from spa.models import SpaBooking, SpaService
from django.contrib.auth.models import Group
from dateutil import parser
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

@login_required
@user_passes_test(lambda u: u.is_staff)
def gest_corsi(req):
    gym = GymClass.objects.all()
    spa = SpaService.objects.all()
    all_corsi = list(gym) + list(spa)
    instructors = User.objects.filter(is_staff=True)
    ctx = {
        'gym_courses': gym,
        'spa_services': spa,
        'all_courses': all_corsi,
        'total_gym_courses': gym.count(),
        'total_spa_services': spa.count(),
        'instructors': instructors,
    }
    return render(req, 'users/gest_corsi.html', ctx)

def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'users/profile.html')

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

def home(req):
    gym_srv = GymClass.objects.all()
    spa_srv = SpaService.objects.all()

    gym_date = {s.id: s.scheduled for s in gym_srv}
    spa_date = {s.id: s.scheduled for s in spa_srv}

    user_gym = []
    user_spa = []
    active_subscription = None

    if req.user.is_authenticated:
        user_gym = list(GymBooking.objects.filter(user=req.user).values_list('class_id', flat=True))
        user_spa = list(SpaBooking.objects.filter(user=req.user).values_list('service_id', flat=True))
        active_subscription = req.user.subscription_set.filter(is_active=True).first()

    ctx = {
        'gym_services': gym_srv,
        'spa_services': spa_srv,
        'gym_service_booking_dates': gym_date,
        'spa_service_booking_dates': spa_date,
        'user_gym_bookings': user_gym,
        'user_spa_bookings': user_spa,
        'active_subscription': active_subscription,
        'timestamp': datetime.now().timestamp(),
    }

    return render(req, 'users/home.html', ctx)


def register(req):
    if req.method == "POST":
        name = req.POST.get("register-name", "").strip()
        mail = req.POST.get("register-email", "").strip().lower()
        pwd = req.POST.get("register-password", "")
        pwd2 = req.POST.get("register-confirm", "")

        if not all([name, mail, pwd, pwd2]):
            messages.error(req, "Compila tutti i campi.")
            return redirect('/login/?tab=register')

        if pwd != pwd2:
            messages.error(req, "Le password non coincidono.")
            return redirect('/login/?tab=register')

        if User.objects.filter(email__iexact=mail).exists():
            messages.error(req, "Utente già esistente con questa email.")
            return redirect('/login/?tab=register')

        pwd_err = User.validate_password(pwd)
        if pwd_err:
            for err in pwd_err:
                messages.error(req, err)
            return redirect('/login/?tab=register')
        try:
            user = User.objects.create_user(email=mail, password=pwd, full_name=name)
            messages.success(req, "Registrazione completata!")
            return redirect("login")
        except Exception as e:
            messages.error(req, "Errore durante la registrazione.")
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

@login_required
@user_passes_test(lambda u: u.is_staff)
def gest_prenotazioni(request):
    gym_bookings = GymBooking.objects.select_related('user', 'class_id').all()
    spa_bookings = SpaBooking.objects.select_related('user', 'service_id').all()

    gym_count = gym_bookings.count()
    spa_count = spa_bookings.count()

    all_bookings = []

    for booking in gym_bookings:
        all_bookings.append({
            'id': booking.id,
            'user': f"{booking.user.full_name}",
            'service': f"{booking.class_id.name} (Palestra)",
            'description': booking.description if booking.description else booking.class_id.description,
            'date': booking.class_id.scheduled,
            'status': 'confirmed',
            'type': 'gym'
        })

    for booking in spa_bookings:
        all_bookings.append({
            'id': booking.id,
            'user': f"{booking.user.full_name}",
            'service': f"{booking.service_id.name} (Spa)",
            'description': booking.description if booking.description else booking.service_id.description,
            'date': booking.service_id.scheduled,
            'status': 'confirmed',
            'type': 'spa'
        })

    all_bookings.sort(key=lambda x: x['date'])

    gym_bookings_data = []
    for booking in gym_bookings:
        gym_bookings_data.append({
            'id': booking.id,
            'user': f"{booking.user.full_name}",
            'course': booking.class_id.name,
            'description': booking.description if booking.description else booking.class_id.description,
            'date': booking.class_id.scheduled,
            'status': 'confirmed',
        })

    spa_bookings_data = []
    for booking in spa_bookings:
        spa_bookings_data.append({
            'id': booking.id,
            'user': f"{booking.user.full_name}",
            'treatment': booking.service_id.name,
            'description': booking.description if booking.description else booking.service_id.description,
            'date': booking.service_id.scheduled,
            'status': 'confirmed',
        })

    ctx = {
        'total_gym_bookings': gym_count,
        'total_spa_bookings': spa_count,
        'all_bookings': all_bookings,
        'gym_bookings': gym_bookings_data,
        'spa_bookings': spa_bookings_data,
        'timestamp': datetime.now().timestamp(),
    }

    return render(request, 'users/gest_prenotazioni.html', ctx)

@login_required
@require_http_methods(["POST"])
def book_gym_class(request, class_id):
    try:
        gym_class = GymClass.objects.get(id=class_id)

        if not gym_class.check_availability():
            return JsonResponse({'success': False, 'error': 'Classe esaurita. Non ci sono posti disponibili.'})

        data = json.loads(request.body)
        date_time_str = data.get('date_time')

        if not date_time_str:
            return JsonResponse({'success': False, 'error': 'Data/ora mancante.'})

        try:
            date_time = parser.isoparse(date_time_str)
            if timezone.is_naive(date_time):
                date_time = timezone.make_aware(date_time)
        except ValueError:
            return JsonResponse({'success': False, 'error': 'Formato data/ora non valido.'})

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

        if not spa_service.check_availability():
            return JsonResponse({'success': False, 'error': 'Servizio non disponibile al momento.'})

        data = json.loads(request.body)
        date_time_str = data.get('date_time')

        if not date_time_str:
            return JsonResponse({'success': False, 'error': 'Data/ora mancante.'})

        try:
            date_time = parser.isoparse(date_time_str)
            if timezone.is_naive(date_time):
                date_time = timezone.make_aware(date_time)
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
    active_subscription = request.user.subscription_set.filter(is_active=True).first()

    ctx = {
        'gym_bookings': gym_bookings,
        'spa_bookings': spa_bookings,
        'active_subscription': active_subscription,
    }

    return render(request, 'users/my_bookings.html', ctx)

@login_required
@user_passes_test(lambda u: u.is_superuser)
@require_http_methods(["DELETE"])
def delete_course(request, type, id):
    try:
        if type == 'gym':
            course = GymClass.objects.get(id=id)
        elif type == 'spa':
            course = SpaService.objects.get(id=id)
        else:
            return JsonResponse({'error': 'Il tipo di corso non è valido (gym o spa)'}, status=400)
        try:
            course.delete()
            return JsonResponse({'message': 'Corso eliminato con successo'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    except (GymClass.DoesNotExist, SpaService.DoesNotExist):
        return JsonResponse({'error': 'Corso non trovato'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@user_passes_test(lambda u: u.is_superuser)
@require_http_methods(["POST"])
def admin_delete_booking(request):
    """
    Permette all'admin di eliminare una prenotazione (gym o spa).
    """
    booking_id = request.POST.get('booking_id')
    booking_type = request.POST.get('type')
    if not booking_id or not booking_type:
        return JsonResponse({'success': False, 'error': 'Dati mancanti.'}, status=400)
    try:
        if booking_type == 'gym':
            booking = GymBooking.objects.get(id=booking_id)
        elif booking_type == 'spa':
            booking = SpaBooking.objects.get(id=booking_id)
        else:
            return JsonResponse({'success': False, 'error': 'Tipo non valido.'}, status=400)
        booking.delete()
        return JsonResponse({'success': True})
    except (GymBooking.DoesNotExist, SpaBooking.DoesNotExist):
        return JsonResponse({'success': False, 'error': 'Prenotazione non trovata.'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
@require_http_methods(["POST"])
def cancel_gym_booking(request, booking_id):
    success, message = request.user.cancel_booking(GymBooking, booking_id)
    if success:
        return JsonResponse({'success': True, 'message': message})
    else:
        status_code = 404 if message == 'Prenotazione non trovata' else 500
        return JsonResponse({'success': False, 'error': message}, status=status_code)

@login_required
@require_http_methods(["POST"])
def cancel_spa_booking(request, booking_id):
    success, message = request.user.cancel_booking(SpaBooking, booking_id)
    if success:
        return JsonResponse({'success': True, 'message': message})
    else:
        status_code = 404 if message == 'Prenotazione non trovata' else 500
        return JsonResponse({'success': False, 'error': message}, status=status_code)

@login_required
@user_passes_test(lambda u: u.is_superuser)
@require_http_methods(["POST"])
def add_course(request):
    """Aggiunge un nuovo corso palestra o servizio spa (solo admin, solo POST)."""
    try:
        course_type = request.POST.get('type')
        name = request.POST.get('name')
        description = request.POST.get('description')
        duration = request.POST.get('duration')
        instructor_id = request.POST.get('instructor')
        image = request.FILES.get('image')
        max_partecipants = request.POST.get('max_partecipants')
        scheduled = request.POST.get('scheduled')

        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if not all([course_type, name, description, duration, instructor_id, image, scheduled]):
            if is_ajax:
                return JsonResponse({
                    'success': False,
                    'error': "Tutti i campi obbligatori devono essere compilati."
                })
            messages.error(request, "Tutti i campi obbligatori devono essere compilati.")
            return redirect('gest-corsi')

        instructor = User.objects.filter(id=instructor_id).first()
        if not instructor:
            if is_ajax:
                return JsonResponse({
                    'success': False,
                    'error': "Istruttore/Operatore non valido."
                })
            messages.error(request, "Istruttore/Operatore non valido.")
            return redirect('gest-corsi')

        try:
            scheduled_dt = timezone.make_aware(datetime.strptime(scheduled, '%Y-%m-%dT%H:%M'))
        except ValueError:
            if is_ajax:
                return JsonResponse({
                    'success': False,
                    'error': "Formato data e ora non valido."
                })
            messages.error(request, "Formato data e ora non valido.")
            return redirect('gest-corsi')

        if course_type == 'gym':
            if not max_partecipants:
                if is_ajax:
                    return JsonResponse({
                        'success': False,
                        'error': "Capacità massima richiesta per i corsi palestra."
                    })
                messages.error(request, "Capacità massima richiesta per i corsi palestra.")
                return redirect('gest-corsi')
            try:
                new_course = GymClass.objects.create(
                    name=name,
                    description=description,
                    duration=duration,
                    instructor=instructor,
                    max_partecipants=max_partecipants,
                    imgs=image,
                    scheduled=scheduled_dt
                )
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'error': "Errore durante la creazione del corso."
                })

            if is_ajax:
                return JsonResponse({
                    'success': True,
                    'message': f"Corso palestra '{name}' aggiunto con successo.",
                    'course': {
                        'id': new_course.id,
                        'name': new_course.name,
                        'description': new_course.description,
                        'duration': new_course.duration,
                        'instructor': instructor.full_name if instructor else '',
                        'instructor_id': instructor.id if instructor else '',
                        'max_partecipants': new_course.max_partecipants,
                        'scheduled': new_course.scheduled.strftime('%Y-%m-%dT%H:%M'),
                        'type': 'gym',
                        'status': 'active',
                        'image_url': new_course.imgs.url if new_course.imgs else '',
                    }
                })
            messages.success(request, f"Corso palestra '{name}' aggiunto con successo.")

        elif course_type == 'spa':
            price = request.POST.get('price')
            spa_type = request.POST.get('spa_type')
            if not price:
                if is_ajax:
                    return JsonResponse({
                        'success': False,
                        'error': "Prezzo richiesto per i servizi spa."
                    })
                messages.error(request, "Prezzo richiesto per i servizi spa.")
                return redirect('gest-corsi')

            new_service = SpaService.objects.create(
                name=name,
                description=description,
                operator=instructor,
                duration=duration,
                price=price,
                imgs=image,
                max_partecipants=max_partecipants if max_partecipants else 1,
                scheduled=scheduled_dt,
                type=spa_type or 'massage'
            )
            if is_ajax:
                return JsonResponse({
                    'success': True,
                    'message': f"Servizio spa '{name}' aggiunto con successo.",
                    'service': {
                        'id': new_service.id,
                        'name': new_service.name,
                        'description': new_service.description,
                        'duration': new_service.duration,
                        'operator': instructor.full_name if instructor else '',
                        'operator_id': instructor.id if instructor else '',
                        'price': new_service.price,
                        'scheduled': new_service.scheduled.strftime('%Y-%m-%dT%H:%M'),
                        'type': spa_type or '',
                        'status': 'active',
                        'image_url': new_service.imgs.url if new_service.imgs else '',
                    }
                })
            messages.success(request, f"Servizio spa '{name}' aggiunto con successo.")

        else:
            if is_ajax:
                return JsonResponse({
                    'success': False,
                    'error': "Tipo corso/servizio non valido."
                })
            messages.error(request, "Tipo corso/servizio non valido.")
            return redirect('gest-corsi')

        if not is_ajax:
            return redirect('gest-corsi')
        return JsonResponse({'success': True})

    except Exception as e:
        if is_ajax:
            return JsonResponse({
                'success': False,
                'error': f"Errore durante l'aggiunta: {str(e)}"
            })
        messages.error(request, f"Errore durante l'aggiunta: {str(e)}")
        return redirect('gest-corsi')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def course_details(request, type, id):
    """Visualizza i dettagli di un corso palestra o servizio spa."""
    try:
        if type == 'gym':
            course = get_object_or_404(GymClass, id=id)
            template = 'gym_course_details.html'
        elif type == 'spa':
            course = get_object_or_404(SpaService, id=id)
            template = 'spa_service_details.html'
        else:
            messages.error(request, "Tipo di corso non valido")
            return redirect('gest-corsi')

        return render(request, template, {'course': course})
    except Exception as e:
        messages.error(request, f"Errore nel caricamento dei dettagli: {str(e)}")
        return redirect('gest-corsi')

@login_required
@user_passes_test(lambda u: u.is_superuser)
@require_http_methods(["POST"])
def edit_course(request, type, id):
    """Modifica un corso palestra o servizio spa esistente."""
    try:
        if type == 'gym':
            course = get_object_or_404(GymClass, id=id)
        elif type == 'spa':
            course = get_object_or_404(SpaService, id=id)
        else:
            return JsonResponse({'error': 'Tipo non valido'}, status=400)

        name = request.POST.get('name')
        description = request.POST.get('description')
        duration = request.POST.get('duration')
        instructor_id = request.POST.get('instructor')
        scheduled = request.POST.get('scheduled')
        image = request.FILES.get('image')

        if not all([name, description, duration, instructor_id, scheduled]):
            return JsonResponse({
                'success': False,
                'error': "Tutti i campi obbligatori devono essere compilati."
            })

        instructor = User.objects.filter(id=instructor_id).first()
        if not instructor:
            return JsonResponse({
                'success': False,
                'error': "Istruttore/Operatore non valido."
            })

        try:
            scheduled_dt = timezone.make_aware(datetime.strptime(scheduled, '%Y-%m-%dT%H:%M'))
        except ValueError:
            return JsonResponse({
                'success': False,
                'error': "Formato data e ora non valido."
            })

        course.name = name
        course.description = description
        course.duration = duration
        course.scheduled = scheduled_dt
        if image:
            course.imgs = image

        if type == 'gym':
            max_partecipants = request.POST.get('max_partecipants')
            if not max_partecipants:
                return JsonResponse({
                    'success': False,
                    'error': "Capacità massima richiesta per i corsi palestra."
                })
            course.max_partecipants = max_partecipants
            course.instructor = instructor
        else:
            price = request.POST.get('price')
            if not price:
                return JsonResponse({
                    'success': False,
                    'error': "Prezzo richiesto per i servizi spa."
                })
            course.price = price
            course.operator = instructor
            course.type = request.POST.get('spa_type') or 'massage'

        course.save()

        return JsonResponse({
            'success': True,
            'message': f"{'Corso' if type == 'gym' else 'Servizio'} modificato con successo.",
            'course': {
                'id': course.id,
                'name': course.name,
                'description': course.description,
                'duration': course.duration,
                'instructor': instructor.full_name if instructor else '',
                'instructor_id': instructor.id if instructor else '',
                'scheduled': course.scheduled.strftime('%Y-%m-%dT%H:%M'),
                'status': 'active',
                'image_url': course.imgs.url if course.imgs else '',
                'type': type,
                **({'max_partecipants': course.max_partecipants} if type == 'gym' else {'price': course.price})
            }
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f"Errore durante la modifica: {str(e)}"
        })    