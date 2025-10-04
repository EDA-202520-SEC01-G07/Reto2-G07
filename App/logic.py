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
            "Duración en (m)": duracion,
            "Distancia": viaje["trip_distance"],
            "Costo_total": viaje["total_amount"]}
        primeros.append(info)
    
    ultimos = []
    for i in range (total-5, total):
        viaje = lt.get_element(catalog["viajes"], i)
        duracion = diferencia_tiempo(viaje)
        viaje = lt.get_element(catalog["viajes"], i)
        info = {"Id_trayecto": viaje["id"],
            "Fecha/Hora inicio": viaje["pickup_datetime"],
            "Fecha/Hora destino": viaje["dropoff_datetime"],
            "Duración en (min)": duracion,
            "Distancia": viaje["trip_distance"],
            "Costo_total": viaje["total_amount"]}
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


def req_1(catalog, pasajeros):
    """
    Retorna el resultado del requerimiento 1 - Juliana Rodríguez
    Calcular la información promedio de los trayectos dado una 
    cantidad de pasajeros.
    """
    # TODO: Modificar el requerimiento 1
    start = get_time()
    trayectos = 0
    duracion = 0 
    costo_total = 0
    distancia = 0
    peajes = 0
    propina = 0
    tipo_pago = {"CREDIT_CARD": 0, "CASH": 0, "NO_CHARGE": 0, "UNKNOWN": 0}
    fechas = {"fechas": lt.new_list(), "frecuencia": lt.new_list()}
    
    tam = lt.size(catalog["viajes"])
    for i in range(0,tam):
        viaje = lt.get_element(catalog["viajes"],i)
        dur = diferencia_tiempo(viaje)
        
        if viaje["passenger_count"] == int(pasajeros):
            trayectos += 1
            duracion += dur
            costo_total += viaje["total_amount"]
            distancia += viaje["trip_distance"]
            peajes += viaje["tolls_amount"]
            propina += viaje["tip_amount"]
            
            if viaje["payment_type"] == "CREDIT_CARD":
                tipo_pago["CREDIT_CARD"]+=1          
            elif viaje["payment_type"] == "CASH":
                tipo_pago["CASH"]+=1
            elif viaje["payment_type"] == "NO_CHARGE":
                tipo_pago["NO_CHARGE"]+=1
            elif viaje["payment_type"] == "UNKNOWN":
                tipo_pago["UNKNOWN"]+=1
            
            cmp_function = lt.default_function
            fecha_i = viaje["pickup_date"]
            ind = lt.is_present(fechas["fechas"],fecha_i, cmp_function)
            if ind is None:
                lt.add_last(fechas["fechas"], fecha_i)
                lt.add_last(fechas["frecuencia"],1)
            elif ind != None:
                frec = lt.get_element(fechas["frecuencia"],ind)
                lt.change_info(fechas["frecuencia"],ind,frec+1)

    duracion_prom = duracion/trayectos
    costo_prom = costo_total/trayectos
    distancia_prom = distancia/trayectos
    peajes_prom = peajes/trayectos
    propina_prom = propina/trayectos
    
    # encontrar el pago más frecuente
    pago_mayor = "CREDIT_CARD"
    mayor = tipo_pago["CREDIT_CARD"]
    if tipo_pago["CASH"] > mayor:
        mayor = tipo_pago["CASH"]
        pago_mayor = "CASH"
    elif  tipo_pago["NO_CHARGE"]>mayor:
        mayor = tipo_pago["NO_CHARGE"]
        pago_mayor = "NO_CHARGE"
    elif tipo_pago["UNKNOWN"]>mayor:
        mayor = tipo_pago["UNKNOWN"]
        pago_mayor = "UNKNOWN"
    
    pago_mas_usado = pago_mayor +" - "+str(mayor)
    
    # Encontrar el día más frecuente
    frecuencia = 0
    fecha_repetida = ""
    for i in range(0, lt.size(fechas["frecuencia"])):
        elem = lt.get_element(fechas["frecuencia"], i)
        if elem > frecuencia:
            frecuencia = elem
            fecha_repetida = lt.get_element(fechas["fechas"],i)
    
    end = get_time()  
    tiempo = delta_time(start, end)
    return tiempo, trayectos, duracion_prom, costo_prom, distancia_prom, peajes_prom, pago_mas_usado, propina_prom, fecha_repetida, frecuencia


