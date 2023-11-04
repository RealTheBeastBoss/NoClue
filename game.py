from card import *
from location import *
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
import os

pygame.font.init()
FPS = 60
WIDTH, HEIGHT = 1920, 1080
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
BUTTON_COOLDOWN_EVENT = pygame.USEREVENT + 1
BOARD_MATRIX = [
   # 1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 1
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],  # 2
    [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],  # 3
    [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],  # 4
    [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],  # 5
    [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],  # 6
    [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0],  # 7
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],  # 8
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],  # 9
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],  # 10
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],  # 11
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],  # 12
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],  # 13
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],  # 14
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],  # 15
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],  # 16
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],  # 17
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],  # 18
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],  # 19
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 20
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],  # 21
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],  # 22
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],  # 23
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],  # 24
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]   # 25
]
GRID = Grid(matrix=BOARD_MATRIX)
FINDER = AStarFinder()

# Game Fonts:
TINY_FONT = pygame.font.Font(os.path.join("Fonts", "beastboss_font.ttf"), 20)
SMALL_FONT = pygame.font.Font(os.path.join("Fonts", "beastboss_font.ttf"), 30)
MEDIUM_FONT = pygame.font.Font(os.path.join("Fonts", "beastboss_font.ttf"), 60)
BIG_FONT = pygame.font.Font(os.path.join("Fonts", "beastboss_font.ttf"), 90)

# Game Colours:
ORANGE = (255, 102, 0)
PINK = (230, 73, 198)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
MUSTARD = (255, 252, 71)
GREEN = (0, 169, 0)
LIGHT_BLUE = (0, 185, 227)
PURPLE = (179, 0, 255)
BLACK = (0, 0, 0)
BACKGROUND = (26, 15, 73)

class ScreenState(Enum):
    START = 1
    JOIN_NETWORK = 2
    CREATE_SERVER = 3
    NAME_PLAYER = 4
    PLAYING_GAME = 5

class TurnStage(Enum):
    START = 1
    ROLL_DICE = 2
    MOVEMENT = 3
    MAKE_GUESS = 4
    END_TURN = 5

# region
# Game Cards:
MISS_SCARLETT = GameCard(CardType.SUSPECT, "Miss Scarlett")
COL_MUSTARD = GameCard(CardType.SUSPECT, "Col. Mustard")
DR_ORCHID = GameCard(CardType.SUSPECT, "Dr Orchid")
REV_GREEN = GameCard(CardType.SUSPECT, "Rev. Green")
MRS_PEACOCK = GameCard(CardType.SUSPECT, "Mrs Peacock")
PROF_PLUM = GameCard(CardType.SUSPECT, "Professor Plum")
CANDLESTICK = GameCard(CardType.WEAPON, "Candlestick")
DAGGER = GameCard(CardType.WEAPON, "Dagger")
LEAD_PIPE = GameCard(CardType.WEAPON, "Lead Pipe")
REVOLVER = GameCard(CardType.WEAPON, "Revolver")
ROPE = GameCard(CardType.WEAPON, "Rope")
WRENCH = GameCard(CardType.WEAPON, "Wrench")
BALLROOM_CARD = GameCard(CardType.LOCATION, "Ballroom")
BILLIARD_ROOM_CARD = GameCard(CardType.LOCATION, "Billiard Room")
CONSERVATORY_CARD = GameCard(CardType.LOCATION, "Conservatory")
DINING_ROOM_CARD = GameCard(CardType.LOCATION, "Dining Room")
HALL_CARD = GameCard(CardType.LOCATION, "Hall")
KITCHEN_CARD = GameCard(CardType.LOCATION, "Kitchen")
LIBRARY_CARD = GameCard(CardType.LOCATION, "Library")
LOUNGE_CARD = GameCard(CardType.LOCATION, "Lounge")
STUDY_CARD = GameCard(CardType.LOCATION, "Study")
GAME_CARDS = [MISS_SCARLETT, COL_MUSTARD, DR_ORCHID, REV_GREEN, MRS_PEACOCK, PROF_PLUM, CANDLESTICK, DAGGER, LEAD_PIPE, REVOLVER, ROPE, WRENCH, BALLROOM_CARD, BILLIARD_ROOM_CARD, CONSERVATORY_CARD, DINING_ROOM_CARD,
              HALL_CARD, KITCHEN_CARD, LIBRARY_CARD, LOUNGE_CARD, STUDY_CARD]

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

