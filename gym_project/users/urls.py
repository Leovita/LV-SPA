from django.urls import path
# from . import views # Questa riga non è necessaria se importi le viste specifiche

from .views.admin import edit_booking, admin_delete_booking, booking_details, gest_prenotazioni
from .views.booking import book_gym_class, book_spa_service, my_bookings, cancel_gym_booking, cancel_spa_booking
from .views.courses import gest_corsi, add_course, edit_course, delete_course, course_details
from .views.auth import login, register, user_logout, change_password_view
from .views.home import home # Corretto: home è in home.py
from .views.profile import profile_view, update_profile, update_profile_picture, delete_account

urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('logout/', user_logout, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('profile/update/', update_profile, name='update_profile'),
    path('profile/update-picture/', update_profile_picture, name='update_profile_picture'),
    path('profile/delete/', delete_account, name='delete_account'),
    path('profile/change-password/', change_password_view, name='change_password'),
    path('gest-corsi/', gest_corsi, name='gest_corsi'),
    path('gest-corsi/add/', add_course, name='add_course'),
    path('gest-corsi/edit/<str:type>/<int:id>/', edit_course, name='edit_course'),
    path('gest-corsi/delete/<str:type>/<int:id>/', delete_course, name='delete_course'),
    path('course-details/<str:type>/<int:id>/', course_details, name='course_details'),
    path('gest-prenotazioni/', gest_prenotazioni, name='gest_prenotazioni'),
    path('gest-prenotazioni/delete/', admin_delete_booking, name='admin_delete_booking'),
    path('booking-details/<str:type>/<int:id>/', booking_details, name='booking_details'),
    path('gest-prenotazioni/edit/<str:type>/<int:id>/', edit_booking, name='edit_booking'),
    path('book/gym/<int:class_id>/', book_gym_class, name='book_gym_class'),
    path('book/spa/<int:service_id>/', book_spa_service, name='book_spa_service'),
    path('my-bookings/', my_bookings, name='my_bookings'),
    path('my-bookings/cancel/gym/<int:booking_id>/', cancel_gym_booking, name='cancel_gym_booking'),
    path('my-bookings/cancel/spa/<int:booking_id>/', cancel_spa_booking, name='cancel_spa_booking'),
]
