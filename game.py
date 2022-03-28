import pygame
import sys
# import time
# import random


# from pygame.locals import *

from lib.render import render
from lib.logic import logic
from lib.controller import controller
from lib.physics import physics
from lib.entity import player
from lib.scoreboard import scoreboard
from lib.map_gen import map_gen
from lib.camera import camera
import lib.load_files as file
import os
## States
#
# Utilizar valores negativos para os cenarios de testes
#
# -9/-8 - Teste de foto
# -1xx  - Testes de inputs
# -11   - Teste de inputs de mãos
# -12   - Teste de inputs de face
# -13   - Teste de inputs de corpo

# -135  - Teste De Geração do Mapa
class game:
    __loop_cond = True

    def __init__(self):
        
        self.__fps = 60
        self.__camera = camera()
        image = self.__camera.take_image()
        # os.environ['SDL_WINDOWID'] = str(self.winfo_id())
        
        self.__window_size = (1920, 1080)

        pygame.init()
        self.__clock = pygame.time.Clock()
        self.__render = render(window_size=self.__window_size)
        self.__controller = controller()
        self.__logic = logic()
        self.__physics = physics()
        self.__entities = []
        self.__scoreboard = scoreboard(self.__window_size)
        self.__map_gen = map_gen()

        self.__bonus_value = 0
        self.__coins = 0
        self.__score = 0
        self.__lives = 5
        self.__state = "menu"

        self.__final_score = -999
    def start(self):

        self.__loop()
    
    def __loop(self):
        feedback2 = ""
        Sampling = 2
        while(self.__loop_cond):
            # Detecta Inputs do teclado
            fake_command = self.__keyboard_event()
            # self.__event()
            self.__score = self.__fps // 5 - 6 + self.__bonus_value
            if self.__state == "game":
                self.__bonus_value = 0
                self.__coins = 0
                self.__score = 0
                self.__lives = 5
            
            if self.__state == "game loop":
                # Recebe imagem da camera
                image = self.__camera.take_image(Sampling=Sampling)
                # Recebe commandos
                command, debug, landmarks = self.__controller.get_commands(state=self.__state, img=image,Sampling=Sampling)
            else:
                # Recebe imagem da camera
                image = self.__camera.take_image(Sampling=1)
                # Recebe commandos
                command, debug, landmarks = self.__controller.get_commands(state=self.__state, img=image,Sampling=1)

            # print(debug)
            # Aplica fisica
            self.__bonus_value, self.__lives, feedback1, debug2, self.__coins = self.__physics.update(state=self.__state,
                                                                                entities=self.__entities, 
                                                                                commands=command, 
                                                                                bonus_val = self.__bonus_value,
                                                                                coins = self.__coins)
            # Desenha cena
            feedback2 = self.__render.draw(state=self.__state, img=image,
                                           entities=self.__entities, landmarks=landmarks,debug=debug,
                                           bonus_val = self.__bonus_value,
                                           lives=self.__lives, score= self.__score, coins = self.__coins, final_score = self.__final_score)
            
            # Aplica logica
            self.__state, self.__fps = self.__logic.update(
                state=self.__state, feedback=[feedback1, feedback2], entities=self.__entities, speed = self.__fps)

            if self.__state == "game over":
                self.__final_score = self.__score
            
            # Controle de Ticks
            self.__clock.tick(self.__fps)
    def __gameOver(self):
        self.__scoreboard.update()
        self.__scoreboard.show()

    def __close(self):
        self.__loop_cond = False

    def __keyboard_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__quit_game()
                # self.__close()
                # pygame.quit()
                # sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.__quit_game()
                    # print("ESC")
                    # self.__close()
                    # pygame.quit()
                    # sys.exit()

            # if event.type == event_ACCELERATE:
            #     self.__fps += 1
        return self.__fake_inputs()
        
    # def __event(self):
    #     for event in pygame.event.get():
            
    def __quit_game(self):
        self.__close()
        pygame.quit()
        sys.exit()

    def __fake_inputs(self):
        pressed_keys = pygame.key.get_pressed()
        command = 0b0000
        if pressed_keys[pygame.K_d]:
            command = command | 0b1000
            # print("Fake Input (D)")
        if pressed_keys[pygame.K_a]:
            command = command | 0b0100
            # print("Fake Input (A)")
        if pressed_keys[pygame.K_w]:
            command = command | 0b0001
            # print("Fake Input (W)")
        if pressed_keys[pygame.K_s]:
            command = command | 0b0010
            # print("Fake Input (S)")
        if pressed_keys[pygame.K_ESCAPE]:
            self.__quit_game()


        return command

if __name__ == '__main__':
    myGame = game()
    myGame.start()
