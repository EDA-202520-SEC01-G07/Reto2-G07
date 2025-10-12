import time
import csv
csv.field_size_limit(2147483647)
from DataStructures.List import array_list as lt
from DataStructures.Map import map_linear_probing as mp
from DataStructures.Map import map_entry as me
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

def sort_criteria_viajes(element_1, element_2):
    is_sorted = False
    if element_1["pickup_datetime"] < element_2["pickup_datetime"]:
        is_sorted = True
    return is_sorted

sort_crit = sort_criteria_viajes
def req_1(catalog, inicio, final, muestra): #preguntar cómo se organiza una lista, preguntar formato
    start = get_time()
    
    trayectos = 0
    viajes_filtrados = lt.new_list()
    for i in range(0, lt.size(catalog["viajes"])):
        viaje = lt.get_element(catalog["viajes"], i)
        if inicio <= viaje["pickup_datetime"] and viaje["pickup_datetime"] <= final:
            trayectos += 1
            lt.add_last(viajes_filtrados, viaje)
    viajes_organizados = lt.quick_sort(viajes_filtrados, sort_crit)
    
    if trayectos >=  2*muestra:
        m1 = mp.new_map(muestra,0.5,109345121)
        for j in range(muestra):
            viaje = lt.get_element(viajes_organizados, j)
            lista = lt.new_list()
            lt.add_last(lista, viaje["pickup_datetime"])
            lt.add_last(lista, f'[{viaje["pickup_latitude"]},{viaje["pickup_longitude"]}]')
            lt.add_last(lista, viaje["dropoff_datetime"])
            lt.add_last(lista, f'[{viaje["dropoff_latitude"]},{viaje["dropoff_longitude"]}]')
            lt.add_last(lista, viaje["trip_distance"])
            lt.add_last(lista, viaje["total_amount"])
            mp.put(m1, viaje["id"], lista)
        m2 = mp.new_map(muestra,0.5,109345121)
        for j in range(lt.size(viajes_organizados)-muestra,lt.size(viajes_organizados)):
            viaje = lt.get_element(viajes_organizados, j)
            lista = lt.new_list()
            lt.add_last(lista, viaje["pickup_datetime"])
            lt.add_last(lista, f'[{viaje["pickup_latitude"]},{viaje["pickup_longitude"]}]')
            lt.add_last(lista, viaje["dropoff_datetime"])
            lt.add_last(lista, f'[{viaje["dropoff_latitude"]},{viaje["dropoff_longitude"]}]')
            lt.add_last(lista, viaje["trip_distance"])
            lt.add_last(lista, viaje["total_amount"])
            mp.put(m2, viaje["id"], lista)
        viajes = {"Primeros viajes:": m1, "Últimos viajes:": m2}
    elif trayectos < 2*muestra:
        viajes = lt.new_list()
        m = mp.new_map(lt.size(viajes_organizados),0.5,109345121)
        for k in range(lt.size(viajes_organizados)):
            viaje = lt.get_element(viajes_organizados, k)
            lista = lt.new_list()
            lt.add_last(lista, viaje["pickup_datetime"])
            lt.add_last(lista, f'[{viaje["pickup_latitude"]},{viaje["pickup_longitude"]}]')
            lt.add_last(lista, viaje["dropoff_datetime"])
            lt.add_last(lista, f'[{viaje["dropoff_latitude"]},{viaje["dropoff_longitude"]}]')
            lt.add_last(lista, viaje["trip_distance"])
            lt.add_last(lista, viaje["total_amount"])
            mp.put(m, viaje["id"], lista)
        viajes = m
    end = get_time()
    tiempo = delta_time(start, end)
    return tiempo, trayectos, viajes
    
def aux_presentacion(viajes):
    start = get_time()
    p = lt.new_list()
    u = lt.new_list()
    if "Primeros viajes:" in viajes:
        primeros = viajes["Primeros viajes:"]
        ultimos = viajes["Últimos viajes:"]
        for i in range(primeros["capacity"]):
            elem = lt.get_element(primeros["table"], i)
            if me.get_key(elem) != None:
                lt.add_last(p, {elem['key']:elem['value']['elements']})
        for i in range(ultimos["capacity"]):
            elem = lt.get_element(ultimos["table"], i)
            if me.get_key(elem) != None:
                lt.add_last(u, {elem['key']:elem['value']['elements']})
        l = {"Primeros viajes:": p['elements'], "Últimos viajes:": u['elements']}
    else:
        l = lt.new_list()
        for i in range(viajes["capacity"]):
            elem = lt.get_element(viajes["table"], i)
            if me.get_key(elem) != None:
                lt.add_last(l, {elem['key']:elem['value']['elements']})
        l = l['elements']
    end = get_time()
    tiempo = delta_time(start, end)
    return tiempo, l
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

