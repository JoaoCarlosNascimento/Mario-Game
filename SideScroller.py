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
Dirt_block = pygame.image.load("Sprite/Ground/GrassWall.png").convert_alpha()
rectDirt = Dirt_block.get_rect()
Dirt_blockX = 0
Dirt_blockX2 = Dirt_block.get_width()

# Bloco terra
Dirt_block2 = pygame.image.load("Sprite/Ground/IceWall.png").convert_alpha()
rectDirt2 = Dirt_block2.get_rect()
Dirt_block2X = 0
Dirt_block2X2 = Dirt_block2.get_width()

# Bloco terra
Dirt_block3 = pygame.image.load("Sprite/Ground/BlueGround.png").convert_alpha()
rectDirt3 = Dirt_block3.get_rect()
Dirt_block3X = 0
Dirt_blockX32 = Dirt_block3.get_width()

# coin1
coin1 = pygame.image.load("Sprite/Bonus/Coin.png").convert_alpha()
rectcoin1 = coin1.get_rect()
coin1_blockX = 0
coin1_blockX2 = coin1.get_width()

# coin2
coin2 = pygame.image.load("Sprite/Bonus/RedCoin.png").convert_alpha()
rectcoin2 = coin2.get_rect()
coin2_blockX = 0
coin2_blockX2 = coin2.get_width()


