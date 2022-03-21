import pygame
from pygame.locals import *
import sys
import random
import math
import pyautogui
import time
import datetime

Screen_Width, Screen_Height = pyautogui.size()
pygame.init()

font = pygame.font.Font('font.TTF', 64)

Loser_Text = font.render('Loser', True, (255, 255, 255), (0, 0, 0))
LoserRect = Loser_Text.get_rect()
LoserRect.center = (Screen_Width // 2, Screen_Height // 2)

clock = pygame.time.Clock()

window = pygame.display.set_mode((Screen_Width, Screen_Height))
pygame.display.set_caption("Test")

# Mover BackGround
BackGround = pygame.image.load("Sprite/BackGround/BackGround.jpg").convert()
BackGround = pygame.transform.scale(BackGround, (Screen_Width, Screen_Height))
BackGroundX = 0
BackGroundX2 = BackGround.get_width()

# Bloco terra
Dirt_block = pygame.image.load("Sprite/Ground/GrassWall.PNG").convert_alpha()
Dirt_blockX = 0
Dirt_blockX2 = Dirt_block.get_width()


# rectDirt_block = Dirt_block.get_rect()
# rectDirt_block.x, rectDirt_block.y = 0, 0

class player(object):
    def __init__(self, x, y, width, height, LookingRight):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.jumping = False
        self.ducking = False
        self.duckCount = 0
        self.jumpCount = 0
        self.runCount = 0
        self.duckUp = False
        self.LookingRight = LookingRight

    def create_anim(self, image, scale, number_images, LookingRight):
        animation = []
        for i in range(number_images):
            animation.append(pygame.image.load(image[i]))
            if LookingRight:
                animation[i] = pygame.transform.flip(animation[i], True, False)
            animation[i] = pygame.transform.scale(animation[i], (Screen_Width / scale[0], Screen_Width / scale[1]))

        return animation

    jumpList = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4,
                4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1,
                -1, -1, -1, -1, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3,
                -3, -3, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4]

    def draw(self, window, y):

        run_string = ["Sprite/Mario/WalkingArmsUp.png", "Sprite/Mario/StandingArmsUp.png"]
        jump_string = ["Sprite/Mario/JumpVictorius.png", "Sprite/Mario/JumpVictorius.png", "Sprite/Mario/JumpVictorius.png", "Sprite/Mario/JumpVictorius.png","Sprite/Mario/JumpingArmsUp.png", "Sprite/Mario/JumpingArmsUp.png", "Sprite/Mario/JumpingArmsUp.png", "Sprite/Mario/JumpingArmsUp.png"]
        duck_string = ["Sprite/Mario/Duck.png", "Sprite/Mario/Duck.png", "Sprite/Mario/Duck.png", "Sprite/Mario/Duck.png", "Sprite/Mario/Duck.png", "Sprite/Mario/Duck.png", "Sprite/Mario/Duck.png", "Sprite/Mario/Duck.png", "Sprite/Mario/Duck.png", "Sprite/Mario/Duck.png", "Sprite/Mario/Duck.png"]
        scale = [12, 12]

        self.run = self.create_anim(run_string, scale, 2, self.LookingRight)
        self.jump = self.create_anim(jump_string, scale, 8, self.LookingRight)
        self.duck = self.create_anim(duck_string, scale, 11, self.LookingRight)

        count = random.randint(0, 1)
        if self.jumping:
            self.y -= self.jumpList[self.jumpCount] * 1.2
            window.blit(self.jump[self.jumpCount // 18], (self.x, self.y))
            self.jumpCount += 1
            if self.jumpCount > 108:
                self.jumpCount = 0
                self.jumping = False
                self.runCount = 0
        elif self.ducking or self.duckUp:
            if self.duckCount < 20:
                self.y += 1
            elif self.duckCount == 70:
                self.y -= 19
                self.ducking = False
                self.duckUp = True
            if self.duckCount >= 100:
                self.duckCount = 0
                self.duckUp = False
                self.runCount = 0
            window.blit(self.duck[self.duckCount // 10], (self.x, self.y + Screen_Height / 25))
            self.duckCount += 1

        else:
            if self.runCount > 42:
                self.runCount = 0

            if random.randint(0, 20) % 5 == 0:
                self.runCount = 0
            else:
                self.runCount = 1
            window.blit(self.run[self.runCount], (self.x, self.y))


# to random sprites
def random_sprites():
    # generate random number to make sprites appear
    n = random.randint(0, 3)

    return n


def redrawWindow(Movement_x, Loser_Text, LoserRect, n):
    # ran = random_sprites()
    j = 0
    n = random.randint(1, 3)
    m = n
    window.blit(BackGround, (BackGroundX, 0))  # draws our first BackGround image
    window.blit(BackGround, (BackGroundX2, 0))  # draws the second BackGround image

    while (j < 3):
        window.blit(Dirt_block, (BackGroundX + Screen_Width + m * 100, Screen_Height / 2 + 301))
        window.blit(Dirt_block, (BackGroundX2 + Screen_Width + m * 100, Screen_Height / 2 + 301))
        window.blit(Dirt_block, (BackGroundX + Screen_Width + m * 100, Screen_Height / 2 + 301))
        window.blit(Dirt_block, (BackGroundX2 + Screen_Width + m * 100, Screen_Height / 2 + 301))
        j += 1

    runner.draw(window,95)  # NEW

    if Movement_x <= -70:
        window.blit(Loser_Text, LoserRect)
    pygame.display.update()  # updates the screen


# Acelerar Segundo Eventos do Jogo
pygame.time.set_timer(USEREVENT + 1, 500)
runner = player(200, Screen_Height / 1.3, 100, 95, True)
speed = 30
run = True
while run:
    n = random.randint(1, 3)
    totaltime = round((time.time() - startime), 2)

    redrawWindow(runner.x, Loser_Text, LoserRect)

    BackGroundX -= 1  # Move both background images back
    BackGroundX2 -= 1

    rectDirt.x -= 1
    rectDirt2.x -= 1
    rectDirt3.x -= 1

    rectcoin1.x -= 1
    rectcoin2.x -= 1

    # Movimentação Default
    runner.x -= Screen_Width / 4000

    # 1º BackGround Image starts at (0,0)
    if BackGroundX < BackGround.get_width() * -1:  # If our BackGround is at the -width then reset its position
        BackGroundX = BackGround.get_width()

    if BackGroundX2 < BackGround.get_width() * -1:
        BackGroundX2 = BackGround.get_width()

    if rectDirt.x < Dirt_block.get_width() * -1:
        rectDirt.x = random.randrange(Screen_Width/2 + 50, Screen_Width)
    if rectDirt2.x < Dirt_block2.get_width() * -1:
        rectDirt2.x = random.randrange(Screen_Width/2 + 100, Screen_Width)
    if rectDirt3.x < Dirt_block3.get_width() * -1:
        rectDirt3.x = random.randrange(Screen_Width/2 + 150, Screen_Width)

    if rectcoin1.x < coin1.get_width() * -1:
        rectcoin1.x = random.randrange(Screen_Width/2 + 150, Screen_Width)
    if rectcoin2.x < coin2.get_width() * -1:
        rectcoin2.x = random.randrange(Screen_Width/2 + 150, Screen_Width)

    for event in pygame.event.get():  # Loop through a list of events
        if event.type == pygame.QUIT:  # See if the user clicks the red x
            run = False  # End the loop
            pygame.quit()  # Quit the game

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                start = False
                pygame.quit()
                sys.exit()

        if event.type == USEREVENT + 1:
            speed += 1

        # Quando várias keys pressionadas, seleciona a 1º
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            if not (runner.jumping):
                runner.jumping = True

        # Mover Para a Direita
        if keys[pygame.K_RIGHT]:
            runner.x += Screen_Width / 60
            runner.LookingRight = True
        # Mover Para a Esquerda
        if keys[pygame.K_LEFT]:
            runner.x -= Screen_Width / 60
            runner.LookingRight = False
        # print(runner.x)

        if keys[pygame.K_DOWN]:
            if not (runner.ducking):
                runner.ducking = True

        clock.tick(speed)
