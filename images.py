from matplotlib import image
import pygame
import game


def load_image(file_name, img_size, translation, resize=1):
    image = pygame.image.load(file_name).convert_alpha()
    if resize:
        image = pygame.transform.scale(image, (img_size[0], img_size[1]))
    image_pos = image.get_rect()
    image_pos.x = game.Screen_Width / 2 - translation[0] * img_size[0] / 2
    image_pos.y = game.Screen_Height / 2 - translation[1] * img_size[1] / 2
    return image, image_pos

def load_gif(folder_name, direction, img_size, translation):
    # Used to load multiple images from folder and store them in the variable "gif"
    gif = []
    if(folder_name == "Image_Menu"):
        for item in range(1,49):
            if(item < 10):
                squat_img = pygame.image.load("Images/" + folder_name + "/Image_"+str(direction)+".00"+str(item)+".png").convert_alpha()
            else:
                squat_img = pygame.image.load("Images/"+folder_name+"/Image_"+str(direction)+".0"+str(item)+".png").convert_alpha()
            squat_img = pygame.transform.scale(squat_img, (img_size[0], img_size[1]))
            gif.append(squat_img)
        image_pos = squat_img.get_rect()
        image_pos.x = game.Screen_Width / 2 - translation[0] * img_size[0] / 2
        image_pos.y = game.Screen_Height / 2 - translation[1] * img_size[1] / 2
    elif (folder_name == "Image_right" or folder_name == "Image_left"):
        for item in range(1,23):
            if(item < 10):
                squat_img = pygame.image.load("Images/" + folder_name + "/Image_"+str(direction)+".00"+str(item)+".png").convert_alpha()
            else:
                squat_img = pygame.image.load("Images/"+folder_name+"/Image_"+str(direction)+".0"+str(item)+".png").convert_alpha()
            squat_img = pygame.transform.scale(squat_img, (img_size[0], img_size[1]))
            gif.append(squat_img)
        image_pos = squat_img.get_rect()
        image_pos.x = game.Screen_Width / 2 - translation[0] * img_size[0] / 2
        image_pos.y = game.Screen_Height / 2 - translation[1] * img_size[1] / 2
    elif (folder_name == "Image_jumpduck"):
        for item in range(1,17):
            if(item < 10):
                squat_img = pygame.image.load("Images/" + folder_name + "/Image_"+str(direction)+".00"+str(item)+".png").convert_alpha()
            else:
                squat_img = pygame.image.load("Images/"+folder_name+"/Image_"+str(direction)+".0"+str(item)+".png").convert_alpha()
            squat_img = pygame.transform.scale(squat_img, (img_size[0], img_size[1]))
            gif.append(squat_img)
        image_pos = squat_img.get_rect()
        image_pos.x = game.Screen_Width / 2 - translation[0] * img_size[0] / 2
        image_pos.y = game.Screen_Height / 2 - translation[1] * img_size[1] / 2

    sprite_ = squatGif(position=(image_pos.x, image_pos.y), imgs=gif)
    sprites = pygame.sprite.Group(sprite_)

    return sprites 

class squatGif(pygame.sprite.Sprite):
    # Used to animate gif
    def __init__(self, position, imgs):
        super(squatGif, self).__init__()
        size = (50,30)
        self.rect = pygame.Rect(position, size)
        self.index = 0
        self.images= imgs
        self.image = imgs[self.index]

        self.animation_frames = 6
        self.current_frame = 0

    def update(self):
        self.current_frame += 2
        if self.current_frame >= self.animation_frames:
            self.current_frame = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]
