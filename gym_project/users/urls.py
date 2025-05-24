from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from palestra.models import GymClass
from spa.models import SpaService

urlpatterns = [
    path('', views.home, name='home'),  
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('profile/update-picture/', views.update_profile_picture, name='update_profile_picture'),
    path('profile/change-password/', views.change_password_view, name='change_password'),
    path('profile/delete-account/', views.delete_account, name='delete_account'),
    path('gest-prenotazioni/', views.gest_prenotazioni, name='gest_prenotazioni'),
    path('book-gym/<int:class_id>/', views.book_gym_class, name='book_gym'),
    path('book-spa/<int:service_id>/', views.book_spa_service, name='book_spa'),
    path('login/', views.login, name='login'), 
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('gest-corsi/', views.gest_corsi, name='gest_corsi'),
    path('cancel-gym-booking/<int:booking_id>/', views.cancel_gym_booking, name='cancel_gym_booking'),
    path('cancel-spa-booking/<int:booking_id>/', views.cancel_spa_booking, name='cancel_spa_booking'),
    path('admin-delete-booking/', views.admin_delete_booking, name='admin_delete_booking'),
    path('delete-course/<str:type>/<int:id>/', views.delete_course, name='delete_course'),
    path('add-course/', views.add_course, name='add_course'),
    path('course-details/<str:type>/<int:id>/', views.course_details, name='course_details'),
    path('edit-course/<str:type>/<int:id>/', views.edit_course, name='edit_course'),
    path('booking-details/<str:type>/<int:id>/', views.booking_details, name='booking_details'),
    path('edit-booking/<str:type>/<int:id>/', views.edit_booking, name='edit_booking'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
