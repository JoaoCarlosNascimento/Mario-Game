from cv2 import KeyPoint
import mediapipe as mp
from google.protobuf.json_format import MessageToDict
import numpy as np
# from mediapipe.framework.formats import landmark_pb2

import cv2
hand_detector = mp.solutions.hands
face_detector = mp.solutions.face_detection
body_detector = mp.solutions.pose

class controller:
    ## MOVE L/R ##
    # move Left/Right parameters
    __move_LR_distance_lim = 999#(75,105)
    __move_LR_angle_lim = (72, 105) #90
    # __move_L_angle_lim = (75, 105) #45(35, 53) #45
    __move_LR_visibility_lim = -999

    ## CROUCH ##
    # crouch parameters
    __crouch_angle_lim = 160
    __crouch_visibility_lim = -999

    ## JUMP ##
    # jump parameters
    __jump_ang_lim = 173
    __jump_pos_lim = 10
    __jump_delta_lim = 20
    __buffer_samples = 5
    # jump variables
    __jump_hips_pose_k = []
    __jump_hips_pose_km1 = []

    def __init__(self):
        
        self.__detectors = {}

        # Inicializando Detector de mãos
        self.__detectors['Hands'] = {}
        self.__detectors['Hands']['Detector'] = hand_detector.Hands(model_complexity=0, min_detection_confidence=0.3, min_tracking_confidence=0.3)
        self.__detectors['Hands']['LastCommands'] = {}
        self.__detectors['Hands']['LastCommands']['Left'] = (-1,-1)
        self.__detectors['Hands']['LastCommands']['Right'] = (-1,-1)

        # Inicializando Detector de face
        self.__detectors['Face'] = {}
        self.__detectors['Face']['Detector'] = face_detector.FaceDetection(model_selection=0, min_detection_confidence=0.5)
        self.__detectors['Face']['LastCommands'] = (-1,-1)

        # Inicializando Detector de corpo
        self.__detectors['Body'] = {}
        self.__detectors['Body']['Detector'] = body_detector.Pose(static_image_mode=False,
                                                                    smooth_landmarks=True,
                                                                    model_complexity=1,
                                                                    enable_segmentation=False,
                                                                    min_detection_confidence=0.5)

        self.__detectors['Body']['LastCommands'] = []
        self.__detectors['Body']['Landmarks'] = []
        
        self.__frame_count = -1

        self.__res = (0,0)

    def get_commands(self, state=0, img=[], Sampling=1):
        if self.__frame_count-1 <= 0:
            if state == "game":
                return self.__hand_detector(img)
            if state in ["save score?", "game over"]:
                return self.__hand_detector(img)
            if state == "prepare pic" or state == "pic":
                com, debug, f = self.__face_detector(img, key_point=[2, 4, 5])
                com, debug, h = self.__hand_detector(img)
                return com, debug, [f, h]
            if state == -11:
                return self.__hand_detector(img)
            elif state == -12:
                return self.__face_detector(img)
            elif state == -13:
                return self.__body_detector(img,0)
            self.__frame_count = Sampling
        self.__frame_count -= 1
        return 0, "", [(-1,-1)]

    def __face_detector(self, img, key_point=[2]):

        if self.__res == (0,0):
            self.__res = (img.shape[1],img.shape[0])


        frameCV_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.__detectors['Face']['Detector'].process(frameCV_RGB)
        self.__detectors['Face']['LastCommands'] = []
        for i in range(len(key_point)):
            self.__detectors['Face']['LastCommands'].append((-1, -1))
        if results.detections:
            for detection in results.detections:
                # Indice 0: Olho Direito
                # Indice 1: Olho Esquerdo
                # Indice 2: Nariz
                # Indice 3: Meio da Boca
                # Indice 4: Ouvido Direito
                # Indice 5: Orelha Esquerda
                for i in range(len(key_point)):
                    kp = detection.location_data.relative_keypoints[key_point[i]]
                    if kp is not None:
                        self.__detectors['Face']['LastCommands'][i] = (self.__res[0]-int(kp.x * self.__res[0]),kp.y * self.__res[1])
                    else:
                        self.__detectors['Face']['LastCommands'][i] = (-1, -1)
        return 0, "", self.__detectors['Face']['LastCommands']

    def __hand_detector(self,img):

        if self.__res == (0,0):
            self.__res = (img.shape[1],img.shape[0])

        # command = 0
        # landmarks = []
        # debug = ""
        
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
                        if id == hand_detector.HandLandmark.INDEX_FINGER_TIP:
                            self.__detectors['Hands']['LastCommands']['Right'] = (self.__res[0]-int(lm.x*self.__res[0]),int(lm.y*self.__res[1]))
                # LEFT HAND #
                if handedness_dict1['classification'][0]['label'] == 'Left':
                    # EACH POINTS OF THE HAND #
                    for id, lm in enumerate(handLms.landmark):
                        if id == hand_detector.HandLandmark.INDEX_FINGER_TIP:
                            self.__detectors['Hands']['LastCommands']['Left'] = (self.__res[0]-int(lm.x*self.__res[0]),int(lm.y*self.__res[1]))
        return 0,"",[self.__detectors['Hands']['LastCommands']['Left'],self.__detectors['Hands']['LastCommands']['Right']]

    def __reset_hand_detector(self):
        self.__detectors['Hands']['LastCommands']['Left']=(-1,-1)
        self.__detectors['Hands']['LastCommands']['Right']=(-1,-1)

    def __body_detector(self,img,state = 1):
        # result = 
        if self.__res == (0,0):
            self.__res = (img.shape[1],img.shape[0])

        frameCV_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.__detectors['Body']['Detector'].process(frameCV_RGB)

        if results.pose_landmarks:
            self.__detectors['Body']['Landmarks'] = results.pose_landmarks

            for landmark in self.__detectors['Body']['Landmarks'].landmark:
                landmark.x = self.__res[0] - landmark.x*self.__res[0]
                landmark.y = landmark.y*self.__res[1]
            
            if state == 0:
                command = 0b0000 # |R|L|C|J|
                ret = {}
                debug = "Controller Debug:\n"
                movR, retB = self.__detect_move_right(self.__detectors['Body']['Landmarks'].landmark)
                command = command | (0b1000 & movR << 3)
                debug += ('\t'+'Move R: ({stat})'.format(stat=movR)+'\n'+'\t\t'+retB+'\n')
                movL, retB = self.__detect_move_left(self.__detectors['Body']['Landmarks'].landmark)
                command = command | (0b0100 & movL << 2)
                debug += ('\t' +'Move L: ({stat})'.format(stat=movL)+'\n'+'\t\t'+retB+'\n')
                movC, retB = self.__detect_crouch(self.__detectors['Body']['Landmarks'].landmark)
                command = command | (0b0010 & movC << 1)
                debug += ('\t' +'Crouch: ({stat})'.format(stat=movC)+'\n'+'\t\t'+retB+'\n')

                movC, retB = self.__detect_jump(self.__detectors['Body']['Landmarks'].landmark)
                command = command | (0b0001 & movC << 0)
                debug += ('\t' +'Jump: ({stat})'.format(stat=movC)+'\n'+'\t\t'+retB+'\n')

                debug += ('\t'+"Command: {0:b}".format(command)+'\n')
                # ret['landmarks'] = self.__detectors['Body']['Landmarks'].landmark
                # ret['com'] = command
                return command, debug, self.__detectors['Body']['Landmarks'].landmark
            # elif state == 1:
            #     ret = {}
            #     mov, ret['debug'] = self.__detect_move_right(self.__detectors['Body']['Landmarks'].landmark)
            #     ret['landmarks'] = self.__detectors['Body']['Landmarks'].landmark
            #     return ret
            # elif state == 2:
            #     self.__detect_move_left(self.__detectors['Body']['Landmarks'].landmark)
            # elif state == 3:
            #     self.__detect_crouch(self.__detectors['Body']['Landmarks'].landmark)
            # elif state == 4:
            #     self.__detect_jump(self.__detectors['Body']['Landmarks'].landmark)

            return 0b0000, "", self.__detectors['Body']['Landmarks'].landmark
        else:
            return 0b0000, "", []

    def __detect_move_right(self,landmarks):
        a_list = [
            landmarks[12],  # right_shouder
            landmarks[24],  # right_hip
            landmarks[14]   # right_elbow
        ]
        if controller.__cehck_visibility(a_list, self.__move_LR_visibility_lim):
            angle = np.rad2deg(controller.__3p_angle(
                landmarks=controller.__landmarks_to_npArray(a_list)
            ))
            cond = ((angle != np.nan) and
                    (angle >= self.__move_LR_angle_lim[0]) and
                    (angle <= self.__move_LR_angle_lim[1]))
            return cond, "Angle: {ang:3.2f}".format(ang=angle)
        return False, "Distance: {dist:3.2f} | Angle: {ang:3.2f}".format(dist=-1, ang=-1)

    def __detect_move_left(self,landmarks):
        a_list = [
            landmarks[11],  # right_shouder
            landmarks[23],  # left_hip
            landmarks[13]   # left_elbow
        ]
        if controller.__cehck_visibility(a_list, self.__move_LR_visibility_lim):
            angle = np.rad2deg(controller.__3p_angle(
                landmarks=controller.__landmarks_to_npArray(a_list)
            ))
            cond = ((angle != np.nan) and
                    (angle >= self.__move_LR_angle_lim[0]) and
                    (angle <= self.__move_LR_angle_lim[1]))
            return cond, "Angle: {ang:3.2f}".format(ang=angle)
        return False, "Angle: {ang:3.2f}".format(ang=-1)

    def __detect_crouch(self,landmarks):
        a_r_list = [
            landmarks[26],  # right_knee
            landmarks[24],  # right_hip
            landmarks[28]   # right_ankle
        ]
        a_l_list = [
            landmarks[25],  # left_knee
            landmarks[23],  # left_hip
            landmarks[27]   # left_ankle
        ]
        if controller.__cehck_visibility(a_r_list, self.__crouch_visibility_lim) and (controller.__cehck_visibility(a_l_list, self.__crouch_visibility_lim)):
            angle_r = np.rad2deg(controller.__3p_angle(
                landmarks=controller.__landmarks_to_npArray(a_r_list)
            ))
            angle_l = np.rad2deg(controller.__3p_angle(
                landmarks=controller.__landmarks_to_npArray(a_l_list)
            ))
            cond = ((angle_r != np.nan) and
                    (angle_r <= self.__crouch_angle_lim) and 
                    (angle_l != np.nan) and
                    (angle_l <= self.__crouch_angle_lim))
            return cond, "AngleR: {angR:3.2f} | AngleL: {angL:3.2f}".format(angR=angle_r,angL=angle_l)
        return False, "AngleR: {angR:3.2f} | AngleL: {angL:3.2f}".format(angR=-1,angL=-1)

    def __detect_jump(self,landmarks):
        a_r_list = [
            landmarks[26],  # right_knee
            landmarks[24],  # right_hip
            landmarks[28]   # right_ankle
        ]
        a_l_list = [
            landmarks[25],  # left_knee
            landmarks[23],  # left_hip
            landmarks[27]   # left_ankle
        ]
        if controller.__cehck_visibility(a_r_list, self.__crouch_visibility_lim) and (controller.__cehck_visibility(a_l_list, self.__crouch_visibility_lim)):
            angle_r = np.rad2deg(controller.__3p_angle(
                landmarks=controller.__landmarks_to_npArray(a_r_list)
            ))
            angle_l = np.rad2deg(controller.__3p_angle(
                landmarks=controller.__landmarks_to_npArray(a_l_list)
            ))
            cond_c = ((angle_r != np.nan) and
                    (angle_r >= self.__jump_ang_lim) and
                    (angle_l != np.nan) and
                    (angle_l >= self.__jump_ang_lim))
            cond_c = True
            cond = False
            if cond_c:
                m1 = (landmarks[23].y + landmarks[24].y)/2
                self.__jump_buffer(m1)
                # print("Act: ",m1," Mean: ",sum(self.__jump_hips_pose_k)/self.__buffer_samples)
                # __jump_delta_lim
                mean = (sum(self.__jump_hips_pose_k)/self.__buffer_samples)
                delta = []
                for sample in range(self.__buffer_samples):
                    delta.append(self.__jump_hips_pose_k[sample]-self.__jump_hips_pose_km1[sample])
                cond = m1 >= mean*(1+self.__jump_pos_lim/100) and sum(delta)/self.__buffer_samples > self.__jump_delta_lim
                if cond:
                    vc = "True\nTrue\nTrue\nTrue\nTrue\nTrue\nTrue\nTrue\n\n\n\n\n\n\nTrueTrueTrueTrueTrueTrueTrueTrueTrue"
                else:
                    vc = "False"
            return cond, "AngleR: {angR:3.2f} | AngleL: {angL:3.2f} | {cond}".format(angR=angle_r, angL=angle_l, mean=mean, act=m1, cond=vc)
        return False, "AngleR: {angR:3.2f} | AngleL: {angL:3.2f}".format(angR=-1, angL=-1)
        
    # def __body_rightArm(self,landmarks):
    #     pass

    # def __body_leftArm(self,landmarks):
    #     pass

    # def __body_rightLeg(self,lanfmarks):
    #     pass

    # def __body_leftLeg(self,landmarks):
    #     pass

    def __cehck_visibility(landmarks,lim):
        for landmark in landmarks:
            if(landmark.visibility < lim):
                return False
        return True

    def __landmarks_to_npArray(landmarks):
        ret = np.zeros((len(landmarks),3))
        count = 0
        for landmark in landmarks:
            ret[count,0] = landmark.x
            ret[count,1] = landmark.y
            ret[count,2] = landmark.z
            count += 1
            # ret[count,3] = landmark.visibility
        return ret

    def __dist_plane(landmarks):
        seg1 = landmarks[0,:] - landmarks[1,:]
        seg2 = landmarks[0,:] - landmarks[2,:]
        Nvec = np.cross(seg1,seg2)
        k = 0
        for i in range(3):
            k -= landmarks[0,i]*Nvec[i]
        Num = 0
        for j in range(3):
            Num += Nvec[j]*landmarks[3,j]
        Num += k
        Den = np.sqrt(Nvec[0]**2+Nvec[1]**2+Nvec[2]**2)
        return np.abs(Num)/Den

    def __3p_angle(landmarks):
        seg1 = landmarks[0,:] - landmarks[1,:]
        seg2 = landmarks[0,:] - landmarks[2,:]
        return np.arccos(np.dot(seg1,seg2)/(np.linalg.norm(seg1)*np.linalg.norm(seg2)))

    def __jump_buffer(self,value):
        if len(self.__jump_hips_pose_km1) == 0:
            for i in range(self.__buffer_samples):
                self.__jump_hips_pose_k.append(value)
                self.__jump_hips_pose_km1.append(value)
        else:
            self.__jump_hips_pose_km1.pop(0)
            self.__jump_hips_pose_km1.append(self.__jump_hips_pose_k[0])
            self.__jump_hips_pose_k.pop(0)
            self.__jump_hips_pose_k.append(value)

        # print('K: ', self.__jump_hips_pose_k,'K-1: ', self.__jump_hips_pose_km1)
