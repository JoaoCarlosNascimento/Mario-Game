import time

class logic:
    def __init__(self):
        self.time = int(round(time.time() * 1000))
        self.counter = 3
    def update(self, state=0, feedback = []):

        return self.__state_machine(state, feedback)

    def __state_machine(self, state, feedback):
        diff_time = int(round(time.time() * 1000)) - self.time
        if state == "menu":
            if feedback != None:
                if "play" in feedback:
                    state = "game"
                elif "ctrl" in feedback:
                    state = "control"
        elif state == "control":
            if feedback != None:
                if "back" in feedback:
                    state = "menu"
        elif state == "game":
            if feedback != None:
                if "dead" in feedback:
                    state = "game over"
        elif state == "game over":
            if diff_time > 1000:
                self.time = int(round(time.time() * 1000))
                state = "save score?"
        
        elif state == "save score?":
            if diff_time > 100:
                self.time = int(round(time.time() * 1000))
                if feedback != None:
                    if "yes score" in feedback:
                        state = "prepare pic"
                    elif "no score" in feedback:
                        state = "leaderboard" 

        elif state == "prepare pic":
            if feedback!= None:
                if diff_time > 1000 and ("ok pic" in feedback):
                    self.time = int(round(time.time() * 1000))
                    state = "pic"
        
        elif state == "pic":
            state = "leaderboard"

        elif state == "leaderboard":
            if diff_time > 2000:
                self.time = int(round(time.time() * 1000))
                state = "game over"
        
        return state
