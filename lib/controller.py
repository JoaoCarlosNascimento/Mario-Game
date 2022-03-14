import mediapipe as mp
from google.protobuf.json_format import MessageToDict

import cv2

hand_detect = mp.solutions.hands
face_detection = mp.solutions.face_detection

class controller:
    def __init__(self):
        
        self.__detectors = {}

        # Inicializando Detector de mãos
        self.__detectors['Hands'] = {}
        self.__detectors['Hands']['Detector'] = hand_detect.Hands(model_complexity=0, min_detection_confidence=0.3, min_tracking_confidence=0.3)
        self.__detectors['Hands']['LastCommands'] = {}
        self.__detectors['Hands']['LastCommands']['Left'] = (-1,-1)
        self.__detectors['Hands']['LastCommands']['Right'] = (-1,-1)

        # Inicializando Detector de mãos
        self.__detectors['Face'] = {}
        self.__detectors['Face']['Detector'] = face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5)
        self.__detectors['Face']['LastCommands'] = (-1,-1)

        self.__res = (0,0)

    def get_commands(self, state=0, img=[]):
        if state == -11:
            return self.__hand_detector(img)
        if state == -12:
            return self.__face_detector(img)
        return (-1,-1)

    def __face_detector(self,img):

        if self.__res == (0,0):
            self.__res = (img.shape[1],img.shape[0])

        self.__detectors['Face']['LastCommands'] = (-1,-1)

        frameCV_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.__detectors['Face']['Detector'].process(frameCV_RGB)

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
                    self.__detectors['Face']['LastCommands'] = (self.__res[0]-int(kp.x * self.__res[0]),kp.y * self.__res[1])
        return [self.__detectors['Face']['LastCommands']]

    def __hand_detector(self,img):

        if self.__res == (0,0):
            self.__res = (img.shape[1],img.shape[0])

        self.__reset_hand_detector()

        frameCV_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        results = self.__detectors['Hands']['Detector'].process(frameCV_RGB) # convert from BGR to RGB
        if results.multi_hand_landmarks is not None:
            # EACH HAND #
            for handLms, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                handedness_dict1 = MessageToDict(handedness)
                # RIGHT HAND  #
                if handedness_dict1['classification'][0]['label'] == 'Right':
                    # EACH POINTS OF THE HAND #
                    for id, lm in enumerate(handLms.landmark):
                        if id == hand_detect.HandLandmark.INDEX_FINGER_TIP:
                            self.__detectors['Hands']['LastCommands']['Right'] = (self.__res[0]-int(lm.x*self.__res[0]),int(lm.y*self.__res[1]))
                # LEFT HAND #
                if handedness_dict1['classification'][0]['label'] == 'Left':
                    # EACH POINTS OF THE HAND #
                    for id, lm in enumerate(handLms.landmark):
                        if id == hand_detect.HandLandmark.INDEX_FINGER_TIP:
                            self.__detectors['Hands']['LastCommands']['Left'] = (self.__res[0]-int(lm.x*self.__res[0]),int(lm.y*self.__res[1]))

        return [self.__detectors['Hands']['LastCommands']['Left'],self.__detectors['Hands']['LastCommands']['Right']]

    def __reset_hand_detector(self):
        self.__detectors['Hands']['LastCommands']['Left']=(-1,-1)
        self.__detectors['Hands']['LastCommands']['Right']=(-1,-1)