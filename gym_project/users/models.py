from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from subscriptions.models import SubscriptionPlan

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
        return self.create_user(email, password, **xtra_F)

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)  
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    img = models.CharField(max_length=255, blank=True, help_text="URL dell'immagine del profilo")
    subscription = models.CharField(max_length=100, blank=True)
    
    USERNAME_FIELD = 'email' 

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) 
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    def edit_profile(self):
        self.save()

    def show_history(self):
        from palestra.models import GymBooking
        from spa.models import SpaBooking
        return GymBooking.objects.filter(user_id=self.user_id).union(
            SpaBooking.objects.filter(user_id=self.user_id)
        ).order_by('-date')

    def __str__(self):
        return self.email 
