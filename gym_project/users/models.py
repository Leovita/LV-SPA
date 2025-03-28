from django.contrib.auth.models import AbstractUser
from django.db import models
from subscriptions.models import SubscriptionPlan

class User(AbstractUser):
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    img = models.CharField(max_length=255, blank=True, help_text="URL dell'immagine del profilo")
    subscription = models.CharField(max_length=100, blank=True)

    def edit_profile(self):
        self.save()

    def show_history(self):
        from palestra.models import GymBooking
        from spa.models import SpaBooking
        return GymBooking.objects.filter(user_id=self.user_id).union(
            SpaBooking.objects.filter(user_id=self.user_id)
        ).order_by('-date')

    def __str__(self):
        return self.username
