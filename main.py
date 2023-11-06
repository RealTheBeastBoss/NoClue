import random
import pygame
import sys
from game import *
from button import Button
from server import check_server, start_server, close_server
from _thread import *
from network import Network
from clue_sheet import ClueSheet, TitleState
from dice import Dice
from pathfinding.finder.a_star import AStarFinder
pygame.display.set_caption("No Clue")

DICE1 = Dice()
DICE2 = Dice()

def draw_window():  # Game Logic and Display
    if Game.SCREEN_STATE == ScreenState.START:
        WINDOW.fill(BACKGROUND)
        draw_text("No Clue", BIG_FONT, ORANGE, (960, 200))
        quit_button = Button("Quit", 960, 590, 60)
        play_button = Button("Play", 960, 490, 60)
        if quit_button.check_click():
            pygame.quit()
            sys.exit()
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
        if Game.CLUE_CARDS_ACTIVE:
            clue_cards_toggle = Button("Disable Clue Cards", 960, 230, 60)
        else:
            clue_cards_toggle = Button("Enable Clue Cards", 960, 230, 60)
        if clue_cards_toggle.check_click():
            Game.CLUE_CARDS_ACTIVE = not Game.CLUE_CARDS_ACTIVE
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
            if Game.FAILED_SELECTION:
                draw_text("That Character has been taken already", SMALL_FONT, ORANGE, (960, 200))
            draw_text("What will your character be?", MEDIUM_FONT, ORANGE, (960, 250))
            scarlett_button = Button("Miss Scarlett", 960, 330, 60)
            mustard_button = Button("Col. Mustard", 960, 415, 60)
            plum_button = Button("Prof. Plum", 960, 500, 60)
            peacock_button = Button("Mrs Peacock", 960, 585, 60)
            green_button = Button("Rev. Green", 960, 670, 60)
            orchid_button = Button("Dr Orchid", 960, 755, 60)
            if scarlett_button.check_click():
                data = ("Player", 0)
                Game.CLIENT_NUMBER = 0
                response = Game.NETWORK.send(data)
                if response:
                    Game.PLAYER_COUNT = response
                else:
                    Game.FAILED_SELECTION = True
            elif mustard_button.check_click():
                data = ("Player", 1)
                Game.CLIENT_NUMBER = 1
                response = Game.NETWORK.send(data)
                if response:
                    Game.PLAYER_COUNT = response
                else:
                    Game.FAILED_SELECTION = True
            elif orchid_button.check_click():
                data = ("Player", 2)
                Game.CLIENT_NUMBER = 2
                response = Game.NETWORK.send(data)
                if response:
                    Game.PLAYER_COUNT = response
                else:
                    Game.FAILED_SELECTION = True
            elif green_button.check_click():
                data = ("Player", 3)
                Game.CLIENT_NUMBER = 3
                response = Game.NETWORK.send(data)
                if response:
                    Game.PLAYER_COUNT = response
                else:
                    Game.FAILED_SELECTION = True
            elif peacock_button.check_click():
                data = ("Player", 4)
                Game.CLIENT_NUMBER = 4
                response = Game.NETWORK.send(data)
                if response:
                    Game.PLAYER_COUNT = response
                else:
                    Game.FAILED_SELECTION = True
            elif plum_button.check_click():
                data = ("Player", 5)
                Game.CLIENT_NUMBER = 5
                response = Game.NETWORK.send(data)
                if response:
                    Game.PLAYER_COUNT = response
                else:
                    Game.FAILED_SELECTION = True
        else:
            draw_text("Waiting for the Game to be Ready", MEDIUM_FONT, ORANGE, (960, 250))
            response = Game.NETWORK.send("?")
            if response:
                Game.PLAYERS = response[0]
                Game.CLUE_CARD_DECK = response[1]
                Game.CLUE_CARDS_ACTIVE = response[2]
                for x in range(len(Game.PLAYERS)):
                    if Game.PLAYERS[x].playerNumber == Game.CLIENT_NUMBER:
                        Game.CLIENT_NUMBER = x
                        break
                Game.SCREEN_STATE = ScreenState.PLAYING_GAME
                for card in Game.PLAYERS[Game.CLIENT_NUMBER].cards:
                    Game.CARD_NAMES.append(card.displayName)
                Game.CLUE_SHEET = ClueSheet()
        temp_button = Button("Quit", 960, 900, 60)
        if temp_button.check_click():
            pygame.quit()
            sys.exit()
    elif Game.SCREEN_STATE == ScreenState.PLAYING_GAME:
        check_updates()
        current_player = Game.PLAYERS[Game.CURRENT_PLAYER]
        WINDOW.fill(BACKGROUND)
        draw_text(str(Game.CLIENT_NUMBER), SMALL_FONT, Game.PLAYERS[Game.CLIENT_NUMBER].playerColour, (5, 5), False)
        draw_game_board()
        if Game.CLUE_SHEET_OPEN:
            Game.CLUE_SHEET.draw()
        if current_player.playerIndex != Game.CLIENT_NUMBER:
            draw_text("It is " + current_player.playerName + "'s turn", SMALL_FONT, ORANGE, (1350, 100))
            if not Game.CLUE_SHEET_OPEN:
                if Game.DISPLAYED_CLUE_CARD is not None:
                    draw_clue_card(Game.DISPLAYED_CLUE_CARD, (1450, 350))
                else:
                    DICE1.draw((1518, 414))
                    DICE2.draw((1614, 414))
        elif Game.TURN_STAGE == TurnStage.START:
            if Game.HAS_DIED:
                draw_text("You have already failed, no turn for you", SMALL_FONT, ORANGE, (1350, 100))
                end_turn_button = Button("End Turn", 1350, 145, 60)
                if end_turn_button.check_click():
                    Game.TURN_STAGE = TurnStage.END_TURN
                return
            Game.TURN_STAGE = TurnStage.ROLL_DICE
        elif Game.TURN_STAGE == TurnStage.ROLL_DICE:
            if not Game.CLUE_SHEET_OPEN:
                DICE1.draw((1518, 414))
                DICE2.draw((1614, 414))
                roll_button = Button("Roll the Dice", 1608, 540, 60)
                if roll_button.check_click():
                    DICE1.value = random.randrange(1, 7)
                    DICE2.value = random.randrange(1, 7)
                    if Game.CLUE_CARDS_ACTIVE:
                        Game.CLUE_TO_DRAW = 0
                        if DICE1.value == 1:
                            Game.CLUE_TO_DRAW += 1
                        if DICE2.value == 1:
                            Game.CLUE_TO_DRAW += 1
                        if Game.CLUE_TO_DRAW > 0:
                            Game.TURN_STAGE = TurnStage.DRAW_CLUE_CARD
                        else:
                            Game.TURN_STAGE = TurnStage.MOVEMENT
                    else:
                        Game.TURN_STAGE = TurnStage.MOVEMENT
                    Game.NETWORK.send(("TurnDice", Game.TURN_STAGE, DICE1.value, DICE2.value))
        elif Game.TURN_STAGE == TurnStage.MOVEMENT:
            draw_text("Select a Place to go or Choose your Option:", SMALL_FONT, ORANGE, (1350, 100))
            if Game.SQUARE_FAIL_DISTANCE != 0:
                draw_text("That square is too far away! " + str(Game.SQUARE_FAIL_DISTANCE), SMALL_FONT, ORANGE, (1350, 180))
            for location in Game.LOCATIONS:
                if check_click_location(location):
                    for square in location.enterSquares:
                        finder = AStarFinder()
                        path = finder.find_path(GRID.node(Game.PLAYERS[Game.CLIENT_NUMBER].location.square[0], Game.PLAYERS[Game.CLIENT_NUMBER].location.square[1]), GRID.node(square.square[0], square.square[1]), GRID)[0]
                        GRID.cleanup()
                        if len(path) - 1 <= DICE1.value + DICE2.value:
                            Game.SELECTED_LOCATION = location
                            Game.SELECTED_SQUARE = None
                            Game.SQUARE_FAIL_DISTANCE = 0
                            break
            for square in SQUARES:
                result = check_click_square(square)
                if result is None:
                    continue
                elif isinstance(result, Square):
                    Game.SELECTED_SQUARE = result
                    Game.SQUARE_FAIL_DISTANCE = 0
                    Game.SELECTED_LOCATION = None
                else:
                    Game.SQUARE_FAIL_DISTANCE = result
                    Game.SELECTED_SQUARE = None
                    Game.SELECTED_LOCATION = None
            if not Game.CLUE_SHEET_OPEN:
                DICE1.draw((1518, 414))
                DICE2.draw((1614, 414))
                if Game.SELECTED_SQUARE is not None:
                    square_button = Button("Go to the Square", 1608, 540, 60)
                    if square_button.check_click():
                        to_location = False
                        for location in Game.LOCATIONS:
                            for entrance in location.enterSquares:
                                if Game.SELECTED_SQUARE == entrance:
                                    current_player.location = location
                                    Game.TURN_STAGE = TurnStage.MAKE_GUESS
                                    Game.PLAYER_GUESS[2] = current_player.location.ref
                                    to_location = True
                        if not to_location:
                            current_player.location = Game.SELECTED_SQUARE
                            Game.TURN_STAGE = TurnStage.END_TURN
                        Game.SELECTED_SQUARE = None
                        Game.NETWORK.send(("TurnPlayer", Game.TURN_STAGE, current_player))
                elif Game.SELECTED_LOCATION is not None:
                    location_button = Button("Go to the " + Game.SELECTED_LOCATION.displayName, 1608, 540, 60)
                    if location_button.check_click():
                        current_player.location = Game.SELECTED_LOCATION
                        Game.SELECTED_LOCATION = None
                        Game.TURN_STAGE = TurnStage.MAKE_GUESS
                        Game.PLAYER_GUESS[2] = current_player.location.ref
                        Game.NETWORK.send(("TurnPlayer", Game.TURN_STAGE, current_player))
                if isinstance(current_player.location, Location):
                    stay_button = Button("Stay where you are", 1608, 575, 60)
                    if stay_button.check_click():
                        Game.TURN_STAGE = TurnStage.MAKE_GUESS
                        Game.PLAYER_GUESS[2] = current_player.location.ref
                        Game.NETWORK.send(("Turn", Game.TURN_STAGE))
                    if current_player.location.passage is not None:
                        passage_button = Button("Use Secret Passage", 1608, 610, 60)
                        if passage_button.check_click():
                            current_player.location = current_player.location.passage
                            Game.TURN_STAGE = TurnStage.MAKE_GUESS
                            Game.PLAYER_GUESS[2] = current_player.location.ref
                            Game.NETWORK.send(("TurnPlayer", Game.TURN_STAGE, current_player))
        elif Game.TURN_STAGE == TurnStage.DRAW_CLUE_CARD:
            draw_text("Draw a Clue Card", SMALL_FONT, ORANGE, (1350, 100))
            clue_rect = pygame.Rect((515, 463), (154, 240))
            if Game.DISPLAYED_CLUE_CARD is None and Game.LEFT_MOUSE_RELEASED and clue_rect.collidepoint(pygame.mouse.get_pos()):
                Game.DISPLAYED_CLUE_CARD = Game.CLUE_CARD_DECK.pop()
                Game.CLUE_TO_DRAW -= 1
                Game.NETWORK.send("Clue")
            if not Game.CLUE_SHEET_OPEN:
                if Game.DISPLAYED_CLUE_CARD is not None:
                    draw_clue_card(Game.DISPLAYED_CLUE_CARD, (1450, 350))
                    continue_button = Button("Continue", 1604, 870, 60)
                    if continue_button.check_click():
                        Game.TURN_STAGE = TurnStage.USE_CLUE_CARD
                        Game.NETWORK.send(("Turn", Game.TURN_STAGE))
                else:
                    DICE1.draw((1518, 414))
                    DICE2.draw((1614, 414))
        elif Game.TURN_STAGE == TurnStage.MAKE_GUESS:
            draw_text("Select a Suspect and Weapon:", SMALL_FONT, ORANGE, (1350, 100))
            if not Game.CLUE_SHEET_OPEN:
                if Game.ACCUSE_SUSPECT:
                    scarlett_button = Button("Miss Scarlett", 1604, 365, 60)
                    if scarlett_button.check_click():
                        Game.ACCUSE_SUSPECT = False
                        Game.PLAYER_GUESS[0] = MISS_SCARLETT
                    mustard_button = Button("Col. Mustard", 1604, 435, 60)
                    if mustard_button.check_click():
                        Game.ACCUSE_SUSPECT = False
                        Game.PLAYER_GUESS[0] = COL_MUSTARD
                    orchid_button = Button("Dr Orchid", 1604, 505, 60)
                    if orchid_button.check_click():
                        Game.ACCUSE_SUSPECT = False
                        Game.PLAYER_GUESS[0] = DR_ORCHID
                    green_button = Button("Rev. Green", 1604, 575, 60)
                    if green_button.check_click():
                        Game.ACCUSE_SUSPECT = False
                        Game.PLAYER_GUESS[0] = REV_GREEN
                    peacock_button = Button("Mrs Peacock", 1604, 645, 60)
                    if peacock_button.check_click():
                        Game.ACCUSE_SUSPECT = False
                        Game.PLAYER_GUESS[0] = MRS_PEACOCK
                    plum_button = Button("Prof. Plum", 1604, 715, 60)
                    if plum_button.check_click():
                        Game.ACCUSE_SUSPECT = False
                        Game.PLAYER_GUESS[0] = PROF_PLUM
                elif Game.GUESS_WEAPON:
                    candlestick_button = Button("Candlestick", 1604, 365, 60)
                    if candlestick_button.check_click():
                        Game.GUESS_WEAPON = False
                        Game.PLAYER_GUESS[1] = CANDLESTICK
                    dagger_button = Button("Dagger", 1604, 435, 60)
                    if dagger_button.check_click():
                        Game.GUESS_WEAPON = False
                        Game.PLAYER_GUESS[1] = DAGGER
                    lead_pipe_button = Button("Lead Pipe", 1604, 505, 60)
                    if lead_pipe_button.check_click():
                        Game.GUESS_WEAPON = False
                        Game.PLAYER_GUESS[1] = LEAD_PIPE
                    revolver_button = Button("Revolver", 1604, 575, 60)
                    if revolver_button.check_click():
                        Game.GUESS_WEAPON = False
                        Game.PLAYER_GUESS[1] = REVOLVER
                    rope_button = Button("Rope", 1604, 645, 60)
                    if rope_button.check_click():
                        Game.GUESS_WEAPON = False
                        Game.PLAYER_GUESS[1] = ROPE
                    wrench_button = Button("Wrench", 1604, 715, 60)
                    if wrench_button.check_click():
                        Game.GUESS_WEAPON = False
                        Game.PLAYER_GUESS[1] = WRENCH
                else:
                    if Game.PLAYER_GUESS[0] is None:
                        suspect_button = Button("Accuse a Suspect", 1604, 400, 60)
                        if suspect_button.check_click():
                            Game.ACCUSE_SUSPECT = True
                    else:
                        draw_text("Suspect: " + Game.PLAYER_GUESS[0].displayName, SMALL_FONT, ORANGE, (1604, 400))
                    if Game.PLAYER_GUESS[1] is None:
                        weapon_button = Button("Guess a Weapon", 1604, 540, 60)
                        if weapon_button.check_click():
                            Game.GUESS_WEAPON = True
                    else:
                        draw_text("Weapon: " + Game.PLAYER_GUESS[1].displayName, SMALL_FONT, ORANGE, (1604, 540))
                    draw_text("Location: " + Game.PLAYER_GUESS[2].displayName, SMALL_FONT, ORANGE, (1604, 680))
                    if Game.PLAYER_GUESS[0] is not None and Game.PLAYER_GUESS[1] is not None:
                        continue_button = Button("Continue", 1604, 740, 60)
                        if continue_button.check_click():
                            selected_player = Game.CLIENT_NUMBER
                            iterations = 0
                            to_continue = True
                            while True:
                                if iterations > 0 and selected_player == Game.CLIENT_NUMBER:
                                    break
                                if selected_player == Game.CLIENT_NUMBER:
                                    if selected_player == Game.PLAYER_COUNT - 1:
                                        selected_player = 0
                                    else:
                                        selected_player += 1
                                    iterations += 1
                                    continue
                                for card in Game.PLAYERS[selected_player].cards:
                                    if card.displayName == Game.PLAYER_GUESS[0].displayName or card.displayName == Game.PLAYER_GUESS[1].displayName or card.displayName == Game.PLAYER_GUESS[1].displayName:
                                        to_continue = False
                                        break
                                if not to_continue:
                                    break
                                if selected_player == Game.PLAYER_COUNT - 1:
                                    selected_player = 0
                                else:
                                    selected_player += 1
                                iterations += 1
                            if selected_player == Game.CLIENT_NUMBER:
                                Game.PLAYER_SHOWING = None
                            else:
                                Game.PLAYER_SHOWING = Game.PLAYERS[selected_player]
                            Game.TURN_STAGE = TurnStage.SHOW_CARD
                            Game.NETWORK.send(("CardShowing", Game.TURN_STAGE, Game.PLAYER_GUESS, Game.PLAYER_SHOWING))
        temp_button = Button("Quit", 1300, 540, 60)
        if temp_button.check_click():
            Game.NETWORK.send("quit")
            pygame.quit()


