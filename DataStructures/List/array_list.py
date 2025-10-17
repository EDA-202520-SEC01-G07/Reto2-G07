def new_list():
    newlist={
        "elements": [],
        "size": 0,
        }
    return newlist

def get_element(my_list, index):
    return my_list["elements"][index]

def is_present(my_list, element, cmp_function):
    size = my_list["size"]
    if size > 0:
        keyexit = False
        for keypos in range(0, size):
            info = my_list["elements"][keypos]
            if cmp_function(element, info) == 0:
                keyexit = True
                break
        if keyexit:
            return keypos
    return -1
def add_first(array_list,element):
    array_list["elements"].insert(0,element)
    array_list["size"]+=1
    return array_list

def add_last(array_list,element):
    array_list["elements"].append(element)
    array_list["size"]+=1
    return array_list

def size(array_list):
    return array_list["size"]   

def first_element(array_list):
    if array_list["size"]>0:
        return array_list["elements"][0]
    return None

def is_empty(array_list):
    return array_list["size"]==0

def last_element(array_list):
    if array_list["size"]>0:
        return array_list["elements"][array_list["size"]-1]
    return None

def delete_element(array_list,index):
    del array_list["elements"][index]
    array_list["size"]-=1
    return array_list

def remove_first(array_list):
    if array_list["size"]>0:
        element=array_list["elements"].pop(0)
        array_list["size"]-=1
        return element
    return None

def remove_last(array_list):
    if array_list["size"]>0:
        element=array_list["elements"].pop(array_list["size"]-1)
        array_list["size"]-=1
        return element
    return None

def insert_element(array_list,index,element):
    array_list["elements"].insert(index,element)
    array_list["size"]+=1
    return array_list

def change_info(array_list,index,element):
    if array_list["size"]>0 and index<array_list["size"]:
        array_list["elements"][index]=element
        return True
    return False

def exchange(array_list,index1,index2):
    if array_list["size"]>0 and index1<array_list["size"] and index2<array_list["size"]:
        temp=array_list["elements"][index1]
        array_list["elements"][index1]=array_list["elements"][index2]
        array_list["elements"][index2]=temp
        return True
    return False

def sub_list(array_list, start_index, num_elements):
    if start_index >= array_list["size"]:
        raise Exception('IndexError: list index out of range')
    else:
        newlist=new_list()
        end_index = start_index+num_elements
        if end_index > array_list["size"]:
            end_index = array_list["size"]
        
        for i in range(start_index,end_index):
            add_last(newlist,array_list["elements"][i])
        return newlist

# Funciones lab 5    
def default_sort_criteria(element_1, element_2):
    is_sorted = False
    if element_1 < element_2:
        is_sorted = True
    return is_sorted


def insertion_sort(my_list, sort_crit):
    sort_list = new_list()
    if my_list["size"]>1:
        sort_crit(my_list["elements"][0], my_list["elements"][1])
        for i in range(0,my_list["size"]):
            if sort_list["size"]==0:
                add_last(sort_list, my_list["elements"][i])
            else:
                position = 0
                while position < sort_list["size"] and sort_crit(sort_list["elements"][position], my_list["elements"][i]):
                    position +=1
                insert_element(sort_list, position, my_list["elements"][i])
    else:
        sort_list = my_list
    return sort_list

def selection_sort(array_list, sort_criteria):
    n = size(array_list)
    for i in range(n):
        min_index = i
        min_elem = get_element(array_list, i)
        for j in range(i + 1, n):
            elem = get_element(array_list, j)
            if sort_criteria(elem, min_elem):
                min_elem = elem
                min_index = j
        if min_index != i:
            exchange(array_list, i, min_index)
    return array_list


def shell_sort(my_list, sort_criteria):
    tam = size(my_list)
    h=(3 * tam + 1)//3
    if tam == 0 or tam == 1:
        return my_list
    else: 
        while h > 0:
            for i in range(tam):
                temp = get_element(my_list, i)
                gap = i+h
                while gap < tam:
                    if sort_criteria(get_element(my_list, gap),temp):
                        exchange(my_list, gap, i)
                    gap += h
            h = h//3
    return my_list

def merge_sort(my_list, sort_crit):
    if my_list["size"] > 1:
        mitad = my_list["size"] // 2
        izq= sub_list(my_list, 0, mitad)
        dere= sub_list(my_list, mitad, my_list["size"]- mitad)

        mitad_izqui = merge_sort(izq, sort_crit)
        mitad_dere = merge_sort(dere, sort_crit)

        return merge(mitad_izqui, mitad_dere, sort_crit)
    else:
        return my_list
def merge(list_1, list_2, sort_crit):
    l=0
    r=0
    merged_list = new_list()
    while l < list_1["size"] and r < list_2["size"]:
        ei= get_element(list_1, l)
        ed= get_element(list_2, r)
        x= sort_crit(ei, ed)
        if x:
            add_last(merged_list, ei)
            l += 1
        else:
            add_last(merged_list, ed)
            r += 1
    return merged_list

def quick_sort(list, sort_crit):
    return quick_sort_1(list, 0, int(size(list))-1, sort_crit)

def quick_sort_1(lst,io,hi,sort_crit):
    if io >= hi:
        return lst
    else:
        pivot = partition(lst, io,hi,sort_crit)
        quick_sort_1(lst,io,pivot-1,sort_crit)
        quick_sort_1(lst,pivot+1,hi,sort_crit)
    return lst
def partition(lst,io,hi,sort_crit):
    f = io
    l = io
    while l<hi:
        if sort_crit(get_element(lst,l),get_element(lst,hi)):
            exchange(lst, f,l)
            f +=1
        l +=1
    exchange(lst,f,hi)
    return f