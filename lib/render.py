import pygame
import numpy as np
import cv2
from lib.entity import entity
from lib.text import TextBox
from lib.scoreboard import scoreboard
import time


class render:
    def __init__(self,window_size=(200,100)):
        self.__window = pygame.display.set_mode(window_size)
        # self.currenttime = int(round(time.time() * 1000))
        self.scoreboard = scoreboard()

    def draw(self, state=0, img=[], entities=[],command=[]):

        for entity in entities:
            pass
        
        if state == -7:
            self.__render_camera(img)

            self.scoreboard.show(self.__window)

        elif state == -9:
            self.__render_camera(img)
            my_scoreboard = scoreboard()

            my_scoreboard.snapshot(self.__window, command[0][0], command[1][0], command[2][0])

            mytext = TextBox(self.__window, size=40)
            mytext.updateText("Say cheese!")
            mytext.display()
            
        elif state == -8:
            self.__render_camera(img)
            my_scoreboard = scoreboard()

            mytext = TextBox(self.__window, size=40)
            mytext.updateText("ITAP!!")
            mytext.display()

            my_scoreboard.snapshot(self.__window, command[0][0], command[1][0], command[2][0], 1)
            
        elif(state == -10):
            self.__render_camera(img)
            mytext = TextBox(self.__window, size=20)
            mytext.updateText("Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n"+
                              "Proin vestibulum, justo lobortis. \n"+
                              "Ut libero sem, eleifend eu maximus suscipit, convallis ac massa.")
            mytext.display()

        if(state == -11):
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
                print(command['debug'])
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
