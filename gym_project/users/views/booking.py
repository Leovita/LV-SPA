import json
from django.utils import timezone
from dateutil import parser
from users.views.utils import ajax_error, ajax_ok
from users.models import User
from palestra.models import GymBooking, GymClass
from spa.models import SpaBooking, SpaService
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import render

@login_required
@require_http_methods(["POST"])
def book_gym_class(request, class_id):
    try:
        gym_class = GymClass.objects.get(id=class_id)

        if not gym_class.check_availability():
            return ajax_error('Classe esaurita. Non ci sono posti disponibili.')

        data = json.loads(request.body)
        date_time_str = data.get('date_time')

        if not date_time_str:
            return ajax_error('Data/ora mancante.')

        try:
            date_time = parser.isoparse(date_time_str)
            if timezone.is_naive(date_time):
                date_time = timezone.make_aware(date_time)
        except ValueError:
            return ajax_error('Formato data/ora non valido.')

        booking = GymBooking.objects.create(
            user=request.user,
            class_id=gym_class,
            date=date_time,
        )

        return ajax_ok(f'Prenotazione per {gym_class.name} confermata!')

    except GymClass.DoesNotExist:
        return ajax_error('Classe non trovata.')
    except Exception as e:
        return ajax_error(str(e))

@login_required
@require_http_methods(["POST"])
def book_spa_service(request, service_id):
    try:
        spa_service = SpaService.objects.get(id=service_id)

        if not spa_service.check_availability():
            return ajax_error('Servizio non disponibile al momento.')

        data = json.loads(request.body)
        date_time_str = data.get('date_time')

        if not date_time_str:
            return ajax_error('Data/ora mancante.')

        try:
            date_time = parser.isoparse(date_time_str)
            if timezone.is_naive(date_time):
                date_time = timezone.make_aware(date_time)
        except ValueError:
            return ajax_error('Formato data/ora non valido.')

        notes = data.get('notes', '')

        booking = SpaBooking.objects.create(
            user=request.user,
            service_id=spa_service,
            date=date_time,
            description=notes
        )

        return ajax_ok(f'Prenotazione per {spa_service.name} confermata!')

    except SpaService.DoesNotExist:
        return ajax_error('Servizio non trovato.')
    except Exception as e:
        return ajax_error(str(e))

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
@require_http_methods(["POST"])
def cancel_gym_booking(request, booking_id):
    success, message = request.user.cancel_booking(GymBooking, booking_id)
    if success:
        return ajax_ok(message)
    else:
        return ajax_error(message)

@login_required
@require_http_methods(["POST"])
def cancel_spa_booking(request, booking_id):
    success, message = request.user.cancel_booking(SpaBooking, booking_id)
    if success:
        return ajax_ok(message)
    else:
        return ajax_error(message) 