import time
import csv
csv.field_size_limit(2147483647)
from DataStructures.List import array_list as lt
from DataStructures.Map import map_linear_probing as mp
from DataStructures.Map import map_entry as me
import math as math
import datetime as datetime

def new_logic():
    """
    Crea el catalogo para almacenar las estructuras de datos
    """
    #TODO: Llama a las funciónes de creación de las estructuras de datos
    catalog = {"viajes": None, 
               "barrios": None,
               "fecha_term": None,
               "fecha_hora_term": None,
               "barrio_recog": None}
    
    catalog["viajes"] = lt.new_list()
    catalog["barrios"] = load_data_neigh()
    catalog["fecha_term"] = mp.new_map(600, 0.5) #req4 Tabla Hash llave sea la fecha de terminación
    catalog["fecha_hora_term"] = mp.new_map(600*24, 0.5) #req5 Tabla Hash llave sea fecha y hora terminación
    catalog["barrio_recog"] = mp.new_map(500, 0.5) #req6 Tabla Hash Barrio
    return catalog
#Función auxiliar apara cargar datos del nyc-neighborhoods.csv
def load_data_neigh():       
    barrios = lt.new_list()
    input_file = csv.DictReader(open("data/nyc-neighborhoods.csv", encoding='utf-8'), delimiter=";")
    for barrio in input_file:
        barrio_limpio = {
            "borough": barrio["borough"].strip(),
            "neighborhood": barrio["neighborhood"].strip(),
            "latitude": float(barrio["latitude"].replace(",",".")),
            "longitude": float(barrio["longitude"].replace(",","."))
        }
        lt.add_last(barrios, barrio_limpio)   
    return barrios

# Funciones para la carga de datos
def load_data(catalog, filename):
    """
    Carga los datos del reto
    """
    # TODO: Realizar la carga de datos
    id = 0    
    start = get_time()
    taxis = filename
    input_file = csv.DictReader(open(taxis, encoding='utf-8'))
    
    for viaje in input_file:
        viaje["id"]=id #El dictreader me da cada fila como un dict, 
                       #pongo una llave id para que sea fácil identificar cada viaje
        viaje["pickup_date"]= viaje["pickup_datetime"][:10] #para obtener fácil la fecha inicio
        viaje["pickup_time"]= viaje["pickup_datetime"][11:] #para obtener fácil la hora inicio
        viaje["dropoff_date"]= viaje["dropoff_datetime"][:10] #para obtener fácil la fecha final
        viaje["dropoff_time"]= viaje["dropoff_datetime"][11:] #para obtener fácil la hora final
        viaje["passenger_count"] = int(viaje["passenger_count"])
        viaje["trip_distance"] = float(viaje["trip_distance"])
        viaje["pickup_longitude"] = float(viaje["pickup_longitude"])
        viaje["pickup_latitude"] = float(viaje["pickup_latitude"])
        viaje["rate_code"] = int(viaje["rate_code"])
        viaje["dropoff_longitude"] = float(viaje["dropoff_longitude"])
        viaje["dropoff_latitude"] = float(viaje["dropoff_latitude"])
        viaje["fare_amount"] = float(viaje["fare_amount"])
        viaje["extra"] = float(viaje["extra"])
        viaje["mta_tax"] = float(viaje["mta_tax"])
        viaje["tip_amount"] = float(viaje["tip_amount"])
        viaje["tolls_amount"] = float(viaje["tolls_amount"])
        viaje["improvement_surcharge"] = float(viaje["improvement_surcharge"])
        viaje["total_amount"] = float(viaje["total_amount"])

        lt.add_last(catalog["viajes"], viaje)  
    
        id += 1
    end = get_time()
    tiempo = delta_time(start, end)
    return tiempo

# Funciones de consulta sobre el catálogo

def get_data(catalog, id):
    """
    Retorna un dato por su ID.
    """
    #TODO: Consulta en las Llamar la función del modelo para obtener un dato
    tam = lt.size(catalog["viajes"])
    if id >= 0 and id < tam:
        for i in range(0,tam):
            dato = lt.get_element(catalog["viajes"], i)
            if id == dato["id"]:
                return dato
    else:
        return None


def sort_criteria_viajes(element_1, element_2):
    f1 = datetime.datetime.strptime(element_1["pickup_datetime"], "%Y-%m-%d %H:%M:%S")
    f2 = datetime.datetime.strptime(element_2["pickup_datetime"], "%Y-%m-%d %H:%M:%S")
    is_sorted = False
    if f1 < f2: #Más antigüo al más reciente
        is_sorted = True
    return is_sorted

