class entity:
    def __init__(self,name=[]):
        if name == []:
            raise NameError("Invalid entity name. You must define a name for the entity!")
        self.name = name
        self.position = (-1,-1)
        self.entity_state = 0
        self.animation_state = 0

    def update(self, state=0,command=[]):
        if self.name == "Player":
            if command != [(-1,-1)]:
                com = command['com']
                moveR = (com & 0b1000) == 0b1000
                moveL = (com & 0b0100) == 0b0100
                moveC = (com & 0b0010) == 0b0010
                moveJ = (com & 0b0001) == 0b0001
                if(moveR):
                    print("Move R")
                if(moveL):
                    print("Move L")
                if(moveC):
                    print("Move C")
                if(moveJ):
                    print("Move J")
