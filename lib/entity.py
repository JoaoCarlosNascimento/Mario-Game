class entity:
    def __init__(self,name=[]):
        if name == []:
            raise NameError("Invalid entity name. You must define a name for the entity!")
        self.name = name
        self.position = (-1,-1)
        self.entity_state = 0
        self.animation_state = 0

    def update(self, state=0,command=[]):
        pass