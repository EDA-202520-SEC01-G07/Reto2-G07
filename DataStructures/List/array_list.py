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
    return None

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

def default_function(elemen_1, element_2):
   if elemen_1 > element_2:
      return 1
   elif elemen_1 < element_2:
      return -1
   return 0