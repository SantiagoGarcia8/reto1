import pandas as pd
from sodapy import Socrata
from django.http import HttpResponse
from django.template import Template, Context, loader
import requests


client = Socrata("www.datos.gov.co", None)
results = client.get("sdvb-4x4j", limit=515)
df = pd.DataFrame.from_records(results)




tabla = df.to_html(justify="center",table_id="tablax",classes="table table-striped table-bordered")


def inicio(request):
    
    doc_externo = loader.get_template("Entrada.html")


    documento = doc_externo.render({"tabla":tabla})

    return HttpResponse(documento)

def primer_filtro(request):
    

    tabla1 = df[df['nom_territorio'] == request.GET["region"]].to_html(justify="center",table_id="tablax",classes="table table-striped table-bordered")

    return HttpResponse(loader.get_template("Primer_filtro.html").render({"tabla1":tabla1}))

def cant_vacunas(request):

    vacunas = df["cantidad"][df["laboratorio_vacuna"] == request.GET["laboratorio"]]
    total_vacunas = 0
    for n in vacunas:
        if n.isnumeric() == True:
            total_vacunas += int(n)

    return HttpResponse(loader.get_template("Laboratorio.html").render({"vacunas":total_vacunas,"laboratorio":request.GET["laboratorio"].lower()}))

def poblacion_vacunada(request):
    
    tabla1 = df[df['uso_vacuna'] == request.GET["poblacion"]]

    entrega = pd.DataFrame(tabla1.groupby('nom_territorio')['nom_territorio'].count()).to_html(justify="center",table_id="tablax1",classes="table table-striped table-bordered")

    return HttpResponse(loader.get_template("Poblacion_vacunada.html").render({"tabla1":tabla1.to_html(justify="center",table_id="tablax",classes="table table-striped table-bordered"),"cantidad":entrega}))