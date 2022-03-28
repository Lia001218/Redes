import Structure
import random
network = Graph()
network_status = None
network_message = None
with open ('script.txt') as f :
    lines = f.readlines()
lines.sort()
time = 0
while lines != None:
    if(line(0) == time):
        execute_instruction(line)
    else:
        time +=1
def execute_instruction(line):
    if(line(1) = 'create'):
        if(line(2) = 'hub'):
            count_hub = int(line(4))
            while(count_hub not 0):
                network.add_node(line(3) +'_' + count_hub )
                count_hub -=1
                
        else:
            network.add_node(line(3)+'_'+ 1)
    elif(line(1) = 'connect'):
        network.add_edge(line(2),line(3))
    elif(line(1)= 'disconnect'):
        network.disconnect(line(2))
    else:
        check_collision() 
        if(not check_collision()):
            send_data(line)
        else: 
            linecurrent_menssage = line(4)
            add_history(line(1),line(0) + line(2) + line(3) + linecurrent_message[1] + 'collision')
            update_network()
            waiting_time = random.randint(0,10)
            for i in lines:
                if(i(1) = 'send' and i(2)=line(2)):
                    i(0) = i(0) + waiting_time
                    lines.sort()
def send_data(line):
    network_message = int(line(3))
    update_network()
def check_collision(): # falta lo del XOR
    
    
    
    
                
                