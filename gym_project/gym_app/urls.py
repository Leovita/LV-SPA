# gym_app/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    
    #auth
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    
    #user
    path('profile/', views.profile_view, name='profile'), 
    path('history/', views.history_view, name='history'),
    
    #gym
    path('classes/', views.gym_class_list, name='gym_class_list'),
    path('classes/<int:class_id>/', views.gym_class_detail, name='gym_class_detail'),
    path('classes/add/', views.add_gym_class, name='add_gym_class'),
    path('classes/<int:class_id>/edit/', views.edit_gym_class, name='edit_gym_class'),
    path('classes/<int:class_id>/delete/', views.delete_gym_class, name='delete_gym_class'),
    path('classes/<int:class_id>/book/', views.book_gym_class, name='book_gym_class'),
    path('bookings/<int:booking_id>/delete/', views.delete_gym_booking, name='delete_gym_booking'),
    
    #spa
    path('spa/', views.spa_service_list, name='spa_service_list'),
    path('spa/<int:service_id>/', views.spa_service_detail, name='spa_service_detail'),
    path('spa/add/', views.add_spa_service, name='add_spa_service'),
    path('spa/<int:service_id>/edit/', views.edit_spa_service, name='edit_spa_service'),
    path('spa/<int:service_id>/delete/', views.delete_spa_service, name='delete_spa_service'),
    path('spa/<int:service_id>/book/', views.book_spa_service, name='book_spa_service'),
    path('spa-bookings/<int:booking_id>/delete/', views.delete_spa_booking, name='delete_spa_booking'),
]