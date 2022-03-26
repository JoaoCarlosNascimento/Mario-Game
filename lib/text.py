from ctypes import alignment
from mimetypes import init
from turtle import back
import pygame
black = (0, 0, 0)
white = (255, 255, 255)
purple = (120, 0, 255)
class TextBox:
    # First, create instance with foo = TextBox(window)
    # Then display it with foo.display()
    def __init__(self, surface, contents="Bla", position=[10,10], size=32, bgcolor=white, color=purple):
        self.contents=[]
        if(contents.find("\n")!=-1):
            self.parse(contents)
        else:
            self.contents.append(contents)
        self.position = position
        self.surface = surface
        self.color = color
        self.bgcolor = bgcolor
        self.size = size
        self.font = pygame.font.SysFont("Calibri", size, bold=True)
        self.Text = []
        self.renderText()
        self.updateBackground()
    
    def updateText(self, new_text):
        self.contents = []
        self.Text = []
        if new_text.find("\n")!=-1 :
            self.parse(new_text)
        else:
            self.contents.append(new_text)
        self.renderText()
        self.updateBackground()

    def renderText(self):
        for T in range(len(self.contents)):
            self.Text.append(self.font.render(self.contents[T], 1, self.color))

    def updateBackground(self, bgcolor = white):
        self.Background = pygame.Surface((self.size*len(max(self.contents, key=len)),10+ self.size*len(self.Text)))
        self.Background.set_alpha(200)
        self.bgcolor = bgcolor
        self.Background.fill(self.bgcolor)

    def parse(self, text):
        aux = text.split("\t")
        newText = ""
        for t in aux:
            newText += t+"   "
        aux = newText.split("\n")
        for t in aux:
            self.contents.append(t)

    def display(self):
        self.surface.blit(self.Background, self.position)
        for T in range(len(self.Text)):
            self.surface.blit(self.Text[T], (self.position[0]+5, self.position[1] + self.size*T+5))




def GameOver(surface):
    size = 120
    font = pygame.font.Font("./resources/PolygonParty.ttf", size, bold=False)
    Text = font.render("Game Over", 1, black)
    
    position = [surface.get_width()/2 - Text.get_width()/2, 
                surface.get_height()/4 - Text.get_height()/2]

    mario = pygame.image.load("./resources/mario.png").convert_alpha()

    surface.blit(mario, [surface.get_width()/2 - mario.get_width()/2, surface.get_height()/2])
    surface.blit(Text, position)

def saveScore(surface, score, hand_pos):
    size = 100
    font = pygame.font.Font("./resources/SuperMario256.ttf", size, bold=False)
    Text = font.render("Your Score: " + str(score), 1, black)
    font = pygame.font.Font("./resources/SuperMario256.ttf", int(size/2), bold=False)
    subText = font.render("Would you like to save your picture?", 1, black)
    yes = font.render("Yes", 1, black)
    no = font.render("No", 1, black)
    
    lakitu = pygame.image.load("./resources/lakitu.png").convert_alpha()
    lakitu = pygame.transform.scale(lakitu, (500, 600))

    background = pygame.Surface([surface.get_width(), surface.get_height()])
    background.fill(white)
    background.set_alpha(100)

    surface.blit(background, (0,0))
    surface.blit(lakitu, [surface.get_width()/2 - lakitu.get_width()/2, surface.get_height()/2])
    surface.blit(Text, [surface.get_width()/2 - Text.get_width()/2, 
                        surface.get_height()/4 - Text.get_height()/2])
    surface.blit(subText, [surface.get_width()/2 - subText.get_width()/2, 
                            surface.get_height()/2 - subText.get_height()/2])
    yes_rect = surface.blit(yes, [surface.get_width()/4 - yes.get_width()/2, 
                                  3*surface.get_height()/4 - yes.get_height()/2])
    no_rect = surface.blit(no, [3*surface.get_width()/4 - no.get_width()/2, 
                      3*surface.get_height()/4 - no.get_height()/2])

    if len(hand_pos) == 2:
        if(yes_rect.collidepoint(hand_pos)):
            return 1
        elif(no_rect.collidepoint(hand_pos)):
            return 0
