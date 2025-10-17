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
    tamano = int(input("Indique el tamaño de la muestra: "))
    coord_ini = float(input("Indique la coordenada inicial de latitud: "))
    coord_fin = float(input("Indique la coordenada final de latitud: "))
    tiempo, total, viajes = logic.req_2(control, coord_ini, coord_fin, tamano)

    print("\n=== Requerimiento 2: Trayectos en rango de latitud ===")
    print(f"Tiempo de ejecución en ms: {tiempo}")
    print(f"Trayectos dentro del rango de latitud: {total}")

    if "Primeros viajes:" in viajes:
        for titulo in ("Primeros viajes:", "Últimos viajes:"):
            print(f"\n-- {titulo[:-1]} --")
            lst = viajes[titulo]
            sz = lt.size(lst)
            i = 0
            while i < sz:
                info = lt.get_element(lst, i)
                print(f"  • ID: {info.get('Id_trayecto', info.get('id'))}")
                print(f"    Recogida: {info.get('Fecha y hora de recogida') or info.get('Fecha y tiempo recogida') or info.get('Fecha/Hora inicio') or info.get('pickup_datetime')}")
                print(f"    [lat,lon] recogida: {info.get('Latitud y longitud de recogida') or info.get('Latitud y longitud recogida')}")
                print(f"    Terminación: {info.get('Fecha y hora de terminación') or info.get('Fecha y tiempo de terminación') or info.get('Fecha/Hora destino') or info.get('dropoff_datetime')}")
                print(f"    [lat,lon] terminación: {info.get('Latitud y longitud de terminación')}")
                print(f"    Distancia: {info.get('Distancia (millas)', info.get('trip_distance'))} mi")
                print(f"    Costo: ${info.get('Costo total', info.get('total_amount'))}\n")
                i += 1
    elif ("table" in viajes) and ("capacity" in viajes):
        cap = viajes["capacity"]
        items = []
        i = 0
        while i < cap:
            e = lt.get_element(viajes["table"], i)
            k = me.get_key(e)
            if k is not None:
                items.append(e["value"])  
            i += 1

        if len(items) > 0 and ("_orden" in items[0]):
            items.sort(key=lambda x: x["_orden"])
        else:
            items.sort(key=lambda x: x.get("Fecha y hora de recogida") or x.get("pickup_datetime") or "")

        j = 0
        n = len(items)
        while j < n:
            info = items[j]
            print(f"  • ID: {info.get('Id_trayecto', info.get('id'))}")
            print(f"    Recogida: {info.get('Fecha y hora de recogida') or info.get('Fecha y tiempo recogida') or info.get('pickup_datetime')}")
            print(f"    [lat,lon] recogida: {info.get('Latitud y longitud de recogida')}")
            print(f"    Terminación: {info.get('Fecha y hora de terminación') or info.get('Fecha y tiempo de terminación') or info.get('dropoff_datetime')}")
            print(f"    [lat,lon] terminación: {info.get('Latitud y longitud de terminación')}")
            print(f"    Distancia: {info.get('Distancia (millas)', info.get('trip_distance'))} mi")
            print(f"    Costo: ${info.get('Costo total', info.get('total_amount'))}\n")
            j += 1
    
    

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
    #fecha_hora = input("Indique la fecha y hora de terminación (AAAA-MM-DD HH): ")
    #muestra = int(input("Indique la cantidad de trayectos a mostrar: "))

    fecha_hora = input("Indique la fecha y hora de terminación (AAAA-MM-DD HH): ")
    muestra = int(input("Indique la cantidad de trayectos a mostrar: "))
    tiempo, trayectos, viajes_organizados = logic.req_5(control, fecha_hora, muestra)

    print("\nTiempo de ejecución en ms: " + str(round(tiempo, 5)))
    print("Trayectos que cumplen con la fecha y hora de terminación '" + fecha_hora + "': " + str(trayectos))

    if trayectos == 0:
        print("\nNo se encontraron trayectos para esa fecha y hora.")
        return

    if trayectos >= 2 * muestra:
        primeros = []
        ultimos = []
        # primeros N
        for i in range(muestra):
            viaje = lt.get_element(viajes_organizados["Primeros"], i)
            lista = {}
            lista["F/T Inicio"] = viaje["pickup_datetime"]
            lista["Lat y long Inicio"] = f'[{viaje["pickup_latitude"]},{viaje["pickup_longitude"]}]'
            lista["F/T Fin"] = viaje["dropoff_datetime"]
            lista["Lat y long Fin"] = f'[{viaje["dropoff_latitude"]},{viaje["dropoff_longitude"]}]'
            lista["Distancia (millas)"] = viaje["trip_distance"]
            lista["Costo total"] = viaje["total_amount"]
            primeros.append(lista)

        # últimos N
        for j in range(lt.size(viajes_organizados["Ultimos"])):
            viaje = lt.get_element(viajes_organizados["Ultimos"], j)
            lista = {}
            lista["F/T Inicio"] = viaje["pickup_datetime"]
            lista["Lat y long Inicio"] = f'[{viaje["pickup_latitude"]},{viaje["pickup_longitude"]}]'
            lista["F/T Fin"] = viaje["dropoff_datetime"]
            lista["Lat y long Fin"] = f'[{viaje["dropoff_latitude"]},{viaje["dropoff_longitude"]}]'
            lista["Distancia (millas)"] = viaje["trip_distance"]
            lista["Costo total"] = viaje["total_amount"]
            ultimos.append(lista)

        print("\nPrimeros viajes:")
        print(tb.tabulate(primeros, headers="keys", tablefmt="simple_grid"))
        print("\nÚltimos viajes:")
        print(tb.tabulate(ultimos, headers="keys", tablefmt="simple_grid"))

    else:
        m = []
        for k in range(lt.size(viajes_organizados)):
            viaje = lt.get_element(viajes_organizados, k)
            lista = {}
            lista["F/T Inicio"] = viaje["pickup_datetime"]
            lista["Lat y long Inicio"] = f'[{viaje["pickup_latitude"]},{viaje["pickup_longitude"]}]'
            lista["F/T Fin"] = viaje["dropoff_datetime"]
            lista["Lat y long Fin"] = f'[{viaje["dropoff_latitude"]},{viaje["dropoff_longitude"]}]'
            lista["Distancia (millas)"] = viaje["trip_distance"]
            lista["Costo total"] = viaje["total_amount"]
            m.append(lista)

        print("\nTodos los viajes encontrados:")
        print(tb.tabulate(m, headers="keys", tablefmt="simple_grid"))