def draw_game_board():
    for location in Game.LOCATIONS:
        pygame.draw.polygon(WINDOW, WHITE, location.corners)
        draw_text(location.displayName, SMALL_FONT, BACKGROUND, location.center)
        if location.card is not None:
            draw_text("(Has a Card)", SMALL_FONT, BACKGROUND, (location.center[0], location.center[1] + 30))
    for square in SQUARES:
        if Game.SELECTED_SQUARE == square:
            colour = ORANGE
        else:
            colour = WHITE
        pygame.draw.rect(WINDOW, colour, square.currentRect)
    for player in Game.PLAYERS:
        if isinstance(player.location, Square):
            player_location = (player.location.topLeft[0] + 21, player.location.topLeft[1] + 21)
        else:
            player_location = player.location.player_to_point[player.playerIndex]
        pygame.draw.circle(WINDOW, player.playerColour, player_location, 18)
    if Game.CLUE_CARDS_ACTIVE:
        clue_rect = pygame.Rect((515, 463), (154, 240))
        pygame.draw.rect(WINDOW, BLACK, clue_rect, 0, 10)
        pygame.draw.rect(WINDOW, WHITE, clue_rect, 5, 10)
        draw_text("Clue", SMALL_FONT, WHITE, (592, 553))
        draw_text("Card", SMALL_FONT, WHITE, (592, 613))


