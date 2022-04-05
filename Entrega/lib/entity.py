import numpy as np
import lib.load_files as file
import pygame
from pygame.locals import *
# import sys
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
        pass



    def collide(self, ent):
        # 0 - x
        # 1 - y
        # 2 - width
        # 3 - height
        # Verifica Colisão em Coordenada x
        if (
            (ent.hitbox[0] < self.hitbox[0] + self.hitbox[2]) and
            (ent.hitbox[0] + ent.hitbox[2] > self.hitbox[0])
            ):
            if (
                (ent.hitbox[1] < self.hitbox[1] + self.hitbox[3]) and
                (ent.hitbox[1] + ent.hitbox[3] > self.hitbox[1])
            ):
                return True
        return False

    def __set_hitbox(self):
        self.hitbox = (
            self.position[0], self.position[1], self.size[0], self.size[1])



import time
class player(entity):
    def __init__(self, pos, size, LookingRight):
        entity.__init__(self, pos=pos, size=size, name="Player")

        self.initDUCK = True
        self.jumping = False
        self.ducking = False
        self.falling = False
        self.duckCount = 0
        self.jumpCount = 0
        self.runCount = 0
        self.duckUp = False
        self.LookingRight = LookingRight
        self.floor = 780

        self.die_timer = int(round(time.time() * 1000))
        self.duck_timer = int(round(time.time() * 1000))

        self.sprites = [] # Indice 1 right, Indice 0 left
        self.sprites.append({"run": file.flip_run_anim, "jump": file.flip_jump,
                            "duck": file.flip_duck, "fall": file.flip_fall, "offset": 30})
        self.sprites.append({"run": file.run_anim,"jump": file.jump,"duck": file.duck,"fall": file.fall,"offset":50})
        

        self.animationPose = self.position
        self.lastAnimationFrame = False
        self.direction = True

        self.hit = False
        self.initCD = True
        self.lives = 5
    def update(self, state, timer):
        pass


    def animation_frame(self):
        if np.abs(self.velocity[0]) > 0:
            if np.abs(self.animationPose[0] - self.position[0]) > 10:
                self.animationPose = self.position
                self.lastAnimationFrame = not self.lastAnimationFrame
        else: 
            self.lastAnimationFrame = True
        return self.lastAnimationFrame

    def draw(self, window, y=0):
        # print(self.position)



        # if self.velocity[0] >= 0
        if np.abs(self.velocity[0]) > 0:
            self.direction = self.velocity[0] >= 0 # False - Left e True - Right
        if self.on_cooldown():
            window.blit(self.sprites[self.direction]["fall"][0],
                        (self.position[0], self.position[1]))
            self.hitbox = (self.position[0], self.position[1], 
                            self.sprites[self.direction]["fall"][0].get_width(), 
                            self.sprites[self.direction]["fall"][0].get_height())
        elif self.position[1] < self.floor-1:
            if not self.duck():
                # Comando jump
                window.blit(self.sprites[self.direction]["jump"][self.animation_frame()],
                            (self.position[0], self.position[1]))
                self.hitbox = (self.position[0], self.position[1], 
                               self.sprites[self.direction]["jump"][self.animation_frame()].get_width(), 
                               self.sprites[self.direction]["jump"][self.animation_frame()].get_height())

            else:
                # Comando jump + duck
                window.blit(self.sprites[self.direction]["duck"][self.animation_frame()],
                            (self.position[0], self.position[1]+35))
                self.hitbox = (self.position[0], self.position[1]+35, 
                               self.sprites[self.direction]["duck"][self.animation_frame()].get_width(), 
                               self.sprites[self.direction]["duck"][self.animation_frame()].get_height())

        else:
            if not self.duck():
                # Comando run
                window.blit(self.sprites[self.direction]["run"][self.animation_frame()],
                            (self.position[0], self.position[1]))
                self.hitbox = (self.position[0],self.position[1], 
                               self.sprites[self.direction]["run"][self.animation_frame()].get_width(), 
                               self.sprites[self.direction]["run"][self.animation_frame()].get_height())
            else:
                # Comando run + duck
                window.blit(self.sprites[self.direction]["duck"][self.animation_frame()],
                            (self.position[0], self.position[1]+70))
                self.hitbox = (self.position[0], self.position[1]+70,
                               self.sprites[self.direction]["duck"][self.animation_frame()].get_width(), 
                               self.sprites[self.direction]["duck"][self.animation_frame()].get_height())





        # Desenha hitbox
        # self.draw_hitbox(window)

        return


    def draw_hitbox(self,window):
        if self.hit:
            pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)
        else:
            pygame.draw.rect(window, (0, 255, 0), self.hitbox, 2)

    def take_hit(self):
        # Set Timer
        self.die_timer = int(round(time.time() * 1000))
        self.lives -= 1

        if self.initCD:
            self.initCD = False

        print("Take Hit")
        pygame.mixer.Sound.play(file.Bump)
        if self.lives <= 0:
            pygame.mixer.Sound.play(file.Mario_Dies)
            return "dead"
            # self.lives = 3 #Reverter
        # self.falling = True  # Reverter

        
    def duck(self,set = False):
        if set:
            # self.ducking = True
            self.duck_timer = int(round(time.time() * 1000))
            if self.initDUCK:
                self.initDUCK = False
        else:
            if self.initDUCK:
                return False
            else:
                return int(round(time.time() * 1000)) - self.duck_timer < 250
            # if int(round(time.time() * 1000)) - self.duck_timer > 1000:
            #     self.ducking = False

    def on_cooldown(self):
        if self.initCD:
            return False
        else:
            return int(round(time.time() * 1000)) - self.die_timer < 2000


# Classe Bonus
class Bonus(entity):
    def __init__(self, pos, size, random_pick):
        entity.__init__(self, pos=pos, size=size, name="Bonus")
        self.random_pick = random_pick
        self.score = 0
        self.random_height = random.randrange(0, 2)

    def draw(self, window):
        img, self.position[1], self.hitbox, self.score = file.pick_bonus(self.random_pick, self.position[0], self.position[1], self.size[0],
                                                                   self.size[1], random_height = self.random_height)
        window.blit(img, (self.position[0], self.position[1]))
        # Desenho da Hitbox
        # pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)


# Class Enemie
class Enemy(entity):
    def __init__(self, pos, size, random_pick):
        entity.__init__(self, pos=pos, size=size, name="Enemy")
        self.random_pick = random_pick

    def draw(self, window):
        img, self.position[1], self.hitbox = file.pick_enemie(self.random_pick, self.position[0], self.position[1], self.size[0], self.size[1])
        window.blit(img, (self.position[0], self.position[1]))
        # Desenho da Hitbox
        # pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)


class Obstacle(entity):
    def __init__(self, pos, size, random_pick):
        entity.__init__(self, pos=pos, size=size, name="Obstacle")
        self.random_pick = random_pick

    def draw(self, window):
        img, self.position[1], self.hitbox = file.pick_obstacle(self.random_pick, self.position[0], self.position[1], self.size[0], self.size[1])
        # self.hitbox = (self.position[0] + 10, self.position[1], self.size[0], self.size[1])
        window.blit(img, (self.position[0], self.position[1]))
        # pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)

