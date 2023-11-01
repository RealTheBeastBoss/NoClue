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

class ClueSheet:
    def __init__(self):
        self.clueTitles = [ClueTitle(MISS_SCARLETT, 80)]
        self.selectedBox = None

    def draw(self):
        pygame.draw.rect(WINDOW, WHITE, pygame.Rect((1300, 20), (1880, 700)), 0, 15)
        for title in self.clueTitles:
            draw_text(title.text, SMALL_FONT, BLACK, (1600, title.height))

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