def req_4(catalog, fecha_terminacion, tiempo_ref, criterio, muestra):
    start = get_time()
    criterio = criterio.lower()
    trayectos = 0
    viajes_filtrados = lt.new_list()
    #Organizar viajes con el filtro de fecha terminación y con el criterio de Antes o Después
    for i in range(lt.size(catalog["viajes"])):
        viaje = lt.get_element(catalog["viajes"], i)
        if viaje["dropoff_date"] == fecha_terminacion: #Filtro fecha
            if criterio == "antes" and viaje["dropoff_time"] < tiempo_ref:
                trayectos += 1
                lt.add_last(viajes_filtrados, viaje)
            elif criterio == "despues" and viaje["dropoff_time"] > tiempo_ref:
                trayectos += 1
                lt.add_last(viajes_filtrados, viaje)
    
    viajes_organizados = lt.quick_sort(viajes_filtrados, sort_crit)
    if trayectos >= 2*muestra:
        primeros = mp.new_map(muestra, 0.5, 10934121)
        ultimos = mp.new_map(muestra, 0.5, 10934121)
        for i in range(muestra):
            viaje = lt.get_element(viajes_organizados, i)
            lista = lt.new_list()
            lt.add_last(lista, viaje["pickup_datetime"])
            lt.add_last(lista, f'[{viaje["pickup_latitude"]},{viaje["pickup_longitude"]}]')
            lt.add_last(lista, viaje["dropoff_datetime"])
            lt.add_last(lista, f'[{viaje["dropoff_latitude"]},{viaje["dropoff_longitude"]}]')
            lt.add_last(lista, viaje["trip_distance"])
            lt.add_last(lista, viaje["total_amount"])
            mp.put(primeros, viaje["dropoff_date"], lista)
        for j in range(lt.size(viajes_organizados)-muestra,lt.size(viajes_organizados)):
            viaje = lt.get_element(viajes_organizados, j)
            lista = lt.new_list()
            lt.add_last(lista, viaje["pickup_datetime"])
            lt.add_last(lista, f'[{viaje["pickup_latitude"]},{viaje["pickup_longitude"]}]')
            lt.add_last(lista, viaje["dropoff_datetime"])
            lt.add_last(lista, f'[{viaje["dropoff_latitude"]},{viaje["dropoff_longitude"]}]')
            lt.add_last(lista, viaje["trip_distance"])
            lt.add_last(lista, viaje["total_amount"])
            mp.put(ultimos, viaje["dropoff_date"], lista)
        viajes = {"Primeros viajes:": primeros, "Últimos viajes:": ultimos}
    elif trayectos < 2*muestra:
        m = mp.new_map(lt.size(viajes_organizados),0.5,109345121)
        for k in range(lt.size(viajes_organizados)):
            viaje = lt.get_element(viajes_organizados, k)
            lista = lt.new_list()
            lt.add_last(lista, viaje["pickup_datetime"])
            lt.add_last(lista, f'[{viaje["pickup_latitude"]},{viaje["pickup_longitude"]}]')
            lt.add_last(lista, viaje["dropoff_datetime"])
            lt.add_last(lista, f'[{viaje["dropoff_latitude"]},{viaje["dropoff_longitude"]}]')
            lt.add_last(lista, viaje["trip_distance"])
            lt.add_last(lista, viaje["total_amount"])
            mp.put(m, viaje["dropoff_date"], lista)
        viajes = m
    end = get_time()
    tiempo = delta_time(start, end)
        
    return tiempo, trayectos, viajes

def req_5(catalog):
    start = get_time()
    
    end = get_time()
    tiempo = delta_time(start, end)
    return tiempo

def req_6(catalog, barrio, hora_ini, hora_fin, tamano_muestra):
    start = get_time()
    
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
