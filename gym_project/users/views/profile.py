from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from users.models import ProfileUpdateForm, ProfilePictureForm
import logging

logger = logging.getLogger(__name__)

@login_required
def profile_view(request):
    """
    Visualizza la pagina del profilo utente.
    """
    return redirect('profile')

@login_required
def update_profile(request):
    """
    Gestisce l'aggiornamento dei dati personali dell'utente con validazione.
    """
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
    """
    Gestisce l'aggiornamento dell'immagine del profilo.
    """
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
    """
    Mostra una pagina di conferma per l'eliminazione dell'account.
    Esegue l'eliminazione solo dopo la conferma (POST).
    """
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, 'Il tuo account è stato eliminato con successo.')
        return redirect('home')
    return redirect('profile') 