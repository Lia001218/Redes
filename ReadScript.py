import Structure

creation_instructions = []
with open ('script.txt') as f :
    lines = f.readlines()
for line in lines :
    if(line[1] = 'create' or 'connect' or 'disconnect'):
        creation_instructions.append(line)
    else:
        if(line[2] in mylist.name):
            mylist[line[2]].Add_Instruction(line)
             mylist[line[2]].Add_Menssage(line[3])
creation_instructions.Sort()

