import numpy as np
import lib.load_files as file
import pygame
from pygame.locals import *
import sys
import random
import time


class entity:
    def __init__(self, pos = (-1,-1), size = (10,10), name=[]):
        if type == []:
            raise NameError("Invalid entity name. You must define a name for the entity!")
        self.name = name

        self.count = 0

        # self.entity_state = 0
        # self.animation_state = 0

        self.position = np.array(pos) # [x_pos,y_pos]
        self.velocity = np.array([0, 0])  # [x_speed,y_speed]

        self.size = size

        self.__set_hitbox()

        self.colision_list = []
    
    def update(self, state=0):
        if self.name == "Player":
            # print('Position: ({pos:.2f})\nSpeed: ({spe:.2f})'.format(pos=self.position,spe=self.velocity))
            print('X Speed: ({speX:.2f}), Y Speed: ({speY:.2f})'.format(speX=self.velocity[0],speY=self.velocity[1]))
    def collide(self, rect):
        # 0 - x
        # 1 - y
        # 2 - width
        # 3 - height
        # Verifica Colisão em Coordenada x
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            # Verifica Colisão em Coordenada y
            if rect[1] + rect[3] > self.hitbox[1]:
                return True
        return False

    def __set_hitbox(self):
        self.hitbox = (
            self.position[0], self.position[1], self.size[0], self.size[1])




class player(entity):
    def __init__(self, pos, size, LookingRight):
        entity.__init__(self, pos=pos, size=size, name="Player")

        self.jumping = False
        self.ducking = False
        self.falling = False
        self.duckCount = 0
        self.jumpCount = 0
        self.runCount = 0
        self.duckUp = False
        self.LookingRight = LookingRight

        self.lives = 3
    def update(self, state, timer):
        if self.falling:
            end_timer = int(round(time.time() * 1000))

            # Duração da Animação Hitted (Quando Colide Com Inimigo/Obstáculo)
            if end_timer - timer > 800:
                self.falling = False
            else:
                self.hitbox = (0, 0, 0, 0)

        # Movimentação Default Do Runner
        self.position[0] -= file.Screen_Width / 4000
    def draw(self, window, y=0):
        # print(self.position)

        if self.LookingRight:
            self.run = file.run_anim
            self.jump = file.jump
            self.duck = file.duck
            self.fall = file.fall
            x_offset = 50
        else:
            x_offset = 30
            self.run = file.flip_run_anim
            self.jump = file.flip_jump
            self.duck = file.flip_duck
            self.fall = file.flip_fall

        if self.jumping:
            if self.falling:
                self.hitbox = (0, 0, 0, 0)
                self.position[1] -= file.jumpList[self.jumpCount] * 1.2
                window.blit(self.fall[0], (self.position[0], self.position[1]))
            else:
                # Hitbox do Mario a Saltar
                self.hitbox = (self.position[0] + x_offset, self.position[1] + 30, self.size[0] - 24, self.size[1] + 20)
                self.position[1] -= file.jumpList[self.jumpCount] * 1.2
                window.blit(self.jump[self.jumpCount // 18], (self.position[0], self.position[1]))

            self.jumpCount += 1
            if self.jumpCount > 108:
                self.jumpCount = 0
                self.jumping = False
                self.runCount = 0

        elif self.ducking or self.duckUp:
            if self.falling:
                self.hitbox = (0, 0, 0, 0)
                window.blit(self.fall[0], (self.position[0], self.position[1]))
            else:
                # Hitbox do Mario a Fazer Duck
                self.hitbox = (self.position[0] + x_offset, self.position[1] + 60, self.size[0] - 24, self.size[1] - 30)

            if self.duckCount < 20:
                self.position[1] += 1
            elif self.duckCount == 70:
                self.position[1] -= 19
                self.ducking = False
                self.duckUp = True
            elif 20 < self.duckCount < 80:
                if self.falling:
                    self.hitbox = (0, 0, 0, 0)
                else:
                    # Hitbox do Mario a Fazer Duck
                    self.hitbox = (self.position[0] + x_offset, self.position[1] + 60, self.size[0] - 8, self.size[1] - 35)
            if self.duckCount >= 100:
                self.duckCount = 0
                self.duckUp = False
                self.runCount = 0
            if not self.falling:
                window.blit(self.duck[self.duckCount // 10], (self.position[0], self.position[1] + file.Screen_Height / 25))
            else:
                window.blit(self.fall[0], (self.position[0], self.position[1]))

            self.duckCount += 1

        elif self.falling:
            window.blit(self.fall[0], (self.position[0], self.position[1]))
        else:
            if self.runCount > 42:
                self.runCount = 0

            if random.randint(0, 20) % 5 == 0:
                self.runCount = 0
            else:
                self.runCount = 1
            window.blit(self.run[self.runCount], (self.position[0], self.position[1]))
            if self.falling:
                self.hitbox = (0, 0, 0, 0)
            else:
                # Hitbox do Mario a Correr
                self.hitbox = (self.position[0] + x_offset, self.position[1] + 30, self.size[0] - 24, self.size[1] + 20)
        # Desenhar Hitbox Do Mario
        if not self.falling:
            pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)


# Classe Bonus
class Bonus(entity):
    def __init__(self, pos, size, random_pick):
        entity.__init__(self, pos=pos, size=size, name="Bonus")
        self.random_pick = random_pick
        self.score = 0

    def draw(self, window):
        img, self.position[1], self.hitbox, self.score = file.pick_bonus(self.random_pick, self.position[0], self.position[1], self.size[0],
                                                                   self.size[1])
        window.blit(img, (self.position[0], self.position[1]))
        # Desenho da Hitbox
        pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)


# Class Enemie
class Enemy(entity):
    def __init__(self, pos, size, random_pick):
        entity.__init__(self, pos=pos, size=size, name="Enemy")
        self.random_pick = random_pick

    def draw(self, window):
        img, self.position[1], self.hitbox = file.pick_enemie(self.random_pick, self.position[0], self.position[1], self.size[0], self.size[1])
        window.blit(img, (self.position[0], self.position[1]))
        # Desenho da Hitbox
        pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)


class Obstacle(entity):
    def __init__(self, pos, size, random_pick):
        entity.__init__(self, pos=pos, size=size, name="Obstacle")
        self.random_pick = random_pick

    def draw(self, window):
        img, self.position[1], self.hitbox = file.pick_obstacle(self.random_pick, self.position[0], self.position[1], self.size[0], self.size[1])
        # self.hitbox = (self.position[0] + 10, self.position[1], self.size[0], self.size[1])
        window.blit(img, (self.position[0], self.position[1]))
        pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)

