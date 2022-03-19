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

        self.con = sqlite3.connect("./history/leaderboards.db")
        self.cur = self.con.cursor()
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

            self.cur.execute("INSERT INTO leaderboard VALUES ('"+ str(index) + "', '"+str(score)+"')")
            self.con.commit()
            return index

    def update(self):
        pass

    def load(self):
        pass

    def show(self, window):
        txt = "HIGHSCORES:\n"
        images = []
        image_pos = []
        for row in self.cur.execute('SELECT * FROM leaderboard ORDER BY score'):
            txt = txt + "\n" + str(row)
            images.append(pygame.image.load("./test/"+str(row[0]) + ".png").convert_alpha())
        
        for i in range(len(images)):
            image_pos.append(images[i].get_rect())
        # background
        leaderboard_screen = pygame.Surface((0.95*window.get_width(), 0.95*window.get_height()))
        leaderboard_screen.fill(white)
        leaderboard_screen.set_alpha(70)
        
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
        # score_screen.fill(black)
        leaderboard_screen.blit(score_screen, (0, fontsize + 30))
        leaderboard_screen.blit(horizontal_line, (0, fontsize+20))
        leaderboard_screen.blit(vertical_line, (leaderboard_screen.get_width()/2+vertical_line.get_width(), fontsize+20))
        leaderboard_screen.blit(text, (leaderboard_screen.get_width()/2-fontsize*len("LEADERBOARD")/3,10))

        window.blit(leaderboard_screen, (round(0.025*self.screensize[0]),round(0.025*self.screensize[1])))
        
        # add images
        ###########################################
        # debug
        mytext = TextBox(window, size=20)
        mytext.updateText(txt)
        mytext.display()

class leaderboardEntry:
    def __init__(self, picture_id, score, window):
        self.id = picture_id
        self.score = score

        self.window = window
