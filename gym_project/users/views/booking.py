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