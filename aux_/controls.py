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

pygame.init()
scale = 6
background_size = [1920, 1080]
gif_right_size = [500, 500]
gif_middle_size = [500, 500]
gif_left_size = [500, 500]
controls_size = [750, 150]
back_size = [180, 100]
dir_right_size = [140, 200]
dir_left_size = [140, 200]
tip_size = [75, 85]

state: 0

# Detector
detector = HandDetector(detectionCon=0.8, maxHands=2)
Screen_Width, Screen_Height = pyautogui.size()

window = pygame.display.set_mode((Screen_Width, Screen_Height))
pygame.display.set_caption("Mario")

fps = 60
clock = pygame.time.Clock()

# controls
imgControl, rectControl = images.load_image( Screen_Width, Screen_Height, file_name='Images/controls_.png',
                                            img_size=controls_size,
                                            translation=(1, 6.5))
# back
imgBack, rectBack = images.load_image( Screen_Width, Screen_Height, file_name='Images/back_.png',
                                      img_size=back_size,
                                      translation=(9.5, 9))
# right arm
imgR_dir, rectR_dir = images.load_image(Screen_Width, Screen_Height, file_name='Images/right_direction.png',
                                      img_size=dir_right_size,
                                      translation=(-8, -2.5))
# left arm
imgL_dir, rectL_dir = images.load_image(Screen_Width, Screen_Height, file_name='Images/left_direction.png',
                                      img_size=dir_left_size,
                                      translation=(10, -2.5))
# Finger Tip
imgTip, rectTip = images.load_image( Screen_Width, Screen_Height, file_name='Images/Star.PNG',
                                      img_size=tip_size,
                                      translation=(1, 3))

# to the right
gif_Right = images.load_gif( Screen_Width, Screen_Height, "Image_right", "right", gif_right_size, (-1.5, 1))
# jump and duck
gif_Middle = images.load_gif( Screen_Width, Screen_Height, "Image_jumpduck", "jumpduck", gif_middle_size, (1, 1))
# to the left
gif_Left = images.load_gif( Screen_Width, Screen_Height, "Image_left", "left", gif_left_size, (3.5, 1))

# background
imgBg, rectBg = images.load_image( Screen_Width, Screen_Height, file_name='Images/background.png',
                                  img_size=(1920, 1080),
                                  translation=(1, 1))
# Variables
speed = 10
startTime = t.time()
totalTime = 18000

def controls_menu(screen,hands):
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
        # Winputs = myAux.webcamInputs(webcamInputs=in_Winputs, vid_stream=in_Winputs.vid_stream,
        #                              offset=in_Winputs.offset, subSampling=in_Winputs.subSampling, detector='FaceHand')
        # img, hands = Winputs.get_inputs()
        if (tcount >= 60):
            # print("Exec Time (main): "+str(round((sum(ctime)/60)/(1000*1000)))+" (ms)")
            ctime.pop(0)

        window.blit(imgBg, rectBg)
        window.blit(imgControl, rectControl)
        window.blit(imgBack, rectBack)
        window.blit(imgR_dir, rectR_dir)
        window.blit(imgL_dir, rectL_dir)

        gif_Right.update()
        gif_Middle.update()
        gif_Left.update()

        gif_Right.draw(window)
        gif_Middle.draw(window)
        gif_Left.draw(window)

        if hands:
            if (hands[0][0] > 0) and (hands[0][1] > 0):
                window.blit(imgTip, hands[0])
            if (hands[1][0] > 0) and (hands[1][1] > 0):
                window.blit(imgTip, hands[1])
            for i in range(2):
                if rectBack.collidepoint(hands[i][0], hands[i][1]):
                    return "back"
