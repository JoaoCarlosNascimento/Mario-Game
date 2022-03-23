import numpy as np
from lib.colision import colision

# id_list = []

class entity:
    def __init__(self,name=[]):
        if type == []:
            raise NameError("Invalid entity name. You must define a name for the entity!")
        self.name = name
        # self.id = entity.__new_id()
        # print(self.id)
        self.entity_state = 0
        self.animation_state = 0


        self.position = np.array([-1, -1]) # [x_pos,y_pos]
        self.velocity = np.array([0, 0])  # [x_speed,y_speed]
        # self.acceleration = (0,0) # (x_acc,y_acc)

        self.colision_list = []

    def update(self, state=0):
        if self.type == "Player":
            # print('Position: ({pos:.2f})\nSpeed: ({spe:.2f})'.format(pos=self.position,spe=self.velocity))
            print('X Speed: ({speX:.2f}), Y Speed: ({speY:.2f})'.format(speX=self.velocity[0],speY=self.velocity[1]))
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

    # def __new_id():
    #     exists = False
    #     for i in range(100):
    #         for id in id_list:
    #             if id == i:
    #                 exists = True
    #                 break
    #         if not exists:
    #             id_list.append(i)
    #             return i
    #         else:
    #             exists = False