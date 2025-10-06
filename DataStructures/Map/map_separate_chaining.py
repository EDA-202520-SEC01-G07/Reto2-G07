from DataStructures.List import array_list as alt
from DataStructures.List import single_linked_list as slt
from DataStructures.Map import map_entry as me
from DataStructures.Map import map_functions as mf
import random 

def default_compare(key, element):

   if (key == me.get_key(element)):
      return 0
   elif (key > me.get_key(element)):
      return 1
   return -1

def rehash(my_map):  ##!!REVISAR EL REHASH POR LA NATURALEZA DEL SEPARATE CHAINING!!##
    """
    Realiza un rehash de la tabla de simbolos.
    Para realizar un rehash se debe seguir los siguientes pasos:
    Crear una nueva tabla map_separate_chaining con capacity que sea el siguiente primo al doble del capacity actual.
    Recorrer la tabla actual y reinsertar cada elemento en la nueva tabla.
    Asignar la nueva tabla como la tabla actual.
    Retornar la tabla nueva.
    """
    cap_nueva = 2*my_map["capacity"]
    if mf.is_prime(cap_nueva):
        cap_nueva += 1
    cap_nueva = mf.next_prime(cap_nueva)
    
    nuevo = new_map(cap_nueva, my_map["limit_factor"], my_map["prime"])
    nuevo["capacity"] = cap_nueva
    for i in range(my_map["capacity"]):
        entry = alt.get_element(my_map["table"], i)
        for j in range(slt.size(entry)):
            elem = slt.get_element(entry, j)
            h = mf.hash_value(nuevo, elem["key"])
            
            entry_nuevo = alt.get_element(nuevo["table"], h)
            slt.add_last(entry_nuevo,me.new_map_entry(elem["key"], elem["value"]))
            nuevo["size"] += 1
            nuevo["current_factor"] = nuevo["size"]/nuevo["capacity"]
    return nuevo

def new_map(num_elements, load_factor, prime=109345121):
    y=mf.next_prime(num_elements//load_factor)
    x = alt.new_list()
    map = {"prime": prime,
           "capacity": y,
           "scale": random.randrange(1, prime-1),
           "shift":random.randrange(0, prime-1),
           "table": x,
           "current_factor": 0,
           "limit_factor": load_factor,
           "size": 0
    }
    for i in range(y):
        lista = slt.new_list()
        alt.add_last(map["table"], lista)
    return map

def put(mapa, key, value):
    llave = mf.hash_value(mapa, key) #Hash de la llave
    entry = alt.get_element(mapa["table"], llave)
    appears = False
    for i in range(slt.size(entry)):
        elem = slt.get_element(entry, i)
        if elem["key"]==key:
            appears = True
            if appears == True:
                me.set_value(entry, value)
    if appears == False:
        slt.add_last(entry, me.new_map_entry(key, value))
        mapa["size"] += 1
        mapa["current_factor"] = mapa["size"]/mapa["capacity"]
       
    if mapa["current_factor"] > mapa["limit_factor"]:
        mapa = rehash(mapa)
    return mapa

def contains(mapa, key):
    encontrado = False
    hash = mf.hash_value(mapa, key)
    entry = alt.get_element(mapa["table"], hash)
    for i in range(slt.size(entry)):
        elem = slt.get_element(entry, i)
        if key == me.get_key(elem):
            encontrado = True
    return encontrado

def get(mapa, key):
    hash = mf.hash_value(mapa,key)
    entry = alt.get_element(mapa["table"], hash)
    x = None
    for i in range(slt.size(entry)):
        elem = slt.get_element(entry, i)
        if key == me.get_key(elem):
            x = me.get_value(elem)
    return x

def remove(mapa, key):
    hash= mf.hash_value(mapa,key)
    entry = alt.get_element(mapa["table"], hash)
    for i in range(slt.size(entry)):
        elem = slt.get_element(entry, i)
        if key == me.get_key(elem):
            slt.delete_element (entry, i)
            mapa["size"] -= 1
            mapa["current_factor"] = mapa["size"]/mapa["capacity"]
    return mapa

def size(mapa):
    return mapa["size"]

def is_empty(mapa):
    vacio = False
    if mapa["size"]==0:
        vacio = True
    return vacio

def key_set(mapa):
    tam = alt.size(mapa["table"])
    llaves = alt.new_list()
    for i in range(tam):
        entry = alt.get_element(mapa["table"], i)
        for i in range(slt.size(entry)):
            elem = slt.get_element(entry, i)
            alt.add_last(llaves, me.get_key(elem))
    return llaves

def value_set(mapa):
    tam = alt.size(mapa["table"])
    valores = alt.new_list()
    for i in range(tam):
        entry = alt.get_element(mapa["table"], i)
        for i in range(slt.size(entry)):
            elem = slt.get_element(entry, i)
            alt.add_last(valores, me.get_value(elem))
    return valores