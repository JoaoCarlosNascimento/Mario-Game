import pygame
from pygame.locals import *
import sys
import random
import time
import load_files as file


Loser_Text = file.font.render('Loser', True, (255, 255, 255), (0, 0, 0))
LoserRect = Loser_Text.get_rect()
LoserRect.center = (file.Screen_Width // 2, file.Screen_Height // 2)

clock = pygame.time.Clock()

window = pygame.display.set_mode((file.Screen_Width, file.Screen_Height))
pygame.display.set_caption("Test")

# Mover BackGround
BackGroundX = 0
BackGroundX2 = file.BackGround.get_width()


def create_anim(image, scale, number_images):
    animation = []
    for i in range(number_images):
        animation.append(pygame.image.load(image[i]))
        animation[i] = pygame.transform.scale(animation[i], (file.Screen_Width / scale[0], file.Screen_Width / scale[1]))
        animation[i] = pygame.transform.flip(animation[i], True, False)

    return animation


def flip_anim(image, number_images):
    animation = []
    for i in range(number_images):
        animation.append(image[i])
        animation[i] = pygame.transform.flip(animation[i], True, False)
    return animation


run_anim = create_anim(file.run_string, file.scale, 2)
jump = create_anim(file.jump_string, file.scale, 8)
duck = create_anim(file.duck_string, file.scale, 11)
fall = create_anim(file.fall_string, file.scale, 1)

flip_run_anim = flip_anim(run_anim, 2)
flip_jump = flip_anim(jump, 8)
flip_duck = flip_anim(duck, 11)
flip_fall = flip_anim(fall, 1)


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

    def draw(self, window, y):

        if self.LookingRight:
            self.run = run_anim
            self.jump = jump
            self.duck = duck
            self.fall = fall
            x_offset = 50
        else:
            x_offset = 30
            self.run = flip_run_anim
            self.jump = flip_jump
            self.duck = flip_duck
            self.fall = flip_fall

        count = random.randint(0, 1)
        if self.jumping:
            if self.falling:
                self.hitbox = (0, 0, 0, 0)
                self.y -= file.jumpList[self.jumpCount] * 1.2
                window.blit(self.fall[0], (self.x, self.y))
            else:
                # Hitbox do Mario a Saltar
                self.hitbox = (self.x + x_offset, self.y + 30, self.width - 24, self.height + 20)
                self.y -= file.jumpList[self.jumpCount] * 1.2
                window.blit(self.jump[self.jumpCount // 18], (self.x, self.y))

            self.jumpCount += 1
            if self.jumpCount > 108:
                self.jumpCount = 0
                self.jumping = False
                self.runCount = 0

        elif self.ducking or self.duckUp:
            if self.falling:
                self.hitbox = (0, 0, 0, 0)
                window.blit(self.fall[0], (self.x, self.y))
            else:
                # Hitbox do Mario a Fazer Duck
                self.hitbox = (self.x + x_offset, self.y + 60, self.width - 24, self.height - 30)

            if self.duckCount < 20:
                self.y += 1
            elif self.duckCount == 70:
                self.y -= 19
                self.ducking = False
                self.duckUp = True
            elif 20 < self.duckCount < 80:
                if self.falling:
                    self.hitbox = (0, 0, 0, 0)
                else:
                    # Hitbox do Mario a Fazer Duck
                    self.hitbox = (self.x + x_offset, self.y + 60, self.width - 8, self.height - 35)
            if self.duckCount >= 100:
                self.duckCount = 0
                self.duckUp = False
                self.runCount = 0
            if not self.falling:
                window.blit(self.duck[self.duckCount // 10], (self.x, self.y + file.Screen_Height / 25))
            else:
                window.blit(self.fall[0], (self.x, self.y))

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
            if self.falling:
                self.hitbox = (0, 0, 0, 0)
            else:
                # Hitbox do Mario a Correr
                self.hitbox = (self.x + x_offset, self.y + 30, self.width - 24, self.height + 20)
        # Desenhar Hitbox Do Mario
        if not self.falling:
            pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)


# Classe Obstaculo
class Enemie(object):
    def __init__(self, x, y, width, height, random_pick):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (x, y, width, height)
        self.count = 0
        self.random_pick = random_pick

    def draw(self, window):
        img = file.pick_enemie(self.random_pick)
        self.hitbox = (self.x + 5, self.y + 5, self.width - 10, self.height)
        window.blit(img, (self.x, self.y))
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
    def draw(self, window):
        img = file.pick_obstacle(self.random_pick)
        self.hitbox = (self.x + 10, self.y, self.width, self.height)
        window.blit(img, (self.x, self.y))
        pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)


def redrawWindow(Movement_x, Loser_Text, LoserRect):
    Score = file.font.render("Score: " + str(score), 1, (0, 0, 0))
    if lives == 3:
        Heart_img = file.Hearts_3
    elif lives == 2:
        Heart_img = file.Hearts_2
    elif lives == 1:
        Heart_img = file.Hearts_1

    window.blit(file.BackGround, (BackGroundX, 0))  # draws our first BackGround image
    window.blit(file.BackGround, (BackGroundX2, 0))  # draws the second BackGround image

    window.blit(Heart_img, (file.Screen_Width / 40, file.Screen_Height / 30))
    window.blit(Score, (file.Screen_Width/1.3, file.Screen_Height / 20))
    for x in objects:
        x.draw(window)

    runner.draw(window, 95)  # NEW

    if Movement_x <= -70:
        window.blit(Loser_Text, LoserRect)

    pygame.display.update()  # updates the screen


# Acelerar Segundo Eventos do Jogo
pygame.time.set_timer(USEREVENT + 1, 500)

# Evento que Gera Objectos entre 3-5 segundos
pygame.time.set_timer(USEREVENT + 2, random.randrange(3000, 5000))

# Declaração dos Objectos
runner = player(file.Screen_Width / 10, file.Screen_Height / 1.3, 100, 95, True)

objects = []

speed = 30
run = True
lives = 3
flag = False
while run:
    score = speed // 5 - 6
    redrawWindow(runner.x, Loser_Text, LoserRect)

    # Move Obstacle/Enemie
    for objectts in objects:
        if objectts.collide(runner.hitbox):
            runner.falling = True
            anim_start_timer = time.time()
            pygame.mixer.Sound.play(file.Bump)
            lives -= 1
            # Game Over
            if lives <= 0:
                pygame.mixer.Sound.play(file.Mario_Dies)
                # Colocar Aqui Função GameOver
                lives = 3
        objectts.x -= 1.4

    if runner.falling:
        anim_end_timer = time.time()

        #Duração da Animação Hitted
        if anim_end_timer - anim_start_timer > 0.8:
            runner.falling = False
        else:
            runner.hitbox = (0, 0, 0, 0)

        # Quando Não Aparece no Ecrã
        if objectts.x < -objectts.width * -1:
            objects.pop(objects.index(objectts))

    BackGroundX -= 1  # Move both background images back
    BackGroundX2 -= 1

    # Movimentação Default
    runner.x -= file.Screen_Width / 4000

    # 1º BackGround Image starts at (0,0)
    if BackGroundX < file.BackGround.get_width() * -1:  # If our BackGround is at the -width then reset its position
        BackGroundX = file.BackGround.get_width()

    if BackGroundX2 < file.BackGround.get_width() * -1:
        BackGroundX2 = file.BackGround.get_width()

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
                random_pick = random.randrange(0, 13)
                objects.append(Enemie(file.Screen_Width, file.Screen_Height / 1.27, 100, 130, random_pick))
            else:
                random_pick = random.randrange(0, 2)
                objects.append(Obstacle(file.Screen_Width, file.Screen_Height / 1.27, 70, 130, random_pick))

        # Quando várias keys pressionadas, seleciona a 1º
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            if not (runner.jumping) and not (runner.falling):
                runner.jumping = True
                pygame.mixer.Sound.play(file.Jump)

        # Mover Para a Direita
        if keys[pygame.K_RIGHT]:
            runner.x += file.Screen_Width / 60
            runner.LookingRight = True

        # Mover Para a Esquerda
        if keys[pygame.K_LEFT]:
            runner.x -= file.Screen_Width / 60
            runner.LookingRight = False

        if keys[pygame.K_DOWN]:
            if not (runner.ducking) and not(runner.falling):
                runner.ducking = True
                pygame.mixer.Sound.play(file.Duck)

        clock.tick(speed)
