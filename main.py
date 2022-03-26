import time as t
import cv2
import pygame
from cvzone.HandTrackingModule import HandDetector
from pygame import *
import old.myTools as myAux
import game
import sys
import os
import pyautogui
import images
import old.controls as controls
import well_done
from lib.scoreboard import scoreboard

if(len(sys.argv) > 1):
    if (sys.argv[1] == '--cam' and sys.argv[2] == '1'):
        camSrc = 'https://192.168.1.169:8080/video'
else:
    camSrc = 0

pygame.init()
scale = 6
background_size = [1920, 1080]
gif_size = [scale*350, 2*350]
play_size = [350, 150]
scores_size = [350, 150]
controls_size = [350, 150]
quit_size = [350, 150]
logo_size = [900, 400]
tip_size = [75, 85]

state: 0

# Detector
detector = HandDetector(detectionCon=0.8, maxHands=2)
Screen_Width, Screen_Height = pyautogui.size()
# Images
screen_size = [(Screen_Width - Screen_Width) / 2,
               (Screen_Height - Screen_Height) / 2]

# Webcam inputs
Winputs = myAux.webcamInputs(src=camSrc, scale=0.7, subSampling=3, windowRes=(Screen_Width, Screen_Height),
                             offset=(screen_size[0], screen_size[1]), detector='Menu')

window = pygame.display.set_mode((Screen_Width, Screen_Height))
pygame.display.set_caption("Mario")

fps = 60
clock = pygame.time.Clock()

# Play button -> done
imgPlay, rectPlay = images.load_image( Screen_Width, Screen_Height, file_name='Images/play_menu.png',
                                      img_size=play_size,
                                      translation=(2.6, 2))
# controls button
imgControl, rectControl = images.load_image( Screen_Width, Screen_Height, file_name='Images/controls_menu.png',
                                      img_size=controls_size,
                                      translation=(-0.6, 2))
# Scores button
imgScore, rectScore = images.load_image( Screen_Width, Screen_Height, file_name='Images/scores_menu.png',
                                      img_size=scores_size,
                                      translation=(2.6, -1))
# Quit button
imgQuit, rectQuit = images.load_image( Screen_Width, Screen_Height, file_name='Images/quit_menu.png',
                                      img_size=quit_size,
                                      translation=(-0.6, -1))
# Logo Mario
imgLogo, rectLogo = images.load_image( Screen_Width, Screen_Height, file_name='Images/logo_menu.png',
                                      img_size=logo_size,
                                      translation=(1, 3))
# Finger Tip
imgTip, rectTip = images.load_image( Screen_Width, Screen_Height, file_name='Images/Star.PNG',
                                      img_size=tip_size,
                                      translation=(1, 3))
# background
imgBg, rectBg = images.load_image( Screen_Width, Screen_Height, file_name='Images/background.png',
                                  img_size=(1920, 1080),
                                  translation=(1, 1))
# menu gif
gif_Menu = images.load_gif( Screen_Width, Screen_Height, "Image_Menu", "Menu", gif_size, (1, 0.57))

# Variables
speed = 10
startTime = t.time()
totalTime = 18000

# Main loop
start = True
ctime = []
ctime_mean = 0
tcount = 0

ct = 0
while start:
   ctime_i = t.time_ns()
   # Get Events
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         start = False
         pygame.quit()
         sys.exit()
      if event.type == pygame.KEYDOWN:
         if event.key == pygame.K_ESCAPE:
            start = False
            pygame.quit()
            sys.exit()

   index = sum([len(files) for r, d, files in os.walk("Pictures")])
   # OpenCV
   img, hands = Winputs.get_inputs()
   if (tcount >= 60):
      # print("Exec Time (main): "+str(round((sum(ctime)/60)/(1000*1000)))+" (ms)")
      ctime.pop(0)

   window.blit(imgBg, rectBg)
   window.blit(imgPlay, rectPlay)
   window.blit(imgScore, rectScore)
   window.blit(imgControl, rectControl)
   window.blit(imgQuit, rectQuit)
   window.blit(imgLogo, rectLogo)

   gif_Menu.update()

   gif_Menu.draw(window)
   if hands:
      if (hands[0][0] > 0) and (hands[0][1] > 0):
          window.blit(imgTip, hands[0])
      if (hands[1][0] > 0) and (hands[1][1] > 0):
         window.blit(imgTip, hands[1])
      for i in range(2):
          if rectControl.collidepoint(hands[i][0], hands[i][1]):
              controls.controls_menu(window, Winputs)
              break
          if rectScore.collidepoint(hands[i][0], hands[i][1]):
              s = scoreboard()
              s.show(window)
              break
          if rectQuit.collidepoint(hands[i][0], hands[i][1]):
              pygame.quit()
              sys.exit()

   # Update Display
   pygame.display.update()

   # Set FPS
   clock.tick(fps)
   ctime.append(t.time_ns() - ctime_i)
   tcount += 1

cv2.destroyAllWindows()
