from django.db import models

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    duration = models.IntegerField(help_text="Durata in giorni")
    description = models.TextField()

    def __str__(self):
        return self.name
