from .models import Restaurante
from main.forms import BusquedaPorNombre
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup
import urllib.request
import lxml
# Create your views here.
def populateDB():
    ### Drop de las tablas
    Restaurante.objects.all().delete()
    f = urllib.request.urlopen("https://www.tripadvisor.es/Restaurants-g187443-Seville_Province_of_Seville_Andalucia.html")
    s = BeautifulSoup(f, "lxml")
    entradas = s.find("div",class_="_1kXteagE").find_all("div", class_="_1llCuDZj")
    nombre = ""
    for entrada in entradas:
        if entrada.find("a",class_="_15_ydu6b").string is None:
            for string in entrada.find("a",class_="_15_ydu6b").stripped_strings:
                nombre += string
        else:
            nombre = entrada.find("a",class_="_15_ydu6b").string
        link = entrada.find("a",class_="_15_ydu6b")['href']
        soup = BeautifulSoup(urllib.request.urlopen("https://www.tripadvisor.es/"+link),'lxml')
        puntuacion = soup.find("span",class_="r2Cf69qf").text.replace(",",".")
        numeroReviews= soup.find("a",class_="_10Iv7dOs").text.replace("opiniones","")
        numeroReviews2 = numeroReviews.replace(".","")
        if soup.find("div", text="RANGO DE PRECIOS") is None:
            precios = "0 € - 0 €"
        else:
            precios = soup.find("div", text="RANGO DE PRECIOS").next_sibling.text
        pricos_procesados = [s for s in precios.split() if s.isdigit()]
        min_precio = pricos_procesados[0]
        max_precio = pricos_procesados[1]
        if soup.find("div", text="Tipos de cocina") is None:
            comidas = "Desconocidas"
        else:
            comidas = soup.find("div", text="Tipos de cocina").next_sibling.text
        if soup.find("span", class_="ui_icon map-pin-fill _3ZW3afUk").next_sibling is None:
            location = "Desconocida"
        else:
            location = soup.find("span", class_="ui_icon map-pin-fill _3ZW3afUk").next_sibling.a.span.text
        Restaurante.objects.create(name=nombre,food=comidas,points=float(puntuacion),num_reviews=int(numeroReviews2),
        min_price=int(min_precio), max_price=int(max_precio),location=location)
        nombre = ""
def carga(request):
    if request.method=='POST':
        if 'Aceptar' in request.POST:      
            populateDB()
            mensaje="Se han almacenado: " + str(len(Restaurante.objects.all())) + " restaurantes"
            return render(request, 'cargaDB.html', {'mensaje':mensaje})
        else:
            return redirect("/")
           
    return render(request, 'confirmacion.html')
def list_restaurants(request):
    resturantes = Restaurante.objects.all()
    return render(request,'restaurantes.html', {'restaurantes':resturantes})

def buscarRestaurantePorNombre(request):
    formulario = BusquedaPorNombre()
    resturantes = None
    
    if request.method=='POST':
        formulario = BusquedaPorNombre(request.POST)      
        if formulario.is_valid():
            resturantes = Restaurante.objects.filter(name__icontains=formulario.cleaned_data['nombre'])
            render(request, 'restaurantesPorNombre.html', {'formulario':formulario, 'resturantes':resturantes})
    return render(request, 'restaurantesPorNombre.html', {'formulario':formulario, 'resturantes':resturantes})