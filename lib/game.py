from html import entities
import pygame
import sys
import time

from lib.render import render
from lib.logic import logic
from lib.controller import controller
from lib.physics import physics
from lib.entity import entity
from lib.scoreboard import scoreboard
from lib.map_gen import map_gen
from lib.camera import camera

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
        self.__scoreboard = scoreboard()
        self.__map_gen = map_gen()

        self.__state = -13

    def start(self):
        self.__entities.append(entity("Player"))

        self.__loop()

    def __loop(self):
        while(self.__loop_cond):
            # Detecta Inputs do teclado
            fake_command = self.__keyboard_event()

            # Recebe imagem da camera
            image = self.__camera.take_image()

            # Recebe commandos
            command, debug, landmarks = self.__controller.get_commands(state=self.__state, img=image)

            # Aplica fisica
            self.__physics.update(state=self.__state, entities=self.__entities, commands=fake_command)

            # Aplica logica
            self.__state = self.__logic.update(state=self.__state)

            # Desenha cena
            self.__render.draw(state=self.__state, img=image,
                               entities=self.__entities, landmarks=landmarks,debug=debug)
            
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
        return game.__fake_inputs()
        

    def __fake_inputs():
        pressed_keys = pygame.key.get_pressed()
        command = 0b0000
        if pressed_keys[pygame.K_d]:
            command = command | 0b1000
            print("Fake Input (D)")
        if pressed_keys[pygame.K_a]:
            command = command | 0b0100
            print("Fake Input (A)")
        if pressed_keys[pygame.K_w]:
            command = command | 0b0010
            print("Fake Input (W)")
        if pressed_keys[pygame.K_s]:
            command = command | 0b0001
            print("Fake Input (S)")

        return command