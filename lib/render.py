import pygame
import numpy as np
import cv2
from lib.entity import entity
from lib.text import TextBox, GameOver, saveScore
from lib.scoreboard import scoreboard
import time


class render:
    def __init__(self,window_size=(200,100)):
        self.__window = pygame.display.set_mode(window_size)
        # self.currenttime = int(round(time.time() * 1000))
        self.scoreboard = scoreboard(window_size)
        self.counter = 3
        self.images = {}
        boo1 = pygame.image.load("./resources/boo1.png").convert_alpha()
        self.images["boo1"] = pygame.transform.scale(boo1, (int(self.__window.get_height()/3), int(self.__window.get_height()/3)))


    def draw(self, state=0, img=[], entities=[],command=[]):

        for entity in entities:
            pass
        if state == "game over":
            self.__render_camera(img)
            GameOver(self.__window)

        elif state == "save score?":
            self.__render_camera(img)
            sc = saveScore(self.__window, 9999, hand_pos=command)
            if (sc == 1):
                return "yes score"
            elif (sc == 0):
                return "no score"
            self.__render_hand_command([command])

        elif state == "leaderboard":
            self.__render_camera(img)
            self.scoreboard.show(self.__window)

        elif state == "prepare pic":
            self.__render_camera(img)
            if len(command) != 4:
                return
            self.scoreboard.display(self.__window,command)

            boo1 = self.__window.blit(self.images["boo1"], [self.__window.get_width() - self.images["boo1"].get_width(),
                                                            self.__window.get_height() - self.images["boo1"].get_height()])

            font = pygame.font.Font("./resources/SuperMario256.ttf", 50, bold=False)
            text = font.render("Touch Boo when you're ready!", 1, (0,0,0))
            self.__window.blit(text, [self.__window.get_width()/2 - text.get_width()/2, 
                                      self.__window.get_height()/4 - text.get_height()/2])
            if (boo1.collidepoint(command[3])):
                return "ok pic"

        elif state == "pic":
            self.__render_camera(img)
            self.scoreboard.snapshot(self.__window, command, 10000)
            

        elif(state == -11):
            self.__render_camera(img)
            self.__render_hand_command(command)
        elif(state == -12):
            self.__render_camera(img)
            self.__render_face_command(command)
        elif(state == -13):
            self.__render_camera(img)
            # print(command['landmarks'])
            if command != [(-1,-1)]:
                self.__render_body_command(command['landmarks'])
                # print(command['debug'])
                mytext = TextBox(self.__window, size=20)
                mytext.updateText(command['debug'])
                mytext.display()
        
        pygame.display.update()


    def __render_camera(self, img=[]):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imgRGB = np.rot90(imgRGB)
        frame = pygame.surfarray.make_surface(imgRGB).convert()
        self.__window.blit(frame, (0,0))

    def __render_hand_command(self,command = []):
        if command != []:
            for com in command:
                if com != (-1,-1):
                    pygame.draw.circle(self.__window, (191, 39, 28), com, 15)

    def __render_face_command(self,command = []):
        if command != []:
            for com in command:
                if com != (-1,-1):
                    pygame.draw.circle(self.__window, (191, 39, 28), com, 15)
    
    def __render_body_command(self,command = []):
        if command:
            # print(command)
            for com in command:
                if com != (-1,-1):
                    pygame.draw.circle(self.__window, (191, 39, 28), (com.x,com.y), 15)
