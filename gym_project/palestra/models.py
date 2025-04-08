from django.db import models
from django.urls import reverse
from users.models import User
from django.utils import timezone

class GymClass(models.Model):
    name = models.CharField(max_length=100, default="Marco Ros")
    description = models.TextField()
    scheduled = models.DateTimeField(default=timezone.now)
    instructor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='instructor_classes')
    max_partecipants = models.IntegerField()
    imgs = models.ImageField(upload_to='palestra/', blank=True, null=True, help_text="Carica un'immagine del corso")

    def check_participants(self):
        return GymBooking.objects.filter(class_id=self.id).count()

    def check_availability(self):
        current_participants = self.check_participants()
        return current_participants < self.max_partecipants

    def __str__(self):
        return f"{self.name} - {self.scheduled.strftime('%d/%m/%Y %H:%M')}"

    def get_absolute_url(self):
        return reverse('all_services_view', args=[str(self.id)])
    
class GymBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class_id = models.ForeignKey(GymClass, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.class_id.name}"
