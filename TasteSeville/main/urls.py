from django.urls import path
from main import views



urlpatterns = [
    path('carga/', views.carga, name='carga'),
    path('restaurantes/', views.list_restaurants, name='restaurantes'),
    path('restaurantes/nombre', views.buscarRestaurantePorNombre, name='restaurantes_nombre')
]