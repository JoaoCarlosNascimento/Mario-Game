# from calendar import c
# from turtle import position
from lib.colision import colision
import numpy as np
import pygame
import lib.load_files as file
import time

# clock = pygame.time.Clock()


class physics:
    def __init__(self):
        self.__timer = 0
        pass

    def update(self, state=0,entities=[], commands=0b0000, score = 0, bonus_val = 0, coins = 0):
        bonus = []
        obstacles = []
        enemies = []
        debug = []
        if state == "game loop":
            if entities:
                for e in entities:
                    if e.name == "Player":
                        mario = e
                    elif e.name == "Enemy":
                        enemies.append(e)
                    elif e.name == "Obstacle":
                        obstacles.append(e)
                    elif e.name == "Bonus":
                        bonus.append(e)
                # Detecta Colisões

                # Atualização das entidades
                self.__timer, bonus, state, coins = self.verify_collision_and_move_mobs(
                    bonus_val, coins, entities, mario, self.__timer)
                # Move mario left
                mario.position[0] -= file.Screen_Width / 4000
                # mario.update(state, self.__timer)
                debug = self.__move(mario,commands=commands)
                # self.keyboards_input(mario)

                return bonus, mario.lives, state, debug, coins
        return 0, 0, 0, "", 0


        # for entity in entities:
        #     return

    # Constantes de aceleração
    __frict_const = np.array([3, 2])  # [acc_x,acc_y]
    __com_acc = np.array([350, -50])+__frict_const  # [acc_x,acc_y]
    __grav_acc = np.array([0, 100])  # [acc_x,acc_y]
    # __norm_acc = -__grav_acc  # [acc_x,acc_y]

    # Constantes de velocidade
    __vel_lim = np.array([200, 150])  # [vel_x,vel_y]
    # __vel_jump = np.array([0, -100])  # [vel_x,vel_y]


    def __move(self,entity,commands = 0b0000):
        dt = 0.1
        # print(dt)
        com_acc = np.array([0,0])

        # Converter comandos em ações
        if ((commands & 0b1000) == 0b1000): # Move Right
            com_acc[0] += self.__com_acc[0]
        if ((commands & 0b0100) == 0b0100): # Move Left
            com_acc[0] -= self.__com_acc[0]
        if ((commands & 0b0010) == 0b0010):  # Move Crouch
            entity.duck(set=True)
            # print("Move C")
            # com_acc[1] += self.__com_acc[1]

        if ((commands & 0b0001) == 0b0001):  # Move Jump
            if entity.velocity[1] == 0 and entity.position[1] > entity.floor-1:
                entity.velocity[1] = -self.__vel_lim[1]
            # print("Move J")
            # com_acc[1] -= self.__com_acc[1]
            pass


        # Calcular fricção
        friction = -self.__frict_const * np.array([np.sign(entity.velocity[0])*np.abs(entity.velocity[0]), 0])
        # Composição das acelerações
        if entity.position[1] > entity.floor-1:
            acc = (com_acc+friction)
            self.jumping = True
            self.falling = False
        else:
            friction[0]*=0.15
            acc = (com_acc+self.__grav_acc+friction)
            self.jumping = False
            self.falling = True
            # self.falling = False

        # Atualização das velocidades
        entity.velocity = entity.velocity + acc*dt

        # Saturador das velocidades
        # Saturador Superior
        if np.abs(entity.velocity[0]) >= self.__vel_lim[0]:
            entity.velocity[0] = np.sign(entity.velocity[0])*self.__vel_lim[0]
        if np.abs(entity.velocity[1]) >= self.__vel_lim[1]:
            entity.velocity[1] = np.sign(entity.velocity[1])*self.__vel_lim[1]
        # Saturador Inferior
        if np.abs(entity.velocity[0]) <= 1e-3:
            entity.velocity[0] = 0
        if np.abs(entity.velocity[1]) <= 1e-3:
            entity.velocity[1] = 0

        # Atualização das posições
        entity.position = entity.position + entity.velocity*dt# + acc*(dt**2)/2

        # Temporario
        if entity.position[1] > entity.floor:
            entity.position[1] = entity.floor
            entity.velocity[1] = 0
        return "dt: {dt}\nVelocity: [{x:.2f},{y:.2f}]\nPosition: [{xp:.2f},{yp:.2f}]".format(dt=dt,x=entity.velocity[0],y=entity.velocity[1],xp=entity.position[0],yp=entity.position[1])

    def verify_collision_and_move_mobs(self, bonus_val, coins,entities, mario, start_timer):
        # Move Obstacle/Enemy
        state = "alive"
        mario.hit = False
        if entities:
            for entity in entities:
                if entity.name == "Enemy" or entity.name == "Obstacle":
                    if entity.collide(mario):
                        if not mario.on_cooldown():
                            state = mario.take_hit()
                        mario.hit = mario.hit | True
                    entity.position[0] -= 1.4
                    # Quando Não Aparece no Ecrã
                    if entity.position[0] < -entity.size[0] * -1:
                        entities.pop(entities.index(entity))
                elif entity.name == "Bonus":
                    entity.position[0] -= 1.4
                    if entity.collide(mario):
                        bonus_val += entity.score
                        coins += 1
                        entities.pop(entities.index(entity))
                        pygame.mixer.Sound.play(file.Coin_Sound)
                        # Quando Não Aparece no Ecrã
                    if entity.position[0] < -entity.size[0] * -1:
                        entities.pop(entities.index(entities))

        return start_timer, bonus_val, state, coins
