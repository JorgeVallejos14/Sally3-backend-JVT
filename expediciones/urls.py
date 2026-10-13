from django.urls import path
from . import views

app_name = 'expediciones'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('expedicion/<int:id>/', views.detalle, name='detalle'),
    path('participantes/', views.participantes, name='participantes'),
]