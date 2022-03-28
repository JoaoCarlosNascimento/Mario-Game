from html import entities
import time
import pygame
import random
from lib.entity import player, Bonus, Obstacle, Enemy
from lib.load_files import Screen_Width, Screen_Height, USEREVENT

############################# Eventos Do Pygame Que Geram Inimigos/Bónus/Obstáculos ##########################
# Acelerar Segundo Eventos do Jogo
pygame.time.set_timer(USEREVENT + 1, 1000)

# Evento que Gera Enemies Terrestres entre 4 segundos
pygame.time.set_timer(USEREVENT + 2, 30000)

# Evento que Gera Enemies Aéreos entre 3 segundos
pygame.time.set_timer(USEREVENT + 3, 45000)

event_ACCELERATE = USEREVENT + 1
event_LAND_ENEMY = USEREVENT + 2
event_AIR_ENEMY = USEREVENT + 3


class logic:
    def __init__(self):
        self.time = int(round(time.time() * 1000))

        self.counter = 3
    def update(self, state=0, feedback = [], entities=[], speed = 0):
        state, speed = self.__state_machine(state, feedback, entities, speed)
        return state, speed

    def __state_machine(self, state, feedback, entities, speed):
        diff_time = int(round(time.time() * 1000)) - self.time
        

        if state == "menu":
            if feedback != None:
                if "play" in feedback:
                    state = "game"
                elif "ctrl" in feedback:
                    state = "control"
        elif state == "control":
            if feedback != None:
                if "back" in feedback:
                    state = "menu"
        elif state == "game":
            entities.clear()
            entities.append(player((1920 / 10, 1080 / 1.3), (100, 95), True))
            state = "game loop"
        elif state == "game loop":
            if feedback != None:
                if "dead" in feedback:
                    state = "game over"
            speed = self.__spawn_entities(entities, speed)
            
        elif state == "game over":
            self.time = int(round(time.time() * 1000))
            state = "game over 2"
        elif state == "game over 2":
            if diff_time > 3000:
                self.time = int(round(time.time() * 1000))
                state = "save score?"

        elif state == "save score?":
            if diff_time > 100:
                self.time = int(round(time.time() * 1000))
                if feedback != None:
                    if "yes score" in feedback:
                        state = "prepare pic"
                    elif "no score" in feedback:
                        state = "leaderboard" 
        elif state == "prepare pic":
            self.time = int(round(time.time() * 1000))
            state = "prepare pic2"
        elif state == "prepare pic2":
            if feedback!= None:
                if diff_time > 1000 and ("ok pic" in feedback):
                    self.time = int(round(time.time() * 1000))
                    state = "pic"
        
        elif state == "pic":
            state = "leaderboard"

        elif state == "leaderboard":
            self.time = int(round(time.time() * 1000))
            state = "leaderboard2"
        elif state == "leaderboard2":
            if diff_time > 2000:
                self.time = int(round(time.time() * 1000))
                state = "menu"
        
        return state,speed

    def __spawn_entities(self, entities = [], speed = 0):
        for event in pygame.event.get():
            if event.type == event_ACCELERATE:
                speed += 3

            if event.type == event_LAND_ENEMY:
                # Escolhe Obstacle/Bónus Terrestres que Aparecem
                pick_object = random.randrange(0, 2)
                if pick_object == 0:
                    random_pick = random.randrange(18, 25)
                    entities.append(
                        Bonus((Screen_Width, Screen_Height / 1.27), (100, 130), random_pick))

                else:
                    pick = random.randrange(0, 1)
                    if pick == 0:
                        random_pick = random.randrange(0,9)
                        entities.append(
                            Enemy((Screen_Width, Screen_Height / 1.27), (100, 130), random_pick))
                    else:
                        random_pick = random.randrange(0, 2)
                        entities.append(
                            Obstacle((Screen_Width, Screen_Height / 1.27), (70, 130), random_pick))

            elif event.type == event_AIR_ENEMY:
                pick_object = random.randrange(0, 2)
                if pick_object == 1:
                    random_pick = random.randrange(10, 13)
                    entities.append(
                        Enemy((Screen_Width, Screen_Height / 1.27), (100, 130), random_pick))
                else:
                    random_pick = random.randrange(0, 17)
                    entities.append(Bonus((Screen_Width, Screen_Height / 1.2), (100, 130), random_pick))
        return speed