def check_updates():
    response = Game.NETWORK.send("!")
    if response:
        print("From Server, Received: " + str(response))
        if "quit" in response:
            pygame.quit()
            sys.exit()
        if "locations" in response:
            for location in response["locations"]:
                for x in range(9):
                    if location.displayName == Game.LOCATIONS[x].displayName:
                        Game.LOCATIONS[x] = location
                        break
        if "turn" in response:
            Game.TURN_STAGE = response["turn"]
        if "dice" in response:
            DICE1.value = response["dice"][0]
            DICE2.value = response["dice"][1]
        if "players" in response:
            for player in response["players"]:
                Game.PLAYERS[player.playerIndex] = player
        if "clue" in response:
            if Game.DISPLAYED_CLUE_CARD is None:
                Game.DISPLAYED_CLUE_CARD = Game.CLUE_CARD_DECK.pop()
            else:
                Game.DISPLAYED_CLUE_CARD = None
        if "card_show" in response:
            Game.PLAYER_SHOWING = response["card_show"][0]
            Game.PLAYER_GUESS = response["card_show"][1]


def draw_clue_card(card, location):
    card_rect = pygame.Rect(location, (308, 480))
    pygame.draw.rect(WINDOW, BLACK, card_rect, 0, 20)
    pygame.draw.rect(WINDOW, WHITE, card_rect, 10, 20)
    draw_text(card.title, SMALL_FONT, WHITE, (location[0] + 154, location[1] + 40))
    for x in range(len(card.action)):
        draw_text(card.action[x], TINY_FONT, WHITE, (location[0] + 154, location[1] + (200 + (x * 25))))
    if card.subtitle is not None:
        for x in range(len(card.subtitle)):
            draw_text(card.subtitle[x], TINY_FONT, WHITE, (location[0] + 154, location[1] + (380 + (x * 25))))


