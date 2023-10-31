from game import *
from button import Button
from server import check_server, start_server, close_server
from _thread import *
from network import Network
from clue_sheet import ClueSheet
pygame.display.set_caption("No Clue")


def draw_window():  # Game Logic and Display
    if Game.SCREEN_STATE == ScreenState.START:
        WINDOW.fill(BACKGROUND)
        draw_text("No Clue", BIG_FONT, ORANGE, (960, 200))
        quit_button = Button("Quit", 960, 590, 60)
        play_button = Button("Play", 960, 490, 60)
        if quit_button.check_click():
            pygame.quit()
        elif play_button.check_click():
            Game.SCREEN_STATE = ScreenState.JOIN_NETWORK
    elif Game.SCREEN_STATE == ScreenState.JOIN_NETWORK:
        WINDOW.fill(BACKGROUND)
        if Game.HAS_SERVER:
            draw_text("Server Active", SMALL_FONT, ORANGE, (960, 100))
        draw_text("Enter the Server IP Address", MEDIUM_FONT, ORANGE, (960, 250))
        draw_text_input()
        back_button = Button("Back", 960, 690, 60)
        join_button = Button("Join Game", 960, 450, 60)
        create_button = Button("Create Game", 960, 540, 60)
        if back_button.check_click():
            Game.SCREEN_STATE = ScreenState.START
            if Game.HAS_SERVER:
                close_server()
            Game.HAS_SERVER = False
        elif create_button.check_click():
            if Game.USER_TEXT != "" and check_server(Game.USER_TEXT):
                Game.SCREEN_STATE = ScreenState.CREATE_SERVER
        elif join_button.check_click():
            Game.NETWORK = Network(Game.USER_TEXT)
            Game.USER_TEXT = ""
            if Game.NETWORK.success:
                Game.SCREEN_STATE = ScreenState.NAME_PLAYER
    elif Game.SCREEN_STATE == ScreenState.CREATE_SERVER:
        WINDOW.fill(BACKGROUND)
        draw_text("How many players?", MEDIUM_FONT, ORANGE, (960, 290))
        back_button = Button("Back", 960, 690, 60)
        two_button = Button("Two Players", 730, 455, 60, SMALL_FONT, BACKGROUND, ORANGE, 210)
        four_button = Button("Four Players", 960, 455, 60, SMALL_FONT, BACKGROUND, ORANGE, 210)
        six_button = Button("Six Players", 1190, 455, 60, SMALL_FONT, BACKGROUND, ORANGE, 210)
        three_button = Button("Three Players", 845, 540, 60, SMALL_FONT, BACKGROUND, ORANGE, 210)
        five_button = Button("Five Players", 1075, 540, 60, SMALL_FONT, BACKGROUND, ORANGE, 210)
        if back_button.check_click():
            Game.SCREEN_STATE = ScreenState.JOIN_NETWORK
        elif two_button.check_click():
            start_new_thread(start_server, (2, Game.USER_TEXT))
            Game.HAS_SERVER = True
            Game.SCREEN_STATE = ScreenState.JOIN_NETWORK
        elif three_button.check_click():
            start_new_thread(start_server, (3, Game.USER_TEXT))
            Game.HAS_SERVER = True
            Game.SCREEN_STATE = ScreenState.JOIN_NETWORK
        elif four_button.check_click():
            start_new_thread(start_server, (4, Game.USER_TEXT))
            Game.HAS_SERVER = True
            Game.SCREEN_STATE = ScreenState.JOIN_NETWORK
        elif five_button.check_click():
            start_new_thread(start_server, (5, Game.USER_TEXT))
            Game.HAS_SERVER = True
            Game.SCREEN_STATE = ScreenState.JOIN_NETWORK
        elif six_button.check_click():
            start_new_thread(start_server, (6, Game.USER_TEXT))
            Game.HAS_SERVER = True
            Game.SCREEN_STATE = ScreenState.JOIN_NETWORK
    elif Game.SCREEN_STATE == ScreenState.NAME_PLAYER:
        WINDOW.fill(BACKGROUND)
        if Game.PLAYER_COUNT == 69:
            draw_text("What will your name be?", MEDIUM_FONT, ORANGE, (960, 250))
            draw_text_input()
            if Game.ENTER_PRESSED and Game.USER_TEXT != "":
                data = ("Name", Game.USER_TEXT)
                response = Game.NETWORK.send(data)
                Game.CLIENT_NUMBER = response[0]
                Game.PLAYER_COUNT = response[1]
        else:
            draw_text("Waiting for the Game to be Ready", MEDIUM_FONT, ORANGE, (960, 250))
            response = Game.NETWORK.send("?")
            if response:
                Game.PLAYERS = response[0]
                Game.SCREEN_STATE = ScreenState.PLAYING_GAME
                Game.CLUE_SHEET = ClueSheet()
        temp_button = Button("Quit", 960, 900, 60)
        if temp_button.check_click():
            pygame.quit()


def check_click_location(location):
    if Game.LEFT_MOUSE_RELEASED:
        count = 0
        xp, yp = pygame.mouse.get_pos()
        for edge in location.edges:
            if (yp < edge[1]) != (yp < edge[3]) and xp < edge[0] + ((yp - edge[1]) / (edge[3] - edge[1])) * (edge[2] - edge[0]):
                count += 1
        return count % 2 == 1
    return False


def draw_text(text, font, colour, location, center = True):  # Draws text centered on a location
    text_surface = font.render(text, True, colour)
    text_width = text_surface.get_width()
    text_height = text_surface.get_height()
    if center:
        WINDOW.blit(text_surface, (location[0] - (text_width/2), location[1] - (text_height/2)))
    else:
        WINDOW.blit(text_surface, location)


def draw_text_input(location = (960, 330), max_length = 300):  # Creates Text Input Visuals
    text_surface = SMALL_FONT.render(Game.USER_TEXT, True, ORANGE)
    if text_surface.get_width() >= max_length:
        Game.CAN_INPUT_TEXT = False
    else:
        Game.CAN_INPUT_TEXT = True
    input_rect_width = max(text_surface.get_width() + 10, 200)
    input_rect = pygame.Rect(location[0] - (input_rect_width / 2), location[1], input_rect_width, 60)
    pygame.draw.rect(WINDOW, ORANGE, input_rect, 5, 5)
    WINDOW.blit(text_surface, ((input_rect.x + (input_rect.width / 2)) - (text_surface.get_width() / 2), (input_rect.y + (input_rect.height / 2)) -
    text_surface.get_height() / 2))


if __name__ == "__main__":
    clock = pygame.time.Clock()
    while True:
        clock.tick(FPS)
        Game.LEFT_MOUSE_RELEASED = False
        Game.ENTER_PRESSED = False
        Game.CAN_INPUT_TEXT = False
        key_to_add = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                Game.LEFT_MOUSE_RELEASED = True
            elif event.type == BUTTON_COOLDOWN_EVENT:
                Game.BUTTONS_ENABLED = True
            elif event.type == pygame.KEYDOWN:
                if event.key in ALLOWED_KEYS:
                    if event.key == pygame.K_BACKSPACE:
                        Game.USER_TEXT = Game.USER_TEXT[:-1]
                    elif event.key == pygame.K_RETURN:
                        Game.ENTER_PRESSED = True
                    else:
                        key_to_add = event.unicode
        draw_window()
        if key_to_add is not None and Game.CAN_INPUT_TEXT:
            Game.USER_TEXT += key_to_add
        pygame.display.update()
