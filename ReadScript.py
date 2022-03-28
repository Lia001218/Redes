import Structure
import random
red = Graph()
creation_instructions = []
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
                red.add_node(line(3) +'_' + count_hub )
                count_hub -=1
                
        else:
            red.add_node(line(3)+'_'+ 1)
    elif(line(1) = 'connect'):
        red.add_edge(line(2),line(3))
    elif(line(1)= 'disconnect'):
        red.disconnect(line(2))
    else:
        check_collision() # funcion que verifica si hay o no colision falta implementar
        if(not check_collision()):
            sed(node,messege)
        else: # si colisiono anadir a la history_operation de la line(2) que colisiono en el time line(1)
            waiting_time = random.randint(0,10)
            for i in lines:
                if(i(1) = 'sed' and i(2)=line(2)):
                    i(0) = i(0) + waiting_time
                
                