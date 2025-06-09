from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
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
@user_passes_test(lambda u: u.is_superuser)
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
@user_passes_test(lambda u: u.is_superuser)
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
@user_passes_test(lambda u: u.is_superuser)
@require_http_methods(["GET", "POST"])
def edit_booking(request, type, id):
    try:
        if type == 'gym':
            booking = get_object_or_404(GymBooking.objects.select_related('user', 'class_id'), id=id)
            related_service = booking.class_id
        elif type == 'spa':
            booking = get_object_or_404(SpaBooking.objects.select_related('user', 'service_id'), id=id)
            related_service = booking.service_id
        else:
            return ajax_error("Tipo di prenotazione non valido.")

        if request.method == 'GET':
            booking_data = {
                'id': booking.id,
                'type': type,
                'user_info': f'{booking.user.full_name} ({booking.user.email})',
                'service_info': f'{related_service.name} (ID: {related_service.id})',
                'datetime': booking.date.strftime('%Y-%m-%dT%H:%M'),
                'notes': booking.description if hasattr(booking, 'description') else ''
            }
            return JsonResponse({'success': True, 'booking': booking_data})

        elif request.method == 'POST':
            data = request.POST
            datetime_str = data.get('datetime')
            
            if not datetime_str:
                return ajax_error('Data e ora sono obbligatorie.')
            
            try:
                try:
                    new_datetime = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M')
                    new_datetime = timezone.make_aware(new_datetime)
                except ValueError:
                    new_datetime = parser.isoparse(datetime_str)
                    if timezone.is_naive(new_datetime):
                        new_datetime = timezone.make_aware(new_datetime)
            except Exception as e:
                return ajax_error('Formato data e ora non valido. Assicurati di selezionare una data valida.')

            booking.date = new_datetime
            if hasattr(booking, 'description'):
                booking.description = data.get('notes', '')
            
            booking.save()
            return ajax_ok(f'Prenotazione #{booking.id} aggiornata con successo.')

    except (GymBooking.DoesNotExist, SpaBooking.DoesNotExist):
        return ajax_error('Prenotazione non trovata.')
    except Exception as e:
        return ajax_error(f'Errore durante la modifica della prenotazione: {str(e)}') 