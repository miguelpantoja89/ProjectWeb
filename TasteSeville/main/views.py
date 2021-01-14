from .models import Restaurante, Review, Evento
from main.forms import BusquedaPorNombre,BuscaTituloCuerpo
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup
import urllib.request
import lxml
import re, os, shutil
import requests
import datetime
from whoosh.index import create_in,open_dir
from whoosh.fields import Schema, TEXT, DATETIME, KEYWORD, NUMERIC
from whoosh.qparser import QueryParser, MultifieldParser, OrGroup



def populateDB():
    ### Drop de las tablas
    Evento.objects.all().delete()
    Restaurante.objects.all().delete()
    Review.objects.all().delete()
    #####
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
        imagen = soup.find("div",attrs={"data-prwidget-name":"common_basic_image"}).find("div").find("img")['data-lazyurl']
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
        min_price=int(min_precio), max_price=int(max_precio),location=location,image=imagen)
        ##### Obtener reviews ######
        review = soup.find("div",class_="listContainer")
        restaurante = Restaurante.objects.get(name=nombre)
        for rev in review.findChildren("div",recursive=False):
            
            if rev.find("span",class_="noQuotes") is None:
                continue
            else:
                ca= rev.find("span",class_="noQuotes")
                quote = strip_emoji(ca.text)
            bubblereview = rev.find_all('span', {'class': re.compile('ui_bubble_rating bubble_\d*')})
            ratings = re.findall('\d+', ''.join(map(str, bubblereview)))
            digits2 = [int(x) for x in str(ratings[0])]
            rating = float(str(digits2[0])+"."+str(digits2[1]))
            if rev.find("p",class_="partial_entry") is None:
                continue
            else:
                entry= rev.find("p",class_="partial_entry")
                entryStriped = strip_emoji(entry.text)
            if rev.find("span",class_="ratingDate") is None:
                continue
            else:
                date = rev.find("span",class_="ratingDate")
                fecha = mesANumero(date['title'])
            Review.objects.create(restaurante=restaurante, titulo=quote, body=entryStriped, point=rating, fecha=fecha)
        nombre = ""
    #### Obtener eventos #######
    fu = urllib.request.urlopen("https://www.eventbrite.es/d/spain--sevilla/all-events/?page=1")
    su = BeautifulSoup(fu, "lxml")
    contenidos = su.find("div",class_="search-main-content").find("ul")
    for contenido in contenidos.find_all("li"):
        mainTitle = contenido.find("div",attrs={"data-spec":"event-card__formatted-name--content"})
        if "siento" in contenido.find("div",class_="card-text--truncated__one").text:
            ubicacion = contenido.find("div",class_="card-text--truncated__one").text.split(" ")[-1]
        else:
            ubicacion = contenido.find("div",class_="card-text--truncated__one").text
        link = contenido.find("a",class_="eds-event-card-content__action-link")['href']
        sop = BeautifulSoup(urllib.request.urlopen(link),"lxml")
        if sop.find("div",class_="js-panel-display-price") is None:
            price2 = "Gratis"
        else:
            price2 = sop.find("div",class_="js-panel-display-price").string.strip()
        body = sop.find_all("div",attrs={"data-automation":"listing-event-description"})
        pic = sop.find("picture")['content']
        Evento.objects.create(titulo = mainTitle.text, ubicacion = ubicacion,precio = price2,body = body[0].text, image = pic)
def SchemaReview():
    schema = Schema(restaurante= NUMERIC(),
                    titulo = TEXT(stored=True),
                    body = TEXT(stored=True),
                    point = NUMERIC(),
                    fecha= DATETIME(stored=True)
    )
    return schema

