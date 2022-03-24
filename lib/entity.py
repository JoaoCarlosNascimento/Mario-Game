import numpy as np
import load_files as file
import pygame
from pygame.locals import *
import sys
import random
import time


# id_list = []
Loser_Text = file.font.render('Loser', True, (255, 255, 255), (0, 0, 0))
LoserRect = Loser_Text.get_rect()
LoserRect.center = (file.Screen_Width // 2, file.Screen_Height // 2)

clock = pygame.time.Clock()

window = pygame.display.set_mode((file.Screen_Width, file.Screen_Height))
pygame.display.set_caption("Test")

# Mover BackGround
BackGroundX = 0
BackGroundX2 = file.BackGround.get_width()


def create_anim(image, scale, number_images):
    animation = []
    for i in range(number_images):
        animation.append(pygame.image.load(image[i]))
        animation[i] = pygame.transform.scale(animation[i], (file.Screen_Width / scale[0], file.Screen_Width / scale[1]))
        animation[i] = pygame.transform.flip(animation[i], True, False)

    return animation


def flip_anim(image, number_images):
    animation = []
    for i in range(number_images):
        animation.append(image[i])
        animation[i] = pygame.transform.flip(animation[i], True, False)
    return animation


run_anim = create_anim(file.run_string, file.scale, 2)
jump = create_anim(file.jump_string, file.scale, 8)
duck = create_anim(file.duck_string, file.scale, 11)
fall = create_anim(file.fall_string, file.scale, 1)

flip_run_anim = flip_anim(run_anim, 2)
flip_jump = flip_anim(jump, 8)
flip_duck = flip_anim(duck, 11)
flip_fall = flip_anim(fall, 1)



class entity:
    def __init__(self, name=[]):
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
        if self.name == "Player":
            # print('Position: ({pos:.2f})\nSpeed: ({spe:.2f})'.format(pos=self.position,spe=self.velocity))
            print('X Speed: ({speX:.2f}), Y Speed: ({speY:.2f})'.format(speX=self.velocity[0],speY=self.velocity[1]))


class player(entity):
    def __init__(self, x, y, width, height, LookingRight):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.jumping = False
        self.ducking = False
        self.falling = False
        self.duckCount = 0
        self.jumpCount = 0
        self.runCount = 0
        self.duckUp = False
        self.LookingRight = LookingRight

    def draw(self, window, y):

        if self.LookingRight:
            self.run = run_anim
            self.jump = jump
            self.duck = duck
            self.fall = fall
            x_offset = 50
        else:
            x_offset = 30
            self.run = flip_run_anim
            self.jump = flip_jump
            self.duck = flip_duck
            self.fall = flip_fall

        count = random.randint(0, 1)
        if self.jumping:
            if self.falling:
                self.hitbox = (0, 0, 0, 0)
                self.y -= file.jumpList[self.jumpCount] * 1.2
                window.blit(self.fall[0], (self.x, self.y))
            else:
                # Hitbox do Mario a Saltar
                self.hitbox = (self.x + x_offset, self.y + 30, self.width - 24, self.height + 20)
                self.y -= file.jumpList[self.jumpCount] * 1.2
                window.blit(self.jump[self.jumpCount // 18], (self.x, self.y))

            self.jumpCount += 1
            if self.jumpCount > 108:
                self.jumpCount = 0
                self.jumping = False
                self.runCount = 0

        elif self.ducking or self.duckUp:
            if self.falling:
                self.hitbox = (0, 0, 0, 0)
                window.blit(self.fall[0], (self.x, self.y))
            else:
                # Hitbox do Mario a Fazer Duck
                self.hitbox = (self.x + x_offset, self.y + 60, self.width - 24, self.height - 30)

            if self.duckCount < 20:
                self.y += 1
            elif self.duckCount == 70:
                self.y -= 19
                self.ducking = False
                self.duckUp = True
            elif 20 < self.duckCount < 80:
                if self.falling:
                    self.hitbox = (0, 0, 0, 0)
                else:
                    # Hitbox do Mario a Fazer Duck
                    self.hitbox = (self.x + x_offset, self.y + 60, self.width - 8, self.height - 35)
            if self.duckCount >= 100:
                self.duckCount = 0
                self.duckUp = False
                self.runCount = 0
            if not self.falling:
                window.blit(self.duck[self.duckCount // 10], (self.x, self.y + file.Screen_Height / 25))
            else:
                window.blit(self.fall[0], (self.x, self.y))

            self.duckCount += 1

        elif self.falling:
            window.blit(self.fall[0], (self.x, self.y))
        else:
            if self.runCount > 42:
                self.runCount = 0

            if random.randint(0, 20) % 5 == 0:
                self.runCount = 0
            else:
                self.runCount = 1
            window.blit(self.run[self.runCount], (self.x, self.y))
            if self.falling:
                self.hitbox = (0, 0, 0, 0)
            else:
                # Hitbox do Mario a Correr
                self.hitbox = (self.x + x_offset, self.y + 30, self.width - 24, self.height + 20)
        # Desenhar Hitbox Do Mario
        if not self.falling:
            pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)

    # Classe Bonus
    class Bonus(entity):
        def __init__(self, x, y, width, height, random_pick):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.hitbox = (x, y, width, height)
            self.count = 0
            self.random_pick = random_pick
            self.score = 0

        def draw(self, window):
            img, self.y, self.hitbox, self.score = file.pick_bonus(self.random_pick, self.x, self.y, self.width,
                                                                   self.height)
            window.blit(img, (self.x, self.y))
            # Desenho da Hitbox
            pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)

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

    # Class Enemie
    class Enemie(entity):
        def __init__(self, x, y, width, height, random_pick):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.hitbox = (x, y, width, height)
            self.count = 0
            self.random_pick = random_pick

        def draw(self, window):
            img, self.y, self.hitbox = file.pick_enemie(self.random_pick, self.x, self.y, self.width, self.height)
            window.blit(img, (self.x, self.y))
            # Desenho da Hitbox
            pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)

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

    class Obstacle(entity):
        def __init__(self, x, y, width, height, random_pick):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.hitbox = (x, y, width, height)
            self.count = 0
            self.random_pick = random_pick

        def draw(self, window):
            img, self.y, self.hitbox = file.pick_obstacle(self.random_pick, self.x, self.y, self.width, self.height)
            # self.hitbox = (self.x + 10, self.y, self.width, self.height)
            window.blit(img, (self.x, self.y))
            pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)

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
