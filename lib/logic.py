import time

class logic:
    def __init__(self):
        self.time = int(round(time.time() * 1000))

    def update(self, state=0):

        return self.__state_machine(state)

    def __state_machine(self,state):
        diff_time = int(round(time.time() * 1000)) - self.time

        if state == -9:
            if diff_time > 1000:
                self.time = int(round(time.time() * 1000))
                state = -8
        elif state == -8:
            state = -10
        
        return state