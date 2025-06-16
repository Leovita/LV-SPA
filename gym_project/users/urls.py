from django.urls import path
# from . import views # Questa riga non è necessaria se importi le viste specifiche

from .views.booking import my_bookings
from .views.auth import profile, login, register, user_logout, change_password_view
from .views.profile import profile_view, update_profile, update_profile_picture, delete_account
from .views.courses import gest_corsi, delete_course, add_course, course_details, edit_course
from .views.admin import gest_prenotazioni, admin_delete_booking, booking_details, edit_booking
from .views.home import home

urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('logout/', user_logout, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('profile/update/', update_profile, name='update-profile'),
    path('profile/update-picture/', update_profile_picture, name='update-profile-picture'),
    path('profile/delete/', delete_account, name='delete-account'),
    path('profile/change-password/', change_password_view, name='change-password'),
    path('gest-corsi/', gest_corsi, name='gest-corsi'),
    path('gest-corsi/add/', add_course, name='add-course'),
    path('gest-corsi/edit/<str:type>/<int:id>/', edit_course, name='edit-course'),
    path('gest-corsi/delete/<str:type>/<int:id>/', delete_course, name='delete-course'),
    path('course-details/<str:type>/<int:id>/', course_details, name='course-details'),
    path('gest-prenotazioni/', gest_prenotazioni, name='gest-prenotazioni'),
    path('gest-prenotazioni/delete/', admin_delete_booking, name='admin-delete-booking'),
    path('booking-details/<str:type>/<int:id>/', booking_details, name='booking-details'),
    path('gest-prenotazioni/edit/<str:type>/<int:id>/', edit_booking, name='edit-booking'),
    path('my-bookings/', my_bookings, name='my-bookings'),
]
