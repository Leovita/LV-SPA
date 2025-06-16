from django.urls import path, re_path
from django.views.generic import TemplateView
from rest_framework import generics
from .models import Service
from .serializers import ServiceSerializer

# View per la SPA
class SPAView(TemplateView):
    template_name = 'spa/index.html'

# API Views
class ServiceListCreateView(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class ServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

urlpatterns = [
    # API endpoints
    path('api/services/', ServiceListCreateView.as_view(), name='service-list-create'),
    path('api/services/<int:pk>/', ServiceDetailView.as_view(), name='service-detail'),
    
    # Frontend routes - catch all per il routing SPA
    re_path(r'^.*$', SPAView.as_view(), name='spa-view'),
] 