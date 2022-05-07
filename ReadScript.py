
from email import message
from multiprocessing.sharedctypes import Value
from pickle import FALSE
import Instruction
import Structure
import random
time = 0 
source_current = ''
network = Structure.Graph()
network_message = {}
instructions = []
def read_script(): # lee el scipt 
    with open ('script.txt') as f :
        lines = f.readlines()
    for line in lines: # crea por cada linea del txt una instruccion 
        instruction = Instruction.Instruction(line)
        instructions.append(instruction)
    instructions.sort()# ordena las instrucciones por tiempo de ejecucion y en caso de tener el mismo tiempo , por prioridad de la accion
    processing()
def processing():
    global time 
    while(instructions != [] or  network_message != {}):# mientras existan todavia instrucciones por ejecutar y queden aun bits por mandar se sigue ejecutando el programa
        if(instructions == [] or instructions[0].time != time):
            time+=1
        if(instructions != [] and instructions[0].time == time):
            execute_instruction(instructions[0])
def update_time_port():
    for i in network.mylist:
        if(i.time_recieve == time):
            i.time_recieve = 0
        if(i.time_send == time):
            i.time_send = 0
def conect_port_of_switch(name):
    for node1 in network.mylist:
        for node2 in network.mylist:
            if(node1 != node2 and node1.name_device_associated == name and  node2.name_device_associated == name):
                network.add_edge(node1,node2)
def execute_instruction(line):
    global source_current 
    if(line.action == 'create'):
        if(line.device == 'switch'):
            network.mydevices.append(Structure.Node(line.name,'switch'))
            count_port_of_switch = int(line.count_port)
            while count_port_of_switch != 0:
                network.add_node(line.name + '_' + str(count_port_of_switch),line.name,'switch')
                count_port_of_switch -=1
            conect_port_of_switch(line.name)   
        else:
            network.mydevices.append(Structure.Node(line.name,'host'))
            network.add_node(line.name+'_' + '1',line.name,'host')
        instructions.pop(0)
    elif(line.action == 'connect'):
        source = search_node(line.source)
        target = search_node(line.target)
        network.add_edge(source,target)
        instructions.pop(0)
    elif(line.action == 'disconnect'):
        port = search_node(line.port)
        network.disconnected_edge(port)
        instructions.pop(0)
    elif(line.action == 'mac'):
        source = search_node(line.source)
        source.mac = line.address
        instructions.pop(0)
    else: 
        port_source = search_node_for_mac(line.source)
        port_recieve = network.adj_list[port_source]
        port_host_recieve = search_hot_for_mac(line.mac_destinatation)
        some_port_used = False
        if(line.mac_destinatation == 'FFFF'):
            some_port_used = some_port_recieve()
        if(port_recieve== []):
            instructions.pop(0)
        elif(some_port_used == True ):
            line.time = int(line.time) + 450
            instructions.sort()
        elif(port_host_recieve == None ):
            line.time = int(line.time) + 450
            instructions.sort()
        elif(port_source.time_send >= time or port_host_recieve.time_recieve >= time):
            update_time_port()
            line.time = int(line.time) + 450
            instructions.sort()
        else:  
            mark = {}
            for i in network.mylist:
                mark[i] = False
            frame = create_frame(line.data,port_source,line.mac_destinatation)
            port_host_recieve.time_recieve  = port_source.time_send  = len(frame) *10
            send_data(port_source,port_recieve[0],frame,mark)
            instructions.pop(0)
        
def some_port_recieve():
    for i in network.mylist:
        if (i.time_recieve >= time):
            return True
    return False
def search_hot_for_mac(mac):
    for device in network.mylist:
        if(device.mac == mac):
            return device
def create_frame(data,source,target):
    mac_to_bit = bin(int(target,16))
    mac_to = mac_to_bit[2:]
    mac_from_bit = bin(int(source.mac,16))
    mac_from = mac_from_bit[2:]
    size_data_bit =  bin(len(data))
    size_data = size_data_bit[2:]
    if(len(size_data) < 8):
        size_data = complete_inf(size_data)
    size_ver_bit = bin(len(data)*2)
    size_ver = size_ver_bit[2:]
    if(len(size_ver) < 8):
        size_ver = complete_inf(size_data)
    ver = create_verfication_code(data)
    return mac_to + mac_from+ size_data+ size_ver +data + ver
def create_verfication_code(data):
    key = create_key(len(data))
    code_secret = encryption(key,data)
    return key + code_secret
def create_key(size):
    key = ''
    while len(key) < size:
        bit = random.randint(0,1)
        key = str(bit) + key 
    return key
