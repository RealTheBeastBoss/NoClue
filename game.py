import pygame
from card import *

pygame.font.init()
FPS = 60
WIDTH, HEIGHT = 1280, 720
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
BUTTON_COOLDOWN_EVENT = pygame.USEREVENT + 1

# Game Fonts:
SMALL_FONT = pygame.font.Font(os.path.join("Fonts", "beastboss_font.ttf"), 30)

# Game Colours:
BLUE = (0, 0, 255)
ORANGE = (255, 102, 0)
BACKGROUND = (26, 15, 73)

# Game Cards:
PROF_PLUM = Card(CardType.SUSPECT, "Professor Plum", "prof_plum.png")

class ScreenState(Enum):
    START = 1

class Game:
    NETWORK = None
    HAS_SERVER = False
    GAME_STATE = ScreenState.START
    # Events:
    BUTTONS_ENABLED = True
    LEFT_MOUSE_RELEASED = False