# Squares:
ORCHID_START = Square(9, 0)
GREEN_START = Square(14, 0)
PEACOCK_START = Square(23, 7)
MUSTARD_START = Square(0, 17)
PLUM_START = Square(23, 19)
SCARLETT_START = Square(7, 24)
BALLROOM_SQUARE1 = Square(7, 5)
BALLROOM_SQUARE2 = Square(16, 5)
BALLROOM_SQUARE3 = Square(9, 8)
BALLROOM_SQUARE4 = Square(14, 8)
CONSERVATORY_SQUARE = Square(18, 6)
BILLIARD_SQUARE1 = Square(17, 9)
BILLIARD_SQUARE2 = Square(22, 13)
LIBRARY_SQUARE1 = Square(20, 13)
LIBRARY_SQUARE2 = Square(16, 16)
STUDY_SQUARE = Square(17, 20)
HALL_SQUARE1 = Square(11, 17)
HALL_SQUARE2 = Square(12, 17)
LOUNGE_SQUARE = Square(6, 18)
DINING_SQUARE1 = Square(8, 12)
DINING_SQUARE2 = Square(6, 16)
KITCHEN_SQUARE = Square(4, 7)
SQUARES = [ORCHID_START, GREEN_START, PEACOCK_START, MUSTARD_START, PLUM_START, SCARLETT_START, Square(7, 1), Square(8, 1), Square(9, 1), Square(14, 1), Square(15, 1), Square(16, 1), Square(6, 2), Square(7, 2),
           Square(16, 2), Square(17, 2), Square(6, 3), Square(7, 3), Square(16, 3), Square(17, 3), Square(6, 4), Square(7, 4), Square(16, 4), Square(17, 4),
           Square(6, 5), Square(17, 5), Square(6, 6), Square(7, 6), Square(16, 6), Square(17, 6), Square(19, 6),
           Square(20, 6), Square(21, 6), Square(22, 6), Square(0, 7), Square(1, 7), Square(2, 7), Square(3, 7), Square(5, 7), Square(6, 7),
           Square(7, 7), Square(16, 7), Square(17, 7), Square(18, 7), Square(19, 7), Square(20, 7), Square(21, 7), Square(22, 7), Square(1, 8), Square(2, 8),
           Square(3, 8), Square(4, 8), Square(5, 8), Square(6, 8), Square(7, 8), Square(8, 8), Square(10, 8), Square(11, 8), Square(12, 8),
           Square(13, 8), Square(15, 8), Square(16, 8), Square(17, 8), Square(5, 9), Square(6, 9), Square(7, 9), Square(8, 9), Square(9, 9),
           Square(10, 9), Square(11, 9), Square(12, 9), Square(13, 9), Square(14, 9), Square(15, 9), Square(16, 9), Square(8, 10),
           Square(9, 10), Square(15, 10), Square(16, 10), Square(17, 10), Square(8, 11), Square(9, 11), Square(15, 11), Square(16, 11), Square(17, 11),
           Square(9, 12), Square(15, 12), Square(16, 12), Square(17, 12), Square(8, 13), Square(9, 13), Square(15, 13), Square(16, 13),
           Square(17, 13), Square(18, 13), Square(19, 13), Square(21, 13), Square(8, 14), Square(9, 14), Square(15, 14),
           Square(16, 14), Square(17, 14), Square(8, 15), Square(9, 15), Square(15, 15), Square(16, 15), Square(1, 16), Square(2, 16), Square(3, 16),
           Square(4, 16), Square(5, 16), Square(7, 16), Square(8, 16), Square(9, 16), Square(15, 16),
           Square(1, 17), Square(2, 17), Square(3, 17), Square(4, 17), Square(5, 17), Square(6, 17), Square(7, 17), Square(8, 17), Square(9, 17),
           Square(10, 17), Square(13, 17), Square(14, 17), Square(15, 17), Square(16, 17), Square(1, 18), Square(2, 18),
           Square(3, 18), Square(4, 18), Square(5, 18), Square(7, 18), Square(8, 18), Square(15, 18), Square(16, 18), Square(17, 18),
           Square(7, 19), Square(8, 19), Square(15, 19), Square(16, 19), Square(17, 19), Square(18, 19), Square(19, 19), Square(20, 19), Square(21, 19),
           Square(22, 19), Square(7, 20), Square(8, 20), Square(15, 20), Square(16, 20), Square(18, 20), Square(19, 20),
           Square(20, 20), Square(21, 20), Square(22, 20), Square(7, 21), Square(8, 21), Square(15, 21), Square(16, 21), Square(7, 22), Square(8, 22),
           Square(15, 22), Square(16, 22), Square(7, 23), Square(8, 23), Square(15, 23), Square(16, 23), Square(16, 24), BALLROOM_SQUARE1, BALLROOM_SQUARE2, BALLROOM_SQUARE3,
           BALLROOM_SQUARE4, CONSERVATORY_SQUARE, BILLIARD_SQUARE1, BILLIARD_SQUARE2, LIBRARY_SQUARE1, LIBRARY_SQUARE2, STUDY_SQUARE, HALL_SQUARE1, HALL_SQUARE2, LOUNGE_SQUARE, DINING_SQUARE1, DINING_SQUARE2, KITCHEN_SQUARE]

