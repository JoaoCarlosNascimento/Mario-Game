# from calendar import c
import numpy as np


class physics:
    def __init__(self):
        pass

    def update(self, state=0,entities=[],commands=0b0000):
        # Atualização das entidades
        # com = commands['com']
        for entity in entities:
            if entity.name == "Player":
                self.__move(entity,commands)
                entity.update(state=state)
            else:
                entity.update(state=state)



        # for entity in entities:
        #     return


    # Constantes de aceleração
    __com_acc = np.array([1, 1]) # [acc_x,acc_y]
    __grav_acc = np.array([0, 0])  # [acc_x,acc_y]
    __frict_acc = np.array([0.1, 0])  # [acc_x,acc_y]

    # Constantes de velocidade
    __vel_lim = np.array([3, 2])  # [vel_x,vel_y]


    def __move(self,entity,commands = 0b0000):
        dt = 0.1
        # entity.position
        com_acc = np.array([0,0])
        if ((commands & 0b1000) == 0b1000): # Move Right
            # print("Move R")
            com_acc[0] += self.__com_acc[0]
        else:
            if entity.velocity[0] > 0:
                com_acc[0] -= self.__frict_acc[0]
        if ((commands & 0b0100) == 0b0100): # Move Left
            # print("Move L")
            com_acc[0] -= self.__com_acc[0]
        else:
            if entity.velocity[0] < 0:
                com_acc[0] += self.__frict_acc[0]
        if ((commands & 0b0010) == 0b0010):  # Move Crouch
            # print("Move C")
            # com_acc[1] += self.__com_acc[1]
            pass
        if ((commands & 0b0001) == 0b0001):  # Move Jump
            # print("Move J")
            com_acc[1] -= self.__com_acc[1]
        
        # Composição das acelerações
        acc = (com_acc+self.__grav_acc)

        # Atualização das velocidades
        entity.velocity = entity.velocity + acc*dt

        # Saturador das velocidades
        if entity.velocity[0] >= self.__vel_lim[0]:
            entity.velocity[0] = self.__vel_lim[0]
        if entity.velocity[1] >= self.__vel_lim[1]:
            entity.velocity[1] = self.__vel_lim[1]

        # Atualização das posições
        entity.position = entity.position + entity.velocity*dt+acc*(dt**2)/2
        
