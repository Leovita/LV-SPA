from django.shortcuts import render
from django.utils import timezone
from dateutil import parser
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
import json
from users.views.utils import ajax_error, ajax_ok
from .models import SpaBooking, SpaService


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

        # Verifica se l'utente ha un abbonamento attivo
        has_subscription = request.user.has_free_spa_access()
        price = spa_service.get_price_for_user(request.user)

        booking = SpaBooking.objects.create(
            user=request.user,
            service_id=spa_service,
            date=date_time,
            description=notes
        )

        message = f'Prenotazione per {spa_service.name} confermata!'
        if not has_subscription:
            message += f' Prezzo: €{price}'

        return ajax_ok(message)

    except SpaService.DoesNotExist:
        return ajax_error('Servizio non trovato.')
    except Exception as e:
        return ajax_error(str(e))

@login_required
@require_http_methods(["POST"])
def cancel_spa_booking(request, booking_id):
    success, message = request.user.cancel_booking(SpaBooking, booking_id)
    if success:
        return ajax_ok(message)
    else:
        return ajax_error(message)
