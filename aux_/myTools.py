import cv2
import time as t
from cv2 import resize
import numpy as np
import mediapipe as mp
import pygame
from pygame import *
import pyautogui
import game
from tkinter.filedialog import *
import os
import images

import imutils
from imutils.video import VideoStream

#Hand Detector
from cvzone.HandTrackingModule import HandDetector
import mediapipe as mp
from google.protobuf.json_format import MessageToDict
import pyautogui
from images import load_image

# Detector
detector = HandDetector(detectionCon=0.8, maxHands=2)
Screen_Width, Screen_Height = pyautogui.size()

#################
#   FUNCTIONS   #
#################

def transform_cap(img, screen, offset=(0, 0)):
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    imgRGB = np.rot90(imgRGB)
    frame = pygame.surfarray.make_surface(imgRGB).convert()
    frame = pygame.transform.flip(frame, True, False)
    screen.blit(frame, offset)


def showFPS(prev_frame_time, new_frame_time):
    new_frame_time = t.time()
    fps = str(int(1/(new_frame_time-prev_frame_time)))
    prev_frame_time = new_frame_time
    return prev_frame_time, new_frame_time, fps


def getNewFrameOpenCV(cap, width, height):
    retval,frame = cap.read()
    frame = cv2.resize(frame, (width, height))
    if not retval:
        return retval, 0, 0, 0, 0

    h, w, c = frame.shape
    return retval, h, w, c, frame


def frameCV2Py(frame):
    frame = np.rot90(frame)
    frame_RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_RGB = pygame.surfarray.make_surface(frame_RGB)
    return frame_RGB


