import sys
import tabulate as tb
import App.logic as logic
from DataStructures.List import array_list as lt
from DataStructures.Map import map_linear_probing as mp
from DataStructures.Map import map_entry as me
import datetime as datetime
default_limit = 1000
sys.setrecursionlimit(default_limit*10) 

def new_logic():
    """
        Se crea una instancia del controlador
    """
    #TODO: Llamar la función de la lógica donde se crean las estructuras de datos
    control = logic.new_logic()
    return control    

def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Ejecutar Requerimiento 1")
    print("3- Ejecutar Requerimiento 2")
    print("4- Ejecutar Requerimiento 3")
    print("5- Ejecutar Requerimiento 4")
    print("6- Ejecutar Requerimiento 5")
    print("7- Ejecutar Requerimiento 6")
    print("0- Salir")

def load_data(control):
    """
    Carga los datos
    """
    #TODO: Realizar la carga de datos
    filename = input('Diga el archivo que quiere evaluar (small, medium, large)\n').strip()
    filename = "data/taxis-"+filename+".csv"
    tiempo = logic.load_data(control, filename)
    total = lt.size(control["viajes"])
    menor = 99999999999999
    mayor = 0.0
    for i in range(0, total):
        viaje = lt.get_element(control["viajes"], i)
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
        viaje = lt.get_element(control["viajes"], i)
        duracion = logic.diferencia_tiempo(viaje)
        info = {"Id_trayecto": viaje["id"],
            "Fecha/Hora inicio": viaje["pickup_datetime"],
            "Fecha/Hora destino": viaje["dropoff_datetime"],
            "Duración (min)": duracion,
            "Distancia (millas)": viaje["trip_distance"],
            "Costo total": viaje["total_amount"]}
        primeros.append(info)
    
    ultimos = []
    for i in range (total-5, total):
        viaje = lt.get_element(control["viajes"], i)
        duracion = logic.diferencia_tiempo(viaje)
        viaje = lt.get_element(control["viajes"], i)
        info = {"Id_trayecto": viaje["id"],
            "Fecha/Hora inicio": viaje["pickup_datetime"],
            "Fecha/Hora destino": viaje["dropoff_datetime"],
            "Duración (min)": duracion,
            "Distancia (millas)": viaje["trip_distance"],
            "Costo total": viaje["total_amount"]}
        ultimos.append(info)
    
    print("\nTiempo de carga: "+str(tiempo)+" [ms].\
        \nTotal de trayectos: "+str(total)+" trayectos.\
        \nEl trayecto con menor distancia es el "+str(menorid)+":  \t Distancia: "+str(menor)+" [millas]\t Fecha: "+str(fecha_menor)+"\tCosto: $"+str(costo_menor)+"\n\
        \nEl trayecto con mayor distancia es el "+str(mayorid)+":  \t Distancia: "+str(mayor)+" [millas]\t Fecha: "+str(fecha_mayor)+"\tCosto: $"+str(costo_mayor)+"\n\
        \nLos primeros 5 viajes fueron:\n"+ tb.tabulate(primeros, headers="keys") +"\n\nLos últimos 5 viajes fueron: \n"+ tb.tabulate(ultimos, headers="keys")+"\n")


def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    identificacion = int(input("Indique el Id del viaje que desea ver: "))
    dato = logic.get_data(control, identificacion)
    print(dato)

