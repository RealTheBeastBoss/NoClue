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
BIG_FONT = pygame.font.Font(os.path.join("Fonts", "beastboss_font.ttf"), 90)

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
PROF_PLUM = GameCard(CardType.SUSPECT, "Professor Plum", "prof_plum.png")

# Clue Cards:
SHOW_DINING = ClueCard("Where?", "Anyone holding the Dining Room card must reveal it!", "Dinner is served.")
SHOW_MUSTARD = ClueCard("What Happened?", "Anyone holding the Col. Mustard card must reveal it!", "That's curious, Colonel Mustard is limping.")
CHOOSE_PLAYER_REVEAL = ClueCard("Under Pressure!", "Choose the guiltiest-looking player to reveal one card from their hand.")
SHOW_HALL = ClueCard("Where?", "Anyone holding the Hall card must reveal it!", "There's a heavy knock at the front door.")
CHOOSE_WEAPON_REVEAL = ClueCard("Look What I Found!", "Name one weapon you want to be revealed.", "It couldn't possibly be...")
SHOW_CANDLESTICK = ClueCard("What Was That?", "Anyone holding the Candlestick card must reveal it!", "Oh no, the electricity has gone again.")
SHOW_GREEN = ClueCard("What Happened?", "Anyone holding the Rev. Green card must reveal it!", "How odd, Reverend Green is sitting alone and in silence.")
SHOW_KITCHEN = ClueCard("Where?", "Anyone holding the Kitchen card must reveal it!", "The oven timer goes off!")
SHOW_ROPE = ClueCard("What Was That?", "Anyone holding the Rope card must reveal it!", "Someone's alibi is beginning to fray at the ends.")
SECRET_PASSAGE = ClueCard("Creeeeak!", "Make any room, that room connects to all secret passages.", "Find a secret passage.")
SHOW_LEFT = ClueCard("You Don't Say!", "All players show one card to the next player.", "There's always time for a good gossip.")
SHOW_LEAD_PIPE = ClueCard("What Was That?", "Anyone holding the Lead Pipe card must reveal it!", "It's become a real weight in your pocket.")
SHOW_DAGGER = ClueCard("What Was That?", "Anyone holding the Dagger card must reveal it!", "We need to sharpen our investigating skills.")
CHOOSE_SUSPECT_REVEAL = ClueCard("Airtight Alibi!", "Name one suspect you want revealed.", "It couldn't possibly be...")
SHOW_BALLROOM = ClueCard("Where?", "Anyone holding the Ballroom card must reveal it!", "A waltz starts echoing around Tudor Mansion.")
SHOW_LOUNGE = ClueCard("Where?", "Anyone holding the Lounge card must reveal it!", "This is no time to relax!")
SHOW_WRENCH = ClueCard("What Was That?", "Anyone holding the Wrench card must reveal it!", "We will get to the truth!")
SHOW_SCARLETT = ClueCard("What Happened?", "Anyone holding the Miss Scarlett card must reveal it!", "Hold on, that's a scratch on Miss Scarlett's cheek.")
SHOW_CONSERVATORY = ClueCard("Where?", "Anyone holding the Conservatory card must reveal it!", "These plants really do need some water.")
ROOM_CHOICE = ClueCard("Screeeeam!", "All players rush to the room of their choice.")
SHOW_BILLIARD = ClueCard("Where?", "Anyone holding the Billiard Room card must reveal it!", "That's your cue!")
SHOW_LIBRARY = ClueCard("Where?", "Anyone holding the Library card must reveal it!", "There's only one place that book could have come from.")
ALL_REVEAL = ClueCard("Dun-Dun-Duuun!", "All players reveal one card from their hand.")
SHOW_STUDY = ClueCard("Where?", "Anyone holding the Study card must reveal it!", "The telephone jangles everybody's nerves.")
SHOW_REVOLVER = ClueCard("What Was That?", "Anyone holding the Revolver card must reveal it!", "We must trigger a reaction.")
CHOOSE_LOCATION_REVEAL = ClueCard("Wink Wink!", "Name one location you want revealed.", "It couldn't possibly be...")
SHOW_PEACOCK = ClueCard("What Happened?", "Anyone holding the Mrs Peacock card must reveal it!", "Wait a minute, Mrs Peacock was last seen with Black.")
SHOW_ORCHID = ClueCard("What Happened?", "Anyone holding the Doctor Orchid card must reveal it!", "Hmmm, Doctor Orchid has a bandage on her hand.")
SHOW_PLUM = ClueCard("What Happened?", "Anyone holding the Prof. Plum card must reveal it!", "Look, the arm of Professor Plum's glasses has been hastily fixed with tape")

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