class player(object):
    def __init__(self, x, y, width, height, LookingRight):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.jumping = False
        self.ducking = False
        self.falling = False
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
        jump_string = ["Sprite/Mario/JumpVictorius.png", "Sprite/Mario/JumpVictorius.png",
                       "Sprite/Mario/JumpVictorius.png", "Sprite/Mario/JumpVictorius.png",
                       "Sprite/Mario/JumpingArmsUp.png", "Sprite/Mario/JumpingArmsUp.png",
                       "Sprite/Mario/JumpingArmsUp.png", "Sprite/Mario/JumpingArmsUp.png"]
        duck_string = ["Sprite/Mario/Duck.png", "Sprite/Mario/Duck.png", "Sprite/Mario/Duck.png",
                       "Sprite/Mario/Duck.png", "Sprite/Mario/Duck.png", "Sprite/Mario/Duck.png",
                       "Sprite/Mario/Duck.png", "Sprite/Mario/Duck.png", "Sprite/Mario/Duck.png",
                       "Sprite/Mario/Duck.png", "Sprite/Mario/Duck.png"]
        fall_string = ["Sprite/Mario/Scared.png"]
        scale = [12, 12]
        x_offset = 0

        self.run = self.create_anim(run_string, scale, 2, self.LookingRight)
        self.jump = self.create_anim(jump_string, scale, 8, self.LookingRight)
        self.duck = self.create_anim(duck_string, scale, 11, self.LookingRight)
        self.fall = self.create_anim(fall_string, scale, 1, self.LookingRight)

        if self.LookingRight:
            x_offset = 50
        else:
            x_offset = 30

        count = random.randint(0, 1)
        if self.jumping:
            self.y -= self.jumpList[self.jumpCount] * 1.2
            window.blit(self.jump[self.jumpCount // 18], (self.x, self.y))

            # Hitbox do Mario a Saltar
            self.hitbox = (self.x + x_offset, self.y + 30, self.width - 24, self.height + 20)
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
            elif self.duckCount > 20 and self.duckCount < 80:
                # Hitbox do Mario a Fazer Duck
                self.hitbox = (self.x + x_offset, self.y + 60, self.width - 8, self.height - 35)
            if self.duckCount >= 100:
                self.duckCount = 0
                self.duckUp = False
                self.runCount = 0
            window.blit(self.duck[self.duckCount // 10], (self.x, self.y + Screen_Height / 25))
            # Hitbox do Mario a Fazer Duck
            self.hitbox = (self.x + x_offset, self.y + 60, self.width - 24, self.height - 30)
            self.duckCount += 1

        elif self.falling:
            window.blit(self.fall[0], (self.x, self.y))
        else:
            if self.runCount > 42:
                self.runCount = 0

            if random.randint(0, 20) % 5 == 0:
                self.runCount = 0
            else:
                self.runCount = 1
            window.blit(self.run[self.runCount], (self.x, self.y))
            # Hitbox do Mario a Correr
            self.hitbox = (self.x + x_offset, self.y + 30, self.width - 24, self.height + 20)
        # Desenhar Hitbox Do Mario
        if not self.falling:
            pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)


# Classe Obstaculo
class Enemie(object):
    img = pygame.image.load("Sprite/Enemies/FatTurtle.png")

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (x, y, width, height)
        self.count = 0

    def draw(self, window):
        self.hitbox = (self.x + 5, self.y + 5, self.width - 10, self.height)
        window.blit(self.img, (self.x, self.y))
        # Desenho da Hitbox
        pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)

    def collide(self, rect):
        # 0 - x
        # 1 - y
        # 2 - width
        # 3 - height
        # Verifica Colisão em Coordenada x
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            # Verifica Colisão em Coordenada y
            if rect[1] + rect[3] > self.hitbox[1]:
                return True
        return False


class Obstacle(Enemie):
    img = pygame.image.load("Sprite/Obstacle/FirePipe.png")

    def draw(self, window):
        self.hitbox = (self.x + 10, self.y, self.width, self.height)
        window.blit(self.img, (self.x, self.y))
        pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)


# to random sprites
def random_sprites():
    # generate random number to make sprites appear
    n = random.randint(0, 3)

    return n


def redrawWindow(Movement_x, Loser_Text, LoserRect):
    # ran = random_sprites()
    # j = 0
    # n = random.randint(1, 3)
    # m = n
    window.blit(BackGround, (BackGroundX, 0))  # draws our first BackGround image
    window.blit(BackGround, (BackGroundX2, 0))  # draws the second BackGround image
    for x in objects:
        x.draw(window)
    """
    while (j < 3):
        window.blit(Dirt_block, (BackGroundX + Screen_Width + m * 100, Screen_Height / 2 + 301))
        window.blit(Dirt_block, (BackGroundX2 + Screen_Width + m * 100, Screen_Height / 2 + 301))
        window.blit(Dirt_block, (BackGroundX + Screen_Width + m * 100, Screen_Height / 2 + 301))
        window.blit(Dirt_block, (BackGroundX2 + Screen_Width + m * 100, Screen_Height / 2 + 301))
        j += 1
    """
    runner.draw(window, 95)  # NEW

    if Movement_x <= -70:
        window.blit(Loser_Text, LoserRect)

    pygame.display.update()  # updates the screen


# Acelerar Segundo Eventos do Jogo
pygame.time.set_timer(USEREVENT + 1, 500)

# Evento que Gera Objectos entre 3-5 segundos
pygame.time.set_timer(USEREVENT + 2, random.randrange(3000, 5000))

# Declaração dos Objectos
runner = player(200, Screen_Height / 1.3, 100, 95, True)

objects = []

speed = 30
run = True
startime = time.time()
while run:
    # n = random.randint(1, 3)
    # totaltime = round((time.time() - startime), 2)

    redrawWindow(runner.x, Loser_Text, LoserRect)

    # Move Obstacle/Enemie
    for objectts in objects:
        if objectts.collide(runner.hitbox):
            runner.falling = True
            anim_start_timer = time.time()
        objectts.x -= 1.4

    if runner.falling:
        anim_end_timer = time.time()
        #Duração da Animação Hitted
        if anim_end_timer - anim_start_timer > 0.5:
            runner.falling = False

        # Quando Não Aparece no Ecrã
        if objectts.x < -objectts.width * -1:
            objects.pop(objects.index(objectts))

    BackGroundX -= 1  # Move both background images back
    BackGroundX2 -= 1
    """
    rectDirt.x -= 1
    rectDirt2.x -= 1
    rectDirt3.x -= 1

    rectcoin1.x -= 1
    rectcoin2.x -= 1
    """
    # Movimentação Default
    runner.x -= Screen_Width / 4000

    # 1º BackGround Image starts at (0,0)
    if BackGroundX < BackGround.get_width() * -1:  # If our BackGround is at the -width then reset its position
        BackGroundX = BackGround.get_width()

    if BackGroundX2 < BackGround.get_width() * -1:
        BackGroundX2 = BackGround.get_width()
    """
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
    """
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

        if event.type == USEREVENT + 2:
            # Escolhe Obstacle/Enemie que Aparece
            pick_object = random.randrange(0, 2)
            if pick_object == 0:
                objects.append(Enemie(Screen_Width, Screen_Height / 1.27, 100, 130))
            else:
                objects.append(Obstacle(Screen_Width, Screen_Height / 1.27, 70, 130))

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
