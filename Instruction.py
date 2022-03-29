class Instruction:
    def __init__(self,instruction):
        instruction = instruction.split()
        self.time = int(instruction[0])
        self.action = instruction[1]
        if(self.action == 'create'):
            self.action_code = 0
        elif(self.action == 'connect'):
            self.action_code = 1
        elif(self.action == 'send'):
            self.action_code = 3
        else :
            self.action_code = 2
    def __lt__(self,b):
        if(self.time < b.time):
            return True
        if(self.time = b.time):
            return self.action_code < b.action_code
        return False
        
        
                