def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    fecha_i = input("Indique la fecha inicial: ")
    fecha_f = input("Indique la fecha final: ")
    muestra = int(input("Indique la cantidad de viajes que quiere ver: "))
    tiempo, trayectos, viajes_organizados= logic.req_1(control, fecha_i, fecha_f, muestra)
    print("\nTiempo de ejecución del requerimiento en [ms]: "+str(round(tiempo,5)) +"\nTrayectos dentro del rango de fechas: " + str(trayectos)+"\n")
    
    if trayectos >=  2*muestra:
        m1 = []
        for j in range(muestra):
            viaje = lt.get_element(viajes_organizados, j)
            lista = {}
            lista["F/T Inicio"]=viaje["pickup_datetime"]
            lista["Lat y long Inicio"]=f'[{viaje["pickup_latitude"]},{viaje["pickup_longitude"]}]'
            lista["F/T Fin"]=viaje["dropoff_datetime"]
            lista["Lat y long fin"]=f'[{viaje["dropoff_latitude"]},{viaje["dropoff_longitude"]}]'
            lista["Distancia (millas)"]=viaje["trip_distance"]
            lista["Costo total"]=viaje["total_amount"]
            m1.append(lista)
        print("Primeros viajes:")
        print(tb.tabulate(m1, headers="keys", tablefmt="simple_grid"))
        m2 = []
        for j in range(lt.size(viajes_organizados)-muestra,lt.size(viajes_organizados)):
            viaje = lt.get_element(viajes_organizados, j)
            lista = {}
            lista["F/T Inicio"]=viaje["pickup_datetime"]
            lista["Lat y long Inicio"]=f'[{viaje["pickup_latitude"]},{viaje["pickup_longitude"]}]'
            lista["F/T Fin"]=viaje["dropoff_datetime"]
            lista["Lat y long fin"]=f'[{viaje["dropoff_latitude"]},{viaje["dropoff_longitude"]}]'
            lista["Distancia (millas)"]=viaje["trip_distance"]
            lista["Costo total"]=viaje["total_amount"]
            m2.append(lista)
        print("\n Últimos viajes:")
        print(tb.tabulate(m2, headers="keys", tablefmt="simple_grid"))
    elif trayectos < 2*muestra:
        m = []
        for k in range(lt.size(viajes_organizados)):
            viaje = lt.get_element(viajes_organizados, k)
            lista = {}
            lista["F/T Inicio"]=viaje["pickup_datetime"]
            lista["Lat y long Inicio"]=f'[{viaje["pickup_latitude"]},{viaje["pickup_longitude"]}]'
            lista["F/T Fin"]=viaje["dropoff_datetime"]
            lista["Lat y long fin"]=f'[{viaje["dropoff_latitude"]},{viaje["dropoff_longitude"]}]'
            lista["Distancia (millas)"]=viaje["trip_distance"]
            lista["Costo total"]=viaje["total_amount"]
            m.append(lista)
        print("\nTodos los viajes:")
        print(tb.tabulate(m, headers="keys", tablefmt="simple_grid"))
    



