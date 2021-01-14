from django import forms
from .models import Restaurante, Review

class BusquedaPorNombre(forms.Form):
    nombre = forms.CharField(label="Nombre del Restaurante")

class BuscaTituloCuerpo(forms.Form):
    contenido = forms.CharField(label="Contenido en cuerpo o titulo")

