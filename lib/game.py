import pygame
import sys
import time
import random


from pygame.locals import *

from lib.render import render
from lib.logic import logic
from lib.controller import controller
from lib.physics import physics
from lib.entity import player, Bonus, Obstacle, Enemy
from lib.scoreboard import scoreboard
from lib.map_gen import map_gen
from lib.camera import camera
import lib.load_files as file
from lib.load_files import Screen_Width, Screen_Height, USEREVENT

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
event_ACCELERATE = USEREVENT + 1
event_LAND_ENEMY = USEREVENT + 2
event_AIR_ENEMY = USEREVENT + 3

class game:
    __loop_cond = True

    def __init__(self):
        pygame.init()
        self.__fps = 60
        self.__clock = pygame.time.Clock()

        self.__camera = camera()
        image = self.__camera.take_image()
        self.__render = render(window_size=(image.shape[1], image.shape[0]))
        self.__controller = controller()
        self.__logic = logic()
        self.__physics = physics()
        self.__entities = []
        self.__scoreboard = scoreboard((1920,1080))
        self.__map_gen = map_gen()

        self.__bonus_value = 0
        self.__score = 0
        self.__lives = 3
        self.__mario = player((Screen_Width / 10, Screen_Height / 1.3), (100, 95), True)
        self.__state = "save score?"

    def start(self):
        self.__entities.append(self.__mario)


        self.__loop()
    
    def __loop(self):
        feedback2 = ""
        while(self.__loop_cond):
            # Detecta Inputs do teclado
            fake_command = self.__keyboard_event()
            # self.__event()
            self.__score = self.__fps // 5 - 6 + self.__bonus_value
            # Recebe imagem da camera
            image = self.__camera.take_image()

            # Recebe commandos
            command, debug, landmarks = self.__controller.get_commands(state=self.__state, img=image)

            # Aplica fisica
            self.__bonus_value, self.__lives, feedback1 = self.__physics.update(state=self.__state, 
                                                                                entities=self.__entities, 
                                                                                commands=fake_command, 
                                                                                bonus_val = self.__bonus_value)

            # Aplica logica
            self.__state = self.__logic.update(state=self.__state, feedback=[feedback1, feedback2])

            # Desenha cena
            feedback2 = self.__render.draw(state=self.__state, img=image,
                                           entities=self.__entities, landmarks=landmarks,debug=debug,
                                           bonus_val = self.__bonus_value,
                                           lives=self.__lives, score= self.__score)

            
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
                self.__close()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.__close()
                    pygame.quit()
                    sys.exit()

            if event.type == event_ACCELERATE:
                self.__fps += 1
            
            if event.type == event_LAND_ENEMY:
                # Escolhe Obstacle/Bónus Terrestres que Aparecem
                pick_object = random.randrange(0, 2)
                if pick_object == 0:
                    random_pick = random.randrange(18, 25)
                    self.__entities.append(Bonus((Screen_Width, Screen_Height / 1.27)(100, 130), random_pick))

                if pick_object == 1:
                    random_pick = random.randrange(0, 9)
                    self.__entities.append(Enemy((Screen_Width, Screen_Height / 1.27), (100, 130), random_pick))

                if pick_object == 2:
                    random_pick = random.randrange(0, 2)
                    self.__entities.append(Obstacle((Screen_Width, Screen_Height / 1.27), (70, 130), random_pick))
                
            if event.type == event_AIR_ENEMY:
                pick_object = random.randrange(0, 1)
                if pick_object == 0:
                    random_pick = random.randrange(10, 13)
                    self.__entities.append(Enemy((Screen_Width, Screen_Height / 1.27), (100, 130), random_pick))
                else:
                    random_pick = random.randrange(0, 17)
                    self.__entities.append(Bonus((Screen_Width, Screen_Height / 1.27) (100, 130), random_pick))
        return game.__fake_inputs()
        
    # def __event(self):
    #     for event in pygame.event.get():
            

    def __fake_inputs():
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

        return command

if __name__ == '__main__':
    myGame = game()
    myGame.start()
