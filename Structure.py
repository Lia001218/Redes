import NumPy
class Node :
    def __init__(self,name):
        self.name = name
        self.menssage = None
        self.history_operation = None
        self.instruction = None
adj_list = {}
mylist = []
def Add_Node(node):
    if(node not in mylist):
        mylist.append(node)
        adj_list.append(node)
    else:
       print('esto tal vez lo quite, en caso que lo deje el mensage es : Node ','node,already exists')
def Add_edge(node1,node2):
    if node1 in mylist and node2 in mylist:
        adj_list[node1].append(node2)
        adj_list[node2].append(node1)
    else:
        print('At least one of the nodes does not exist ')
def Save_Message(node , message):
    self.message = message
def Add_History(node,action):
    self.history.append(action)
def Add_Instruction(node , instruction): # Implemetarlo como Heap que el valor con menor tiempo siempre este al principio
    self.instruction.append(instruction)
def Delete_Instruction(node):
    instruction.remove()

