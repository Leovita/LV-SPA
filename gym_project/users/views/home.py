from django.shortcuts import render
from palestra.models import GymClass, GymBooking
from spa.models import SpaService, SpaBooking
from datetime import datetime

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