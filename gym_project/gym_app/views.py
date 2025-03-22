# gym_app/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, SubscriptionPlan, GymClass, GymBooking, SpaService, SpaBooking
from .forms import (
    UserRegistrationForm, UserLoginForm, UserProfileForm, 
    GymClassForm, GymBookingForm, SpaServiceForm, SpaBookingForm
)

# Viste per l'utente
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registrazione avvenuta con successo!')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'gym_app/user/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login effettuato con successo!')
                return redirect('home')
            else:
                messages.error(request, 'Username o password non validi')
    else:
        form = UserLoginForm()
    return render(request, 'gym_app/user/login.html', {'form': form})

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profilo aggiornato con successo!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'gym_app/user/profile.html', {'form': form})

@login_required
def history_view(request):
    history = request.user.show_history()
    return render(request, 'gym_app/user/history.html', {'history': history})

# Viste per le classi della palestra
def gym_class_list(request):
    classes = GymClass.objects.filter(date__gte=timezone.now()).order_by('date')
    return render(request, 'gym_app/gym_class/class_list.html', {'classes': classes})

def gym_class_detail(request, class_id):
    gym_class = get_object_or_404(GymClass, class_id=class_id)
    return render(request, 'gym_app/gym_class/class_detail.html', {'gym_class': gym_class})

@login_required
def add_gym_class(request):
    if request.method == 'POST':
        form = GymClassForm(request.POST)
        if form.is_valid():
            gym_class = form.save(commit=False)
            gym_class.add_class()
            messages.success(request, 'Classe aggiunta con successo!')
            return redirect('gym_class_list')
    else:
        form = GymClassForm()
    return render(request, 'gym_app/gym_class/class_form.html', {'form': form})

@login_required
def edit_gym_class(request, class_id):
    gym_class = get_object_or_404(GymClass, class_id=class_id)
    if request.method == 'POST':
        form = GymClassForm(request.POST, instance=gym_class)
        if form.is_valid():
            gym_class = form.save(commit=False)
            gym_class.change_class()
            messages.success(request, 'Classe modificata con successo!')
            return redirect('gym_class_detail', class_id=gym_class.class_id)
    else:
        form = GymClassForm(instance=gym_class)
    return render(request, 'gym_app/gym_class/class_form.html', {'form': form})

@login_required
def delete_gym_class(request, class_id):
    gym_class = get_object_or_404(GymClass, class_id=class_id)
    if request.method == 'POST':
        gym_class.delete_class()
        messages.success(request, 'Classe eliminata con successo!')
        return redirect('gym_class_list')
    return render(request, 'gym_app/gym_class/class_confirm_delete.html', {'gym_class': gym_class})

@login_required
def book_gym_class(request, class_id):
    gym_class = get_object_or_404(GymClass, class_id=class_id)
    if request.method == 'POST':
        form = GymBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.class_id = gym_class
            if booking.book_gym_class():
                messages.success(request, 'Prenotazione effettuata con successo!')
                return redirect('gym_class_list')
            else:
                messages.error(request, 'Impossibile prenotare: classe piena')
    else:
        form = GymBookingForm()
    return render(request, 'gym_app/gym_class/class_booking.html', {'form': form, 'gym_class': gym_class})

@login_required
def delete_gym_booking(request, booking_id):
    booking = get_object_or_404(GymBooking, id=booking_id, user=request.user)
    if request.method == 'POST':
        booking.delete_gym_booking()
        messages.success(request, 'Prenotazione eliminata con successo!')
        return redirect('history')
    return render(request, 'gym_app/gym_class/booking_confirm_delete.html', {'booking': booking})

# Viste per i servizi spa
def spa_service_list(request):
    services = SpaService.objects.all()
    return render(request, 'gym_app/spa/service_list.html', {'services': services})

def spa_service_detail(request, service_id):
    service = get_object_or_404(SpaService, service_id=service_id)
    return render(request, 'gym_app/spa/service_detail.html', {'service': service})

@login_required
def add_spa_service(request):
    if request.method == 'POST':
        form = SpaServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.add_service()
            messages.success(request, 'Servizio spa aggiunto con successo!')
            return redirect('spa_service_list')
    else:
        form = SpaServiceForm()
    return render(request, 'gym_app/spa/service_form.html', {'form': form})

@login_required
def edit_spa_service(request, service_id):
    service = get_object_or_404(SpaService, service_id=service_id)
    if request.method == 'POST':
        form = SpaServiceForm(request.POST, instance=service)
        if form.is_valid():
            service = form.save(commit=False)
            service.change_service()
            messages.success(request, 'Servizio spa modificato con successo!')
            return redirect('spa_service_detail', service_id=service.service_id)
    else:
        form = SpaServiceForm(instance=service)
    return render(request, 'gym_app/spa/service_form.html', {'form': form})

@login_required
def delete_spa_service(request, service_id):
    service = get_object_or_404(SpaService, service_id=service_id)
    if request.method == 'POST':
        service.delete_service()
        messages.success(request, 'Servizio spa eliminato con successo!')
        return redirect('spa_service_list')
    return render(request, 'gym_app/spa/service_confirm_delete.html', {'service': service})

@login_required
def book_spa_service(request, service_id):
    service = get_object_or_404(SpaService, service_id=service_id)
    if request.method == 'POST':
        form = SpaBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.service_id = service
            if booking.book_spa_service():
                messages.success(request, 'Prenotazione servizio spa effettuata con successo!')
                return redirect('spa_service_list')
            else:
                messages.error(request, 'Impossibile prenotare: servizio completo')
    else:
        form = SpaBookingForm()
    return render(request, 'gym_app/spa/service_booking.html', {'form': form, 'service': service})

@login_required
def delete_spa_booking(request, booking_id):
    booking = get_object_or_404(SpaBooking, id=booking_id, user=request.user)
    if request.method == 'POST':
        booking.delete_spa_booking()
        messages.success(request, 'Prenotazione servizio spa eliminata con successo!')
        return redirect('history')
    return render(request, 'gym_app/spa/booking_confirm_delete.html', {'booking': booking})

# Home page
def home(request):
    upcoming_classes = GymClass.objects.filter(date__gte=timezone.now()).order_by('date')[:5]
    spa_services = SpaService.objects.all()[:5]
    context = {
        'upcoming_classes': upcoming_classes,
        'spa_services': spa_services,
    }
    return render(request, 'gym_app/home.html', context)