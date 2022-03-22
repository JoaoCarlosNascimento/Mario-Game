import numpy as np

class entity:
    def __init__(self,name=[]):
        if name == []:
            raise NameError("Invalid entity name. You must define a name for the entity!")
        self.name = name
        self.entity_state = 0
        self.animation_state = 0


        self.position = np.array([-1, -1]) # [x_pos,y_pos]
        self.velocity = np.array([0, 0])  # [x_speed,y_speed]
        # self.acceleration = (0,0) # (x_acc,y_acc)

    def update(self, state=0):
        if self.name == "Player":
            print('Player position: ({pos})'.format(pos=self.position))
            # if state == -13:
            #     # command
            #     # if command != [(-1,-1)]:
            #     #     # com = command['com']
            #     moveR = (command & 0b1000) == 0b1000
            #     moveL = (command & 0b0100) == 0b0100
            #     moveC = (command & 0b0010) == 0b0010
            #     moveJ = (command & 0b0001) == 0b0001
            #     if(moveR):
            #         print("Move R")
            #     if(moveL):
            #         print("Move L")
            #     if(moveC):
            #         print("Move C")
            #     if(moveJ):
            #         print("Move J")
