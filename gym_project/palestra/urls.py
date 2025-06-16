from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:class_id>/', views.book_gym_class, name='book-gym-class'),
    path('cancel/<int:booking_id>/', views.cancel_gym_booking, name='cancel-gym-booking'),
]
