import time
import csv
csv.field_size_limit(2147483647)
from DataStructures.List import array_list as lt
import math as math

def new_logic():
    """
    Crea el catalogo para almacenar las estructuras de datos
    """
    #TODO: Llama a las funciónes de creación de las estructuras de datos
    catalog = {"viajes": None, 
               "barrios": None}
    catalog["viajes"] = lt.new_list()
    catalog["barrios"] = load_data_neigh()
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
        viaje["pickup_time"]=viaje["pickup_datetime"][11:] #para obtener fácil la hora inicio
        viaje["dropoff_date"]=viaje["dropoff_datetime"][:10] #para obtener fácil la fecha final
        viaje["dropoff_time"]=viaje["dropoff_datetime"][11:] #para obtener fácil la hora final
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
    
    total = lt.size(catalog["viajes"])
    menor = 99999999999999
    mayor = 0.0
    for i in range(0, total):
        viaje = lt.get_element(catalog["viajes"], i)
            #calcula el viaje con menor distancia y el mayor
        if viaje["trip_distance"] < menor and viaje["trip_distance"] > 0.0:
            menorid = viaje["id"]
            menor = viaje["trip_distance"]
            fecha_menor = viaje["pickup_datetime"]
            costo_menor = viaje["total_amount"]
            
        if viaje["trip_distance"] > mayor:
            mayorid = viaje["id"]
            mayor = viaje["trip_distance"]
            fecha_mayor = viaje["pickup_datetime"]
            costo_mayor = viaje["total_amount"]
    
    primeros = []
    for i in range (0,5):
        viaje = lt.get_element(catalog["viajes"], i)
        duracion = diferencia_tiempo(viaje)
        info = {"Id_trayecto": viaje["id"],
            "Fecha/Hora inicio": viaje["pickup_datetime"],
            "Fecha/Hora destino": viaje["dropoff_datetime"],
            "Duración (min)": duracion,
            "Distancia (millas)": viaje["trip_distance"],
            "Costo total": viaje["total_amount"]}
        primeros.append(info)
    
    ultimos = []
    for i in range (total-5, total):
        viaje = lt.get_element(catalog["viajes"], i)
        duracion = diferencia_tiempo(viaje)
        viaje = lt.get_element(catalog["viajes"], i)
        info = {"Id_trayecto": viaje["id"],
            "Fecha/Hora inicio": viaje["pickup_datetime"],
            "Fecha/Hora destino": viaje["dropoff_datetime"],
            "Duración (min)": duracion,
            "Distancia (millas)": viaje["trip_distance"],
            "Costo total": viaje["total_amount"]}
        ultimos.append(info)
    return tiempo, total, menorid, menor, fecha_menor, costo_menor, mayorid, mayor, fecha_mayor, costo_mayor, primeros, ultimos


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


def req_1():
    return None

def req_2():
    return None

def req_3():
    return None

def req_4():
    return None

def req_5():
    return None

def req_6():
    return None


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
