import pygame
import sqlite3
from lib.text import TextBox
import os

white = (255, 255, 255)
black = (0, 0, 0)
class scoreboard:
    # TODO: Enquadrar rosto corretamente e tirar foto
    def __init__(self):
        self.load()
        self.screensize = [1280, 720]

        self.connection = sqlite3.connect("./history/leaderboards.db")
        self.cursor = self.connection.cursor()

    def snapshot(self, window, nose_position, ear_position_1, ear_position_2, picture = 0, score = 0):
        if nose_position[0] < 0 or nose_position[1] < 0:
            return
        nose = []
        nose.append(round(nose_position[0]))
        nose.append(round(nose_position[1]))

        width = (round(3*abs(nose[0]-ear_position_1[0])) + round(3*abs(nose[0]-ear_position_2[0])))/2

        width_height = (width, width)
        rect = pygame.Rect((0,0), width_height)
        rect.center = (nose[0], nose[1])
        
        face = pygame.Surface(width_height)
        face.blit(window, (0,0), area=rect)
        
        pygame.draw.rect(window, color=(120, 0, 255), rect=rect, width=1)
        if picture==1:
            arr=os.listdir("./test")
            if arr:
                index= int("".join(x for x in arr[-1] if x.isdigit())) + 1 
            else:
                index = 1
            mytext = TextBox(window, size=20)
            mytext.updateText(str(index))
            mytext.display()
    
            pygame.image.save(face, "./test/"+str(index)+".png")

            self.cursor.execute("INSERT INTO leaderboard VALUES ('"+ str(index) + "', '"+str(score)+"')")
            
            self.connection.commit()
            return index

    def update(self):
        pass

    def load(self):
        pass

    def show(self, window):
        txt = "HIGHSCORES:\n"
        
        entries = []
        # background
        leaderboard_screen = pygame.Surface((0.95*window.get_width(), 0.95*window.get_height()))
        leaderboard_screen.fill(white)
        leaderboard_screen.set_alpha(100)
        
        vertical_line = pygame.Surface((0.01*leaderboard_screen.get_width(), leaderboard_screen.get_height()))
        vertical_line.fill(black)
        vertical_line.set_alpha(100)

        horizontal_line = pygame.Surface((leaderboard_screen.get_width(), 0.02*leaderboard_screen.get_height()))
        horizontal_line.fill(black)
        horizontal_line.set_alpha(100)
        
        fontsize = 80
        font = pygame.font.Font("./resources/PolygonParty.ttf", fontsize)
        text = font.render("LEADERBOARD", 1, black)
        
        score_screen = pygame.Surface((leaderboard_screen.get_width(), leaderboard_screen.get_height() - fontsize - 30))
        i = 0
        for row in self.cursor.execute('SELECT * FROM leaderboard ORDER BY score'):
            if entries:
                entries.append(leaderboardEntry(row[0], row[1], score_screen, entries[-1]))
            else:
                entries.append(leaderboardEntry(row[0], row[1], score_screen, None))
            if i >= 8:
                break
            i = i + 1
        
        leaderboard_screen.blit(horizontal_line, (0, fontsize+20))
        leaderboard_screen.blit(vertical_line, (leaderboard_screen.get_width()/2+vertical_line.get_width(), fontsize+20))
        leaderboard_screen.blit(text, (leaderboard_screen.get_width()/2-fontsize*len("LEADERBOARD")/3,10))
        
        for e in entries:
            e.render()
        leaderboard_screen.blit(score_screen, (0, fontsize + 30))
        window.blit(leaderboard_screen, (round(0.025*self.screensize[0]),round(0.025*self.screensize[1])))


class leaderboardEntry:
    def __init__(self, picture_id, score, window, parent = None):
        self.id = picture_id        
        self.parent = parent

        self.width = window.get_width()/2
        self.height = window.get_height()/4

        if self.parent == None:
            self.pos = (10,10)
            self.ranking = 1
        else:
            self.ranking = self.parent.ranking + 1
            if self.ranking ==5:
                self.pos = (self.width, 10)
            else:
                self.pos = (self.parent.pos[0], self.parent.pos[1] + self.height)
            
        
        self.window = window
        picturename = str(picture_id) + ".png"
        picturepath = "./test/"+picturename
        
        if picturename not in os.listdir("./test"):
            self.picture = pygame.image.load("./resources/shyguy.png").convert_alpha()
        else:
            self.picture = pygame.image.load(picturepath).convert_alpha()
        self.picture = pygame.transform.scale(self.picture, (0.8*self.height, 0.8*self.height))
        
        self.surface = pygame.Surface((self.width, self.height))

        font = pygame.font.Font("./resources/SuperMario256.ttf", int(self.height))
        if self.ranking == 1:
            self.text = font.render("1", 1, (255,215,0))
        elif self.ranking == 2:
            self.text = font.render("2", 1, (192,192,192))
        elif self.ranking == 3:
            self.text = font.render("3", 1, (176, 141, 87))
        else:
            self.text = font.render(str(self.ranking), 1, white)
        
        font = pygame.font.Font("./resources/SuperMario256.ttf", int(self.height*0.9))
        self.score = font.render(str(score), 1, white)
    def render(self):
        self.surface.blit(self.picture, (self.height+10,0), self.picture.get_rect())
        self.surface.blit(self.text, (10,0))
        self.surface.blit(self.score, (self.height*2+10, 0.05*self.height))
        self.window.blit(self.surface, self.pos)
