from game import *

class TitleState(Enum):
    BLANK = 0
    CROSSED = 1
    CIRCLED = 2

def draw_text(text, font, colour, location, clue_title = None):
    text_surface = font.render(text, True, colour)
    text_width = text_surface.get_width()
    text_height = text_surface.get_height()
    if clue_title is None:
        WINDOW.blit(text_surface, (location[0] - (text_width / 2), location[1] - (text_height / 2)))
    else:
        WINDOW.blit(text_surface, (location[0] - text_width, location[1] - (text_height / 2)))
        text_rect = text_surface.get_rect()
        text_rect.topleft = (location[0] - text_width, location[1] - (text_height/2))
        if Game.BUTTONS_ENABLED:
            if Game.LEFT_MOUSE_RELEASED and text_rect.collidepoint(pygame.mouse.get_pos()):
                Game.BUTTONS_ENABLED = False
                pygame.time.set_timer(BUTTON_COOLDOWN_EVENT, 100, 1)
                if clue_title.state == TitleState.CIRCLED:
                    clue_title.state = TitleState.BLANK
                elif clue_title.state == TitleState.CROSSED:
                    clue_title.state = TitleState.CIRCLED
                else:
                    clue_title.state = TitleState.CROSSED
        if clue_title.state == TitleState.CIRCLED:
            pygame.draw.rect(WINDOW, ORANGE, text_rect, 3, 15)
        elif clue_title.state == TitleState.CROSSED:
            pygame.draw.line(WINDOW, ORANGE, (text_rect.topleft[0], text_rect.topleft[1] + (text_height / 2)), (text_rect.topleft[0] + text_width, text_rect.topleft[1] + (text_height / 2)), 3)

class ClueSheet:
    def __init__(self):
        self.clueTitles = [ClueTitle(MISS_SCARLETT, 245), ClueTitle(COL_MUSTARD, 280), ClueTitle(DR_ORCHID, 315), ClueTitle(REV_GREEN, 350), ClueTitle(MRS_PEACOCK, 385),
                           ClueTitle(PROF_PLUM, 420), ClueTitle(CANDLESTICK, 475), ClueTitle(DAGGER, 510), ClueTitle(LEAD_PIPE, 545), ClueTitle(REVOLVER, 580), ClueTitle(ROPE, 615),
                           ClueTitle(WRENCH, 650), ClueTitle(BALLROOM_CARD, 705), ClueTitle(BILLIARD_ROOM_CARD, 740), ClueTitle(CONSERVATORY_CARD, 775), ClueTitle(DINING_ROOM_CARD, 810),
                           ClueTitle(HALL_CARD, 845), ClueTitle(KITCHEN_CARD, 880), ClueTitle(LIBRARY_CARD, 915), ClueTitle(LOUNGE_CARD, 950), ClueTitle(STUDY_CARD, 985)]
        self.clueBoxes = []
        for title in self.clueTitles:
            if title.text in Game.CARD_NAMES:
                title.state = TitleState.CROSSED
            for x in range(Game.PLAYER_COUNT):
                self.clueBoxes.append(ClueBox(title, 1600 + (x * 45), x))
        self.selectedBox = None

    def draw(self):
        pygame.draw.rect(WINDOW, WHITE, pygame.Rect((1326, 180), (564, 870)), 0, 15)
        for title in self.clueTitles:
            draw_text(title.text, SMALL_FONT, BLACK, (1560, title.height), title)
        selected_player = Game.CLIENT_NUMBER
        iterations = 0
        while True:
            if iterations > 0 and selected_player == Game.CLIENT_NUMBER:
                break
            pygame.draw.circle(WINDOW, Game.PLAYERS[selected_player].playerColour, (1600 + (iterations * 45), 210), 15)
            if selected_player == Game.PLAYER_COUNT - 1:
                selected_player = 0
            else:
                selected_player += 1
            iterations += 1
        if Game.LEFT_MOUSE_RELEASED:
            self.selectedBox = None
        for box in self.clueBoxes:
            if Game.LEFT_MOUSE_RELEASED and box.rect.collidepoint(pygame.mouse.get_pos()):
                self.selectedBox = box
            if box == self.selectedBox:
                colour = ORANGE
            else:
                colour = BLACK
            pygame.draw.rect(WINDOW, colour, box.rect, 2)
            if box.text is not None:
                if box.text == "X":
                    colour = RED
                elif box.text == "O":
                    colour = GREEN
                else:
                    colour = BLACK
                draw_text(box.text, TINY_FONT, colour, (box.topLeft[0] + (box.width / 2), box.topLeft[1] + (box.height / 2)))

class ClueTitle:
    def __init__(self, card_reference, height):
        self.height = height
        self.text = card_reference.displayName
        self.state = TitleState.BLANK

class ClueBox:
    def __init__(self, title, middle, col):
        self.clueTitle = title
        if col == 0:
            if title.text in Game.CARD_NAMES:
                self.text = "O"
            else:
                self.text = "X"
        else:
            self.text = None
        self.dotCount = 0
        self.column = col
        self.height = 25
        self.width = 25
        self.topLeft = (middle - (self.width / 2), (title.height + 2) - (self.height / 2))
        self.rect = pygame.Rect(self.topLeft, (self.width, self.height))
