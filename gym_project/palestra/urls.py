from django.urls import path
from . import views  

urlpatterns = [

    path('gym_class/<int:id>/', views.gym_class_detail_view, name='gym_class_detail'),
]
