# import NumPy
class Node:
    def __init__(self, name):
        self.name = name
        self.value = None
        self.type = None
        self.menssage = None
        self.history_operation = None
        self.instruction = None       
class Graph:
    def __init__(self):
        self.adj_list = {}
        self.mylist = []
        
    def add_node(self, node):
        if(node not in self.mylist):
            self.mylist.append(node)
            self.adj_list[node] = []
        else:
            print('node,already exists')

    def add_edge(self, node1, node2):
        if node1 in self.mylist and node2 in self.mylist:
            self.adj_list[node2].append(node1)
            self.adj_list[node1].append(node2)
        else:
            print('At least one of the nodes does not exist ')
    def add_history(self, node, action):
        self.history.append(action)
    def disconnected_edge(self,node):
        for i in adj_list[node]:
            if(i[0:i.index('_')] == node[0:node('_')]) :
                continue
            self.adj_list.remove(i)
            
    def graph(self):
        for node in self.adj_list:
            print(node, " --- ", [i for i in self.adj_list[node]])

    
graph1  = Graph()

graph1.add_node(0)
graph1.add_node(1)
graph1.add_node(2)
graph1.add_node(3)
graph1.add_node(4)
graph1.add_edge(0,1)
graph1.add_edge(1,2)
graph1.add_edge(2,3)
graph1.add_edge(3,0)
graph1.add_edge(3,4)
graph1.add_edge(4,0)
graph1.graph()