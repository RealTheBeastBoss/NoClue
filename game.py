from card import *
from location import *
from pathfinding.core.grid import Grid
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

# Game Fonts:
TINY_FONT = pygame.font.Font(os.path.join("Fonts", "beastboss_font.ttf"), 20)
SMALL_FONT = pygame.font.Font(os.path.join("Fonts", "beastboss_font.ttf"), 30)
MEDIUM_FONT = pygame.font.Font(os.path.join("Fonts", "beastboss_font.ttf"), 60)
BIG_FONT = pygame.font.Font(os.path.join("Fonts", "beastboss_font.ttf"), 90)

def get_wrapped_text(text, font, max_width):
    text_lines = []
    word_list = []
    for word in text.split():
        word_list.append(word)
        test_text = ""
        for x in range(len(word_list)):
            test_text += word_list[x]
            if x != len(word_list) - 1:
                test_text += " "
        width = font.size(test_text)[0]
        if width > max_width:
            next_word = word_list.pop()
            test_text = ""
            for x in range(len(word_list)):
                test_text += word_list[x]
                if x != len(word_list) - 1:
                    test_text += " "
            text_lines.append(test_text)
            word_list.clear()
            word_list.append(next_word)
    if len(word_list) > 0:
        test_text = ""
        for x in range(len(word_list)):
            test_text += word_list[x]
            if x != len(word_list) - 1:
                test_text += " "
        text_lines.append(test_text)
    return text_lines

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
    DRAW_CLUE_CARD = 3
    USE_CLUE_CARD = 4
    MOVEMENT = 5
    MAKE_GUESS = 6
    END_TURN = 7

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
SHOW_DINING = ClueCard("Where?", get_wrapped_text("Anyone holding the Dining Room card must reveal it!", TINY_FONT, 280), get_wrapped_text("Dinner is served.", TINY_FONT, 280))
SHOW_MUSTARD = ClueCard("What Happened?", get_wrapped_text("Anyone holding the Col. Mustard card must reveal it!", TINY_FONT, 280), get_wrapped_text("That's curious, Colonel Mustard is limping.", TINY_FONT, 280))
CHOOSE_PLAYER_REVEAL = ClueCard("Under Pressure!", get_wrapped_text("Choose the guiltiest-looking player to reveal one card from their hand.", TINY_FONT, 280))
SHOW_HALL = ClueCard("Where?", get_wrapped_text("Anyone holding the Hall card must reveal it!", TINY_FONT, 280), get_wrapped_text("There's a heavy knock at the front door.", TINY_FONT, 280))
CHOOSE_WEAPON_REVEAL = ClueCard("Look What I Found!", get_wrapped_text("Name one weapon you want to be revealed.", TINY_FONT, 280), get_wrapped_text("It couldn't possibly be...", TINY_FONT, 280))
SHOW_CANDLESTICK = ClueCard("What Was That?", get_wrapped_text("Anyone holding the Candlestick card must reveal it!", TINY_FONT, 280), get_wrapped_text("Oh no, the electricity has gone again.", TINY_FONT, 280))
SHOW_GREEN = ClueCard("What Happened?", get_wrapped_text("Anyone holding the Rev. Green card must reveal it!", TINY_FONT, 280), get_wrapped_text("How odd, Reverend Green is sitting alone and in silence.", TINY_FONT, 280))
SHOW_KITCHEN = ClueCard("Where?", get_wrapped_text("Anyone holding the Kitchen card must reveal it!", TINY_FONT, 280), get_wrapped_text("The oven timer goes off!", TINY_FONT, 280))
SHOW_ROPE = ClueCard("What Was That?", get_wrapped_text("Anyone holding the Rope card must reveal it!", TINY_FONT, 280), get_wrapped_text("Someone's alibi is beginning to fray at the ends.", TINY_FONT, 280))
SECRET_PASSAGE = ClueCard("Creeeeak!", get_wrapped_text("Make any room, that room connects to all secret passages.", TINY_FONT, 280), get_wrapped_text("Find a secret passage.", TINY_FONT, 280))
SHOW_LEFT = ClueCard("You Don't Say!", get_wrapped_text("All players show one card to the next player.", TINY_FONT, 280), get_wrapped_text("There's always time for a good gossip.", TINY_FONT, 280))
SHOW_LEAD_PIPE = ClueCard("What Was That?", get_wrapped_text("Anyone holding the Lead Pipe card must reveal it!", TINY_FONT, 280), get_wrapped_text("It's become a real weight in your pocket.", TINY_FONT, 280))
SHOW_DAGGER = ClueCard("What Was That?", get_wrapped_text("Anyone holding the Dagger card must reveal it!", TINY_FONT, 280), get_wrapped_text("We need to sharpen our investigating skills.", TINY_FONT, 280))
CHOOSE_SUSPECT_REVEAL = ClueCard("Airtight Alibi!", get_wrapped_text("Name one suspect you want revealed.", TINY_FONT, 280), get_wrapped_text("It couldn't possibly be...", TINY_FONT, 280))
SHOW_BALLROOM = ClueCard("Where?", get_wrapped_text("Anyone holding the Ballroom card must reveal it!", TINY_FONT, 280), get_wrapped_text("A waltz starts echoing around Tudor Mansion.", TINY_FONT, 280))
SHOW_LOUNGE = ClueCard("Where?", get_wrapped_text("Anyone holding the Lounge card must reveal it!", TINY_FONT, 280), get_wrapped_text("This is no time to relax!", TINY_FONT, 280))
SHOW_WRENCH = ClueCard("What Was That?", get_wrapped_text("Anyone holding the Wrench card must reveal it!", TINY_FONT, 280), get_wrapped_text("We will get to the truth!", TINY_FONT, 280))
SHOW_SCARLETT = ClueCard("What Happened?", get_wrapped_text("Anyone holding the Miss Scarlett card must reveal it!", TINY_FONT, 280), get_wrapped_text("Hold on, that's a scratch on Miss Scarlett's cheek.", TINY_FONT, 280))
SHOW_CONSERVATORY = ClueCard("Where?", get_wrapped_text("Anyone holding the Conservatory card must reveal it!", TINY_FONT, 280), get_wrapped_text("These plants really do need some water.", TINY_FONT, 280))
ROOM_CHOICE = ClueCard("Screeeeam!", get_wrapped_text("All players rush to the room of their choice.", TINY_FONT, 280))
SHOW_BILLIARD = ClueCard("Where?", get_wrapped_text("Anyone holding the Billiard Room card must reveal it!", TINY_FONT, 280), get_wrapped_text("That's your cue!", TINY_FONT, 280))
SHOW_LIBRARY = ClueCard("Where?", get_wrapped_text("Anyone holding the Library card must reveal it!", TINY_FONT, 280), get_wrapped_text("There's only one place that book could have come from.", TINY_FONT, 280))
ALL_REVEAL = ClueCard("Dun-Dun-Duuun!", get_wrapped_text("All players reveal one card from their hand.", TINY_FONT, 280))
SHOW_STUDY = ClueCard("Where?", get_wrapped_text("Anyone holding the Study card must reveal it!", TINY_FONT, 280), get_wrapped_text("The telephone jangles everybody's nerves.", TINY_FONT, 280))
SHOW_REVOLVER = ClueCard("What Was That?", get_wrapped_text("Anyone holding the Revolver card must reveal it!", TINY_FONT, 280), get_wrapped_text("We must trigger a reaction.", TINY_FONT, 280))
CHOOSE_LOCATION_REVEAL = ClueCard("Wink Wink!", get_wrapped_text("Name one location you want revealed.", TINY_FONT, 280), get_wrapped_text("It couldn't possibly be...", TINY_FONT, 280))
SHOW_PEACOCK = ClueCard("What Happened?", get_wrapped_text("Anyone holding the Mrs Peacock card must reveal it!", TINY_FONT, 280), get_wrapped_text("Wait a minute, Mrs Peacock was last seen with Black.", TINY_FONT, 280))
SHOW_ORCHID = ClueCard("What Happened?", get_wrapped_text("Anyone holding the Doctor Orchid card must reveal it!", TINY_FONT, 280), get_wrapped_text("Hmmm, Doctor Orchid has a bandage on her hand.", TINY_FONT, 280))
SHOW_PLUM = ClueCard("What Happened?", get_wrapped_text("Anyone holding the Prof. Plum card must reveal it!", TINY_FONT, 280), get_wrapped_text("Look, the arm of Professor Plum's glasses has been hastily fixed with tape.", TINY_FONT, 280))

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
BALLROOM = Location(BALLROOM_CARD, (570, 196), [BALLROOM_SQUARE1, BALLROOM_SQUARE2, BALLROOM_SQUARE3, BALLROOM_SQUARE4], {
    0: (484, 131),
    1: (570, 131),
    2: (656, 131),
    3: (484, 260),
    4: (570, 260),
    5: (656, 260)
}, (485, 46), (655, 46), (655, 89), (741, 89), (741, 345), (399, 345), (399, 89), (485, 89), (485, 46))
CONSERVATORY = Location(CONSERVATORY_CARD, (957, 153), [CONSERVATORY_SQUARE], {
    0: (871, 88),
    1: (957, 88),
    2: (1043, 88),
    3: (871, 217),
    4: (957, 217),
    5: (1043, 157)
}, (829, 46), (1085, 46), (1085, 216), (1042, 216), (1042, 259), (829, 259), (829, 46))
BILLIARD_ROOM = Location(BILLIARD_ROOM_CARD, (957, 454), [BILLIARD_SQUARE1, BILLIARD_SQUARE2], {
    0: (871, 389),
    1: (957, 389),
    2: (1043, 389),
    3: (871, 518),
    4: (957, 518),
    5: (1043, 518)
}, (829, 347), (1085, 347), (1085, 560), (829, 560), (829, 347))
LIBRARY = Location(LIBRARY_CARD, (936, 712), [LIBRARY_SQUARE1, LIBRARY_SQUARE2], {
    0: (871, 647),
    1: (936, 647),
    2: (1000, 647),
    3: (871, 776),
    4: (936, 776),
    5: (1000, 776)
}, (829, 605), (1042, 605), (1042, 648), (1085, 648), (1085, 775), (1042, 775), (1042, 818), (829, 818), (829, 775), (786, 775), (786, 648), (829, 648), (829, 605))
STUDY = Location(STUDY_CARD, (936, 991), [STUDY_SQUARE], {
    0: (871, 948),
    1: (936, 948),
    2: (1000, 948),
    3: (871, 1034),
    4: (936, 1034),
    5: (1000, 1034)
}, (786, 906), (1085, 906), (1085, 1077), (829, 1077), (829, 1033), (786, 1033), (786, 906))
HALL = Location(HALL_CARD, (570, 927), [HALL_SQUARE1, HALL_SQUARE2], {
    0: (484, 819),
    1: (570, 819),
    2: (656, 819),
    3: (484, 1034),
    4: (570, 1034),
    5: (656, 1034)
}, (442, 777), (698, 777), (698, 1077), (442, 1076), (442, 777))
LOUNGE = Location(LOUNGE_CARD, (205, 948), [LOUNGE_SQUARE], {
    0: (97, 862),
    1: (205, 862),
    2: (313, 862),
    3: (97, 1034),
    4: (205, 1034),
    5: (313, 991)
}, (55, 820), (354, 820), (354, 1034), (312, 1034), (312, 1077), (55, 1077), (55, 820))
DINING_ROOM = Location(DINING_ROOM_CARD, (226, 539), [DINING_SQUARE1, DINING_SQUARE2], {
    0: (97, 476),
    1: (226, 476),
    2: (355, 476),
    3: (97, 605),
    4: (226, 605),
    5: (355, 605)
}, (55, 390), (268, 390), (268, 433), (397, 433), (397, 689), (55, 689), (55, 390))
KITCHEN = Location(KITCHEN_CARD, (183, 174), [KITCHEN_SQUARE], {
    0: (97, 131),
    1: (183, 131),
    2: (269, 131),
    3: (97, 217),
    4: (183, 217),
    5: (269, 217)
}, (55, 46), (311, 46), (311, 302), (98, 302), (98, 259), (55, 259), (55, 46))
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
    SELECTED_SQUARE = None
    SELECTED_LOCATION = None
    SQUARE_FAIL_DISTANCE = 0
    CLUE_TO_DRAW = 0
    DISPLAYED_CLUE_CARD = None
    PLAYER_GUESS = []
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