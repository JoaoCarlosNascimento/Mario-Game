import pygame
import pyautogui

Screen_Width, Screen_Height = pyautogui.size()
window = pygame.display.set_mode((Screen_Width, Screen_Height))

class map_gen:
    def __init__(self):
        self.jumping = False
        self.jumpCount = 0
        self.runCount = 0
        BackGround = pygame.image.load("Sprite/BackGround/BackGround.jpg")

    def draw(self, win):
        if self.jumping:
            pass
            # self.y -=


        pass