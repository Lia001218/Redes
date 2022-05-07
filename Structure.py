
from platform import node
from unicodedata import name

class Node:
    def __init__(self,name,type):
        self.name = name
        self.value = None
        self.type = type
        self.history_operation = []
        self.instruction = None   
    def write_txt(self):
        with open (self.name + ".txt", 'w') as f:
            f.writelines(self.history_operation)
class Host(Node):
    def __init__(self, name,type):
        Node.__init__(self,name,type)
        self.mac = ''
        self.menssage = []
        self.receive = False
class Link_Device(Node):
    def __init__(self, name,type):
        Node.__init__(name, type)
        self.memory = []   
class Port():
    def __init__(self,name,name_device_associated,type_device_associated):
        self.name = name
        self.name_device_associated = name_device_associated
        self.type_device_associated = type_device_associated
        self.frame = ''
        self.mac = ''
        self.associated_mac = []
        self.time_recieve = 0
        self.time_send = 0
    def recive(self,bit):
        self.frame.add(bit)
        if(len (self.frame) == 15):
            self.mac_to = self.frame
    def send(self):
        return self.frame.pop(0)
class Graph:
    def __init__(self):
        self.adj_list = {}
        self.mylist = []
        self.mydevices = []
        self.node = None
    
    def add_node(self, name,name_device_associated,type_device_associated):
        node = Port(name,name_device_associated,type_device_associated)
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
        node.history_operation.append(action)
    def disconnected_edge(self,node):
        for i in self.mylist:
            for j in self.adj_list[i]:
                if(j == node):
                    self.adj_list[i].remove(j)
        self.adj_list[node] = []
    def update_mylist(self, list_hub):
        new_mylist = []
        for node in self.mylist:
            if(node.type == 'pc'):
                new_mylist.append(node)
        self.mylist = new_mylist + list_hub
    def graph(self):
        for node in self.adj_list:
            print(node, " --- ", [i for i in self.adj_list[node]])
