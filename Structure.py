import NumPy


class Node:
    def __init__(self, name):
        self.name = name
        self.menssage = None
        self.history_operation = None
        self.instruction = None
        self.adj_list = {}
        self.mylist = []

    def add_Node(self, node):
        if(node not in mylist):
            self.mylist.append(node)
            self.adj_list.append(node)
        else:
            print('esto tal vez lo quite, en caso que lo deje el mensage es : Node ',
                  'node,already exists')

    def add_edge(self, node1, node2):
        if node1 in mylist and node2 in mylist:
            self.adj_list[node2].append(node1)
            self.adj_list[node1].append(node2)
        else:
            print('At least one of the nodes does not exist ')

    def save_message(self.node, message):
        self.message = message

    def add_history(self, node, action):
        self.history.append(action)

    # Implemetarlo como Heap que el valor con menor tiempo siempre este al principio
    def add_instruction(self, node, instruction):
        self.instruction.append(instruction)

    def delete_instruction(self, node):
        instruction.remove()
