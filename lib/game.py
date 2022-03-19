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
# -131  - Teste de inputs move right
# -132  - Teste de inputs move left
# -133  - Teste de inputs crouch
# -134  - Teste de inputs jump

# -135  - Teste De Geração do Mapa


class game:
    __loop_cond = True

    def __init__(self):
        pygame.init()
        self.__fps = 60
        self.__clock = pygame.time.Clock()

        self.__render = render(window_size=(1280, 720))
        self.__controller = controller()
        self.__logic = logic()
        self.__physics = physics()
        self.__entities = []
        self.__scoreboard = scoreboard()
        self.__camera = camera()

        self.__state = -9

    def start(self):
        self.__entities.append(entity("Player"))

        self.__loop()

    def __loop(self):
        while(self.__loop_cond):
            # Detecta Inputs do teclado
            self.__keyboard_event()

            # Recebe imagem da camera
            image = self.__camera.take_image()

            # Recebe commandos
            command = self.__controller.get_commands(state=self.__state, img=image)

            # Atualização das entidades
            for entity in self.__entities:
                if entity.name == "Player":
                    entity.update(state=self.__state, command=command)
                else:
                    entity.update(state=self.__state)

            # Aplica fisica
            self.__physics.update(state=self.__state, entities=self.__entities)

            # Aplica logica
            self.__state = self.__logic.update(state=self.__state)

            # Desenha cena
            self.__render.draw(state=self.__state, img=image, entities=self.__entities, command=command)
            
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
