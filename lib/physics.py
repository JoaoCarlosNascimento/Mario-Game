# from calendar import c
# from turtle import position
from lib.colision import colision
import numpy as np
import pygame
import lib.load_files as file
import time


class physics:
    def __init__(self):
        self.__timer = 0
        pass

    def update(self, state=0,entities=[], commands=0b0000, score = 0, bonus_val = 0):
        bonus = []
        obstacles = []
        enemies = []

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
        self.__timer, bonus, lives, state = self.verify_collision(bonus_val, enemies, mario, bonus, self.__timer)
        mario.update(state, self.__timer)
        self.keyboards_input(mario)

        return bonus, lives, state


        # for entity in entities:
        #     return

    # Constantes de aceleração
    __frict_const = np.array([2, 0])  # [acc_x,acc_y]
    __com_acc = np.array([2, 1])+__frict_const  # [acc_x,acc_y]
    __grav_acc = np.array([0, -3])  # [acc_x,acc_y]
    __norm_acc = -__grav_acc  # [acc_x,acc_y]

    # Constantes de velocidade
    __vel_lim = np.array([3, 2])  # [vel_x,vel_y]
    __vel_jump = np.array([0, 5])  # [vel_x,vel_y]


    def __move(self,entity,commands = 0b0000):
        dt = 0.1
        com_acc = np.array([0,0])

        # Converter comandos em ações
        if ((commands & 0b1000) == 0b1000): # Move Right
            com_acc[0] += self.__com_acc[0]
        if ((commands & 0b0100) == 0b0100): # Move Left
            com_acc[0] -= self.__com_acc[0]
        if ((commands & 0b0010) == 0b0010):  # Move Crouch
            # print("Move C")
            # com_acc[1] += self.__com_acc[1]
            pass
        if ((commands & 0b0001) == 0b0001):  # Move Jump
            if entity.velocity[1] == 0:
                entity.velocity[1] = self.__vel_jump[1]
            # print("Move J")
            # com_acc[1] -= self.__com_acc[1]
            pass


        # Calcular fricção
        friction = -self.__frict_const * np.array([np.sign(entity.velocity[0])*np.abs(entity.velocity[0]), 0])
        # Composição das acelerações
        acc = (com_acc+self.__grav_acc+friction)

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
        entity.position = entity.position + entity.velocity*dt + acc*(dt**2)/2

        # Temporario
        if entity.position[1] < 0:
            entity.position[1] = 0
        

    def __detect_colisions(self,entity_list):
        for entity in entity_list:
            filt_entity_list = []
            for ent in entity_list:
                if ent != entity:
                    filt_entity_list.append(ent)
            

            #print(filt_entity_list)
        pass

    def keyboards_input(self, character):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            if not character.jumping and not character.falling:
                character.jumping = True
                pygame.mixer.Sound.play(file.Jump)

        # Mover Para a Direita
        if keys[pygame.K_RIGHT]:
            character.x += file.Screen_Width / 60
            character.LookingRight = True

        # Mover Para a Esquerda
        if keys[pygame.K_LEFT]:
            character.x -= file.Screen_Width / 60
            character.LookingRight = False

        if keys[pygame.K_DOWN]:
            if not character.ducking and not character.falling:
                character.ducking = True
                pygame.mixer.Sound.play(file.Duck)

    def verify_collision(self, bonus_val, enemies, mario, plus, start_timer):
        # Move Obstacle/Enemy
        state = "alive"
        for x in enemies:
            if x.collide(mario.hitbox):
                start_timer = int(round(time.time() * 1000))
                pygame.mixer.Sound.play(file.Bump)
                mario.lives -= 1
                # Game Over
                if mario.lives <= 0:
                    pygame.mixer.Sound.play(file.Mario_Dies)
                    state = "dead"
                    # mario.lives = 3
                mario.falling = True
            x.x -= 1.4
            # Quando Não Aparece no Ecrã
            if x.x < -x.width * -1:
                enemies.pop(enemies.index(x))
        # Move Bonus
        for y in plus:
            if y.collide(mario.hitbox):
                bonus_val += y.score
                plus.pop(plus.index(y))
                pygame.mixer.Sound.play(file.Coin_Sound)
                # Quando Não Aparece no Ecrã
            if y.x < -y.width * -1:
                plus.pop(plus.index(y))
            y.x -= 1.4

        return start_timer, bonus_val, mario.lives, state

    # def detectCollision(self,character, start_timer):
    #     if character.falling:
    #         end_timer = time.time()

    #         # Duração da Animação Hitted (Quando Colide Com Inimigo/Obstáculo)
    #         if end_timer - start_timer > 0.8:
    #             character.falling = False
    #         else:
    #             character.hitbox = (0, 0, 0, 0)

    #     # Movimentação Default Do Runner
    #     character.x -= file.Screen_Width / 4000
