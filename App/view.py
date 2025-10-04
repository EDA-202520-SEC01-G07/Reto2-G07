import sys
import tabulate as tb
import App.logic as logic

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
    tiempo, total, menorid, menor, fecha_menor, costo_menor, mayorid, mayor, fecha_mayor, costo_mayor, primeros, ultimos = logic.load_data(control, filename)
    print("\nTiempo de carga: "+str(tiempo)+" [ms].\
        \nTotal de trayectos: "+str(total)+" trayectos.\
        \nEl trayecto con menor distancia es el "+str(menorid)+":  \t Distancia: "+str(menor)+" [millas]\t Fecha: "+str(fecha_menor)+"\tCosto: $"+str(costo_menor)+"\n\
        \nEl trayecto con mayor distancia es el "+str(mayorid)+":  \t Distancia: "+str(mayor)+" [millas]\t Fecha: "+str(fecha_mayor)+"\tCosto: $s"+str(costo_mayor)+"\n\
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
    # TODO: Imprimir el resultado del requerimiento 1
    pas = input("Indique la cantidad de pasajeros: ").strip()
    tiempo, trayectos, duracion_prom, costo_prom, distancia_prom, peajes_prom, pago_mas_usado, propina_prom, fecha_repetida, frecuencia = logic.req_1(control, pas)
    print("\nTiempo de ejecución: "+str(tiempo)+" [ms].\
        \nCantidad de trayectos con "+str(pas)+" pasajeros: "+str(trayectos)+"\
        \nEstadísitcas:\n\t- Duración promedio [min] de los trayectos: "+str(duracion_prom)+"\
        \n\t- Costo promedio [dólares] de los trayectos: "+str(costo_prom)+"\
        \n\t- Distancia promedio [millas] de los trayectos: "+str(distancia_prom)+"\
        \n\t- Promedio costos de peajes: "+str(peajes_prom)+"\
        \n\t- Tipo de pago más usado: "+str(pago_mas_usado)+"\
        \n\t- Pago propina promedio de los trayectos: "+str(propina_prom)+"\
        \n\t- La fecha con más trayectos es "+fecha_repetida+" donde hubo "+str(frecuencia)+" trayectos.")

def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    pago = input("Indique el tipo de pago que desea consultar (CREDIT_CARD, CASH, NO_CHARGE, UNKNOWN): ").strip().upper()
    tiempo, contador, duracion, costo, distancia_total, peajes_total, cantidad_pasa, propina, fecha_mayor = logic.req_2(control, pago)

    data = [
        ["Tiempo de consulta [ms]", str(tiempo)],
        ["Total de trayectos con tipo de pago " + str(pago), str(contador)],
        ["Duración promedio de los viajes [min]", str(duracion)],
        ["Costo promedio de los viajes [USD]", str(costo)],
        ["Distancia promedio de los viajes [millas]", str(distancia_total)],
        ["Peajes promedio de los viajes [USD]", str(peajes_total)],
        ["Cantidad de pasajeros más frecuente “#número de pasajeros – cantidad”", str(cantidad_pasa)],
        ["Propina promedio [USD]", str(propina)],
        ["Fecha de finalización de trayecto con mayor frecuencia ", str(fecha_mayor)]
    ]

    print("\n=== Resultados del Requerimiento 2 ===")
    print(tb.tabulate(data, headers=["Descripción", "Valor"]))
    print("=======================================\n")

def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    menor= input("Indique el valor menor del precio total pagado: ").strip()
    mayor= input("Indique el valor mayor del precio total pagado: ").strip()
    tiempo, contador, duracion, costo, distancia_total, peajes_total, cantidad_pasa, propina, fecha_mayor = logic.req_3(control, mayor, menor)  
    print("\nTiempo de ejecución: "+str(tiempo)+" [ms].\
        \nCantidad de trayectos con precio total pagado entre "+str(menor)+" y "+str(mayor)+": "+str(contador)+"\
        \nEstadísitcas:\n\t- Duración promedio [min] de los trayectos: "+str(duracion)+"\
        \n\t- Costo promedio [dólares] de los trayectos: "+str(costo)+"\
        \n\t- Distancia promedio [millas] de los trayectos: "+str(distancia_total)+"\
        \n\t- Promedio costos de peajes: "+str(peajes_total)+"\
        \n\t- Cantidad de pasajeros más frecuente “#número de pasajeros – cantidad”: "+str(cantidad_pasa)+"\
        \n\t- Pago propina promedio de los trayectos: "+str(propina)+"\
        \n\t- La fecha con más trayectos es "+fecha_mayor+".")
    return None


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    filtro = input("Digite filtro (MAYOR/MENOR): ").strip().upper()
    fecha_ini = input("Digite fecha inicial (YYYY-MM-DD): ").strip()
    fecha_fin = input("Digite fecha final (YYYY-MM-DD): ").strip()

    tiempo, filtro, total, origen, destino, dist_prom, dur_prom, costo_prom = logic.req4(
        control, filtro, fecha_ini, fecha_fin
    )

    if total == 0:
        print("\nNo se encontraron trayectos en el rango de fechas.")
    else:
        data = [
            ["Tiempo de consulta [ms]", str(round(tiempo, 2))],
            ["Filtro aplicado", str(filtro)],
            ["Total de trayectos en el rango de fechas", str(total)],
            ["Barrio de origen", str(origen)],
            ["Barrio de destino", str(destino)],
            ["Distancia promedio de los trayectos [millas]", str(round(dist_prom, 2))],
            ["Duración promedio de los trayectos [min]", str(round(dur_prom, 2))],
            ["Costo promedio de los trayectos [USD]", str(round(costo_prom, 2))]
        ]

        print("\n=== Resultados del Requerimiento 4 ===")
        print(tb.tabulate(data, headers=["Descripción", "Valor"]))
        print("=======================================\n")


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    filtro = input("Digite filtro (MAYOR/MENOR): ").strip().upper()
    fecha_ini = input("Digite fecha inicial (YYYY-MM-DD): ").strip()
    fecha_fin = input("Digite fecha final (YYYY-MM-DD): ").strip()
    
    tiempo_ms, filtro_usado, total_trayectos_en_rango, franja, costo_promedio, num_trayectos_franja, duracion_promedio_min, pasajeros_promedio, costo_max_franja, costo_min_franja = logic.req_5(control, filtro, fecha_ini, fecha_fin)
    
    if franja is None:
        print("\nNo hay franjas con datos en ese rango de fechas.")
        return None
    
    print("\nTiempo de ejecución: " + str(tiempo_ms) + " [ms]." +
        "\nFiltro aplicado: " + str(filtro_usado) +
        "\nCantidad de trayectos en el rango de fechas: " + str(total_trayectos_en_rango))

    print("\nFranja horaria seleccionada: " + str(franja) +
        "\n\t- Costo promedio [USD]: " + str(costo_promedio) +
        "\n\t- Número de trayectos: " + str(num_trayectos_franja) +
        "\n\t- Duración promedio [min]: " + str(duracion_promedio_min) +
        "\n\t- Pasajeros promedio: " + str(pasajeros_promedio) +
        "\n\t- Costo total máximo en la franja [USD]: " + str(costo_max_franja) +
        "\n\t- Costo total mínimo en la franja [USD]: " + str(costo_min_franja))
    return None



def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    barrio = input("Indique qué barrio quiere evaluar: ").strip()
    fecha_i = input("Digite fecha inicial (YYYY-MM-DD): ").strip()
    fecha_f = input("Digite fecha final (YYYY-MM-DD): ").strip()
    t, trayectos, distancia_prom, tiempo_prom, destino_repetido, info_pagos = logic.req_6(control, barrio, fecha_i,fecha_f)
    print(
        "\nTiempo de ejecución: "+str(t)+" [ms].\
        \nCantidad de trayectos hechos en el rango de fechas y desde el barrio dado: "+str(trayectos)+"\
        \nDistancia promedio [millas] de los trayectos: "+str(distancia_prom)+"\
        \nTiempo promedio [min] de los trayectos: "+str(tiempo_prom)+"\
        \n\nBarrio más visitado como destino de los trayectos: "+str(destino_repetido)+" \
        \n\nDatos para cada medio de pago:\n"+tb.tabulate(info_pagos, headers="keys",tablefmt="simple")+"\n\n")


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
