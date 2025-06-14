from datetime import timedelta
from django.db import models
from django.utils import timezone
from dateutil.relativedelta import relativedelta

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    duration = models.IntegerField(help_text="Durata in mesi")
    description = models.TextField()

    def __str__(self):
        return self.name

class Subscription(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    plan = models.ForeignKey('subscriptions.SubscriptionPlan', on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.plan:
            if not self.start_date:
                self.start_date = timezone.now()
            if not self.end_date:
                self.end_date = self.start_date + relativedelta(months=self.plan.duration)
        if self.end_date and self.end_date < timezone.now():
            self.is_active = False  
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.email} - {self.plan.name}"
