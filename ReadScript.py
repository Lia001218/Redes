
import Instruction
import Structure
import random
time = 0 
source_current = ''
network = Structure.Graph()
network_message = []
instructions = []
hub = []
grouped_bub_port = []
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
    while(instructions != [] or  network_message != []):# mientras existan todavia instrucciones por ejecutar y queden aun bits por mandar se sigue ejecutando el programa
        if(instructions == [] or instructions[0].time != time):
            time+=1
            send_data()
        if(instructions != [] and instructions[0].time == time):
            execute_instruction(instructions[0])
  
def execute_instruction(line):
    global source_current 
    if(line.action == 'create'):
        if(line.device == 'hub'): # si es un hub se crea un nodo por cada puerto del hub y se conectan entre ellos
            count_hub = int(line.count_hub)
            port_hub = []
            while(count_hub - 1 >=0): 
                if(count_hub == int(line.count_hub)):
                    network.add_node(line.name + '_' + str(count_hub), 'hub')
                    count_hub -= 1
                else:
                    network.add_node(line.name + '_' + str(count_hub), 'hub')
                    network.add_edge(network.mylist[len(network.mylist) - 1], network.mylist[len(network.mylist) - 2])
                    count_hub -=1  
                    
            hub.append(line.name)         
        else:
            network.add_node(line.name+'_' + '1', 'pc')
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
    else: # si la instruccion es un send entonces se comprueba si hay colision
        source = search_node(line.source)
        if(check_collision(source) == None):# si no hay colision pues se guarda el nodo que va a enviar un mensaje , el mensaje y se quita la instruccion de la lista
           create_tupla(int(line.time),line.data)
           source_current = source
           instructions.pop(0)
        else:# si hay colision , pues se anade al historial de nodo que colisiono que intenti mandar un bit
            linecurrent_menssage = line.data
            network.add_history(source,str(line.time) + '_' + str(line.source) + ' '
             + str(line.action)+ ' ' + str(linecurrent_menssage[0][0])+ ' ' + 'collision' + '\n')
            waiting_time = random.randint(1,10)
            for i in instructions:
                if(i.action == 'send' and i.source==line.source):
                    i.time = i.time + waiting_time     
            instructions.sort()     
    send_data()
def send_data():
    if(network_message != [] and time == int(network_message[0][1])):#si hay mensaje y el tiempo de envio del bit del mensaje coincide con ek tiempo actual entonces se envia
        if(len(network_message) == 1):
            network_message.pop(0)
            for i in network.mylist:
                i.value = None
        else:
            network.add_history(source_current,str(time)+ ' ' + source_current.name + ' ' +'send ' +' ' +str(network_message[0][0])+ ' ' + 'ok' + '\n')
            source_current.value = network_message[0][0]
            BFS(source_current,network_message[0][0])
            network_message.pop(0)
           
def create_tupla(time,message):
    network_message.append((message[0],time))
    for i in range(1,len(message)):
        network_message.append((message[i],network_message[i-1][1] + 10))
        if(i == len(message) - 1):# para asegurar que el ultimo bit del mensaje se este transmitiendo 10 mls
            network_message.append((message[i],network_message[i-1][1] + 20))
def check_collision(node):
    return node.value 
def update_historyhub(node):
    network.add_history(node, str(time) + ' ' + node.name + ' ' + 'receive' + ' ' + str(node.value) + '\n')
    for i in network.mylist: # si un bit entro por un puerto del hub entonces sale por el resto de los puertos
        if(i.name[0:i.name.index('_')] == node.name[0:node.name.index('_')]) :
            network.add_history(node, str(time) + ' ' + i.name + ' ' + 'send' + ' ' + ' ' +str(node.value) + '\n')   
def BFS(node,bit):
    global grouped_bub_port
    q = []
    visited = {}
    for i in range(len(network.mylist)):
        visited[network.mylist[i]] = False
    visited_hub = {}
    for i in hub:
        visited_hub[i] = False
    q.insert(0,node)
    while len(q) > 0:
        node_temp = q.pop(0)
        for i in network.adj_list[node_temp]:
            if(not visited[i]):
                visited[i] = True
                i.value = int(bit) 
                if(i.type == 'hub'):
                    hub_current = i.name[0:i.name.index('_')]
                    node_hub = Structure.Node(hub_current,'hub')
                    if(visited_hub[hub_current] == False):
                        update_historyhub(i)
                        if(check_hub(node_hub)):
                            for node in grouped_bub_port:
                                if(node.name == node_hub.name):
                                    node_hub = node
                        else:
                            grouped_bub_port.append(node_hub)      
                        node_hub.history_operation = i.history_operation
                        visited_hub[hub_current] = True
                if(i.type == 'pc' and i != source_current):
                    network.add_history(i, str(time) + ' ' + i.name + ' ' + 'receive' + ' ' + ' ' +str(i.value) + '\n')   
                q.append(i)
def check_hub(node):
    for i in grouped_bub_port:
        if(node.name == i.name) :
            return True
    return False
def search_node(name):
    for i in network.mylist :
        if(i.name == name):
            return i 
read_script()
network.update_mylist(grouped_bub_port)
for device in network.mylist:
    device.write_txt()
                    



        
            
       

    
    
                
                