class webcamInputs:
    def __init__(self,webcamInputs=[],vid_stream=[],subSampling=0,src=0,scale=0.7,windowRes=(1920,1080),offset=(0,0),detector='Menu'):
        if(webcamInputs != []):
            self.vid_stream=webcamInputs.vid_stream
            self.scale=webcamInputs.scale
            self.windowRes=webcamInputs.windowRes
            self.offset=webcamInputs.offset
            self.detector=webcamInputs.detector
            self.subSampling=webcamInputs.subSampling

            if(self.windowRes != (1920,1080)):
                self.windowRes = windowRes
            if(self.scale != 0.7):
                self.scale = scale
            if(self.offset != (0,0)):
                self.offset = offset
            if(self.subSampling != 0):
                self.subSampling = subSampling
        else:
            self.windowRes = windowRes
            self.scale = scale
            self.offset = offset
            self.subSampling = subSampling

        if(vid_stream == []):
            self.vid_stream = VideoStream(src=src).start()
        else:
            self.vid_stream = vid_stream

        self.outRes = (round(self.windowRes[0]*scale),round(self.windowRes[1]*scale))
        frame = self.vid_stream.read()
        height, width = frame.shape[0], frame.shape[1]
        self.hscale = (self.outRes[0]/width,self.outRes[1]/height)

        self.detectorType = detector

        self.l_cords = []
        self.l_cords.append((-1,-1)) #Left Hand(Opponent)
        self.l_cords.append((-1,-1)) #Right Hand(Player)
        self.l_cords.append((-1,-1)) #Left Face(Opponent)
        self.l_cords.append((-1,-1)) #Right Face(Player)

        if self.detectorType == 'Menu':
            self.detector = HandDetector(detectionCon=0.8, maxHands=2)

        elif self.detectorType == 'FaceDetection':
            mp_face_detection = mp.solutions.face_detection
            mp_drawing = mp.solutions.drawing_utils
            self.detector = mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5)

        elif self.detectorType == 'GameHand':
            mp_drawing = mp.solutions.drawing_utils
            mp_drawing_styles = mp.solutions.drawing_styles
            self.mp_hands = mp.solutions.hands
            self.detector = self.mp_hands.Hands(model_complexity=0, min_detection_confidence=0.3, min_tracking_confidence=0.3)
        elif self.detectorType == 'FaceHand':
            self.detector = []

            mp_drawing = mp.solutions.drawing_utils
            mp_drawing_styles = mp.solutions.drawing_styles
            self.mp_hands = mp.solutions.hands

            self.detector.append(self.mp_hands.Hands(model_complexity=0, min_detection_confidence=0.3, min_tracking_confidence=0.3))

            mp_face_detection = mp.solutions.face_detection
            mp_drawing = mp.solutions.drawing_utils

            self.detector.append(mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5))

        self.subSampCounter = self.subSampling

        self.l_frame = []
        self.l_detected = []

    def reset_cords(self):
        for i in range(len(self.l_cords)):
            self.l_cords[i] = (-1,-1)

    def get_inputs(self,frame=[]):
        if(self.subSampCounter <= (self.subSampling-1) or self.l_frame == [] or frame != []):
            if frame == []:
                frame = self.vid_stream.read()

            self.reset_cords()

            if self.detectorType == 'Menu':
                frame = cv2.flip(frame, 1)
                hands, frame = self.detector.findHands(frame, flipType=False)

                if hands:
                    for hand in hands:
                        x, y, c = hand['lmList'][8]
                        if hand['type'] == 'Left':
                            self.l_cords[0] = (x*self.hscale[0]+self.offset[0], y*self.hscale[1]+self.offset[1])
                        else:
                            self.l_cords[1] = (x*self.hscale[0]+self.offset[0], y*self.hscale[1]+self.offset[1])

            elif self.detectorType == 'FaceDetection':
                frameCV_RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.detector.process(frameCV_RGB)

                if results.detections:
                    for detection in results.detections:
                        # Indice 0: Olho Direito
                        # Indice 1: Olho Esquerdo
                        # Indice 2: Nariz
                        # Indice 3: Meio da Boca
                        # Indice 4: Ouvido Direito
                        # Indice 5: Olho
                        kp = detection.location_data.relative_keypoints[2]
                        if kp is not None:
                            x, y = self.outRes[0] - int(kp.x * self.outRes[0]) + self.offset[0], int(
                                kp.y * self.outRes[1]) + self.offset[1]
                            if kp.x >= 0.5:
                                self.l_cords[1] = (x, y)
                            else:
                                self.l_cords[0] = (x, y)

            elif self.detectorType == 'GameHand':
                frameCV_RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                results = self.detector.process(frameCV_RGB) # convert from BGR to RGB
                if results.multi_hand_landmarks is not None:
                    # EACH HAND #
                    for handLms, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                        handedness_dict1 = MessageToDict(handedness)
                        # RIGHT HAND  #
                        if handedness_dict1['classification'][0]['label'] == 'Right':
                            # EACH POINTS OF THE HAND #
                            for id, lm in enumerate(handLms.landmark):
                                if id == self.mp_hands.HandLandmark.INDEX_FINGER_TIP:
                                    x, y = self.outRes[0]-int(lm.x*self.outRes[0])+self.offset[0], int(lm.y*self.outRes[1])+self.offset[1]
                                    self.l_cords[1] = (x,y)
                        # LEFT HAND #
                        if handedness_dict1['classification'][0]['label'] == 'Left':
                            # EACH POINTS OF THE HAND #
                            for id, lm in enumerate(handLms.landmark):
                                if id == self.mp_hands.HandLandmark.INDEX_FINGER_TIP:
                                    x, y = self.outRes[0]-int(lm.x*self.outRes[0])+self.offset[0], int(lm.y*self.outRes[1])+self.offset[1]
                                    self.l_cords[0] = (x,y)

            elif self.detectorType == 'FaceHand':
                self.reset_cords()
                frameCV_RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                results = self.detector[0].process(frameCV_RGB) # convert from BGR to RGB
                if results.multi_hand_landmarks is not None:
                    # EACH HAND #
                    for handLms, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                        handedness_dict1 = MessageToDict(handedness)
                        # RIGHT HAND  #
                        if handedness_dict1['classification'][0]['label'] == 'Right':
                            # EACH POINTS OF THE HAND #
                            for id, lm in enumerate(handLms.landmark):
                                if id == self.mp_hands.HandLandmark.INDEX_FINGER_TIP:
                                    x, y = self.outRes[0]-int(lm.x*self.outRes[0])+self.offset[0], int(lm.y*self.outRes[1])+self.offset[1]
                                    self.l_cords[1] = (x,y)
                        # LEFT HAND #
                        if handedness_dict1['classification'][0]['label'] == 'Left':
                            # EACH POINTS OF THE HAND #
                            for id, lm in enumerate(handLms.landmark):
                                if id == self.mp_hands.HandLandmark.INDEX_FINGER_TIP:
                                    x, y = self.outRes[0]-int(lm.x*self.outRes[0])+self.offset[0], int(lm.y*self.outRes[1])+self.offset[1]
                                    self.l_cords[0] = (x,y)

                                frameCV_RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.detector[1].process(frameCV_RGB)

                if results.detections:
                    for detection in results.detections:
                        # Indice 0: Olho Direito
                        # Indice 1: Olho Esquerdo
                        # Indice 2: Nariz
                        # Indice 3: Meio da Boca
                        # Indice 4: Ouvido Direito
                        # Indice 5: Olho
                        kp = detection.location_data.relative_keypoints[2]
                        if kp is not None:
                            x, y = self.outRes[0] - int(kp.x * self.outRes[0]) + self.offset[0], int(
                                kp.y * self.outRes[1]) + self.offset[1]
                            if kp.x >= 0.5:
                                self.l_cords[3] = (x, y)
                            else:
                                self.l_cords[2] = (x, y)

            frame = cv2.resize(frame, (self.outRes[0], self.outRes[1]), interpolation=cv2.INTER_AREA)
            self.l_frame = frame
            self.subSampCounter = self.subSampling

        self.subSampCounter -= 1

        if self.detectorType != 'Menu':
            self.l_frame = frameCV2Py(self.l_frame)

        return self.l_frame, self.l_cords 
