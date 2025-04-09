from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from palestra.views import all_services_view

urlpatterns = [
    # piano abbonamento attivo
    path('subscription-plans/', views.subscription_plans, name='subscription_plans'),
    path('subscribe/<int:plan_id>/', views.subscribe_plan, name='subscribe_plan'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)