sort_crit = sort_criteria_viajes
def req_1(catalog, inicio, final, muestra): #preguntar cómo se organiza una lista, preguntar formato
    start = get_time()
    trayectos = 0
    viajes_filtrados = lt.new_list()
    for i in range(0, lt.size(catalog["viajes"])):
        viaje = lt.get_element(catalog["viajes"], i)
        f = datetime.datetime.strptime(viaje["pickup_datetime"], "%Y-%m-%d %H:%M:%S")
        if datetime.datetime.strptime(inicio,"%Y-%m-%d %H:%M:%S") <= f and f <= datetime.datetime.strptime(final, "%Y-%m-%d %H:%M:%S"):
            viaje["pickup_longitude"] = round(viaje["pickup_longitude"],2)
            viaje["pickup_latitude"] = round(viaje["pickup_latitude"],2)
            viaje["dropoff_longitude"] = round(viaje["dropoff_longitude"],2)
            viaje["dropoff_latitude"] = round(viaje["dropoff_latitude"],2)
            trayectos += 1
            lt.add_last(viajes_filtrados, viaje)
    viajes_organizados = lt.quick_sort(viajes_filtrados, sort_crit)
    end = get_time()
    tiempo = delta_time(start, end)
    return tiempo, trayectos, viajes_organizados
    
    
def sort_crit2(element_1, element_2):
    is_sorted = False
    if float(element_1["pickup_latitude"]) > float(element_2["pickup_latitude"]):
        is_sorted = True
    elif float(element_1["pickup_latitude"]) == float(element_2["pickup_latitude"]):
        if float(element_1["pickup_longitude"]) > float(element_2["pickup_longitude"]):
            is_sorted = True
    return is_sorted

def req_2(catalog,coord_ini, coord_fin, tamano_muestra):
    start = get_time()
    tamano= lt.size(catalog["viajes"])
    viajes_filtrados = lt.new_list()
    trayectos = 0
    for i in range(0, tamano):
        viaje = lt.get_element(catalog["viajes"], i)
        lat_ini = float(viaje["pickup_latitude"])
        if lat_ini>=coord_ini and lat_ini<=coord_fin:
            trayectos += 1
            lt.add_last(viajes_filtrados, viaje)
    viajes_orden = lt.quick_sort(viajes_filtrados, sort_crit2) 
    if trayectos>=2*tamano_muestra:
        primeros=lt.new_list()
        for j in range(0,tamano_muestra):
            viaje=lt.get_element(viajes_orden,j)
            info={"Id_trayecto": viaje["id"],
                "Fecha y tiempo recogida": viaje["pickup_datetime"],
                "Latitud y longitud recogida": f'[{viaje["pickup_latitude"]},{viaje["pickup_longitude"]}]',
                "Fecha y tiempo de terminación": viaje["dropoff_datetime"],
                "Latitud y longitud de terminación": f'[{viaje["dropoff_latitude"]},{viaje["dropoff_longitude"]}]',
                "Distancia (millas)": viaje["trip_distance"],
                "Costo total": viaje["total_amount"]}
            primeros=lt.add_last(primeros,info)
        ultimos=lt.new_list()
        for j in range(lt.size(viajes_orden)-tamano_muestra,lt.size(viajes_orden)):
            viaje=lt.get_element(viajes_orden,j)
            info={"Id_trayecto": viaje["id"],
                "Fecha y tiempo recogida": viaje["pickup_datetime"],
                "Latitud y longitud recogida": f'[{viaje["pickup_latitude"]},{viaje["pickup_longitude"]}]',
                "Fecha y hora de terminación": viaje["dropoff_datetime"],
                "Latitud y longitud de terminación": f'[{viaje["dropoff_latitude"]},{viaje["dropoff_longitude"]}]',
                "Distancia (millas)": viaje["trip_distance"],
                "Costo total": viaje["total_amount"]}
            ultimos=lt.add_last(ultimos,info)
        viajes_orden={"Primeros viajes:": primeros,"Últimos viajes:": ultimos}
    else:
        m=mp.new_map(lt.size(viajes_orden),0.5,109345121)
        for k in range(lt.size(viajes_orden)):
            viaje=lt.get_element(viajes_orden,k)
            lista=lt.new_list()
            lt.add_last(lista, viaje["pickup_datetime"])
            lt.add_last(lista, f'[{viaje["pickup_latitude"]},{viaje["pickup_longitude"]}]')
            lt.add_last(lista, viaje["dropoff_datetime"])
            lt.add_last(lista, f'[{viaje["dropoff_latitude"]},{viaje["dropoff_longitude"]}]')
            lt.add_last(lista, viaje["trip_distance"])
            lt.add_last(lista, viaje["total_amount"])
            mp.put(m, viaje["id"], lista)
        viajes_orden=m
          
    end= get_time()
    tiempo= delta_time(start,end)
    return tiempo,trayectos,viajes_orden

def req_3(catalog):
    start = get_time()
    
    end = get_time()
    tiempo = delta_time(start, end)
    return tiempo

