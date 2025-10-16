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

def print_req_1(control): #preguntar cómo se organiza una lista, preguntar formato
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
        Función que imprime la solución del Requerimiento 2 en consola
    """
    tamano=int(input("Indique el tamaño de la muestra: "))
    inicio=float(input("Indique la coordenada inicial de latitud: "))
    fin=float(input("Indique la coordenada final de latitud: "))
    tiempo, trayectos, viajes = logic.req_2(control, inicio, fin,tamano)
    print("Tiempo de ejecución en ms: " + str(tiempo))
    print("Trayectos dentro del rango de latitud: " + str(trayectos))
    print(viajes)
    
    # TODO: Imprimir el resultado del requerimiento 2
    
def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    

def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    #f_terminacion = input("Indique la fecha de terminación: ")
    #t_ref = input("Indique el tiempo de referencia: ")
    #criterio = input("Indique si quiere los viajes antes o después al tiempo de referencia (sin tildes): ")
    n = int(input("Indique la muestra del viaje: "))
    # BORRAR; SOLO PARA PRUEBAS
    f_terminacion = "2015-01-20"
    t_ref = "00:05:00"
    criterio = "Antes"
    tiempo, trayectos, v = logic.req_4(control, f_terminacion, t_ref, criterio, n)
    tiempo1, viajes = logic.aux_presentacion(v)
    print("Tiempo de ejecución en ms: " + str(tiempo+tiempo1))
    print("Trayectos ["+criterio+"] que cumplieron los requisitos de fecha y hora de terminación: " + str(trayectos))
    print(viajes)
    
def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    

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
