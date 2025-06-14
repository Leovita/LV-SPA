from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from users.models import ProfileUpdateForm, ProfilePictureForm
import logging

logger = logging.getLogger(__name__)

@login_required
def profile_view(request):
    return render(request, 'users/profile.html')

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Il tuo profilo è stato aggiornato con successo!')
            return redirect('profile')

        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

    return redirect('profile')

@login_required
def update_profile_picture(request):
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'La tua immagine del profilo è stata aggiornata con successo!')
            return redirect('profile')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

    return redirect('profile')

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, 'Il tuo account è stato eliminato con successo.')
        return redirect('home')
    return render(request, 'users/delete_account.html') 