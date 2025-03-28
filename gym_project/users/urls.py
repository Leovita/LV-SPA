from django.urls import path
from . import views

urlpatterns = [
    #url specifiche per user
    path('profile/', views.profile, name='profile'),
    path('login/', views.login, name='login'),
]
