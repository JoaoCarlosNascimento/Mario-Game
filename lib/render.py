from cv2 import pyrMeanShiftFiltering
import pygame
import numpy as np
import cv2
from lib.entity import entity
from lib.text import TextBox, GameOver, saveScore
from lib.scoreboard import scoreboard
import time

white = (255, 255, 255)
black = (0, 0, 0)
class render:
    def __init__(self,window_size=(200,100)):
        self.__window = pygame.display.set_mode(window_size)
        # self.currenttime = int(round(time.time() * 1000))
        self.scoreboard = scoreboard(window_size)
        self.counter = 3
        self.images = {}
        boo1 = pygame.image.load("./resources/boo1.png").convert_alpha()
        self.images["coin"] = pygame.image.load("./sprite/bonus/Coin.png").convert_alpha()
        self.images["mario2"] = pygame.image.load("./resources/mario2.png").convert_alpha()
        self.images["boo1"] = pygame.transform.scale(boo1, (int(self.__window.get_height()/3), int(self.__window.get_height()/3)))


    def draw(self, state=0, img=[], entities=[], command=[], landmarks=[],debug=""):

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
            
        elif state == "test":
            self.__render_camera(img)
            self.__render_HUD(self.__window, 3, 2000, 3)

        elif(state == -11):
            self.__render_camera(img)
            self.__render_hand_command(command)
        elif(state == -12):
            self.__render_camera(img)
            self.__render_face_command(command)
        elif(state == -13):
            self.__render_camera(img)
            # print(command['landmarks'])
            # if command != [(-1,-1)]:
            if landmarks:
                self.__render_body_command(landmarks)
                mytext = TextBox(self.__window, size=20)
                mytext.updateText(debug)
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

    def __render_HUD(self, window, lives, score, coins):
        HUD = pygame.Surface((window.get_width(), window.get_height()/8))
        HUD.fill(black)
        HUD.set_alpha(150)

        font = pygame.font.Font("./resources/SuperMario256.ttf", HUD.get_height(), bold=False)
        font_s = pygame.font.Font("./resources/SuperMario256.ttf", int(HUD.get_height()*0.8), bold=False)
        
        score = font.render(str(score), 1, white)
        x = font_s.render("x", 1, white)
        coin = font.render("{:03}".format(coins), 1, white)
        
        lives = font.render("{:02}".format(lives), 1, white)
        self.images["mario2"] = pygame.transform.scale(self.images["mario2"], 
                                                      (int(HUD.get_height()), int(HUD.get_height())))
        self.images["coin"] = pygame.transform.scale(self.images["coin"], (int(HUD.get_height()), int(HUD.get_height())))
        HUD.blit(self.images["mario2"], (0,0))
        HUD.blit(x, ((HUD.get_height(), x.get_height()/3)))
        HUD.blit(lives, (HUD.get_height() + x.get_width(), 10))
        HUD.blit(score, (HUD.get_width()/2-score.get_width()/2, 10))
        HUD.blit(self.images["coin"], (HUD.get_width() - HUD.get_height() - x.get_width() - coin.get_width(),0))
        HUD.blit(x, (HUD.get_width() - coin.get_width() - x.get_width(), x.get_height()/3))
        HUD.blit(coin, (HUD.get_width() - coin.get_width(), 10))
        
        window.blit(HUD, (0,0))