import pygame
class image():
    def __init__(self, string,  window, size=[], position = []):
        self.load(string)
        self.window = window
        if size != []:
            self.resize(size)
        if position != []:
            self.position(position)
        pass
    def load(self, string):
        self.image = pygame.image.load(string).convert_alpha()
        self.rect = self.image.get_rect()
        return self
    def resize(self, size):
        self.image = pygame.transform.scale(self.image, size)
        return self
    def position(self, translation):
        self.rect.x = self.window.get_width()/2 - translation[0]*self.image.get_width()/2
        self.rect.y = self.window.get_height()/2 - translation[1]*self.image.get_height()/2
        return self.rect
    def get_rect(self):
        return self.rect
    def get_width(self):
        return self.image.get_width()
    def get_height(self):
        return self.image.get_height()
    def display(self, position = []):
        if position == []:
            position = self.rect
        self.window.blit(self.image, position)
    def collide(self, point):
        return self.get_rect().collidepoint(point)

class gif(pygame.sprite.Sprite):
    # Used to animate gif
    def __init__(self, position, size, foldername, window, limit):
        super(gif, self).__init__()
        self.images= self.load(limit, foldername, window, size, position)

        # self.rect = self.images[1].get_rect()
        self.index = 0
        self.image = self.images[self.index]
        self.window = window
        self.animation_frames = 6
        self.current_frame = 0

        self.sprites = pygame.sprite.Group(self)

    def update(self):
        self.current_frame += 2
        if self.current_frame >= self.animation_frames:
            self.current_frame = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]
    def load(self, limit, foldername, window, size, position):
        sprites = []
        for item in range(1, limit):
            img = image("Images/"+ foldername+"/"+foldername+".{:03}".format(item) + ".png", window, size, position)
            sprites.append(img.image)
        self.rect = img.get_rect()
        return sprites
    def draw(self):
        self.sprites.update()
        self.sprites.draw(self.window)