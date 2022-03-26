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

    def update(self, state=0,entities=[], commands=0b0000, score = 0, bonus_val = 0):
        bonus = []
        obstacles = []
        enemies = []
        debug = []
        if state == "game":

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
            self.__timer, bonus, state = self.verify_collision_and_move_mobs(
                bonus_val, enemies, mario, bonus, self.__timer)
            # Move mario left
            mario.position[0] -= file.Screen_Width / 4000
            # mario.update(state, self.__timer)
            debug = self.__move(mario,commands=commands)
            # self.keyboards_input(mario)

            return bonus, mario.lives, state, debug
        return 0, 0, 0, ""


        # for entity in entities:
        #     return

    # Constantes de aceleração
    __frict_const = np.array([2, 2])  # [acc_x,acc_y]
    __com_acc = np.array([350, -50])+__frict_const  # [acc_x,acc_y]
    __grav_acc = np.array([0, 100])  # [acc_x,acc_y]
    __norm_acc = -__grav_acc  # [acc_x,acc_y]

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
            entity.ducking = True
            # print("Move C")
            # com_acc[1] += self.__com_acc[1]

        if ((commands & 0b0001) == 0b0001):  # Move Jump
            if entity.velocity[1] == 0 and entity.position[1] > 829:
                entity.velocity[1] = -self.__vel_lim[1]
            # print("Move J")
            # com_acc[1] -= self.__com_acc[1]
            pass


        # Calcular fricção
        friction = -self.__frict_const * np.array([np.sign(entity.velocity[0])*np.abs(entity.velocity[0]), 0])
        # Composição das acelerações
        if entity.position[1] > 829:
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
        if entity.position[1] > 830:
            entity.position[1] = 830
            entity.velocity[1] = 0
        return "dt: {dt}\nVelocity: [{x:.2f},{y:.2f}]\nPosition: [{xp:.2f},{yp:.2f}]".format(dt=dt,x=entity.velocity[0],y=entity.velocity[1],xp=entity.position[0],yp=entity.position[1])
        

    # def __detect_colisions(self,entity_list):
    #     for entity in entity_list:
    #         filt_entity_list = []
    #         for ent in entity_list:
    #             if ent != entity:
    #                 filt_entity_list.append(ent)
            

    #         #print(filt_entity_list)
    #     pass

    # def keyboards_input(self, character):
    #     keys = pygame.key.get_pressed()
    #     if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
    #         if not character.jumping and not character.falling:
    #             character.jumping = True
    #             pygame.mixer.Sound.play(file.Jump)

    #     # Mover Para a Direita
    #     if keys[pygame.K_RIGHT]:
    #         character.position[0] += file.Screen_Width / 60
    #         character.LookingRight = True

    #     # Mover Para a Esquerda
    #     if keys[pygame.K_LEFT]:
    #         character.position[0] -= file.Screen_Width / 60
    #         character.LookingRight = False

    #     if keys[pygame.K_DOWN]:
    #         if not character.ducking and not character.falling:
    #             character.ducking = True
    #             pygame.mixer.Sound.play(file.Duck)

    def verify_collision_and_move_mobs(self, bonus_val, enemies, mario, plus, start_timer):
        # Move Obstacle/Enemy
        state = "alive"
        for x in enemies:
            if x.collide(mario.hitbox):
                if not mario.on_cooldown():
                    mario.take_hit()
                mario.hit = True
            else:
                mario.hit = False
            x.position[0] -= 1.4
            # Quando Não Aparece no Ecrã
            if x.position[0] < -x.size[0] * -1:
                enemies.pop(enemies.index(x))
        # Move Bonus
        for y in plus:
            if y.collide(mario.hitbox):
                bonus_val += y.score
                plus.pop(plus.index(y))
                pygame.mixer.Sound.play(file.Coin_Sound)
                # Quando Não Aparece no Ecrã
            if y.position[0] < -y.size[0] * -1:
                plus.pop(plus.index(y))
            y.position[0] -= 1.4

        return start_timer, bonus_val, state

    # def detectCollision(self,character, start_timer):
    #     if character.falling:
    #         end_timer = time.time()

    #         # Duração da Animação Hitted (Quando Colide Com Inimigo/Obstáculo)
    #         if end_timer - start_timer > 0.8:
    #             character.falling = False
    #         else:
    #             character.hitbox = (0, 0, 0, 0)

    #     # Movimentação Default Do Runner
    #     character.position[0] -= file.Screen_Width / 4000
