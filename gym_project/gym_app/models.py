# gym_app/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class SubscriptionPlan(models.Model):
    plan_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.FloatField()
    duration = models.IntegerField(help_text="Duration in days")
    description = models.TextField()
    
    def book_gym_class(self):
        # Logica per prenotare una classe in palestra
        pass

    def delete_gym_booking(self):
        # Logica per eliminare una prenotazione di palestra
        pass

    def show_booking_details(self):
        # Logica per mostrare i dettagli della prenotazione
        pass

    def __str__(self):
        return self.name

class User(AbstractUser):
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    img = models.CharField(max_length=255, blank=True, help_text="URL dell'immagine del profilo")
    subscription = models.CharField(max_length=100, blank=True)

    def register(self):
        # Logica per registrarsi (già gestita da Django Auth)
        self.save()

    def login(self):
        # Logica per il login (già gestita da Django Auth)
        pass

    def edit_profile(self):
        # Logica per modificare il profilo
        self.save()

    def show_history(self):
        # Logica per mostrare la cronologia dell'utente
        return GymBooking.objects.filter(user_id=self.user_id).union(
            SpaBooking.objects.filter(user_id=self.user_id)
        ).order_by('-date')

    def __str__(self):
        return self.username

class GymClass(models.Model):
    class_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    instructor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='instructor_classes')
    date = models.DateTimeField()
    max_partecipants = models.IntegerField()
    imgs = models.CharField(max_length=255, blank=True, help_text="URLs delle immagini separate da virgola")

    def add_class(self):
        # Logica per aggiungere una classe
        self.save()

    def change_class(self):
        # Logica per modificare una classe
        self.save()

    def delete_class(self):
        # Logica per eliminare una classe
        self.delete()

    def check_participants(self):
        # Logica per controllare i partecipanti
        return GymBooking.objects.filter(class_id=self.class_id).count()

    def check_availability(self):
        current_participants = self.check_participants()
        return current_participants < self.max_partecipants

    def __str__(self):
        return f"{self.name} - {self.date.strftime('%d/%m/%Y %H:%M')}"

class GymBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class_id = models.ForeignKey(GymClass, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    date = models.DateTimeField(default=timezone.now)

    def book_gym_class(self):
        # Logica per prenotare una classe
        if self.class_id.check_availability():
            self.save()
            return True
        return False

    def delete_gym_booking(self):
        self.delete()
    
    def show_booking_details(self):
        return {
            'user': self.user.username,
            'class': self.class_id.name,
            'date': self.class_id.date,
            'description': self.description
        }

    def __str__(self):
        return f"{self.user.username} - {self.class_id.name}"

class SpaService(models.Model):
    service_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    operator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='operator_services')
    service_len = models.IntegerField(help_text="Durata del servizio in minuti")
    price = models.IntegerField()
    max_partecipants = models.IntegerField(default=1)
    imgs = models.CharField(max_length=255, blank=True, help_text="URLs delle immagini separate da virgola")

    def add_service(self):
        self.save()

    def change_service(self):
        self.save()

    def delete_service(self):
        self.delete()

    def check_availability(self):
        # Controlla se ci sono ancora posti disponibili
        return SpaBooking.objects.filter(service_id=self.service_id).count() < self.max_partecipants

    def show_spa_partecipants(self):
        # Mostra i partecipanti al servizio spa
        return SpaBooking.objects.filter(service_id=self.service_id)

    def __str__(self):
        return self.name

class SpaBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    service_id = models.ForeignKey(SpaService, on_delete=models.CASCADE)
    schedule = models.DateTimeField()
    max_partecipants = models.IntegerField(default=1)

    def book_spa_service(self):
        if self.service_id.check_availability():
            self.save()
            return True
        return False

    def delete_spa_booking(self):
        # Logica per eliminare una prenotazione spa
        self.delete()

    def show_booking_details(self):
        # Logica per mostrare i dettagli della prenotazione
        return {
            'user': self.user.username,
            'service': self.service_id.name,
            'schedule': self.schedule,
            'description': self.description
        }

    def __str__(self):
        return f"{self.user.username} - {self.service_id.name}"