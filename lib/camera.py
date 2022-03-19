import sys
from imutils.video import VideoStream

class camera:
    def __init__(self):
        if(len(sys.argv) > 1):
            if(sys.argv[1] == '--cam' and sys.argv[2] == '1'):
                camSrc = 'https://192.168.1.169:8080/video'
            else:
                camSrc = 0
        else:
            camSrc = 0

        self.__vid_stream = VideoStream(src=camSrc).start()

        self.__frame_count = -1
        

    def take_image(self, Sampling=1):
        if self.__frame_count-1 <= 0:
            self.last_frame = self.__vid_stream.read()
            self.__frame_count = Sampling
        self.__frame_count -= 1
        return self.last_frame
