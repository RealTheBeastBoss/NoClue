from game import *

class TitleState(Enum):
    BLANK = 0
    CROSSED = 1
    CIRCLED = 2

def draw_text(text, font, colour, location):  # Draws text for the Clue Titles
    text_surface = font.render(text, True, colour)
    text_width = text_surface.get_width()
    text_height = text_surface.get_height()
    WINDOW.blit(text_surface, (location[0] - text_width, location[1] - (text_height/2)))
    text_rect = text_surface.get_rect()
    text_rect.topleft = (location[0] - text_width, location[1] - (text_height/2))
    pygame.draw.rect(WINDOW, BLACK, text_rect, 1)

class ClueSheet:
    def __init__(self):
        self.clueTitles = [ClueTitle(MISS_SCARLETT, 245), ClueTitle(COL_MUSTARD, 280), ClueTitle(DR_ORCHID, 315), ClueTitle(REV_GREEN, 350), ClueTitle(MRS_PEACOCK, 385),
                           ClueTitle(PROF_PLUM, 420), ClueTitle(CANDLESTICK, 475), ClueTitle(DAGGER, 510), ClueTitle(LEAD_PIPE, 545), ClueTitle(REVOLVER, 580), ClueTitle(ROPE, 615),
                           ClueTitle(WRENCH, 650), ClueTitle(BALLROOM_CARD, 705), ClueTitle(BILLIARD_ROOM_CARD, 740), ClueTitle(CONSERVATORY_CARD, 775), ClueTitle(DINING_ROOM_CARD, 810),
                           ClueTitle(HALL_CARD, 845), ClueTitle(KITCHEN_CARD, 880), ClueTitle(LIBRARY_CARD, 915), ClueTitle(LOUNGE_CARD, 950), ClueTitle(STUDY_CARD, 985)]
        self.selectedBox = None

    def draw(self):
        pygame.draw.rect(WINDOW, WHITE, pygame.Rect((1326, 180), (564, 870)), 0, 15)
        for title in self.clueTitles:
            draw_text(title.text, SMALL_FONT, BLACK, (1560, title.height))

class ClueTitle:
    def __init__(self, card_reference, height):
        self.height = height
        self.cardReference = card_reference
        self.text = card_reference.displayName
        self.state = TitleState.BLANK
        self.rect = None

class ClueBox:
    def __init__(self, title, player_ref):
        self.clueTitle = title
        self.playerRef = player_ref
        self.text = None
        self.dotCount = 0
        self.rect = None