def print_req_2(control):
    """
    Imprime la solución del Requerimiento 2 en consola, respetando el orden.
    Soporta ambos formatos que retorna logic.req_2:
      A) {"Primeros viajes:": lt.list, "Últimos viajes:": lt.list}
      B) mp.map con todos los viajes (cuando total < 2 * tamano_muestra)
    """
    tamano = int(input("Indique el tamaño de la muestra: "))
    coord_ini = float(input("Indique la coordenada inicial de latitud: "))
    coord_fin = float(input("Indique la coordenada final de latitud: "))

    tiempo, total, viajes = logic.req_2(control, coord_ini, coord_fin, tamano)

    print("\n=== Requerimiento 2: Trayectos en rango de latitud ===")
    print(f"Tiempo de ejecución en ms: {tiempo}")
    print(f"Trayectos dentro del rango de latitud: {total}")

    # --- helpers locales SOLO dentro de esta función (no afecta otras) ---
    def pick(d, *keys, default="—"):
        for k in keys:
            if k in d:
                return d[k]
        return default

    def _print_info(info: dict):
        # Si por algún motivo vino como {"id":..., "datos": {...}}, destápalo
        if isinstance(info, dict) and "datos" in info and isinstance(info["datos"], dict):
            base = info["datos"]
            base.setdefault("Id_trayecto", info.get("id", info.get("Id_trayecto")))
            info = base

        id_tray = pick(info, "Id_trayecto", "id", "ID")

        ini_dt = pick(info,
            "Fecha y hora de recogida", "Fecha y tiempo recogida", "Fecha/Hora inicio",
            "pickup_datetime", "tpep_pickup_datetime"
        )
        ini_xy = pick(info,
            "Latitud y longitud de recogida", "Latitud y longitud recogida",
            "pickup_xy", "pickup_coords"
        )

        fin_dt = pick(info,
            "Fecha y hora de terminación", "Fecha y tiempo de terminación", "Fecha/Hora destino",
            "dropoff_datetime", "tpep_dropoff_datetime"
        )
        fin_xy = pick(info,
            "Latitud y longitud de terminación", "dropoff_xy", "dropoff_coords"
        )

        dist  = pick(info, "Distancia (millas)", "trip_distance", default=0)
        costo = pick(info, "Costo total", "total_amount", default=0)

        print(f"  • ID: {id_tray}")
        print(f"    Fecha y hora de recogida     : {ini_dt}")
        if ini_xy != "—":
            print(f"    Lat/Lon de recogida          : {ini_xy}")
        print(f"    Fecha y hora de terminación  : {fin_dt}")
        if fin_xy != "—":
            print(f"    Lat/Lon de terminación       : {fin_xy}")
        print(f"    Distancia                    : {dist} mi")
        print(f"    Costo                        : ${costo}\n")

    def _print_list(titulo: str, lst):
        print(f"\n-- {titulo} --")
        for i in range(0, lt.size(lst)):  # 0-based
            info = lt.get_element(lst, i)
            _print_info(info)

    # --- impresión según formato devuelto por logic ---
    if isinstance(viajes, dict) and "Primeros viajes:" in viajes:
        _print_list("Primeros viajes", viajes["Primeros viajes:"])
        _print_list("Últimos viajes", viajes["Últimos viajes:"])

    elif isinstance(viajes, dict) and "table" in viajes and "capacity" in viajes:
        print("\n-- Todos los trayectos (menos de 2N) --")
        items = []
        cap = viajes["capacity"]
        for i in range(0, cap):  # 0-based
            entry = lt.get_element(viajes["table"], i)
            if me.get_key(entry) is not None:
                items.append(entry["value"])  # dict 'info'

        # Orden preferente por _orden si existe; si no, por fecha de recogida
        if items and isinstance(items[0], dict) and "_orden" in items[0]:
            items.sort(key=lambda x: x["_orden"])
        else:
            items.sort(key=lambda x: pick(
                x,
                "Fecha y hora de recogida", "Fecha y tiempo recogida", "Fecha/Hora inicio",
                "pickup_datetime", "tpep_pickup_datetime",
                default=""
            ))
        for info in items:
            _print_info(info)

    else:
        print("\n(Formato de salida no reconocido por el view)")

    