# Locations:
BALLROOM = Location("Ballroom", (570, 196), [BALLROOM_SQUARE1, BALLROOM_SQUARE2, BALLROOM_SQUARE3, BALLROOM_SQUARE4], (485, 46), (655, 46), (655, 89), (741, 89), (741, 345), (399, 345), (399, 89), (485, 89), (485, 46))
CONSERVATORY = Location("Conservatory", (957, 153), [CONSERVATORY_SQUARE], (829, 46), (1085, 46), (1085, 216), (1042, 216), (1042, 259), (829, 259), (829, 46))
BILLIARD_ROOM = Location("Billiard Room", (957, 454), [BILLIARD_SQUARE1, BILLIARD_SQUARE2], (829, 347), (1085, 347), (1085, 560), (829, 560), (829, 347))
LIBRARY = Location("Library", (936, 712), [LIBRARY_SQUARE1, LIBRARY_SQUARE2], (829, 605), (1042, 605), (1042, 648), (1085, 648), (1085, 775), (1042, 775), (1042, 818), (829, 818), (829, 775), (786, 775), (786, 648), (829, 648), (829, 605))
STUDY = Location("Study", (936, 991), [STUDY_SQUARE], (786, 906), (1085, 906), (1085, 1077), (829, 1077), (829, 1033), (786, 1033), (786, 906))
HALL = Location("Hall", (570, 927), [HALL_SQUARE1, HALL_SQUARE2], (442, 777), (698, 777), (698, 1077), (442, 1076), (442, 777))
LOUNGE = Location("Lounge", (205, 948), [LOUNGE_SQUARE], (55, 820), (354, 820), (354, 1034), (312, 1034), (312, 1077), (55, 1077), (55, 820))
DINING_ROOM = Location("Dining Room", (226, 539), [DINING_SQUARE1, DINING_SQUARE2], (55, 390), (268, 390), (268, 433), (397, 433), (397, 689), (55, 689), (55, 390))
KITCHEN = Location("Kitchen", (183, 174), [KITCHEN_SQUARE], (55, 46), (311, 46), (311, 302), (98, 302), (98, 259), (55, 259), (55, 46))
# endregion

class Game:
    NETWORK = None
    HAS_SERVER = False
    PLAYER_COUNT = 69
    CLIENT_NUMBER = 69
    CLUE_CARDS_ACTIVE = True
    SCREEN_STATE = ScreenState.START
    TURN_STAGE = TurnStage.START
    USER_TEXT = ""
    CAN_INPUT_TEXT = False
    PLAYERS = None
    CURRENT_PLAYER = 0
    CLUE_SHEET = None
    CLUE_SHEET_OPEN = False
    FAILED_SELECTION = False
    HAS_DIED = False
    SELECTED_PLACE = None
    SQUARE_FAIL_DISTANCE = 0
    CARD_NAMES = []
    LOCATIONS = [BALLROOM, CONSERVATORY, BILLIARD_ROOM, LIBRARY, STUDY, HALL, LOUNGE, DINING_ROOM, KITCHEN]
    CLUE_CARD_DECK = [SHOW_SCARLETT, SHOW_MUSTARD, SHOW_ORCHID, SHOW_GREEN, SHOW_PEACOCK, SHOW_PLUM, SHOW_CANDLESTICK, SHOW_DAGGER, SHOW_LEAD_PIPE, SHOW_REVOLVER, SHOW_ROPE, SHOW_WRENCH, SHOW_BALLROOM, SHOW_BILLIARD,
                      SHOW_CONSERVATORY, SHOW_DINING, SHOW_HALL, SHOW_KITCHEN, SHOW_LIBRARY, SHOW_LOUNGE, SHOW_STUDY, CHOOSE_PLAYER_REVEAL, CHOOSE_SUSPECT_REVEAL, CHOOSE_WEAPON_REVEAL, CHOOSE_LOCATION_REVEAL,
                      SECRET_PASSAGE, ROOM_CHOICE, ALL_REVEAL, SHOW_LEFT]
    # Events:
    BUTTONS_ENABLED = True
    LEFT_MOUSE_RELEASED = False
    ENTER_PRESSED = False

# Misc:
DICE_ONE = pygame.image.load(os.path.join("Assets", "dice_one.png"))
DICE_TWO = pygame.image.load(os.path.join("Assets", "dice_two.png"))
DICE_THREE = pygame.image.load(os.path.join("Assets", "dice_three.png"))
DICE_FOUR = pygame.image.load(os.path.join("Assets", "dice_four.png"))
DICE_FIVE = pygame.image.load(os.path.join("Assets", "dice_five.png"))
DICE_SIX = pygame.image.load(os.path.join("Assets", "dice_six.png"))
DICE_CLUE = pygame.image.load(os.path.join("Assets", "dice_clue.png"))

PLAYER_TO_COLOUR = {
    0: RED,
    1: MUSTARD,
    2: PINK,
    3: GREEN,
    4: LIGHT_BLUE,
    5: PURPLE,
}
ALLOWED_KEYS = [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_a, pygame.K_b,
                pygame.K_c, pygame.K_d, pygame.K_e, pygame.K_f, pygame.K_g, pygame.K_h, pygame.K_i, pygame.K_j, pygame.K_k, pygame.K_l, pygame.K_m, pygame.K_n,
                pygame.K_o, pygame.K_p, pygame.K_q, pygame.K_r, pygame.K_s, pygame.K_t, pygame.K_u, pygame.K_v, pygame.K_w, pygame.K_x, pygame.K_y, pygame.K_z,
                pygame.K_BACKSLASH, pygame.K_BACKSPACE, pygame.K_COMMA, pygame.K_SPACE, pygame.K_RETURN, pygame.K_PERIOD]