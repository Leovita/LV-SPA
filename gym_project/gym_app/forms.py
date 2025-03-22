# gym_app/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, SubscriptionPlan, GymClass, GymBooking, SpaService, SpaBooking

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password1', 'password2']

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'img']

class SubscriptionPlanForm(forms.ModelForm):
    class Meta:
        model = SubscriptionPlan
        fields = ['name', 'price', 'duration', 'description']

class GymClassForm(forms.ModelForm):
    class Meta:
        model = GymClass
        fields = ['name', 'description', 'instructor', 'date', 'max_partecipants', 'imgs']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class GymBookingForm(forms.ModelForm):
    class Meta:
        model = GymBooking
        fields = ['description']

class SpaServiceForm(forms.ModelForm):
    class Meta:
        model = SpaService
        fields = ['name', 'description', 'operator', 'service_len', 'price', 'max_partecipants', 'imgs']

class SpaBookingForm(forms.ModelForm):
    class Meta:
        model = SpaBooking
        fields = ['description', 'schedule', 'max_partecipants']
        widgets = {
            'schedule': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }