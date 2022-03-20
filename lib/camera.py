import sys
from imutils.video import VideoStream
import cv2

class camera:
    def __init__(self):
        self.__flip = False
        if(len(sys.argv) > 1):
            if(sys.argv[1] == '--cam' and sys.argv[2] == '1'):
                camSrc = 'https://192.168.1.169:8080/video'
            elif(sys.argv[1] == '--cam' and sys.argv[2] == '2'):
                camSrc = 'https://192.168.1.156:8080/video'
                self.__flip = True
                # cv2.flip(frame, 1)
            else:
                camSrc = 0
        else:
            camSrc = 0

        self.__vid_stream = VideoStream(src=camSrc).start()

        self.__frame_count = -1
        

    def take_image(self, Sampling=1):
        if self.__frame_count-1 <= 0:
            self.last_frame = self.__vid_stream.read()
            if self.__flip:
                pass
                # self.last_frame = cv2.flip(self.last_frame, 1)
            self.__frame_count = Sampling
        self.__frame_count -= 1
        return self.last_frame
