import pygame
from pygame.locals import *
import sys
import random
import time
import load_files as file
from lib.render import render
from lib.physics import physics
from lib.entity import Enemie, Bonus, Obstacle, player


"""
def check_pygame_events(velocity, bonuss, objectss, event):
    #for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

    if event.type == USEREVENT + 1:
        velocity += 1

    if event.type == USEREVENT + 2:
        # Escolhe Obstacle/Bónus Terrestres que Aparecem
        pick_object = random.randrange(0, 2)
        if pick_object == 0:
            random_pick = random.randrange(18, 25)
            bonuss.append(Bonus(file.Screen_Width, file.Screen_Height / 1.27, 100, 130, random_pick))

        if pick_object == 1:
            random_pick = random.randrange(0, 9)
            objectss.append(Enemie(file.Screen_Width, file.Screen_Height / 1.27, 100, 130, random_pick))

        if pick_object == 2:
            random_pick = random.randrange(0, 2)
            objectss.append(Obstacle(file.Screen_Width, file.Screen_Height / 1.27, 70, 130, random_pick))

    if event.type == USEREVENT + 3:
        # Escolhe Enemies/Bonus Aéreos que Aparecem
        pick_object = random.randrange(0, 1)
        if pick_object == 0:
            random_pick = random.randrange(10, 13)
            objectss.append(Enemie(file.Screen_Width, file.Screen_Height / 1.27, 100, 130, random_pick))
        else:
            random_pick = random.randrange(0, 17)
            bonuss.append(Bonus(file.Screen_Width, file.Screen_Height / 1.27, 100, 130, random_pick))

    if bonuss is not None:
        return bonuss

    if objectss is not None:
        return objectss
"""

# Variáveis Utilizadas No Game
objects = []
bonus = []
speed = 30
run = True
lives = 3
bonus_value = 0
anim_start_timer = 0

# Declaração dos Objectos
entity_render = render(file.window_size)
entity_physics = physics()
runner = player(file.Screen_Width / 10, file.Screen_Height / 1.3, 100, 95, True)

while run:
    score = speed // 5 - 6 + bonus_value

    entity_render.redrawWindow(runner.x, objects, bonus, runner, score, lives)
    anim_start_timer, bonus_value, lives = entity_physics.verify_collision(bonus_value, objects, runner, lives, bonus, anim_start_timer)

    entity_physics.detectCollision(runner, anim_start_timer)
    entity_render.check_BackGround()

    for event in pygame.event.get(): 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        if event.type == USEREVENT + 1:
            speed += 1

        if event.type == USEREVENT + 2:
            # Escolhe Obstacle/Bónus Terrestres que Aparecem
            pick_object = random.randrange(0, 2)
            if pick_object == 0:
                random_pick = random.randrange(18, 25)
                bonus.append(Bonus(file.Screen_Width, file.Screen_Height / 1.27, 100, 130, random_pick))

            if pick_object == 1:
                random_pick = random.randrange(0, 9)
                objects.append(Enemie(file.Screen_Width, file.Screen_Height / 1.27, 100, 130, random_pick))

            if pick_object == 2:
                random_pick = random.randrange(0, 2)
                objects.append(Obstacle(file.Screen_Width, file.Screen_Height / 1.27, 70, 130, 2))

        if event.type == USEREVENT + 3:
            # Escolhe Enemies/Bonus Aéreos que Aparecem
            pick_object = random.randrange(0, 1)
            if pick_object == 0:
                random_pick = random.randrange(10, 13)
                objects.append(Enemie(file.Screen_Width, file.Screen_Height / 1.27, 100, 130, random_pick))
            else:
                random_pick = random.randrange(0, 17)
                bonus.append(Bonus(file.Screen_Width, file.Screen_Height / 1.27, 100, 130, random_pick))

        # Controlos KeyBoard
        entity_physics.keyboards_input(runner)

        file.clock.tick(speed)
