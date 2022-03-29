import Structure
import random
network = Graph()
network_message = None
with open ('script.txt') as f :
    lines = f.readlines()
lines.sort() # javier 
time = 0
for line in lines:
    if(int(line[0]) == time):
        execute_instruction(line)
    else:
        time +=1
def execute_instruction(line):
    if(line[1] = 'create'):
        if(line[2] = 'hub'):
            count_hub = int(line[4])
            while(count_hub not 0):
                network.add_node(line[3] +'_' + count_hub )
                if(count_hub not int(line[4])):
                    network.add_edge(line[3] +'_' + count_hub,line[3] +'_' + count_hub + 1)
                count_hub -=1 
                
        else:
            network.add_node(line[3]+'_'+ 1)
    elif(line[1] = 'connect'):
        network.add_edge(line[2],line[3])
    elif(line[1]= 'disconnect'):
        network.disconnect(line[2])
    else:
        if(not check_collision(line[2])):
           create_tupla(line[1],line[3])
            send_data(line)
        else: 
            linecurrent_menssage = line[3]
            add_history(line[1],line[0] + line[2] + line[3] + linecurrent_message[0] + 'collision')
            update_network()
            waiting_time = random.randint(0,10)
            for i in lines:
                if(i[1] = 'send' and i[2]=line[2]):
                    i[0] = i[0] + waiting_time
                    lines.sort()
def send_data(line):
   BFS(line[2],network_message[0])
   network_message.Remove(0)
def create_tupla(time,message):
    network_message.append(message[0], time)
    for i = 1 in message:
        network_message.append(message[i],time[i-1] + 10)
def check_collision(node):
    return node.value not None
def BFS(node,bit):
    q = []
    visited = [false for i = 0 to range(network.mylist)]
    q.insert(0,node)
    while len(q) > 0
    node_temp = q.pop(0)
    for i in network.adj_list(node_temp):
        if(not visited(i))
            visited[i] = true
            network.node.value = bit
            q.push(network.adj_list(node)[i])           


    
    
    
    
                
                