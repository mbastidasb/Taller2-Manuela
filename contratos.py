# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 12:33:19 2020

@author: mbasti
"""

"Tercer cambio en el archivo"

"Cambio en el archivo"

"Segundo comentario en el archivo"
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

"Cambio en doc Manuela"


def datos_cargar_doc (archivo: str)->pd.DataFrame:
    """requerimiento 0, cargar datos
    parámetros=nombre del archivo
    """
    contratos= pd.read_csv(archivo)
    return contratos

df=cargar_datos("2019.csv")
def contratos_mas_caros (contratos: pd.DataFrame)->pd.DataFrame:
    """requerimiento 1, 10 contratos más caros, ordenados en DataFrame
    incluye entidad contratante, departamento de la entidad, nombre del proveedor al cual se adjudicó el contrato y valor del contrato.
    """
    ordenado=contratos.sort_values("ValordelContrato", ascending=False)
    nuevo= ordenado.iloc[0:10,[0,1,14,17]]
    return nuevo

def deuda_por_departamento(contratos: pd.DataFrame)->None:
    """ requerimiento 2
    departamentos que más dinero deben de los contratos celebrados
    representados en bargraph
    """
    df=contratos.iloc[:,[1,-4]]
    agrupado=df.groupby("Departamento").sum()
    preparado=agrupado.sort_values("ValorPendientedePago",ascending=False)
    preparado=preparado.iloc[0:10,:]
    preparado=preparado.sort_values("ValorPendientedePago")
    plt.figure()
    preparado.plot(kind="barh", legend=False)
    plt.title("Departamentos más deudores")
    plt.xlabel("Valor pendiente de pago")
    return None

def valor_contratos_por_rama(contratos:pd.DataFrame, limite_inferior:int,limite_superior:int)->None:
    """requerimiento 3, plotbox contratos por rama
    usar la columna ValordelContrato y agrupar los datos de
    acuerdo con la columna Rama.
    """
    prueba=contratos.loc[:,["Rama","ValordelContrato"]]
    prueba2=prueba[prueba.ValordelContrato>limite_inferior][prueba.ValordelContrato<limite_superior]
    
    print(prueba2)
    prueba2.boxplot(by="Rama")
    plt.title("Valor de contratos por rama")
    plt.ylabel("Valor del contrato")
    plt.xlabel("Rama contratadora")
    return None
  

def reparticion_contratos_entre_ramas(contratos:pd.DataFrame)->None:
    """requerimiento 4
    Repartición porcentual del valor total de los contratos entre las diferentes ramas del Estado
    crea piechart repartición contratos
    
    """
    filtrado=contratos.loc[:,["Rama","ValordelContrato"]]
    agrupado=filtrado.groupby("Rama").sum()
    plt.figure()
    agrupado.plot(kind="pie", subplots=True, autopct='%.2f',figsize=(8,8),legend=False)
    plt.title("Distribución de valor de contratos por rama")
    plt.ylabel("Rama del contrato")
    return None
    

def distribucion_valores_contratos (contratos: pd.DataFrame)->None:
    """ requerimiento 5
    Distribución de los valores de los contratos
     generar una gráfica de tipo KDE usando la columna ValordelContrato
    """
    plt.figure()
    nuevodf=contratos[contratos.ValordelContrato<100.000000]
    nuevodf=nuevodf.loc[:,["ValordelContrato"]]
    nuevodf.plot.kde(legend=False)
    plt.title("Distribución de los valores de contratos")
    plt.xlabel("Valor contrato")
    plt.ylabel("Densidad de probabilidad")
    plt.xlim((0,100))
    return None

def construccion_matriz (contratos: pd.DataFrame)->list:
    """ 
    requerimiento 6
    construir una matriz que cruce departamentos con sectores
    primera fila: sectores
    siguientes filas: departamento, valores de sector vs departamento
    """
    filtrado=contratos[contratos.Departamento != "No Definido"]
    agrupado=filtrado.groupby(["Departamento","Sector"],as_index=False)["ValordelContrato"].sum()
    departamentos=agrupado.Departamento.unique().tolist()
    sectores=agrupado.Sector.unique().tolist()
    sectores[:0]=" "
    matriz=[]
    matriz.append(sectores)
    for departamento in departamentos:
        lista=[]
        lista.append(departamento)
        for sector in sectores[1:]:
            valor=(agrupado[agrupado.Departamento==departamento][agrupado.Sector==sector]).ValordelContrato
            if valor.empty:
                valor=0
            else:
                valor=float(valor)
            lista.append(valor)
        matriz.append(lista)
    return matriz

def inversion_estado (matriz:list, tipo:int)->tuple:
    """requerimiento 7, 
    sector con mayor o menor inversión
    1=menor gasto, 2=mayor gasto
    retorna tupla con el sector y el valor
    """
    diccionario={}
    for i in range(1,len(matriz[0])):
        index_sector=i
        suma=0
        for x in range(1,len(matriz)):
            suma+=matriz[x][index_sector]
        diccionario[matriz[0][index_sector]]=suma
    if tipo==1:
        gasto=99999999
        sector_elegido=" "
        for sector in diccionario:
            if diccionario[sector]<gasto:
                gasto=diccionario[sector]
                sector_elegido=sector
    else:
        gasto=-1
        sector_elegido=" "
        for sector in diccionario:
            if diccionario[sector]>gasto:
                gasto=diccionario[sector]
                sector_elegido=sector
    tupla=(sector_elegido, gasto)
    return tupla

        
def valor_contratos_por_departamento(matriz:list,dept:str)->float:
    """
    requerimiento 8 
    valor total de los contratos de un departamento a partir de la matriz
    """
    suma=0
    for i in range(1,len(matriz)):
        if dept in matriz[i]:
            for x in range(1,len(matriz[0])):
                suma+=matriz[i][x]
    return suma

def mayor_gasto(matriz:list)->dict:
    """"
    requerimento 9
    parte 1: retorna diccionario con los 10 departamentos de mayor gasto
    """
    diccionario={}
    for i in range(1,len(matriz)):
        dept=matriz[i][0]
        total=valor_contratos_por_departamento(matriz,dept)
        diccionario[dept]=total
    dict_final={}
    for i in range(0,10):
        maximo=-1
        for departamento in diccionario:
            if diccionario[departamento]>maximo:
                maximo=diccionario[departamento]
                mayor=departamento
        dict_final[mayor]=diccionario[mayor]
        del diccionario[mayor]
    return dict_final

def grafica_mayor_gasto(dict_final:dict)->None:
    """"
    requerimento 9
    parte 2: crea gráfica de barras a partir del diccionario creado anteriormente
    """
    df = pd.DataFrame.from_dict(dict_final,orient='index',columns=['Gasto'])
    plt.figure()
    df.plot(kind="bar")
    plt.title("Departamentos con mayor gasto")
    plt.ylabel("Valor total de contratos")
    plt.xlabel("Departamento")
    return None


def dedicacion_por_sector(matriz:list,sector:str)->dict:
    """"
    requerimiento 10
    parte 1: retorna diccionario con los departamentos que mas invierten en el sector
    retorna máximo 5, pero puede retornar menos
    """
    diccionario={}
    for i in range(len(matriz[0])):
        if matriz[0][i]==sector:
            index_sector=i
    for i in range(1,len(matriz)):
        gasto=valor_contratos_por_departamento(matriz,matriz[i][0])
        gasto_sector=float((matriz[i][index_sector]))
        if gasto==0:
           dedicacion=0 
        else:
            dedicacion=(gasto_sector/gasto)*100
        diccionario[matriz[i][0]]=dedicacion
    dict_final={}
    for i in range(0,5):
        maximo=-1
        for departamento in diccionario:
            if diccionario[departamento]>maximo:
                maximo=diccionario[departamento]
                mayor=departamento
        if maximo!=0:
            dict_final[mayor]=diccionario[mayor]
        del diccionario[mayor]
    return dict_final

def cargar_coordenadas(nombre_archivo:str)->dict:
     """"
     requerimiento 10
     parte 2: carga las coordenadas de los departamentos
     """
     deptos = {}
     archivo = open(nombre_archivo, encoding="utf8")
     titulos = archivo.readline()
     linea = archivo.readline()
     while len(linea) > 0:
         linea = linea.strip()
         datos = linea.split(";")
         deptos[datos[0]] = (int(datos[1]),int(datos[2]))
         linea = archivo.readline()
     return deptos
        
def dedicacion_sobre_mapa(top5:dict, coordenadas:dict, matriz:list, sector:str)->None:
    """"
    requerimiento 10
    parte 3: pinta cuadrados de 13x13 pixeles en los departamentos con mayor dedicación
    sobre un mapa de Colombia
    """
    mapa = mpimg.imread("mapa.png").tolist()
    top5=dedicacion_por_sector(matriz,sector)
    coordenadas=cargar_coordenadas("coordenadas.txt")
    colores=[[0.94, 0.10, 0.10] ,[0.94, 0.10, 0.85],[0.10, 0.50, 0.94],[0.34, 0.94, 0.10],[0.99, 0.82, 0.09]]
    color=0
    for departamento in top5:
        x=coordenadas[departamento][0]
        y=coordenadas[departamento][1]
        a=-6
        for i in range(13):
            b=-6
            nuevox=x+a
            for z in range(13):
                nuevoy=y+b
                mapa[nuevox][nuevoy]=colores[color]
                b+=1
            a+=1
        color+=1
    plt.imshow(mapa)
    plt.show()
    return None
    




    
    