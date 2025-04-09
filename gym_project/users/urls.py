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
    # piano abbonamento attivo
    path('subscription-plans/', views.subscription_plans, name='subscription_plans'),
    path('subscribe/<int:plan_id>/', views.subscribe_plan, name='subscribe_plan'),


    # path('profile/change-password/', views.change_password_view, name='change_password'),
    path('profile/delete_account/', views.delete_account, name='delete_account'),
    
    path('login/', views.login, name='login'), 
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)