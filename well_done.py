import time as t
import cv2
import pygame
from cvzone.HandTrackingModule import HandDetector
from pygame import *
import myTools as myAux
import game
import sys
import os
import pyautogui
import images

pygame.init()

well_done_size = [950, 150]
tip_size = [75, 85]
back_over_size = [1920, 1080]
state: 0

# Detector
detector = HandDetector(detectionCon=0.8, maxHands=2)
Screen_Width, Screen_Height = pyautogui.size()

window = pygame.display.set_mode((Screen_Width, Screen_Height))
pygame.display.set_caption("Mario")

fps = 60
clock = pygame.time.Clock()

# well done
imgWell_done, rectWell_done = images.load_image( Screen_Width, Screen_Height, file_name='Images/well_done.png',
                                                img_size=well_done_size,
                                                translation=(1, 6.5))
# Finger Tip
imgTip, rectTip = images.load_image( Screen_Width, Screen_Height, file_name='Images/Star.PNG',
                                    img_size=tip_size,
                                    translation=(1, 3))
# background of this menu
imgBackground, rectBackground = images.load_image( Screen_Width, Screen_Height, file_name='Images/back_over.png',
                                    img_size=back_over_size,
                                    translation=(1, 1))

# Variables
speed = 10
startTime = t.time()
totalTime = 18000

def Well_done_menu(screen, in_Winputs):
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
        Winputs = myAux.webcamInputs(webcamInputs=in_Winputs, vid_stream=in_Winputs.vid_stream,
                                     offset=in_Winputs.offset, subSampling=in_Winputs.subSampling, detector='FaceHand')
        img, hands = Winputs.get_inputs()
        if (tcount >= 60):
            # print("Exec Time (main): "+str(round((sum(ctime)/60)/(1000*1000)))+" (ms)")
            ctime.pop(0)

        window.blit(imgBackground, rectBackground)
        window.blit(imgWell_done, rectWell_done)

        if hands:
            if (hands[0][0] > 0) and (hands[0][1] > 0):
                window.blit(imgTip, hands[0])
            if (hands[1][0] > 0) and (hands[1][1] > 0):
                window.blit(imgTip, hands[1])

        # Update Display
        pygame.display.update()

        # Set FPS
        clock.tick(fps)
        ctime.append(t.time_ns() - ctime_i)
        tcount += 1


cv2.destroyAllWindows()
