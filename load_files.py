import pygame
from pygame import *
import pyautogui


Screen_Width, Screen_Height = pyautogui.size()
pygame.init()
window = pygame.display.set_mode((Screen_Width, Screen_Height))
#Load das Imagens Bonus
# Bónus Aéreos e Terrestres
Coin = pygame.image.load("Sprite/Bonus/Coin.png").convert_alpha()
RedCoin = pygame.image.load("Sprite/Bonus/RedCoin.png").convert_alpha()
BlueCoin = pygame.image.load("Sprite/Bonus/BlueCoin.png").convert_alpha()
PurpleCoin = pygame.image.load("Sprite/Bonus/PurpleCoin.png").convert_alpha()
GreenCoin = pygame.image.load("Sprite/Bonus/GreenCoin.png").convert_alpha()

BigPrincessCoin = pygame.image.load("Sprite/Bonus/BigPrincessCoin.png").convert_alpha()
BigYoshiCoin = pygame.image.load("Sprite/Bonus/BigYoshiCoin.png").convert_alpha()
BigACoin = pygame.image.load("Sprite/Bonus/BigACoin.png").convert_alpha()

PinkApple = pygame.image.load("Sprite/Bonus/PinkApple.png").convert_alpha()
PurpleApple = pygame.image.load("Sprite/Bonus/PurpleApple.png").convert_alpha()
RedApple = pygame.image.load("Sprite/Bonus/RedApple.png").convert_alpha()
YellowApple = pygame.image.load("Sprite/Bonus/YellowApple.png").convert_alpha()


Star = pygame.image.load("Sprite/Bonus/Star.png").convert_alpha()
RedStar = pygame.image.load("Sprite/Bonus/RedStar.png").convert_alpha()
BlackStar = pygame.image.load("Sprite/Bonus/BlackStar.png").convert_alpha()
GreenStar = pygame.image.load("Sprite/Bonus/GreenStar.png").convert_alpha()
PurpleStar = pygame.image.load("Sprite/Bonus/PurpleStar.png").convert_alpha()
MoonBonus = pygame.image.load("Sprite/Bonus/MoonBonus.png").convert_alpha()

# Bónus Terrestres
RedMushroom = pygame.image.load("Sprite/Bonus/RedMushroom.png").convert_alpha()
ExtendedMushroom = pygame.image.load("Sprite/Bonus/ExtendedMushroom.png").convert_alpha()
BlueMushroom = pygame.image.load("Sprite/Bonus/BlueMushroom.png").convert_alpha()
PurpleMushroom = pygame.image.load("Sprite/Bonus/PurpleMushroom.png").convert_alpha()

YellowFlowerBonus = pygame.image.load("Sprite/Bonus/YellowFlowerBonus.png").convert_alpha()
Red_YellowFlowerBonus = pygame.image.load("Sprite/Bonus/Red_YellowFlowerBonus.png").convert_alpha()
BlueFlowerBonus = pygame.image.load("Sprite/Bonus/BlueFowerBonus.png").convert_alpha()
HappyBonusPlant = pygame.image.load("Sprite/Bonus/HappyBonusPlant.png").convert_alpha()


#Load das Imagens Enemies
FatTurtle = pygame.image.load("Sprite/Enemies/FatTurtle.png")
Gumba = pygame.image.load("Sprite/Enemies/Gumba.png")
LeftBullet = pygame.image.load("Sprite/Enemies/LeftBullet.png")
RedGhost = pygame.image.load("Sprite/Enemies/RedGhost.png")
RedTurtleSpikes = pygame.image.load("Sprite/Enemies/RedTurtleSpikes.png")
Animal = pygame.image.load("Sprite/Enemies/Animal.png")
BlackFlower = pygame.image.load("Sprite/Enemies/BlueSpikeTurtle.png")
FlowerLeftObstacle = pygame.image.load("Sprite/Enemies/FlowerLeftObstacle.png")
ScaredRedFish = pygame.image.load("Sprite/Enemies/ScaredRedFish.png")
SmallBowser = pygame.image.load("Sprite/Enemies/SmallBowser.png")
SurprisedFish = pygame.image.load("Sprite/Enemies/SurprisedFish.png")
TurtleGhost = pygame.image.load("Sprite/Enemies/TurtleGhost.png")
TurtleShell = pygame.image.load("Sprite/Enemies/TurtleShell.png")
TurtleWithSpike = pygame.image.load("Sprite/Enemies/TurtleWithSpike.png")

#Load Obstacles
FirePipe = pygame.image.load("Sprite/Obstacle/FirePipe.png")
DarkFirePipe = pygame.image.load("Sprite/Obstacle/DarkFirePipe.png")
Vine = pygame.image.load("Sprite/Obstacle/Vine.png")

run_string = ["Sprite/Mario/WalkingArmsUp.png", "Sprite/Mario/StandingArmsUp.png"]
jump_string = ["Sprite/Mario/JumpVictorius.png", "Sprite/Mario/JumpVictorius.png",
                   "Sprite/Mario/JumpVictorius.png", "Sprite/Mario/JumpVictorius.png",
                   "Sprite/Mario/JumpingArmsUp.png", "Sprite/Mario/JumpingArmsUp.png",
                   "Sprite/Mario/JumpingArmsUp.png", "Sprite/Mario/JumpingArmsUp.png"]
duck_string = ["Sprite/Mario/Duck.png", "Sprite/Mario/Duck.png", "Sprite/Mario/Duck.png",
                   "Sprite/Mario/Duck.png", "Sprite/Mario/Duck.png", "Sprite/Mario/Duck.png",
                   "Sprite/Mario/Duck.png", "Sprite/Mario/Duck.png", "Sprite/Mario/Duck.png",
                   "Sprite/Mario/Duck.png", "Sprite/Mario/Duck.png"]
fall_string = ["Sprite/Mario/Scared.png"]
scale = [12, 12]

font = pygame.font.Font("resources/SuperMario256.ttf", 64)