from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:service_id>/', views.book_spa_service, name='book-spa-service'),
    path('cancel/<int:booking_id>/', views.cancel_spa_booking, name='cancel-spa-booking'),
]
