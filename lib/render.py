import pygame
import numpy as np
import cv2
from lib.entity import entity
from lib.text import TextBox
class render:
    def __init__(self,window_size=(200,100)):
        self.__window = pygame.display.set_mode(window_size)

    def draw(self, state=0, img=[], entities=[],command=[]):

        for entity in entities:
            pass
        
        if(state == -10):
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
            self.__render_body_command(command)

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
