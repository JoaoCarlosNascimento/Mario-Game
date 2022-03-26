from html import entities
import time
import pygame
import random
from lib.entity import player, Bonus, Obstacle, Enemy
from lib.load_files import Screen_Width, Screen_Height, USEREVENT

event_ACCELERATE = USEREVENT + 1
event_LAND_ENEMY = USEREVENT + 2
event_AIR_ENEMY = USEREVENT + 3


class logic:
    def __init__(self):
        self.time = int(round(time.time() * 1000))
        self.counter = 3
    def update(self, state=0, feedback = [],entities=[]):

        return self.__state_machine(state, feedback, entities)

    def __state_machine(self, state, feedback, entities):
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
            if feedback != None:
                if "dead" in feedback:
                    state = "game over"
            self.__spawn_entities(entities)
        elif state == "game over":
            if diff_time > 1000:
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
            if feedback!= None:
                if diff_time > 1000 and ("ok pic" in feedback):
                    self.time = int(round(time.time() * 1000))
                    state = "pic"
        
        elif state == "pic":
            state = "leaderboard"

        elif state == "leaderboard":
            if diff_time > 2000:
                self.time = int(round(time.time() * 1000))
                state = "game over"
        
        return state

    def __spawn_entities(self, entities = []):
        for event in pygame.event.get():
            if event.type == event_LAND_ENEMY:
                # Escolhe Obstacle/Bónus Terrestres que Aparecem
                pick_object = random.randrange(0, 2)
                if pick_object == 0:
                    random_pick = random.randrange(18, 25)
                    entities.append(
                        Bonus((Screen_Width, Screen_Height / 1.27), (100, 130), random_pick))

                if pick_object == 1:
                    random_pick = random.randrange(0, 9)
                    entities.append(
                        Enemy((Screen_Width, Screen_Height / 1.27), (100, 130), random_pick))

                if pick_object == 2:
                    random_pick = random.randrange(0, 2)
                    entities.append(
                        Obstacle((Screen_Width, Screen_Height / 1.27), (70, 130), random_pick))

            if event.type == event_AIR_ENEMY:
                pick_object = random.randrange(0, 1)
                if pick_object == 0:
                    random_pick = random.randrange(10, 13)
                    entities.append(
                        Enemy((Screen_Width, Screen_Height / 1.27), (100, 130), random_pick))
                else:
                    random_pick = random.randrange(0, 17)
                    entities.append(Bonus((Screen_Width, Screen_Height / 1.27), (100, 130), random_pick))