def mapas(catalog):
    catalog["fecha_term"] = mp.new_map(2000, 0.5) #req4 Tabla Hash llave sea la fecha de terminación
    catalog["fecha_hora_term"] = mp.new_map(2000*24, 0.5) #req5 Tabla Hash llave sea fecha y hora terminación
    catalog["barrio_recog"] = mp.new_map(1000, 0.5) #req6 Tabla Hash Barrio

def req_4(catalog, fecha_terminacion, tiempo_ref, criterio, muestra):
    start = get_time()
    criterio = criterio.lower()
    trayectos = 0
    viajes_filtrados = lt.new_list()
    #Organizar viajes con el filtro de fecha terminación y con el criterio de Antes o Después
    for i in range(lt.size(catalog["viajes"])):
        viaje = lt.get_element(catalog["viajes"], i)
        if viaje["dropoff_date"] == fecha_terminacion: #Filtro fecha
            viaje["pickup_longitude"] = round(viaje["pickup_longitude"],2)
            viaje["pickup_latitude"] = round(viaje["pickup_latitude"],2)
            viaje["dropoff_longitude"] = round(viaje["dropoff_longitude"],2)
            viaje["dropoff_latitude"] = round(viaje["dropoff_latitude"],2)
            if criterio == "antes" and viaje["dropoff_time"] < tiempo_ref:
                trayectos += 1
                lt.add_last(viajes_filtrados, viaje)
            elif criterio == "despues" and viaje["dropoff_time"] > tiempo_ref:
                trayectos += 1
                lt.add_last(viajes_filtrados, viaje)
    
    viajes_organizados = lt.quick_sort(viajes_filtrados, sort_crit)
    end = get_time()
    tiempo = delta_time(start, end)    
    return tiempo, trayectos, viajes_organizados

def req_5(catalog):
    start = get_time()
    
    end = get_time()
    tiempo = delta_time(start, end)
    return tiempo
def sort_crit6(element_1, element_2):
    is_sorted = False
    if element_1["pickup_time"] > element_2["pickup_time"]:
        is_sorted = True
    return is_sorted
def req_6(catalog, barrio, hora_ini, hora_fin, tamano_muestra):
    start = get_time()
    trayectos = 0
    viajes_filtrados = lt.new_list()
    tamano= lt.size(catalog["viajes"])
    for i in range(0, tamano):
        viaje=lt.get_element(catalog["viajes"], i)
        lat=viaje["pickup_latitude"]
        lon=viaje["pickup_longitude"]
        barrio_rec = barrio_mas_cercano(lat, lon, catalog["barrios"])
        if barrio_rec == barrio:
            hora = int(viaje["pickup_time"].split(":"))
            if hora_ini <= hora and hora <= hora_fin:
                trayectos += 1
                lt.add_last(viajes_filtrados, viaje)
    viajes_orden = lt.quick_sort(viajes_filtrados, sort_crit6)
    end = get_time()
    tiempo = delta_time(start, end)
    return tiempo


# Funciones para medir tiempos de ejecucion
def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed


def barrio_mas_cercano(lat, lon, barrios):
    """
    barrios: lista/dict con centroides { "neighborhood": str, "latitude": float, "longitude": float }
    """
    barrio_cercano = None
    distancia_min = 1000000000
    for i in range(lt.size(barrios)):
        b = lt.get_element(barrios, i)

        d = haversine(lat, lon, b["latitude"], b["longitude"])
        if d < distancia_min:
            distancia_min = d
            barrio_cercano = b["neighborhood"]   # o podrías devolver también borough
    
    return barrio_cercano

# Función auxiliar para calcular la distancia entre dos puntos geográficos hecha con https://pypi.org/project/haversine/ y Gemini, quien nos ayudó a entender como se implementaba. 
# No se pudo usar el import haversine ya que en 2 de nuestros computadores hubo un problema al instalarlo, por lo que lo hicimos con la fórmula.
def haversine(lat1, lon1, lat2, lon2):
    """
    Calcula la distancia entre dos puntos (lat1, lon1) y (lat2, lon2)
    """
    R = 3956  # Radio de la Tierra en millas. Usa 6371 para kilómetros

    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon / 2) * math.sin(dLon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distancia = R * c
    return distancia

def diferencia_tiempo(viaje):
    #tiempo               
    x_ini= viaje["pickup_time"].split(":")
    Dura_ini = int(x_ini[0]) * 60 + int(x_ini[1])
    x_fin= viaje["dropoff_time"].split(":")
    Dura_fin = int(x_fin[0]) * 60 + int(x_fin[1])
    if Dura_fin >= Dura_ini:
        Dura = Dura_fin - Dura_ini
    else:
        Dura = (1440 - Dura_ini) + Dura_fin
    return Dura
