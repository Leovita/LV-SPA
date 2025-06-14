from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_services_view, name='all_services_view'),
    # Aggiungi altri URL per la gestione dei dettagli, se necessario
]