def req_2(catalog, pago):
    start = get_time()
    total = lt.size(catalog["viajes"])
    contador = 0
    Duracion = 0
    filtro = []
    costo_total = 0
    distancia_total = 0
    peajes_total = 0
    pasajeros = {}
    pasa = 0
    cantidad = 0
    propina = 0
    fecha = {}
    fech = 0
    
    for i in range(0, total):
        viaje = lt.get_element(catalog["viajes"], i)
        if viaje["payment_type"] == pago:
            contador += 1
            filtro.append(viaje)
    
    for viaje in filtro:
        dur = diferencia_tiempo(viaje)
        Duracion += dur
        costo_total += viaje["total_amount"]
        distancia_total += viaje["trip_distance"]
        peajes_total += viaje["tolls_amount"]
        propina += viaje["tip_amount"]

        if viaje["passenger_count"] in pasajeros:
            pasajeros[viaje["passenger_count"]] += 1
        else:
            pasajeros[viaje["passenger_count"]] = 1

        fecha_fin = viaje["dropoff_date"]
        if fecha_fin in fecha:
            fecha[fecha_fin] += 1
        else:
            fecha[fecha_fin] = 1
    
    for key in pasajeros:
        if pasajeros[key] > pasa:
            pasa = pasajeros[key]
            cantidad = key
    
    fecha_mas_frec = None
    for key in fecha:
        if fecha[key] > fech:
            fech = fecha[key]
            fecha_mas_frec = key
    
    duracion = Duracion / contador
    costo = costo_total / contador
    distancia_total = distancia_total / contador
    peajes_total = peajes_total / contador
    propina = propina / contador
    cantidad_pasa = str(cantidad) + "-" + str(pasa)
    
    end = get_time()
    tiempo = delta_time(start, end)
    
    return round(tiempo,2), contador, round(duracion,2), round(costo,2), round(distancia_total,2), round(peajes_total,2), cantidad_pasa, round(propina,4), fecha_mas_frec


def req_3(catalog, maximo, minimo):
    start=get_time()
    tamano=lt.size(catalog["viajes"])
    trayectos=0
    duracion=0
    costo=0
    distancia=0
    peajes=0
    propina=0
    frecuencias_pasa={}
    frecuencias_fechas={}
    
    for i in range(0,tamano):
        viaje=lt.get_element(catalog["viajes"],i)
        if viaje["total_amount"]>=float(minimo) and viaje["total_amount"]<=float(maximo):
            trayectos+=1
            dura = diferencia_tiempo(viaje)
            duracion+=dura
            costo+=viaje["total_amount"]
            distancia+=viaje["trip_distance"]
            peajes+=viaje["tolls_amount"]
            propina+=viaje["tip_amount"]
              
            if viaje["passenger_count"] in frecuencias_pasa:
                frecuencias_pasa[viaje["passenger_count"]]+=1
            else:
                frecuencias_pasa[viaje["passenger_count"]]=1
            
            if viaje["dropoff_date"] in frecuencias_fechas:
                frecuencias_fechas[viaje["dropoff_date"]]+=1
            else:
                frecuencias_fechas[viaje["dropoff_date"]]=1
            
    duracion_prom=duracion/trayectos
    costo_prom=costo/trayectos
    distancia_prom=distancia/trayectos
    peajes_prom=peajes/trayectos
    propina_prom=propina/trayectos
       
    max_cantidad = 0
    num_pasajeros = 0
    for key in frecuencias_pasa:
        if frecuencias_pasa[key] > max_cantidad:
            max_cantidad = frecuencias_pasa[key]  
            num_pasajeros = key              

    max_cpasajeros = str(num_pasajeros) + " - " + str(max_cantidad)

    max_fech = 0
    fecha_frec = None
    for key in frecuencias_fechas:
        if frecuencias_fechas[key] > max_fech:
            max_fech = frecuencias_fechas[key]
            fecha_frec = key             
    end=get_time()
    tiempo=delta_time(start,end)
    return round(tiempo,2), trayectos, round(duracion_prom,2), round(costo_prom,2), round(distancia_prom,2), round(peajes_prom,2), max_cpasajeros, round(propina_prom,4), fecha_frec
              