def print_req_3(control):
    """
        Imprime la solución del Requerimiento 3 (distancia de trayectos)
    """
    distancia_min = float(input("Ingrese la distancia mínima (en millas): "))
    distancia_max = float(input("Ingrese la distancia máxima (en millas): "))
    cantidad_mostrar = int(input("Ingrese el número de trayectos a mostrar (N): "))

    tiempo, total_trayectos, viajes_ordenados = logic.req_3(control, distancia_min, distancia_max, cantidad_mostrar)

    print("\nTiempo de ejecución del requerimiento en [ms]:", round(tiempo, 5))
    print("Total de trayectos dentro del rango de distancia:", total_trayectos, "\n")

    # Si hay suficientes viajes, mostrar primeros N y últimos N
    if total_trayectos >= 2 * cantidad_mostrar:
        primeros = []
        for i in range(cantidad_mostrar):
            viaje = lt.get_element(viajes_ordenados, i)
            fila = {
                "Fecha/Hora inicio": viaje["pickup_datetime"],
                "Coord inicio": f'[{viaje["pickup_latitude"]}, {viaje["pickup_longitude"]}]',
                "Fecha/Hora fin": viaje["dropoff_datetime"],
                "Coord fin": f'[{viaje["dropoff_latitude"]}, {viaje["dropoff_longitude"]}]',
                "Distancia (millas)": viaje["trip_distance"],
                "Costo total ($)": viaje["total_amount"]
            }
            primeros.append(fila)

        print("Primeros trayectos del rango:")
        print(tb.tabulate(primeros, headers="keys", tablefmt="simple_grid"))

        ultimos = []
        for i in range(lt.size(viajes_ordenados) - cantidad_mostrar, lt.size(viajes_ordenados)):
            viaje = lt.get_element(viajes_ordenados, i)
            fila = {
                "Fecha/Hora inicio": viaje["pickup_datetime"],
                "Coord inicio": f'[{viaje["pickup_latitude"]}, {viaje["pickup_longitude"]}]',
                "Fecha/Hora fin": viaje["dropoff_datetime"],
                "Coord fin": f'[{viaje["dropoff_latitude"]}, {viaje["dropoff_longitude"]}]',
                "Distancia (millas)": viaje["trip_distance"],
                "Costo total ($)": viaje["total_amount"]
            }
            ultimos.append(fila)

        print("\nÚltimos trayectos del rango:")
        print(tb.tabulate(ultimos, headers="keys", tablefmt="simple_grid"))

    # Si hay pocos viajes, mostrar todos
    else:
        todos = []
        for i in range(lt.size(viajes_ordenados)):
            viaje = lt.get_element(viajes_ordenados, i)
            fila = {
                "Fecha/Hora inicio": viaje["pickup_datetime"],
                "Coord inicio": f'[{viaje["pickup_latitude"]}, {viaje["pickup_longitude"]}]',
                "Fecha/Hora fin": viaje["dropoff_datetime"],
                "Coord fin": f'[{viaje["dropoff_latitude"]}, {viaje["dropoff_longitude"]}]',
                "Distancia (millas)": viaje["trip_distance"],
                "Costo total ($)": viaje["total_amount"]
            }
            todos.append(fila)

        print("Trayectos encontrados en el rango:")
        print(tb.tabulate(todos, headers="keys", tablefmt="simple_grid"))

    

def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    f_terminacion = input("Indique la fecha de terminación: ")
    t_ref = input("Indique el tiempo de referencia: ")
    criterio = input("Indique si quiere los viajes antes o después al tiempo de referencia (sin tildes): ")
    muestra = int(input("Indique la muestra del viaje: "))
       
    tiempo, trayectos, viajes_organizados = logic.req_4(control, f_terminacion, t_ref, criterio, muestra)
    print("Tiempo de ejecución en ms: " + str(round(tiempo,5)))
    print("Trayectos ["+criterio+"] que cumplieron los requisitos de fecha y hora de terminación: " + str(trayectos))
    
    if trayectos >= 2*muestra:
        primeros = []
        ultimos = []
        for i in range(muestra):
            viaje = lt.get_element(viajes_organizados, i)
            lista = {}
            lista["F/T Inicio"]=viaje["pickup_datetime"]
            lista["Lat y long Inicio"]=f'[{viaje["pickup_latitude"]},{viaje["pickup_longitude"]}]'
            lista["F/T Fin"]=viaje["dropoff_datetime"]
            lista["Lat y long fin"]=f'[{viaje["dropoff_latitude"]},{viaje["dropoff_longitude"]}]'
            lista["Distancia (millas)"]=viaje["trip_distance"]
            lista["Costo total"]=viaje["total_amount"]
            primeros.append(lista) 
            
        for j in range(lt.size(viajes_organizados)-muestra,lt.size(viajes_organizados)):
            viaje = lt.get_element(viajes_organizados, j)
            lista = {}
            lista["F/T Inicio"]=viaje["pickup_datetime"]
            lista["Lat y long Inicio"]=f'[{viaje["pickup_latitude"]},{viaje["pickup_longitude"]}]'
            lista["F/T Fin"]=viaje["dropoff_datetime"]
            lista["Lat y long fin"]=f'[{viaje["dropoff_latitude"]},{viaje["dropoff_longitude"]}]'
            lista["Distancia (millas)"]=viaje["trip_distance"]
            lista["Costo total"]=viaje["total_amount"]
            ultimos.append(lista) 
        print("\n Primeros viajes:")
        print(tb.tabulate(primeros, headers="keys", tablefmt="simple_grid"))
        print("\n Últimos viajes:")
        print(tb.tabulate(ultimos, headers="keys", tablefmt="simple_grid"))
        
    elif trayectos < 2*muestra:
        m = []
        for k in range(lt.size(viajes_organizados)):
            viaje = lt.get_element(viajes_organizados, k)
            lista = {}
            lista["F/T Inicio"]=viaje["pickup_datetime"]
            lista["Lat y long Inicio"]=f'[{viaje["pickup_latitude"]},{viaje["pickup_longitude"]}]'
            lista["F/T Fin"]=viaje["dropoff_datetime"]
            lista["Lat y long fin"]=f'[{viaje["dropoff_latitude"]},{viaje["dropoff_longitude"]}]'
            lista["Distancia (millas)"]=viaje["trip_distance"]
            lista["Costo total"]=viaje["total_amount"]
            m.append(lista)
        print("\nTodos los viajes:")
        print(tb.tabulate(m, headers="keys", tablefmt="simple_grid"))
    
