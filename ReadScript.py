from lib2to3.pytree import Node
from pickle import FALSE
import Instruction
import Structure
import random
time = 0 
source_current = None
network = Structure.Graph()
network_message = []
instructions = []
def read_script():
    with open ('script.txt') as f :
        lines = f.readlines()
    for line in lines:
        instruction = Instruction.Instruction(line)
        instructions.append(instruction)
    instructions.sort()
    processing()
def processing():
    for line in instructions:
        time = int(line.time)
        execute_instruction(line)
def execute_instruction(line):
    if(line.action == 'create'):
        if(line.device == 'hub'):
            count_hub = int(line.count_hub)
            while(count_hub - 1 >=0):
                if(count_hub == int(line.count_hub)):
                    network.add_node(line.name + '_' + str(count_hub), 'hub')
                    count_hub -= 1
                else:
                    network.add_node(line.name + '_' + str(count_hub), 'hub')
                    network.add_edge(network.mylist[len(network.mylist) - 1], network.mylist[len(network.mylist) - 2])
                    count_hub -=1                
        else:
            network.add_node(line.name+'_' + '1', 'pc')
    elif(line.action == 'connect'):
        source = search_node(line.source)
        target = search_node(line.target)
        network.add_edge(source,target)
    elif(line.action == 'disconnect'):
        network.disconnect(line.port)
    else:
        source = search_node(line.source)
        if(check_collision(source) == None):
           create_tupla(int(line.time),line.data)
           source_current = source
        else: 
            linecurrent_menssage = line.data
            network.add_history(source,str(line.time) + str(line.source)
             + str(line.action) + network.linecurrent_message[0][0] + 'collision')
            waiting_time = random.randint(0,10)
            for i in instructions:
                if(i.action == 'send' and i.source==line.source):
                    i.time = i.time + waiting_time
                    instructions.sort()
        send_data()
def send_data():
    network.add_history(source_current,str(time)
    + ' ' + str(source_current.name)+ ' ' +str(network_message[0][0])+ ' ' + 'ok')
    if(time == int(network_message[0][1])):
        BFS(source_current,network_message[0][0])
        network_message.pop(0)
def create_tupla(time,message):
    network_message.append((message[0],time))
    for i in range(1,len(message)):
        network_message.append((message[i],network_message[i-1][1] + 10))
def check_collision(node):
    return node.value 
def update_historyhub(node):
    node.add_history(node, str(time) + 'receive' + node.value)
    for i in network.adj_list[node]:
        if(i[0:i.index('_')] == node[0:node('_')]) :
            node.add_history(node, str(time) + i.name + 'send' + node.value)   
def BFS(node,bit):
    q = []
    visited = {}
    for i in range(len(network.mylist)):
        visited[network.mylist[i]] = False
    q.insert(0,node)
    while len(q) > 0:
        node_temp = q.pop(0)
        for i in network.adj_list[node_temp]:
            if(not visited[i]):
                visited[i] = True
                i.value = int(bit)
                if(i.type == 'hub'):
                    update_historyhub(i)
                q.append(i)
                #if(i.type == 'hub'):
                 #   update_historyhub(i)
def search_node(name):
    for i in network.mylist :
        if(i.name == name):
            return i 
read_script()
                    



        
            
       

    
    
                
                