def req4(catalog, filtro, fecha_inicial, fecha_final):
    start = get_time()
    viajes = catalog["viajes"]
    barrios = catalog["barrios"]
    tamaño = lt.size(viajes)
    resultados = []
    total_trayectos = 0

    for i in range(0, tamaño):   # índice base 0
        viaje = lt.get_element(viajes, i)
        fecha = viaje["pickup_date"]  # YYYY-MM-DD

        if fecha_inicial <= fecha <= fecha_final:
            origen = barrio_mas_cercano(viaje["pickup_latitude"], viaje["pickup_longitude"], barrios)
            destino = barrio_mas_cercano(viaje["dropoff_latitude"], viaje["dropoff_longitude"], barrios)

            if origen != destino:
                # calcular duración en minutos
                ini = viaje["pickup_datetime"]
                fin = viaje["dropoff_datetime"]
                duracion = (int(fin[11:13]) * 60 + int(fin[14:16])) - (int(ini[11:13]) * 60 + int(ini[14:16]))
                if duracion < 0:
                    duracion += 1440

                # buscar si ya existe combinación en resultados
                encontrado = False
                j = 0
                while j < len(resultados):
                    r = resultados[j]
                    if r["origen"] == origen and r["destino"] == destino:
                        r["distancia"] += viaje["trip_distance"]
                        r["duracion"]  += duracion
                        r["costo"]     += viaje["total_amount"]
                        r["conteo"]    += 1
                        encontrado = True
                    j += 1

                if not encontrado:
                    resultados.append({
                        "origen": origen,
                        "destino": destino,
                        "distancia": viaje["trip_distance"],
                        "duracion": duracion,
                        "costo": viaje["total_amount"],
                        "conteo": 1
                    })
                total_trayectos += 1

    # elegir mejor combinación
    mejor = None
    mejor_valor = None
    k = 0
    while k < len(resultados):
        r = resultados[k]
        promedio_costo = r["costo"] / r["conteo"]

        if filtro == "MAYOR":
            if mejor_valor is None or promedio_costo > mejor_valor:
                mejor = r
                mejor_valor = promedio_costo
        else:  # MENOR
            if mejor_valor is None or promedio_costo < mejor_valor:
                mejor = r
                mejor_valor = promedio_costo
        k += 1

    end = get_time()
    tiempo = delta_time(start, end)

    if mejor:
        return (tiempo, filtro, total_trayectos, mejor["origen"], mejor["destino"], mejor["distancia"] / mejor["conteo"], mejor["duracion"] / mejor["conteo"], mejor["costo"] / mejor["conteo"])
    else:
        return {"mensaje": "No hay trayectos en ese rango de fechas"}
    

def req_5(catalog, filtro, fecha_menor, fecha_mayor):
    """
    Retorna el resultado del requerimiento 5
    """
    start = get_time()

    franjas = lt.new_list()
    for h in range(24):
        lt.add_last(franjas, f"[{h} - {h+1})")  
    sum_cost   = [0.0]*24
    count_tr   = [0]*24
    sum_durmin = [0.0]*24
    sum_pax    = [0]*24
    max_cost   = [float("-inf")]*24
    max_drop   = [""]*24
    min_cost   = [float("inf")]*24
    min_drop   = [""]*24

    viajes = catalog["viajes"]
    tamano = lt.size(viajes)
    trayectos_filtro = 0

    for i in range(0, tamano):
        viaje = lt.get_element(viajes, i)
        fecha_inicio_str = str(viaje["pickup_datetime"])[:10]
        if fecha_inicio_str >= fecha_menor and fecha_inicio_str <= fecha_mayor:
            trayectos_filtro += 1

            fech_ini = str(viaje["pickup_datetime"])
            fech_fin = str(viaje["dropoff_datetime"])
            viaje["pickup_time"]  = fech_ini[11:16]
            viaje["dropoff_time"] = fech_fin[11:16]
            duracion_min = diferencia_tiempo(viaje)
            hora = int(viaje["pickup_time"][:2])

            costo_viaje = float(viaje["total_amount"])
            pasajeros   = int(viaje["passenger_count"])

            sum_cost[hora]   += costo_viaje
            count_tr[hora]   += 1
            sum_durmin[hora] += duracion_min
            sum_pax[hora]    += pasajeros

            if (costo_viaje > max_cost[hora]) or (costo_viaje == max_cost[hora] and fech_fin > max_drop[hora]):
                max_cost[hora] = costo_viaje
                max_drop[hora] = fech_fin

            if (costo_viaje < min_cost[hora]) or (costo_viaje == min_cost[hora] and fech_fin > min_drop[hora]):
                min_cost[hora] = costo_viaje
                min_drop[hora] = fech_fin

    mejor_index = -1
    mejor_prom_costo = None

    for hora in range(24):
        if count_tr[hora] == 0:
            continue
        promedio_costo = sum_cost[hora] / count_tr[hora]
        if filtro == "MAYOR":
            if mejor_index == -1 or promedio_costo > mejor_prom_costo:
                mejor_index, mejor_prom_costo = hora, promedio_costo
        else:  
            if mejor_index == -1 or promedio_costo < mejor_prom_costo:
                mejor_index, mejor_prom_costo = hora, promedio_costo

    end = get_time()
    tiempo_e = delta_time(start, end)
    
    if mejor_index == -1:
        return ("no hay datos que cumplan con el filtro")
    franja     = lt.get_element(franjas, mejor_index)
    costo_promedio = sum_cost[mejor_index] / count_tr[mejor_index]
    duracion_prom  = sum_durmin[mejor_index] / count_tr[mejor_index]
    pasajeros_prom = sum_pax[mejor_index] / count_tr[mejor_index]

    return (tiempo_e,filtro,trayectos_filtro,franja,costo_promedio,count_tr[mejor_index],duracion_prom,pasajeros_prom,max_cost[mejor_index],min_cost[mejor_index])

