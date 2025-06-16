from django.shortcuts import render
from palestra.models import GymClass
import json
from django.utils import timezone
from dateutil import parser
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from users.views.utils import ajax_error, ajax_ok
from .models import GymBooking

@login_required
@require_http_methods(["POST"])
def book_gym_class(request, class_id):
    try:
        if not request.user.has_free_spa_access():
            return ajax_error('È necessario un abbonamento attivo per prenotare i corsi della palestra.')

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
def cancel_gym_booking(request, booking_id):
    success, message = request.user.cancel_booking(GymBooking, booking_id)
    if success:
        return ajax_ok(message)
    else:
        return ajax_error(message)