def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5


def print_req_6(control):
    barrio = input("Barrio: ")
    hora_ini = input("Hora inicial (HH): ")
    hora_fin = input("Hora final (HH): ")
    N = int(input("Tamaño de la muestra: "))

    t, total, viajes = logic.req_6(control, barrio, hora_ini, hora_fin, N)

    print("\n=== Requerimiento 6 ===")
    print(f"Tiempo (ms): {t}")
    print(f"Trayectos filtrados: {total}")

    def p(info):  # imprime un item dict del logic
        print(f"  • ID: {info['Id_trayecto']}")
        print(f"    Recogida: {info.get('Fecha y tiempo recogida')}")
        print(f"    [lat,lon] recogida: {info.get('Latitud y longitud recogida')}")
        fin = info.get('Fecha y tiempo de terminación', info.get('Fecha y hora de terminación'))
        print(f"    Terminación: {fin}")
        print(f"    [lat,lon] terminación: {info.get('Latitud y longitud de terminación')}")
        print(f"    Distancia: {info['Distancia (millas)']} mi")
        print(f"    Costo: ${info['Costo total']}\n")

    if isinstance(viajes, dict) and "Primeros viajes:" in viajes:
        for titulo in ("Primeros viajes:", "Últimos viajes:"):
            print(f"\n-- {titulo[:-1]} --")
            lst = viajes[titulo]
            for i in range(0, lt.size(lst)):
                p(lt.get_element(lst, i))
    else:
        print("\n-- Todos (<2N) --")
        cap = viajes["capacity"]
        for i in range(0, cap):
            e = lt.get_element(viajes["table"], i)
            if me.get_key(e) is None: 
                continue
            vals = e["value"]  # es una lt.list con 6 campos en orden
            print(f"  • ID: {me.get_key(e)}")
            print(f"    Recogida: {lt.get_element(vals, 0)}")
            print(f"    [lat,lon] recogida: {lt.get_element(vals, 1)}")
            print(f"    Terminación: {lt.get_element(vals, 2)}")
            print(f"    [lat,lon] terminación: {lt.get_element(vals, 3)}")
            print(f"    Distancia: {lt.get_element(vals, 4)} mi")
            print(f"    Costo: ${lt.get_element(vals, 5)}\n")

    

# Se crea la lógica asociado a la vista
control = new_logic()

# main del ejercicio
def main():
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 1:
            print("Cargando información de los archivos ....\n")
            data = load_data(control)
        elif int(inputs) == 2:
            print_req_1(control)

        elif int(inputs) == 3:
            print_req_2(control)

        elif int(inputs) == 4:
            print_req_3(control)

        elif int(inputs) == 5:
            print_req_4(control)

        elif int(inputs) == 6:
            print_req_5(control)

        elif int(inputs) == 7:
            print_req_6(control)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa") 
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