def print_req_6(control):
    barrio = input("Barrio: ")
    hora_ini = input("Hora inicial (HH): ")
    hora_fin = input("Hora final (HH): ")
    N = int(input("Tamaño de la muestra: "))

    t, total, viajes = logic.req_6(control, barrio, hora_ini, hora_fin, N)

    print("\n=== Requerimiento 6: Trayectos por barrio y rango de horas ===")
    print(f"Tiempo (ms): {t}")
    print(f"Trayectos filtrados: {total}")

    if "Primeros viajes:" in viajes:
        for titulo in ("Primeros viajes:", "Últimos viajes:"):
            print(f"\n-- {titulo[:-1]} --")
            lst = viajes[titulo]
            sz = lt.size(lst)
            i = 0
            while i < sz:
                info = lt.get_element(lst, i)
                fin_txt = info.get('Fecha y tiempo de terminación')
                if fin_txt is None:
                    fin_txt = info.get('Fecha y hora de terminación')
                print(f"  • ID: {info['Id_trayecto']}")
                print(f"    Recogida: {info['Fecha y tiempo recogida']}")
                print(f"    [lat,lon] recogida: {info['Latitud y longitud recogida']}")
                print(f"    Terminación: {fin_txt}")
                print(f"    [lat,lon] terminación: {info['Latitud y longitud de terminación']}")
                print(f"    Distancia: {info['Distancia (millas)']} mi")
                print(f"    Costo: ${info['Costo total']}\n")
                i += 1
    elif ("table" in viajes) and ("capacity" in viajes):
        print("\n-- Todos los trayectos (<2N) --")
        cap = viajes["capacity"]
        i = 0
        while i < cap:
            e = lt.get_element(viajes["table"], i)
            k = me.get_key(e)
            if k is not None:
                vals = e["value"]  # lt.list con 6 campos en orden
                print(f"  • ID: {k}")
                print(f"    Recogida: {lt.get_element(vals, 0)}")
                print(f"    [lat,lon] recogida: {lt.get_element(vals, 1)}")
                print(f"    Terminación: {lt.get_element(vals, 2)}")
                print(f"    [lat,lon] terminación: {lt.get_element(vals, 3)}")
                print(f"    Distancia: {lt.get_element(vals, 4)} mi")
                print(f"    Costo: ${lt.get_element(vals, 5)}\n")
            i += 1

    

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
