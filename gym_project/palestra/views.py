from django.shortcuts import render
from palestra.models import GymClass

def all_services_view(request):
    gym_services = GymClass.objects.all()
    print("HOME VIEW CHIAMATA ", gym_services.count())
    return render(request, 'users/home.html', {'gym_services': gym_services})
