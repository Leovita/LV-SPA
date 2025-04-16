from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from palestra.views import all_services_view 

urlpatterns = [
    #url specifiche per user
    path('', views.home, name='home'),  
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('profile/update-picture/', views.update_profile_picture, name='update_profile_picture'),

    # path('profile/change-password/', views.change_password_view, name='change_password'),
    path('profile/delete_account/', views.delete_account, name='delete_account'),
    
    # gestione abbonamenti
    path('gest_prenotazioni/', views.gest_prenotazioni, name='gest_prenotazioni'),

    #viste dinamiche servizi
    path('book-gym/<int:class_id>/', views.book_gym_class, name='book_gym'),
    path('book-spa/<int:service_id>/', views.book_spa_service, name='book_spa'),

    #auth
    path('login/', views.login, name='login'), 
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),

    #bookings
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    #cancer
    path('cancel-gym-booking/<int:booking_id>/', views.cancel_gym_booking, name='cancel_gym_booking'),
    path('cancel-spa-booking/<int:booking_id>/', views.cancel_spa_booking, name='cancel_spa_booking'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)