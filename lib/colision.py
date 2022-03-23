class colision:
    # Types
    #   Enemy
    #   Solid Right
    #   Solid Left
    #   Solid Up
    #   Solid Down

    def __init__(self,entity1,entity2):
        self.type = "Solid Down"
        self.entity1 = entity1
        self.entity2 = entity2