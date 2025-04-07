from django.db import models
from users.models import User
from django.utils import timezone

class SpaService(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    operator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='operator_services')
    scheduled = models.DateTimeField(default=timezone.now)
    price = models.IntegerField()
    max_partecipants = models.IntegerField(default=1)
    imgs = models.CharField(max_length=255, blank=True, help_text="URLs delle immagini")

    def check_availability(self):
        return SpaBooking.objects.filter(service_id=self.id).count() < self.max_partecipants

    def __str__(self):
        return self.name

class SpaBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service_id = models.ForeignKey(SpaService, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.service_id.name}"
