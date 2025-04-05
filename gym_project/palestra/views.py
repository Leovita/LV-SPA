from django.shortcuts import render, get_object_or_404
from .models import GymClass

def gym_class_detail_view(request, id):
    gym_class = get_object_or_404(GymClass, id=id)
    return render(request, 'palestra/gym_class_detail.html', {'gym_class': gym_class})