def encryption(key,data):
    result = ''
    for i in range(0,len(key)):
        result = result + str(int(key[i])^int(data[i]))
    return result
def complete_inf(string):
    bits_miss = 8 - len(string)
    temp = ''
    while bits_miss!= 0:
        temp = temp + '0'
        bits_miss -=1 
    return temp + string
def search_port(device):
    for i in network.mylist:
        if(i.name_device_associate == device):
            return i 
def send_data(source,target,frame,mark):
    mark[target] = True
    if(target.type_device_associated == 'host'):
        if(IsmyMessage(target,frame[:16])):
            device = search(network.mydevices,target.name_device_associated)
            mac_hex = hex(int(frame[16:32],2))
            if(encryption(frame[48+ int(frame[32:40],2):48+ 2*int(frame[32:40],2)], frame[48+ 2*int(frame[32:40],2) :])== frame[48:48 + int(frame[32:40],2)]): 
                device.history_operation.append(str(time)+ ' ' + mac_hex[2:]+ ' ' + frame[48:48 + int(frame[32:40],2)]+ '\n')
            else:
                device.history_operation.append(str(time)+ ' ' + mac_hex[2:]+ ' ' + frame[48:48 + int(frame[32:40],2)] + ' '+ 'ERROR' + '\n')
    if(target.type_device_associated == 'switch'):
        target.associated_mac.append((source.mac,time + 10))
        port_this_switch = []
        message_sent = False
        for i in network.mylist:
            if(i.name_device_associated == target.name_device_associated):
                for mac in i.associated_mac :
                    if(mac[0] == frame[:16]):
                        send_data(i,frame,mark)
                        message_sent = True
                        break
                port_this_switch.append(i)
        if(message_sent == False):
            for i in port_this_switch:
                if (mark[i] == False):
                    for j in network.adj_list[i]:
                        if(mark[j] == False and j.name[0:j.name.index('_')] != i.name[0:i.name.index('_')]):
                            p = random.randint(1,100)
                            #p = 95
                            if(p >= 90 and p <= 100 ):
                                data_change = change_data(frame[48:48 + int(frame[32:40],2)])
                                frame = frame[:48] + data_change + frame[48 + int(frame[32:40],2):]
                            davice = search(network.mydevices,target.name_device_associated)
                            davice.history_operation.append(str(time)+ ' ' + 'from' + ' ' + str(i.name)+ ' ' + str(source.frame)+ ' ' 
                            + 'to' + ' ' +str(j.name) + ' ' + frame[48:48 + int(frame[32:40],2)] +'\n')
                            send_data(i,j,frame,mark)
        update_time_mac()
def change_data(data):
    pos_change = random.randint(0,len(data)-1)
    if(data[pos_change] == '0'):
        bit_change = '1'
    else :
        bit_change = '0'
    return data[:pos_change] + bit_change + data[pos_change + 1:]
def update_time_mac():
    for i in network.mylist:
        if(i.type_device_associated == 'switch' and i.associated_mac != [] and i.associated_mac[0][1] == time ):
            i.associated_mac.pop(0)
def IsmyMessage(target,mac):
    mac_bin = bin(int(target.mac,16))
    return mac_bin[2:] == mac or mac == '1111111111111111'
def search(network_davices,davice):
    for i in network_davices:
        if (i.name == davice):
            return i         
def create_tupla(time,message):
    network_message[source_current].append((message[0],time))
    for i in range(1,len(message)):
        network_message[source_current].append((message[i],network_message[source_current][i-1][1] + 10))
        if(i == len(message) - 1):# para asegurar que el ultimo bit del mensaje se este transmitiendo 10 mls
            network_message[source_current].append((message[i],network_message[source_current][i-1][1] + 20))
def check_collision(node):
    return node.value 
def update_historyhub(node):
    network.add_history(node, str(time) + ' ' + node.name + ' ' + 'receive' + ' ' + str(node.value) + '\n')
    for i in network.mylist: # si un bit entro por un puerto del hub entonces sale por el resto de los puertos
        if(i.name[0:i.name.index('_')] == node.name[0:node.name.index('_')]) :
            network.add_history(node, str(time) + ' ' + i.name + ' ' + 'send' + ' ' + ' ' +str(node.value) + '\n')   

def search_node(name):
    for i in network.mylist :
        if(i.name == name):
            return i 
def search_node_for_mac(host_source):
    for node in network.mylist:
        if(node.name_device_associated == host_source):
            return node
read_script()
for device in network.mydevices:
    device.write_txt()
                    



        
            
       

    
    
                
                