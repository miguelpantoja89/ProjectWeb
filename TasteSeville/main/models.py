from django.db import models

# Create your models here.
class Restaurante(models.Model):
    name = models.TextField(verbose_name='Nombre')
    food = models.TextField(verbose_name='Tipos de Comida', default='Otro')
    points = models.FloatField(verbose_name='Puntuacion',default=0.0)
    num_reviews = models.IntegerField(verbose_name='Numero de puntuaciones',default=0) 
    min_price = models.IntegerField(verbose_name='Menor precio',default=0)
    max_price = models.IntegerField(verbose_name='Mayor precio',default=0)
    location = models.TextField(verbose_name="Ubicacion", default="Desconocido")
    image = models.URLField(max_length=500, default="")

class Review(models.Model):
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE)
    titulo= models.TextField(verbose_name='titulo')
    body = models.TextField(verbose_name='cuerpo')
    point = models.FloatField(verbose_name='puntuacion')
    fecha = models.DateField(verbose_name='fecha')

class Evento(models.Model):
    titulo = models.TextField(verbose_name='titulo')
    ubicacion = models.TextField(verbose_name='ubicacion')
    precio = models.TextField(verbose_name='precio')
    body = models.TextField(verbose_name='precio')
    image = models.URLField(max_length=500, default="")