def req_6(catalog, barrio, fecha_i, fecha_f):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    start = get_time()
    trayectos = 0
    distancia = 0
    tiempo = 0
    b_fin = {"barrio": lt.new_list(), "frecuencia": lt.new_list()}
    size = lt.size(catalog["viajes"])
    pagos = lt.new_list()
    info_pagos = []
    for i in range(0, size):
        viaje = lt.get_element(catalog["viajes"],i)
        #Requerimiento de fecha
        fecha = viaje["pickup_date"]
        if fecha >= fecha_i and fecha <= fecha_f:
            lat = viaje["pickup_latitude"]
            long = viaje["pickup_longitude"]
            barrio_salida = barrio_mas_cercano(lat, long, catalog["barrios"])
            if barrio == barrio_salida:
                trayectos += 1
                distancia += viaje["trip_distance"]
                tmp= diferencia_tiempo(viaje)
                tiempo += tmp
                
                f_latitud = viaje["dropoff_latitude"]
                f_longitud = viaje["dropoff_longitude"]
                barrio_destino = barrio_mas_cercano(f_latitud, f_longitud, catalog["barrios"])
                cmp_function = lt.default_function
                ind = lt.is_present(b_fin["barrio"],barrio_destino, cmp_function)
                if ind is None and barrio_destino != barrio:
                    lt.add_last(b_fin["barrio"], barrio_destino)
                    lt.add_last(b_fin["frecuencia"],1)
                elif ind != None:
                    frec = lt.get_element(b_fin["frecuencia"], ind)
                    lt.change_info(b_fin["frecuencia"],ind,frec+1)
                
                #metodo pagos
                tipo = viaje["payment_type"]
                ind = lt.is_present(pagos, tipo, cmp_function) 
                if ind is None:
                    lt.add_last(pagos, tipo)
                    info_pagos.append({"Tipo pago": tipo, "Num tray": 1, "Precio":viaje["total_amount"], "Tiempo": tiempo})
                    
                elif ind != None:
                    info_pagos[ind]["Num tray"] += 1
                    info_pagos[ind]["Precio"] += viaje["total_amount"]
                    info_pagos[ind]["Tiempo"] += tmp
                    
    # barrio destino más repetido           
    frecuencia = 0
    destino_repetido = ""
    for i in range(0, lt.size(b_fin["frecuencia"])):
        elem = lt.get_element(b_fin["frecuencia"], i)
        if elem > frecuencia:
            frecuencia = elem
            destino_repetido = lt.get_element(b_fin["barrio"],i)
            
    distancia_prom = distancia/trayectos
    tiempo_prom = tiempo/trayectos
    
    mayor1 = 0 #num trayectos
    mayor2 = 0 #más recaudo
    for i in range(0, lt.size(pagos)):
        if mayor2 < info_pagos[i]["Precio"]:
            mayor2 = info_pagos[i]["Precio"]
            mayor_recaudo = i
        if mayor1 < info_pagos[i]["Num tray"]:
            mayor1 = info_pagos[i]["Num tray"]
            mas_usado = i
        
        info_pagos[i]["Precio"] = info_pagos[i]["Precio"]/info_pagos[i]["Num tray"]
        info_pagos[i]["Tiempo"] = info_pagos[i]["Tiempo"]/info_pagos[i]["Num tray"]
    
    info_pagos[mas_usado]["¿Más usado?"] = "Sí"
    info_pagos[mayor_recaudo]["¿Mayor recaudo?"] = "Sí"
        
    end = get_time()
    t = delta_time(start, end)
    return t, trayectos, distancia_prom, tiempo_prom, destino_repetido, info_pagos


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
