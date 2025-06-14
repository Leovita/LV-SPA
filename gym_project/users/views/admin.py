from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from palestra.models import GymBooking, GymClass
from spa.models import SpaBooking, SpaService
from users.views.utils import ajax_error, ajax_ok
from datetime import datetime
from django.utils import timezone
from dateutil import parser
import json

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
            'description': booking.description or booking.class_id.description,
            'date': booking.class_id.scheduled,
            'status': 'confirmed',
            'type': 'gym'
        })

    for booking in spa_bookings:
        all_bookings.append({
            'id': booking.id,
            'user': f"{booking.user.full_name}",
            'service': f"{booking.service_id.name} (Spa)",
            'description': booking.description or booking.service_id.description,
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
            'description': booking.description or booking.class_id.description,
            'date': booking.class_id.scheduled,
            'status': 'confirmed',
        })

    spa_bookings_data = []
    for booking in spa_bookings:
        spa_bookings_data.append({
            'id': booking.id,
            'user': f"{booking.user.full_name}",
            'treatment': booking.service_id.name,
            'description': booking.description or booking.service_id.description,
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
@user_passes_test(lambda u: u.is_staff)
@require_http_methods(["POST"])
def admin_delete_booking(request):
    booking_id = request.POST.get('booking_id')
    booking_type = request.POST.get('type')
    if not booking_id or not booking_type:
        return ajax_error('Dati mancanti.')
    try:
        if booking_type == 'gym':
            booking = GymBooking.objects.get(id=booking_id)
        elif booking_type == 'spa':
            booking = SpaBooking.objects.get(id=booking_id)
        else:
            return ajax_error('Tipo non valido.')
        booking.delete()
        return ajax_ok('Prenotazione eliminata con successo.')
    except (GymBooking.DoesNotExist, SpaBooking.DoesNotExist):
        return ajax_error('Prenotazione non trovata.')
    except Exception as e:
        return ajax_error(str(e))

@login_required
@user_passes_test(lambda u: u.is_staff)
def booking_details(request, type, id):
    try:
        if type == 'gym':
            booking = get_object_or_404(GymBooking.objects.select_related('user', 'class_id'), id=id)
        elif type == 'spa':
            booking = get_object_or_404(SpaBooking.objects.select_related('user', 'service_id'), id=id)
        else:
            messages.error(request, "Tipo di prenotazione non valido.")
            return redirect('gest_prenotazioni')

        return render(request, 'users/booking_details.html', {'booking': booking, 'type': type})
    except Exception as e:
        messages.error(request, f"Errore nel caricamento dei dettagli della prenotazione: {str(e)}")
        return redirect('gest_prenotazioni')

@login_required
@user_passes_test(lambda u: u.is_staff)
@require_http_methods(["GET", "POST"])
def edit_booking(request, type, id):
    if request.method == 'POST':
        datetime_str = request.POST.get('datetime')
        notes = request.POST.get('notes', '')

        # --- LOG DI DEBUG ---
        print(f"[DEBUG BACKEND] datetime_str ricevuto: '{datetime_str}', Tipo: {type}, ID: {id}")
        # --- FINE LOG DI DEBUG ---

        if not all([datetime_str]):
            return ajax_error('Dati mancanti.')

        try:
            try:
                new_datetime = timezone.make_aware(datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M'))
            except ValueError as e:
                return ajax_error(f'Formato data non valido. Usa il formato YYYY-MM-DDTHH:mm. Errore: {str(e)}')

            if type == 'gym':
                booking = GymBooking.objects.get(id=id)
                booking.class_id.scheduled = new_datetime
                booking.class_id.save()
            elif type == 'spa':
                booking = SpaBooking.objects.get(id=id)
                booking.service_id.scheduled = new_datetime
                if notes:
                    booking.description = notes
                booking.service_id.save()
            else:
                return ajax_error('Tipo di prenotazione non valido.')
            
            return ajax_ok('Prenotazione modificata con successo!')
        except (GymBooking.DoesNotExist, SpaBooking.DoesNotExist):
            return ajax_error('Prenotazione non trovata.')
        except Exception as e:
            return ajax_error(f'Errore durante la modifica della prenotazione: {str(e)}')
    
    return ajax_error('Metodo non supportato.') 