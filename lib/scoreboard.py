import pygame
import sqlite3
from lib.text import TextBox
import os

white = (255, 255, 255)
black = (0, 0, 0)

class scoreboard:
    # TODO: Enquadrar rosto corretamente e tirar foto
    def __init__(self, window_size=(1920,1080)):
        self.screensize = window_size
        self.folder  = "./history/faces/"
        self.connection = sqlite3.connect("./history/leaderboards.db")
        self.cursor = self.connection.cursor()

    def snapshot(self, window, commands, score = 9999):
        if((-1, -1) not in commands[0]):
            face = self.display(window, commands)
            aux = []
            for row in self.cursor.execute('SELECT * FROM leaderboard ORDER BY id + 0 DESC'):
                aux.append([row[0], row[1]])
            if aux:
                index = int(aux[0][0]) + 1
            else:
                index = 1
            
            pygame.image.save(face, self.folder+str(index)+".png")

            self.cursor.execute("INSERT INTO leaderboard (id, score) VALUES ('"+ str(index) + "', '"+str(score)+"')")
            
            self.connection.commit()
            return index

    def display(self, window, commands):
        nose_position =  commands[0][0]
        ear_position_1 = commands[0][1]
        ear_position_2 = commands[0][2]
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
        return face

    def show(self, window):
        txt = "HIGHSCORES:\n"
        
        entries = []
        # background
        leaderboard_screen = pygame.Surface((0.95*window.get_width(), 0.95*window.get_height()))
        leaderboard_screen.fill(black)
        leaderboard_screen.set_alpha(300)
        
        vertical_line = pygame.Surface((0.01*leaderboard_screen.get_width(), leaderboard_screen.get_height()))
        vertical_line.fill(white)
        vertical_line.set_alpha(100)

        horizontal_line = pygame.Surface((leaderboard_screen.get_width(), 0.02*leaderboard_screen.get_height()))
        horizontal_line.fill(white)
        horizontal_line.set_alpha(100)
        
        fontsize = 80
        font = pygame.font.Font("./resources/PolygonParty.ttf", fontsize)
        text = font.render("LEADERBOARD", 1, white)
        
        score_screen = pygame.Surface((leaderboard_screen.get_width(), leaderboard_screen.get_height() - fontsize - 30))
        i = 0
        # self.cursor.execute("ORDER BY score DESC")
        for row in self.cursor.execute('SELECT * FROM leaderboard ORDER BY score + 0 DESC'):
            if entries:
                entries.append(leaderboardEntry(row[0], row[1], score_screen, entries[-1]))
            else:
                entries.append(leaderboardEntry(row[0], row[1], score_screen, None))
            if i >= 8:
                break
            i = i + 1
        
        leaderboard_screen.blit(horizontal_line, (0, fontsize+7))
        leaderboard_screen.blit(text, (leaderboard_screen.get_width()/2-fontsize*len("LEADERBOARD")/3,5))
        
        for e in entries:
            e.render()
        
        leaderboard_screen.blit(score_screen, (0, fontsize + 30))
        leaderboard_screen.blit(vertical_line, (leaderboard_screen.get_width()/2, fontsize+27))

        window.blit(leaderboard_screen, (round(0.025*self.screensize[0]),round(0.025*self.screensize[1])))
    

class leaderboardEntry:
    def __init__(self, picture_id, score, window, parent = None):
        self.id = picture_id        
        self.parent = parent

        self.width = window.get_width()/2
        self.height = window.get_height()/4

        if self.parent == None:
            self.pos = (0,10)
            self.ranking = 1
        else:
            self.ranking = self.parent.ranking + 1
            if self.ranking ==5:
                self.pos = (self.width + self.height*0.1, 10)
            else:
                self.pos = (self.parent.pos[0], self.parent.pos[1] + self.height)
            
        
        self.window = window
        picturename = str(picture_id) + ".png"
        picturepath =  "./history/faces/"+picturename
        
        if picturename not in os.listdir("./history/faces/"):
            self.picture = pygame.image.load("./resources/shyguy.png").convert_alpha()
        else:
            self.picture = pygame.image.load(picturepath).convert_alpha()
        self.picture = pygame.transform.scale(self.picture, (0.8*self.height, 0.8*self.height))
        
        self.surface = pygame.Surface((self.width, self.height))

        font = pygame.font.Font("./resources/SuperMario256.ttf", int(self.height))
        if self.ranking == 1:
            self.rank = font.render("1", 1, (255,215,0))
        elif self.ranking == 2:
            self.rank = font.render("2", 1, (192,192,192))
        elif self.ranking == 3:
            self.rank = font.render("3", 1, (176, 141, 87))
        else:
            self.rank = font.render(str(self.ranking), 1, white)
        
        font = pygame.font.Font("./resources/SuperMario256.ttf", int(self.height*0.9))
        self.score = font.render(str(score), 1, white)
    def render(self):
        self.surface.blit(self.picture, (self.height,0), self.picture.get_rect())
        self.surface.blit(self.rank, (0.1*self.height,0))
        self.surface.blit(self.score, (self.height*2-10, 0.05*self.height))
        self.window.blit(self.surface, self.pos)
