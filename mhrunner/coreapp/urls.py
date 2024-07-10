from django.urls import path
from . import views

urlpatterns = [
    path('connections/', views.connections_view, name='connections'),
]