def load_whoosh():
    reviews = Review.objects.all()
    if os.path.exists("whooshIndex"):
        shutil.rmtree("whooshIndex")
    os.mkdir("whooshIndex")
    ix = create_in("whooshIndex", schema=SchemaReview())
    writer = ix.writer()
    i=0
    for review in reviews:
        writer.add_document(restaurante=review.restaurante.pk ,titulo=str(review.titulo), body = str(review.body), point = review.point, fecha=datetime.datetime.combine(review.fecha, datetime.datetime.min.time()))
        i+=1
    writer.commit()
    return i
def strip_emoji(text):
    RE_EMOJI = re.compile(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])')
    new = re.sub(r'[^\w\.]', ' ', RE_EMOJI.sub(r'', text))
    return new
def mesANumero(string):
    m = {
        'enero': "01",
        'febrero': "02",
        'marzo': "03",
        'abril': "04",
        'mayo': "05",
        'junio': "06",
        'julio': "07",
        'agosto': "08",
        'septiembre': "09",
        'octubre': "10",
        'noviembre': "11",
        'diciembre': "12"
        }
    
    fecha = string.replace('de','').split(" ")
    dia =  fecha[0]
    mes =  fecha[2]
    anio = fecha[4]

    try:
        out = str(m[mes.lower()])
        result = datetime.datetime.strptime(dia+out+anio, "%d%m%Y").date()
        #result = date.strftime('%d-%m-%Y')
    except:
        raise ValueError('No es un mes')      
    return result
def carga(request):
    if request.method=='POST':
        if 'Aceptar' in request.POST:      
            populateDB()
            num=load_whoosh()
            mensaje="Se han almacenado: " + str(len(Restaurante.objects.all())) + " restaurantes,"+ str(len(Evento.objects.all())) +" eventos" + "y se han indexado" + str(num)+" reviews"
            return render(request, 'cargaDB.html', {'mensaje':mensaje})
        else:
            return redirect("/")
           
    return render(request, 'confirmacion.html')
def list_restaurants(request):
    resturantes = Restaurante.objects.all()
    return render(request,'restaurantes.html', {'restaurantes':resturantes})

def list_eventos(request):
    eventos = Evento.objects.all()
    return render(request,'eventos.html', {'eventos':eventos})

def show_reviews(request,pk):
    restaurante = Restaurante.objects.get(pk=pk)
    reviews = Review.objects.filter(restaurante=restaurante)
    return render(request,'reviews.html', {'reviews':reviews})

def buscarRestaurantePorNombre(request):
    formulario = BusquedaPorNombre()
    resturantes = None
    
    if request.method=='POST':
        formulario = BusquedaPorNombre(request.POST)      
        if formulario.is_valid():
            resturantes = Restaurante.objects.filter(name__icontains=formulario.cleaned_data['nombre'])
            render(request, 'restaurantesPorNombre.html', {'formulario':formulario, 'resturantes':resturantes})
    return render(request, 'restaurantesPorNombre.html', {'formulario':formulario, 'resturantes':resturantes})

def buscaReviewPorTituloContenido(request):
    formulario = BuscaTituloCuerpo()
    reviews = None
    mensaje = "Primero debes indexar usando Carga DB"
    cargado = False
    if request.method=='POST':
        if not os.path.exists("whooshIndex"):
            cargado = True
            return render(request, 'reviewWhoosh.html', {'formulario':formulario, 'reviews':reviews, 'mensaje':mensaje, 'cargado':cargado})
        formulario = BuscaTituloCuerpo(request.POST)
        if formulario.is_valid():
            ix=open_dir("whooshIndex")
            with ix.searcher() as searcher:
                #MultifieldParser(["titulo","body"], ix.schema, group=OrGroup)
                #QueryParser("body", ix.schema)
                query = MultifieldParser(["titulo","body"], ix.schema, group=OrGroup).parse(str(formulario.cleaned_data['contenido']))
                reviews = searcher.search(query)
                return render(request, 'reviewWhoosh.html', {'formulario':formulario, 'reviews':reviews})
    return render(request, 'reviewWhoosh.html', {'formulario':formulario, 'reviews':reviews})