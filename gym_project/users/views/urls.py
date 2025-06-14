from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('profile/update-picture/', views.update_profile_picture, name='update_profile_picture'),
    path('profile/delete/', views.delete_account, name='delete_account'),
    path('profile/change-password/', views.change_password_view, name='change_password'),
    path('gest-corsi/', views.gest_corsi, name='gest_corsi'),
    path('gest-corsi/add/', views.add_course, name='add_course'),
    path('gest-corsi/edit/<str:type>/<int:id>/', views.edit_course, name='edit_course'),
    path('gest-corsi/delete/<str:type>/<int:id>/', views.delete_course, name='delete_course'),
    path('gest-corsi/details/<str:type>/<int:id>/', views.course_details, name='course_details'),
    path('gest-prenotazioni/', views.gest_prenotazioni, name='gest_prenotazioni'),
    path('gest-prenotazioni/delete/', views.admin_delete_booking, name='admin_delete_booking'),
    path('gest-prenotazioni/details/<str:type>/<int:id>/', views.booking_details, name='booking_details'),
    path('gest-prenotazioni/edit/<str:type>/<int:id>/', views.edit_booking, name='edit_booking'),
    path('book/gym/<int:class_id>/', views.book_gym_class, name='book_gym_class'),
    path('book/spa/<int:service_id>/', views.book_spa_service, name='book_spa_service'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('my-bookings/cancel/gym/<int:booking_id>/', views.cancel_gym_booking, name='cancel_gym_booking'),
    path('my-bookings/cancel/spa/<int:booking_id>/', views.cancel_spa_booking, name='cancel_spa_booking'),
] 