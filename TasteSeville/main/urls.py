from django.urls import path
from main import views



urlpatterns = [
    path('carga/', views.carga, name='carga'),
    path('restaurantes/', views.list_restaurants, name='restaurantes'),
    path('eventos/', views.list_eventos, name='eventos'),
    path('restaurantes/nombre', views.buscarRestaurantePorNombre, name='restaurantes_nombre'),
    path('restaurantes/review/<int:pk>', views.show_reviews, name='show_review'),
    path('restaurantes/review', views.buscaReviewPorTituloContenido, name='review_whoosh'),
]