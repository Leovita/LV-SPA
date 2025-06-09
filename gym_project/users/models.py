from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import os
from subscriptions.models import SubscriptionPlan
import re

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **xtra_F):
        if not email:
            raise ValueError('L\'email deve essere fornita')
        email = self.normalize_email(email)
        user = self.model(email=email, **xtra_F)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **xtra_F):
        xtra_F.setdefault('is_staff', True)
        xtra_F.setdefault('is_superuser', True)
        xtra_F.setdefault('profile_picture', 'profile_pics/admin_def.jpg')
        return self.create_user(email, password, **xtra_F)

class User(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=255, default="Nome Cognome")
    email = models.EmailField(unique=True)  
    phone = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(
        upload_to="profile_pics/",
        default="profile_pics/def_pfp.png",
        null=True,
        blank=True
    )    
    USERNAME_FIELD = 'email' 

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) 
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    @staticmethod
    def validate_password(pwd):
        RULES = [
            (r'.{,}', "Minimo 8 caratteri."),
            (r'[A-Z]', "Almeno una MAIUSCOLA."),
            (r'[a-z]', "Almeno una minuscola."),
            (r'\d', "Almeno un numero."),
            (r'[!@#$%^&*(),.?\":{}|<>]', "Almeno un simbolo speciale.")
        ]
        return [msg for rgx, msg in RULES if not re.search(rgx, pwd)]

    def edit_profile(self):
        self.validate_password(self.password)
        self.save()

    def show_history(self):
        from palestra.models import GymBooking
        from spa.models import SpaBooking
        return GymBooking.objects.filter(user_id=self.user_id).union(
            SpaBooking.objects.filter(user_id=self.user_id)
        ).order_by('-date')

    def __str__(self):
        return self.email 

    def cancel_booking(self, booking_model, booking_id):
        try:
            booking = booking_model.objects.get(id=booking_id, user=self)
            booking.delete()
            return True, 'Prenotazione annullata con successo'
        except booking_model.DoesNotExist:
            return False, 'Prenotazione non trovata'
        except Exception as e:
            return False, str(e)


class ProfileUpdateForm(forms.ModelForm):
    """
    Form per l'aggiornamento delle informazioni personali dell'utente.
    """
    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone']
        
    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name', '').strip()
        if not re.match(r'^[A-Za-zÀ-ÿ\s]{3,}$', full_name) or len(full_name.split()) < 2:
            raise ValidationError(_("Il nome completo deve contenere almeno nome e cognome (solo lettere)."))
        return full_name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_id = self.instance.id
        
        #s e gia usata
        if email and User.objects.filter(email=email).exclude(id=user_id).exists():
            raise ValidationError(_('Questa email è già in uso da un altro account.'))
            
        return email
        
    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        
        if phone and (not phone.isdigit() or len(phone) != 10):
            raise ValidationError(_("Il numero di telefono deve contenere esattamente 10 cifre numeriche."))
            
        return phone

class ProfilePictureForm(forms.ModelForm):
    """
    Form per l'aggiornamento dell'immagine del profilo.
    """
    class Meta:
        model = User
        fields = ['profile_picture']
        
    def clean_profile_picture(self):
        profile_picture = self.cleaned_data.get('profile_picture')
        
        if profile_picture:
            if profile_picture.size > 5 * 1024 * 1024:
                raise ValidationError(_('La dimensione dell\'immagine non può superare 5MB.'))
                
            valid_extensions = ['jpg', 'jpeg', 'png', 'gif']
            
            ext = os.path.splitext(profile_picture.name)[1][1:].lower()
            if ext not in valid_extensions:
                raise ValidationError(_('Formato file non supportato. Usa JPG, JPEG, PNG o GIF.'))
                
        return profile_picture