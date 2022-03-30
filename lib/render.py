from cv2 import pyrMeanShiftFiltering
import pygame
import numpy as np
import cv2
from lib.entity import entity
from lib.text import TextBox
from lib.scoreboard import scoreboard
import lib.load_files as file
import time
from lib.image import gif, image
from lib.entity import Enemy, Bonus, Obstacle, player
# from lib.controls import controls_menu

white = (255, 255, 255)
black = (0, 0, 0)



class render:
    def __init__(self, window_size=(1920,1080)):
        self.__window = file.window
        # self.currenttime = int(round(time.time() * 1000))
        self.scoreboard = scoreboard(window_size)
        self.counter = 3
        self.__window_size = window_size
        self.__load_images()
        self.__load_fonts()
        self.__load_text()
    def draw(self, state=0, img=[], entities=[], command=[], landmarks=[],debug="", bonus_val = 0, lives = 3, score = 0, coins = 0, final_score = 0):
        enemies = []
        obstacles = []
        bonus = []

        feedback = "" 
    
        if state == "menu":
            imgScale = self.__render_camera(img)

            for i in range(2):
                if landmarks[i] != (-1, -1):
                    landmarks[i] = (
                        imgScale[0]*landmarks[i][0],
                        imgScale[1]*landmarks[i][1]
                    )
            feedback = self.__render_menu(landmarks)
        elif state == "control":
            imgScale = self.__render_camera(img)
            for i in range(2):
                if landmarks[i] != (-1, -1):
                    landmarks[i] = (
                        imgScale[0]*landmarks[i][0],
                        imgScale[1]*landmarks[i][1]
                    )
            feedback = self.__render_control_menu(landmarks)
        elif state == "game over 2":
            self.__render_camera(img)
            # GameOver(self.__window)
            self.__render_gameOver()

        elif state == "save score?":
            scale_factor = self.__render_camera(img)
            # print(landmarks)
            correctedLandmark = (scale_factor[0]*landmarks[0][0],scale_factor[1]*landmarks[0][1])
            # print(correctedLandmark)

            sc = self.__render_saveScore(final_score, correctedLandmark)
            if (sc == 1):
                feedback = "yes score"
            elif (sc == 0):
                feedback = "no score"
                self.scoreboard.snapshot(self.__window, [correctedLandmark], score=final_score, save=0)
            self.__render_cursor([correctedLandmark, (-1, -1)])

        elif state == "leaderboard2":
            self.__render_camera(img)
            self.scoreboard.show(self.__window)

        elif state == "prepare pic2":
            imgScale = self.__render_camera(img)

            for i in range(3):
                if landmarks[0][i] != (-1, -1):
                    landmarks[0][i] = (
                        imgScale[0]*landmarks[0][i][0],
                        imgScale[1]*landmarks[0][i][1]
                    )

            for i in range(2):
                if landmarks[1][i] != (-1, -1):
                    landmarks[1][i] = (
                        imgScale[0]*landmarks[1][i][0],
                        imgScale[1]*landmarks[1][i][1]
                    )


            boo1 = self.__window.blit(self.images["boo1"].image, [self.__window.get_width() - self.images["boo1"].get_width(),
                                                                  self.__window.get_height() - self.images["boo1"].get_height()])

            # font = pygame.font.Font("./resources/SuperMario256.ttf", 50, bold=False)
            text = self.fonts["normal"].render("Touch Boo when you're ready!", 1, (0,0,0))
            self.__window.blit(text, [self.__window.get_width()/2 - text.get_width()/2, 
                                      self.__window.get_height()/4 - text.get_height()/2])

            self.scoreboard.display(self.__window, landmarks) # Draw Square
            self.__render_cursor([landmarks])
            if (boo1.collidepoint(landmarks[1][0])):
                return "ok pic"
            if landmarks[1][0] != (-1, -1) or landmarks[1][1] != (-1, -1):
                self.__render_cursor(landmarks[1])

        elif state == "pic":
            imgScale = self.__render_camera(img)
            for i in range(3):
                if landmarks[0][i] != (-1, -1):
                    landmarks[0][i] = (
                        imgScale[0]*landmarks[0][i][0],
                        imgScale[1]*landmarks[0][i][1]
                    )

            for i in range(2):
                if landmarks[1][i] != (-1, -1):
                    landmarks[1][i] = (
                        imgScale[0]*landmarks[1][i][0],
                        imgScale[1]*landmarks[1][i][1]
                    )
            self.scoreboard.snapshot(self.__window, landmarks, final_score, 1)
            
        elif state == "game loop":
            if entities:
                for entity in entities:
                    if entity.name == "Player":
                        mario = entity
                    elif entity.name == "Enemy":
                        enemies.append(entity)
                    elif entity.name == "Obstacle":
                        obstacles.append(entity)
                    elif entity.name == "Bonus":
                        bonus.append(entity)
                self.redrawWindow(mario.position[0], entities, mario, score, lives, coins)
                self.check_BackGround()
            t = TextBox(self.__window, debug)
            t.display()

        elif(state == -11):
            self.__render_camera(img)
            self.__render_hand_command(landmarks)
        elif(state == -12):
            self.__render_camera(img)
            self.__render_face_command(landmarks)
        elif(state == -13):
            self.__render_camera(img)
            if landmarks:
                self.__render_body_command(landmarks)
            mytext = TextBox(self.__window, size=20)
            mytext.updateText(debug)
            mytext.display()
        
        pygame.display.update()
        return feedback

    def __render_camera(self, img=[], size=(1920,1080)):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imgRGB = np.rot90(imgRGB)
        priorSize = imgRGB.shape
        imgRGB = cv2.resize(imgRGB, (size[1],size[0]), interpolation = cv2.INTER_AREA)
        frame = pygame.surfarray.make_surface(imgRGB).convert()
        self.__window.blit(frame, (0,0))
        outputFactor = (imgRGB.shape[0]/priorSize[0],imgRGB.shape[1]/priorSize[1])
        return outputFactor

    def __render_hand_command(self,command = []):
        # if len(command) >= 2:
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

    def __render_HUD(self, lives, score, coins):
        # print(score) # Ajustar scores
        HUD = pygame.Surface((self.__window_size[0], self.__window_size[1]/8),  pygame.SRCALPHA, 32)

        # font = pygame.font.Font("./resources/SuperMario256.ttf", HUD.get_height(), bold=False)
        # font_s = pygame.font.Font("./resources/SuperMario256.ttf", int(HUD.get_height()*0.8), bold=False)
        
        score = self.fonts["HUD"].render(str(score), 1, white)
        coin = self.fonts["HUD"].render("{:03}".format(coins), 1, white)
        
        lives = self.fonts["HUD"].render("{:02}".format(lives), 1, white)
        self.images["mario2"].resize((int(HUD.get_height()), int(HUD.get_height())))
        self.images["coin"].resize((int(HUD.get_height()), int(HUD.get_height())))
        HUD.blit(self.images["mario2"].image, (0, 0))
        HUD.blit(self.text["x"], ((HUD.get_height(), self.text["x"].get_height()/3)))
        HUD.blit(lives, (HUD.get_height() + self.text["x"].get_width(), 10))
        HUD.blit(score, (HUD.get_width()/2-score.get_width()/2, 10))
        HUD.blit(self.images["coin"].image, (HUD.get_width() - HUD.get_height() - self.text["x"].get_width() - coin.get_width(),0))
        HUD.blit(self.text["x"], (HUD.get_width() - coin.get_width() - self.text["x"].get_width(), self.text["x"].get_height()/3))
        HUD.blit(coin, (HUD.get_width() - coin.get_width(), 10))
        
        self.__window.blit(HUD, (0,0))

    # Função Utilizada Durante o Jogo Para Desenhar HUD(Score e Vidas), Inimigos, Bónus, Mario e Obstáculos
    def redrawWindow(self,Movement_x, entities, runner, score, lives, coins):
        file.window.blit(file.BackGround, (file.BackGroundX, 0))  # draws our first BackGround image
        file.window.blit(file.BackGround, (file.BackGroundX2, 0))  # draws the second BackGround image

        self.__render_HUD(lives, score, coins)
        if entities:
            for entity in entities:
                if entity.name == "Enemy" or entity.name == "Obstacle":
                    if entity.position[0] >= -entity.size[0] * -1:
                        entity.draw(file.window)
                    else:
                        entities.pop(entities.index(entity))
                elif entity.name == "Bonus":
                    entity.draw(file.window)

        # Objectos = Lista que Contém Inimigos/Obstáculos

        # Bonus = Lista que Contém Bónus

        # Condição que Verifica se Mario Saiu Do Ecrã
        if Movement_x <= -70:
            runner.take_hit()
            runner.position = np.array([1920 / 10, 1080 / 1.3])

        runner.draw(file.window, 95)  # NEW

        #     file.window.blit(file.Loser_Text, file.LoserRect)

    # Atualiza BackGround
    def check_BackGround(self):
        file.BackGroundX -= 1  # Move both background images back
        file.BackGroundX2 -= 1

        # 1º BackGround Image starts at (0,0)
        if file.BackGroundX < file.BackGround.get_width() * -1:  # If our BackGround is at the -width then reset its position
            file.BackGroundX = file.BackGround.get_width()

        if file.BackGroundX2 < file.BackGround.get_width() * -1:
            file.BackGroundX2 = file.BackGround.get_width()
    def __load_images(self):
        self.images = {}
        self.gifs = {}
        
        size = [int(self.__window.get_width()/6), self.__window.get_height()/8]
        well_done_size = [950, 150]
        logo_size = [900, 400]
        tip_size = [75, 85]

        ctrl_gif_size = [500, 500]
        controls_size = [750, 150]
        back_size = [180, 100]
        tip_size = [75, 85]
        dir_size = [140, 200]
        # HUD
        self.images["coin"] = image("./sprite/bonus/Coin.png", self.__window)
        self.images["mario2"] = image("./resources/mario2.png", self.__window)
        self.images["boo1"] = image("./resources/boo1.png", self.__window, (int(self.__window.get_height()/3), 
                                                                           int(self.__window.get_height()/3)))
        # main menu 
        self.images["play"] = image("Images/play_menu.png", self.__window, size, (2.6, 2))
        self.images["ctrl_menu"] = image("Images/controls_menu.png", self.__window, size, (-0.6, 2))
        self.images["score"] = image("Images/scores_menu.png", self.__window, size, (1, -1))
        self.images["logo"] = image("Images/logo_menu.png", self.__window, logo_size, (1, 3))
        self.images["star"] = image("Images/Star.PNG", self.__window, tip_size, (1, 1))
        self.images["background"] = image("Images/background.PNG", self.__window, self.__window_size)
        # ctrl menu
        self.images["ctrl"] = image("Images/controls_.png", self.__window, controls_size, position=(1, 6.5))
        self.images["back"] = image("Images/back_.png", self.__window, back_size, position=(9.5, 9))
        self.images["right"] = image("Images/right_direction.png", self.__window, dir_size, position=(-8, -2.5))
        self.images["left"] = image("Images/left_direction.png", self.__window, dir_size, position=(10, -2.5))
        
        # game over
        self.images["well_done"] = image('Images/well_done.png', self.__window, well_done_size)
        self.images["game_over_background"] = image('Images/back_over.png', self.__window, self.__window_size)
        # save score?
        self.images["lakitu"] = image("./resources/lakitu.png", self.__window, (500, 600), (1, 0))

        # gifs
        self.gifs["menu"] = gif(position=(1, 1), size=self.__window_size, foldername="Image_Menu", window=self.__window, limit=49)

        self.gifs["ctrl_right"] = gif(position=(-1.5, 1), size=ctrl_gif_size, foldername="Image_right", window=self.__window, limit=23)
        self.gifs["ctrl_left"] = gif(position=(3.5, 1), size=ctrl_gif_size, foldername="Image_left", window=self.__window, limit=23)
        self.gifs["jump_duck"] = gif(position=(1, 1), size=ctrl_gif_size, foldername="Image_jumpduck", window=self.__window, limit=17)
    def __load_fonts(self):
        self.fonts = {}
        self.fonts["big"] = pygame.font.Font("./resources/SuperMario256.ttf", int(self.__window_size[1]/10), bold=False)
        self.fonts["small"] = pygame.font.Font("./resources/SuperMario256.ttf", int(self.__window_size[1]/20), bold=False)
        self.fonts["normal"] = pygame.font.Font("./resources/SuperMario256.ttf", int(self.__window_size[1]/15), bold=False)

        self.fonts["HUD"] = pygame.font.Font("./resources/SuperMario256.ttf", int(self.__window_size[1]/8), bold=False)
        self.fonts["HUD_small"] = pygame.font.Font("./resources/SuperMario256.ttf", int(0.8*self.__window_size[1]/8), bold=False)
    

    def __load_text(self):
        self.text = {}
        self.text["save?"] = self.fonts["normal"].render("Would you like to save your picture?", 1, black)
        self.text["yes"] = self.fonts["normal"].render("Yes", 1, black)
        self.text["no"] = self.fonts["normal"].render("No", 1, black)
        
        # scroller
        self.text["x"] = self.fonts["HUD_small"].render("x", 1, white)

    def __render_menu(self, landmarks):
        
        self.images["background"].display()
        self.images["play"].display()
        self.images["ctrl_menu"].display()
        self.images["score"].display()
        self.images["score"].display()
        self.images["logo"].display()
        
        self.gifs["menu"].draw()

        if landmarks[0] != (-1, -1) or landmarks[1] != (-1, -1):
            self.__render_cursor(landmarks)
            if self.images["play"].collide(landmarks[0]) or self.images["play"].collide(landmarks[1]):
                return "play"
            elif self.images["ctrl_menu"].collide(landmarks[0]) or self.images["ctrl_menu"].collide(landmarks[1]):
                return "ctrl"
            elif self.images["score"].collide(landmarks[0]) or self.images["score"].collide(landmarks[1]):
                self.scoreboard.show(self.__window)
                return

    def __render_control_menu(self, landmarks):
        self.images["background"].display()

        self.images["ctrl"].display()
        self.images["back"].display()
        self.images["right"].display()
        self.images["left"].display()

        self.gifs["ctrl_right"].draw()
        self.gifs["ctrl_left"].draw()
        self.gifs["jump_duck"].draw()
        
        if landmarks[0] != (-1, -1) or landmarks[1] != (-1, -1):
            self.__render_cursor(landmarks)
            if self.images["back"].collide(landmarks[0]) or self.images["back"].collide(landmarks[1]):
                return "back"
    def __render_cursor(self, landmarks):
        if len(landmarks) != 2:
            return
        if landmarks[0] != (-1, -1):
                self.__window.blit(self.images["star"].image, 
                                   (landmarks[0][0] - self.images["star"].get_width()/2, 
                                   landmarks[0][1] - self.images["star"].get_height()/2))
        elif landmarks[1] != (-1, -1):
                self.__window.blit(self.images["star"].image, 
                                   (landmarks[1][0] - self.images["star"].get_width()/2, 
                                   landmarks[1][1] - self.images["star"].get_height()/2))
    def __render_gameOver(self):
        self.images["game_over_background"].display()
        self.images["well_done"].display()
    def __render_saveScore(self, score, landmarks):
        Text = self.fonts["big"].render("Your Score: " + str(score), 1, black)
        
        background = pygame.Surface(self.__window_size)
        background.fill(white)
        background.set_alpha(100)

        self.__window.blit(background, (0,0))
        self.images["lakitu"].display()

        self.__window.blit(Text, [self.__window_size[0]/2 - Text.get_width()/2, 
                                  self.__window_size[1]/4 - Text.get_height()/2])
        self.__window.blit(self.text["save?"], [self.__window_size[0]/2 - self.text["save?"].get_width()/2, 
                                                self.__window_size[1]/2 - self.text["save?"].get_height()/2])
        yes_rect = self.__window.blit(self.text["yes"], [self.__window_size[0]/4 - self.text["yes"].get_width()/2, 
                                                         3*self.__window_size[1]/4 - self.text["yes"].get_height()/2])
        no_rect = self.__window.blit(self.text["no"], [3*self.__window_size[0]/4 - self.text["no"].get_width()/2, 
                                                        3*self.__window_size[1]/4 - self.text["no"].get_height()/2])

        if len(landmarks) == 2:
            if(yes_rect.collidepoint(landmarks)):
                return 1
            elif(no_rect.collidepoint(landmarks)):
                return 0