def check_click_location(location):
    if Game.LEFT_MOUSE_RELEASED:
        count = 0
        xp, yp = pygame.mouse.get_pos()
        for edge in location.edges:
            if (yp < edge[1]) != (yp < edge[3]) and xp < edge[0] + ((yp - edge[1]) / (edge[3] - edge[1])) * (edge[2] - edge[0]):
                count += 1
        return count % 2 == 1
    return False


def check_click_square(square):
    if Game.LEFT_MOUSE_RELEASED and square.currentRect.collidepoint(pygame.mouse.get_pos()):
        finder = AStarFinder()
        path = finder.find_path(GRID.node(Game.PLAYERS[Game.CLIENT_NUMBER].location.square[0], Game.PLAYERS[Game.CLIENT_NUMBER].location.square[1]),
                                GRID.node(square.square[0], square.square[1]), GRID)[0]
        GRID.cleanup()
        if len(path) - 1 > DICE1.value + DICE2.value:
            return len(path) - 1
        else:
            return square
    return None


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
    CONSERVATORY.passage = LOUNGE
    LOUNGE.passage = CONSERVATORY
    STUDY.passage = KITCHEN
    KITCHEN.passage = STUDY
    while True:
        clock.tick(FPS)
        Game.LEFT_MOUSE_RELEASED = False
        Game.ENTER_PRESSED = False
        Game.CAN_INPUT_TEXT = False
        key_to_add = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                Game.LEFT_MOUSE_RELEASED = True
            elif event.type == BUTTON_COOLDOWN_EVENT:
                Game.BUTTONS_ENABLED = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    Game.CLUE_SHEET_OPEN = not Game.CLUE_SHEET_OPEN
                elif event.mod and pygame.KMOD_SHIFT and event.key == pygame.K_1 and Game.CLUE_SHEET_OPEN and Game.CLUE_SHEET.selectedBox is not None:
                    Game.CLUE_SHEET.selectedBox.text = "!"
                elif event.mod and pygame.KMOD_SHIFT and event.key == pygame.K_SLASH and Game.CLUE_SHEET_OPEN and Game.CLUE_SHEET.selectedBox is not None:
                    Game.CLUE_SHEET.selectedBox.text = "?"
                elif event.key == pygame.K_x and Game.CLUE_SHEET_OPEN and Game.CLUE_SHEET.selectedBox is not None:
                    Game.CLUE_SHEET.selectedBox.text = "X"
                elif event.key == pygame.K_RETURN and Game.CLUE_SHEET_OPEN and Game.CLUE_SHEET.selectedBox is not None:
                    Game.CLUE_SHEET.selectedBox.text = "O"
                    Game.CLUE_SHEET.selectedBox.clueTitle.state = TitleState.CROSSED
                elif event.key in ALLOWED_KEYS:
                    if event.key == pygame.K_BACKSPACE:
                        Game.USER_TEXT = Game.USER_TEXT[:-1]
                        if Game.CLUE_SHEET_OPEN and Game.CLUE_SHEET.selectedBox is not None:
                            Game.CLUE_SHEET.selectedBox.text = None
                    elif event.key == pygame.K_RETURN:
                        Game.ENTER_PRESSED = True
                    else:
                        key_to_add = event.unicode
        draw_window()
        if key_to_add is not None and Game.CAN_INPUT_TEXT:
            Game.USER_TEXT += key_to_add
        pygame.display.update()
