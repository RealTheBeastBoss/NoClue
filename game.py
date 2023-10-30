import pygame
from card import *

pygame.font.init()
FPS = 60
WIDTH, HEIGHT = 1920, 1080
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
BUTTON_COOLDOWN_EVENT = pygame.USEREVENT + 1

# Game Fonts:
SMALL_FONT = pygame.font.Font(os.path.join("Fonts", "beastboss_font.ttf"), 30)
MEDIUM_FONT = pygame.font.Font(os.path.join("Fonts", "beastboss_font.ttf"), 60)

# Game Colours:
ORANGE = (255, 102, 0)
BACKGROUND = (26, 15, 73)

class ScreenState(Enum):
    START = 1
    JOIN_NETWORK = 2
    CREATE_SERVER = 3
    NAME_PLAYER = 4
    PLAYING_GAME = 5

class Game:
    NETWORK = None
    HAS_SERVER = False
    PLAYER_COUNT = 69
    CLIENT_NUMBER = 69
    CLUE_CARDS_ACTIVE = True
    SCREEN_STATE = ScreenState.START
    USER_TEXT = ""
    CAN_INPUT_TEXT = False
    PLAYERS = None
    CLUE_SHEET = None
    # Events:
    BUTTONS_ENABLED = True
    LEFT_MOUSE_RELEASED = False
    ENTER_PRESSED = False

# Game Cards:
PROF_PLUM = Card(CardType.SUSPECT, "Professor Plum", "prof_plum.png")

# Misc:
PLAYER_TO_COLOUR = {
    0: ORANGE,
    1: ORANGE,
    2: ORANGE,
    3: ORANGE,
    4: ORANGE,
    5: ORANGE,
}
ALLOWED_KEYS = [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_a, pygame.K_b,
                pygame.K_c, pygame.K_d, pygame.K_e, pygame.K_f, pygame.K_g, pygame.K_h, pygame.K_i, pygame.K_j, pygame.K_k, pygame.K_l, pygame.K_m, pygame.K_n,
                pygame.K_o, pygame.K_p, pygame.K_q, pygame.K_r, pygame.K_s, pygame.K_t, pygame.K_u, pygame.K_v, pygame.K_w, pygame.K_x, pygame.K_y, pygame.K_z,
                pygame.K_BACKSLASH, pygame.K_BACKSPACE, pygame.K_COMMA, pygame.K_QUESTION, pygame.K_SPACE, pygame.K_RETURN, pygame.K_PERIOD]