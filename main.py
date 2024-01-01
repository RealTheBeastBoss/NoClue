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
        if Game.CLUE_SHEET_OPEN and not Game.TURN_STAGE == TurnStage.GAME_OVER:
            Game.CLUE_SHEET.draw()
        if current_player.playerIndex != Game.CLIENT_NUMBER:
            draw_text("It is " + current_player.playerName + "'s turn", SMALL_FONT, current_player.playerColour, (1503, 100))
            if Game.TURN_STAGE == TurnStage.USE_CLUE_CARD:
                draw_text("Using the Clue Card!", SMALL_FONT, ORANGE, (1503, 140))
                if not Game.CLUE_SHEET_OPEN:
                    if Game.REVEALING_CARD[0] == "Wait":  # Waiting for Continue
                        draw_text("Waiting for others to continue", SMALL_FONT, ORANGE, (1503, 540))
                    elif Game.COMPLETED_PASSAGE:
                        draw_text("A Secret Passage is in the " + Game.SELECTED_LOCATION.displayName, SMALL_FONT, ORANGE, (1503, 540))
                        continue_button = Button("Continue", 1503, 610, 60)
                        if continue_button.check_click():
                            Game.NETWORK.send("TurnClick")
                            Game.REVEALING_CARD[0] = "Wait"
                            Game.SELECTED_LOCATION = None
                            Game.COMPLETED_PASSAGE = False
                    elif Game.PLAYER_CHOOSING is not None:  # Waiting for a Player to Choose
                        if Game.PLAYER_CHOOSING.playerIndex == Game.CLIENT_NUMBER:
                            draw_text("You need to choose a card to reveal!", SMALL_FONT, ORANGE, (1503, 240))
                            for x in range(len(Game.PLAYERS[Game.CLIENT_NUMBER].cards)):
                                is_reveal = False
                                card = Game.PLAYERS[Game.CLIENT_NUMBER].cards[x]
                                for reveal in Game.REVEALED_CARDS:
                                    if reveal.displayName == card.displayName:
                                        is_reveal = True
                                        break
                                if is_reveal:
                                    continue
                                button = Button(card.displayName, 1503, 300 + (x * 70), 60)
                                if button.check_click():
                                    Game.REVEALING_CARD[0] = card
                                    Game.REVEALING_CARD[1] = Game.PLAYER_CHOOSING
                                    Game.PLAYER_CHOOSING = None
                                    Game.REVEALED_CARDS.append(card)
                                    Game.NETWORK.send(("ChosenCard", card))
                                    break
                        else:
                            draw_text("Waiting for " + Game.PLAYER_CHOOSING.playerName + " to choose a card", SMALL_FONT, ORANGE, (1503, 540))
                    elif Game.DISPLAYED_CLUE_CARD is not None:
                        if Game.REVEALING_CARD[0] is not None:  # Reveal Card
                            if Game.REVEALING_CARD[1] is None:
                                draw_text("Nobody has the \"" + Game.REVEALING_CARD[0].displayName + "\" card", SMALL_FONT, ORANGE, (1503, 540))
                            else:
                                draw_text(Game.REVEALING_CARD[1].playerName + " has the \"" + Game.REVEALING_CARD[0].displayName + "\" card", SMALL_FONT, ORANGE, (1503, 540))
                            continue_button = Button("Continue", 1503, 610, 60)
                            if continue_button.check_click():
                                Game.NETWORK.send("TurnClick")
                                Game.REVEALING_CARD[0] = "Wait"
                        elif Game.DISPLAYED_CLUE_CARD.title == "Screeeeam!":
                            draw_text("Click on a Location to Travel There:", SMALL_FONT, ORANGE, (1503, 200))
                            for location in Game.LOCATIONS:
                                if check_click_location(location):
                                    Game.SELECTED_LOCATION = location
                            if Game.SELECTED_LOCATION is not None:
                                location_button = Button("Confirm " + Game.SELECTED_LOCATION.displayName, 1503, 540, 60)
                                if location_button.check_click():
                                    Game.PLAYERS[Game.CLIENT_NUMBER].location = Game.SELECTED_LOCATION
                                    Game.REVEALING_CARD[0] == "Wait"
                                    Game.NETWORK.send(("MoveLocation", Game.PLAYERS[Game.CLIENT_NUMBER]))
                                    Game.SELECTED_LOCATION = None
                        elif Game.DISPLAYED_CLUE_CARD.title == "You Don't Say!":
                            if Game.CARD_SENT == 0:
                                draw_text("Choose a Card to Send to the Next Player:", SMALL_FONT, ORANGE, (1503, 200))
                                for x in range(len(Game.PLAYERS[Game.CLIENT_NUMBER].cards)):
                                    is_reveal = False
                                    card = Game.PLAYERS[Game.CLIENT_NUMBER].cards[x]
                                    for reveal in Game.REVEALED_CARDS:
                                        if reveal.displayName == card.displayName:
                                            is_reveal = True
                                            break
                                    if is_reveal:
                                        continue
                                    button = Button(card.displayName, 1503, 300 + (x * 70), 60)
                                    if button.check_click():
                                        Game.CARD_SENT = 1
                                        Game.NETWORK.send(("ShowCard", Game.PLAYERS[Game.CLIENT_NUMBER], card))
                                        break
                            elif Game.CARD_SENT == 1:
                                draw_text("Waiting for the others to choose", SMALL_FONT, ORANGE, (1503, 200))
                            elif Game.CARD_SENT == 2:
                                draw_text(Game.CARDS_FOR_SHOWING[0][0].playerName + " has shown you " + Game.CARDS_FOR_SHOWING[0][1].displayName, SMALL_FONT, Game.CARDS_FOR_SHOWING[0][0].playerColour, (1503, 500))
                                continue_button = Button("Continue", 1503, 560, 60)
                                if continue_button.check_click():
                                    Game.CARDS_FOR_SHOWING.clear()
                                    Game.CARD_SENT = 0
                                    Game.REVEALING_CARD[0] = "Wait"
                                    Game.NETWORK.send("TurnClick")
                        elif Game.DISPLAYED_CLUE_CARD.title == "Dun-Dun-Duuun!":
                            if Game.CARD_SENT == 0:
                                draw_text("Choose a Card to Reveal:", SMALL_FONT, ORANGE, (1503, 200))
                                for x in range(len(Game.PLAYERS[Game.CLIENT_NUMBER].cards)):
                                    is_reveal = False
                                    card = Game.PLAYERS[Game.CLIENT_NUMBER].cards[x]
                                    for reveal in Game.REVEALED_CARDS:
                                        if reveal.displayName == card.displayName:
                                            is_reveal = True
                                            break
                                    if is_reveal:
                                        continue
                                    button = Button(card.displayName, 1503, 300 + (x * 70), 60)
                                    if button.check_click():
                                        Game.REVEALED_CARDS.append(card)
                                        Game.CARD_SENT = 1
                                        Game.NETWORK.send(("SentCard", Game.PLAYERS[Game.CLIENT_NUMBER], card))
                                        break
                            elif Game.CARD_SENT == 1:
                                draw_text("Waiting for the others to choose", SMALL_FONT, ORANGE, (1503, 200))
                            elif Game.CARD_SENT == 2:
                                for x in range(len(Game.CARDS_FOR_SHOWING)):
                                    player = Game.CARDS_FOR_SHOWING[x][0]
                                    card = Game.CARDS_FOR_SHOWING[x][1]
                                    draw_text(player.playerName + " has revealed " + card.displayName, SMALL_FONT, player.playerColour, (1503, 420 + (x * 40)))
                                continue_button = Button("Continue", 1503, 430 + (len(Game.CARDS_FOR_SHOWING) * 40), 60)
                                if continue_button.check_click():
                                    Game.CARDS_FOR_SHOWING.clear()
                                    Game.CARD_SENT = 0
                                    Game.REVEALING_CARD[0] = "Wait"
                                    Game.NETWORK.send("TurnClick")
                        elif Game.DISPLAYED_CLUE_CARD.title == "Creeeeak!" or Game.DISPLAYED_CLUE_CARD.title == "Wink Wink!":
                            draw_text("Waiting for " + current_player.playerName + " to Choose a Location", SMALL_FONT, ORANGE, (1503, 540))
                        elif Game.DISPLAYED_CLUE_CARD.title == "Look What I Found!":
                            draw_text("Waiting for " + current_player.playerName + " to Choose a Weapon", SMALL_FONT, ORANGE, (1503, 540))
                        elif Game.DISPLAYED_CLUE_CARD.title == "Airtight Alibi!":
                            draw_text("Waiting for " + current_player.playerName + " to Choose a Suspect", SMALL_FONT, ORANGE, (1503, 540))
            elif Game.TURN_STAGE == TurnStage.GAME_OVER:
                if Game.WINNER == "Nobody":
                    draw_text("Nobody has won the Game!", SMALL_FONT, ORANGE, (1503, 540))
                else:
                    draw_text(Game.WINNER.playerName + " has won the Game!", SMALL_FONT, Game.WINNER.playerColour, (1503, 540))
            elif Game.TURN_STAGE == TurnStage.SHOW_CARD:
                if not Game.CLUE_SHEET_OPEN:
                    if Game.SHOWN_CARD is not None:
                        if Game.SHOWN_CARD == "Wait":
                            draw_text("Waiting for others to continue", SMALL_FONT, ORANGE, (1503, 540))
                        else:
                            draw_text("Suspect: " + Game.PLAYER_GUESS[0].displayName, SMALL_FONT, ORANGE, (1503, 450))
                            draw_text("Weapon: " + Game.PLAYER_GUESS[1].displayName, SMALL_FONT, ORANGE, (1503, 590))
                            draw_text("Location: " + Game.PLAYER_GUESS[2].displayName, SMALL_FONT, ORANGE, (1503, 730))
                            draw_text(Game.PLAYER_SHOWING.playerName + " has showed " + current_player.playerName + " a card", SMALL_FONT, Game.PLAYER_SHOWING.playerColour, (1503, 400))
                            continue_button = Button("Continue", 1503, 780, 60)
                            if continue_button.check_click():
                                Game.NETWORK.send("TurnClick")
                                Game.SHOWN_CARD = "Wait"
                    else:
                        draw_text("Suspect: " + Game.PLAYER_GUESS[0].displayName, SMALL_FONT, ORANGE, (1503, 300))
                        draw_text("Weapon: " + Game.PLAYER_GUESS[1].displayName, SMALL_FONT, ORANGE, (1503, 440))
                        draw_text("Location: " + Game.PLAYER_GUESS[2].displayName, SMALL_FONT, ORANGE, (1503, 580))
                        if Game.PLAYER_SHOWING is not None:
                            if Game.PLAYER_SHOWING.playerIndex == Game.CLIENT_NUMBER:
                                draw_text("You have card(s) to show!", SMALL_FONT, ORANGE, (1503, 650))
                                to_continue = True
                                for x in range(len(Game.PLAYER_GUESS)):
                                    is_reveal = False
                                    for reveal in Game.REVEALED_CARDS:
                                        if reveal.displayName == Game.PLAYER_GUESS[x].displayName:
                                            is_reveal = True
                                            break
                                    if is_reveal:
                                        continue
                                    for card in Game.PLAYERS[Game.CLIENT_NUMBER].cards:
                                        if card.displayName == Game.PLAYER_GUESS[x].displayName:
                                            button = Button(card.displayName, 1503, 700 + (x * 65), 60)
                                            if button.check_click():
                                                Game.SHOWN_CARD = card
                                                Game.NETWORK.send(("ShownCard", Game.SHOWN_CARD))
                                                to_continue = False
                                        if not to_continue:
                                            break
                                    if not to_continue:
                                        break
                            else:
                                draw_text(Game.PLAYER_SHOWING.playerName + " has to show a card!", SMALL_FONT, Game.PLAYER_SHOWING.playerColour, (1503, 650))
                        else:
                            draw_text("Nobody else has the cards accused!", SMALL_FONT, ORANGE, (1503, 650))
                            continue_button = Button("Continue", 1503, 780, 60)
                            if continue_button.check_click():
                                Game.NETWORK.send("TurnClick")
                                Game.SHOWN_CARD = "Wait"
            elif Game.TURN_STAGE == TurnStage.FINAL_ACCUSATION:
                draw_text(current_player.playerName + " is making a Final Accusation!", SMALL_FONT, current_player.playerColour, (1503, 150))
                if not Game.CLUE_SHEET_OPEN:
                    pass
            else:
                if not Game.CLUE_SHEET_OPEN:
                    if Game.DISPLAYED_CLUE_CARD is not None:
                        draw_clue_card(Game.DISPLAYED_CLUE_CARD, (1349, 350))
                    else:
                        DICE1.draw((1417, 414))
                        DICE2.draw((1513, 414))
        elif Game.TURN_STAGE == TurnStage.START:
            if current_player.playerDied:
                draw_text("You have already failed, no turn for you", SMALL_FONT, ORANGE, (1503, 100))
                end_turn_button = Button("End Turn", 1503, 145, 60)
                if end_turn_button.check_click():
                    Game.TURN_STAGE = TurnStage.START
                    if Game.CURRENT_PLAYER == Game.PLAYER_COUNT - 1:
                        Game.CURRENT_PLAYER = 0
                    else:
                        Game.CURRENT_PLAYER += 1
                    Game.NETWORK.send("EndTurn")
                return
            Game.TURN_STAGE = TurnStage.ROLL_DICE
        elif Game.TURN_STAGE == TurnStage.ROLL_DICE:
            if not Game.CLUE_SHEET_OPEN:
                DICE1.draw((1417, 414))
                DICE2.draw((1513, 414))
                roll_button = Button("Roll the Dice", 1507, 540, 60)
                if roll_button.check_click():
                    DICE1.value = random.randrange(1, 7)
                    DICE2.value = random.randrange(1, 7)
                    if Game.CLUE_CARDS_ACTIVE and len(Game.CLUE_CARD_DECK) > 0:
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
            draw_text("Select a Place to go or Choose your Option:", SMALL_FONT, ORANGE, (1503, 100))
            if Game.SQUARE_FAIL_DISTANCE != 0:
                draw_text("That square is too far away! " + str(Game.SQUARE_FAIL_DISTANCE), SMALL_FONT, ORANGE, (1503, 180))
            for location in Game.LOCATIONS:
                if check_click_location(location):
                    for square in location.enterSquares:
                        finder = AStarFinder()
                        if isinstance(current_player.location, Square):
                            path = finder.find_path(GRID.node(current_player.location.square[0], current_player.location.square[1]), GRID.node(square.square[0], square.square[1]), GRID)[0]
                            GRID.cleanup()
                            if len(path) - 1 <= DICE1.value + DICE2.value:
                                Game.SELECTED_LOCATION = location
                                Game.SELECTED_SQUARE = None
                                Game.SQUARE_FAIL_DISTANCE = 0
                                break
                        else:
                            shortest_number = 0
                            for enter_square in Game.PLAYERS[Game.CLIENT_NUMBER].location.enterSquares:
                                path = finder.find_path(GRID.node(enter_square.square[0], enter_square.square[1]), GRID.node(square.square[0], square.square[1]), GRID)[0]
                                GRID.cleanup()
                                if len(path) - 1 > DICE1.value + DICE2.value:
                                    shortest_number = min(shortest_number, len(path) - 1)
                                else:
                                    shortest_number = 420
                                    Game.SELECTED_SQUARE = None
                                    Game.SQUARE_FAIL_DISTANCE = 0
                                    Game.SELECTED_LOCATION = location
                                    break
                            if shortest_number == 420:
                                break
                            Game.SQUARE_FAIL_DISTANCE = shortest_number
                            Game.SELECTED_LOCATION = None
                            Game.SELECTED_SQUARE = None
            for square in SQUARES:
                result = check_click_square(square)
                if result is None:
                    continue
                elif isinstance(result, Square):
                    Game.SELECTED_SQUARE = result
                    Game.SQUARE_FAIL_DISTANCE = 0
                    Game.SELECTED_LOCATION = None
                    break
                else:
                    Game.SQUARE_FAIL_DISTANCE = result
                    Game.SELECTED_SQUARE = None
                    Game.SELECTED_LOCATION = None
            if not Game.CLUE_SHEET_OPEN:
                DICE1.draw((1417, 414))
                DICE2.draw((1513, 414))
                if Game.SELECTED_SQUARE is not None:
                    square_button = Button("Go to the Square", 1507, 540, 60)
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
                    location_button = Button("Go to the " + Game.SELECTED_LOCATION.displayName, 1507, 540, 60)
                    if location_button.check_click():
                        current_player.location = Game.SELECTED_LOCATION
                        Game.SELECTED_LOCATION = None
                        Game.TURN_STAGE = TurnStage.MAKE_GUESS
                        Game.PLAYER_GUESS[2] = current_player.location.ref
                        Game.NETWORK.send(("TurnPlayer", Game.TURN_STAGE, current_player))
                if isinstance(current_player.location, Location):
                    stay_button = Button("Stay where you are", 1507, 610, 60)
                    if stay_button.check_click():
                        Game.TURN_STAGE = TurnStage.MAKE_GUESS
                        Game.PLAYER_GUESS[2] = current_player.location.ref
                        Game.NETWORK.send(("Turn", Game.TURN_STAGE))
                    for x in range(len(current_player.location.passage)):
                        passage_button = Button("Passage to " + current_player.location.passage[x].displayName, 1507, 680 + (x * 65), 60)
                        if passage_button.check_click():
                            current_player.location = current_player.location.passage[x]
                            Game.TURN_STAGE = TurnStage.MAKE_GUESS
                            Game.PLAYER_GUESS[2] = current_player.location.ref
                            Game.NETWORK.send(("TurnPlayer", Game.TURN_STAGE, current_player))
                            break
        elif Game.TURN_STAGE == TurnStage.DRAW_CLUE_CARD:
            draw_text("Draw a Clue Card", SMALL_FONT, ORANGE, (1503, 100))
            clue_rect = pygame.Rect((515, 463), (154, 240))
            if Game.DISPLAYED_CLUE_CARD is None and Game.LEFT_MOUSE_RELEASED and len(Game.CLUE_CARD_DECK) > 0 and clue_rect.collidepoint(pygame.mouse.get_pos()):
                Game.DISPLAYED_CLUE_CARD = Game.CLUE_CARD_DECK.pop()
                Game.CLUE_TO_DRAW -= 1
                Game.NETWORK.send(("Clue", Game.DISPLAYED_CLUE_CARD))
                if Game.DISPLAYED_CLUE_CARD.card is not None:
                    Game.REVEALING_CARD[0] = Game.DISPLAYED_CLUE_CARD.card
                    for player in Game.PLAYERS:
                        for card in player.cards:
                            if card.displayName == Game.REVEALING_CARD[0].displayName:
                                Game.REVEALED_CARDS.append(card)
                                Game.REVEALING_CARD[1] = player
                                break
                        if Game.REVEALING_CARD[1] is not None:
                            break
            if not Game.CLUE_SHEET_OPEN:
                if Game.DISPLAYED_CLUE_CARD is not None:
                    draw_clue_card(Game.DISPLAYED_CLUE_CARD, (1349, 350))
                    continue_button = Button("Continue", 1503, 870, 60)
                    if continue_button.check_click():
                        Game.TURN_STAGE = TurnStage.USE_CLUE_CARD
                        Game.NETWORK.send(("Turn", Game.TURN_STAGE))
                else:
                    DICE1.draw((1417, 414))
                    DICE2.draw((1513, 414))
        elif Game.TURN_STAGE == TurnStage.MAKE_GUESS:
            if isinstance(current_player.location, Location) and current_player.location.card is not None and current_player.location.displayName not in Game.SEEN_CARDS:
                if not Game.CLUE_SHEET_OPEN:
                    draw_text("You are in a location with a card:", SMALL_FONT, ORANGE, (1503, 480))
                    draw_text(current_player.location.card.displayName, SMALL_FONT, ORANGE, (1503, 540))
                    continue_button = Button("Continue", 1503, 600, 60)
                    if continue_button.check_click():
                        Game.SEEN_CARDS.append(current_player.location.displayName)
            else:
                draw_text("Select a Suspect and Weapon:", SMALL_FONT, ORANGE, (1503, 100))
                if not Game.CLUE_SHEET_OPEN:
                    if Game.ACCUSE_SUSPECT:
                        scarlett_button = Button("Miss Scarlett", 1503, 365, 60)
                        if scarlett_button.check_click():
                            Game.ACCUSE_SUSPECT = False
                            Game.PLAYER_GUESS[0] = MISS_SCARLETT
                        mustard_button = Button("Col. Mustard", 1503, 435, 60)
                        if mustard_button.check_click():
                            Game.ACCUSE_SUSPECT = False
                            Game.PLAYER_GUESS[0] = COL_MUSTARD
                        orchid_button = Button("Dr Orchid", 1503, 505, 60)
                        if orchid_button.check_click():
                            Game.ACCUSE_SUSPECT = False
                            Game.PLAYER_GUESS[0] = DR_ORCHID
                        green_button = Button("Rev. Green", 1503, 575, 60)
                        if green_button.check_click():
                            Game.ACCUSE_SUSPECT = False
                            Game.PLAYER_GUESS[0] = REV_GREEN
                        peacock_button = Button("Mrs Peacock", 1503, 645, 60)
                        if peacock_button.check_click():
                            Game.ACCUSE_SUSPECT = False
                            Game.PLAYER_GUESS[0] = MRS_PEACOCK
                        plum_button = Button("Prof. Plum", 1503, 715, 60)
                        if plum_button.check_click():
                            Game.ACCUSE_SUSPECT = False
                            Game.PLAYER_GUESS[0] = PROF_PLUM
                    elif Game.GUESS_WEAPON:
                        candlestick_button = Button("Candlestick", 1503, 365, 60)
                        if candlestick_button.check_click():
                            Game.GUESS_WEAPON = False
                            Game.PLAYER_GUESS[1] = CANDLESTICK
                        dagger_button = Button("Dagger", 1503, 435, 60)
                        if dagger_button.check_click():
                            Game.GUESS_WEAPON = False
                            Game.PLAYER_GUESS[1] = DAGGER
                        lead_pipe_button = Button("Lead Pipe", 1503, 505, 60)
                        if lead_pipe_button.check_click():
                            Game.GUESS_WEAPON = False
                            Game.PLAYER_GUESS[1] = LEAD_PIPE
                        revolver_button = Button("Revolver", 1503, 575, 60)
                        if revolver_button.check_click():
                            Game.GUESS_WEAPON = False
                            Game.PLAYER_GUESS[1] = REVOLVER
                        rope_button = Button("Rope", 1503, 645, 60)
                        if rope_button.check_click():
                            Game.GUESS_WEAPON = False
                            Game.PLAYER_GUESS[1] = ROPE
                        wrench_button = Button("Wrench", 1503, 715, 60)
                        if wrench_button.check_click():
                            Game.GUESS_WEAPON = False
                            Game.PLAYER_GUESS[1] = WRENCH
                    else:
                        if Game.PLAYER_GUESS[0] is None:
                            suspect_button = Button("Accuse a Suspect", 1503, 400, 60)
                            if suspect_button.check_click():
                                Game.ACCUSE_SUSPECT = True
                        else:
                            draw_text("Suspect: " + Game.PLAYER_GUESS[0].displayName, SMALL_FONT, ORANGE, (1503, 400))
                        if Game.PLAYER_GUESS[1] is None:
                            weapon_button = Button("Guess a Weapon", 1503, 540, 60)
                            if weapon_button.check_click():
                                Game.GUESS_WEAPON = True
                        else:
                            draw_text("Weapon: " + Game.PLAYER_GUESS[1].displayName, SMALL_FONT, ORANGE, (1503, 540))
                        draw_text("Location: " + Game.PLAYER_GUESS[2].displayName, SMALL_FONT, ORANGE, (1503, 680))
                        if Game.PLAYER_GUESS[0] is not None and Game.PLAYER_GUESS[1] is not None:
                            continue_button = Button("Continue", 1503, 740, 60)
                            if continue_button.check_click():
                                print("Revealed Cards: " + str(len(Game.REVEALED_CARDS)))
                                for reveal in Game.REVEALED_CARDS:
                                    print(reveal.displayName)
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
                                        is_revealed = False
                                        for revealed in Game.REVEALED_CARDS:
                                            if card.displayName == revealed.displayName:
                                                is_revealed = True
                                                break
                                        if is_revealed:
                                            continue
                                        if card.displayName == Game.PLAYER_GUESS[0].displayName or card.displayName == Game.PLAYER_GUESS[1].displayName or card.displayName == Game.PLAYER_GUESS[2].displayName:
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
        elif Game.TURN_STAGE == TurnStage.SHOW_CARD:
            if not Game.CLUE_SHEET_OPEN:
                if Game.SHOWN_CARD is not None:
                    if Game.SHOWN_CARD == "Wait":
                        draw_text("Waiting for others to continue", SMALL_FONT, ORANGE, (1503, 540))
                    else:
                        draw_text("Suspect: " + Game.PLAYER_GUESS[0].displayName, SMALL_FONT, ORANGE, (1503, 450))
                        draw_text("Weapon: " + Game.PLAYER_GUESS[1].displayName, SMALL_FONT, ORANGE, (1503, 590))
                        draw_text("Location: " + Game.PLAYER_GUESS[2].displayName, SMALL_FONT, ORANGE, (1503, 730))
                        draw_text(Game.PLAYER_SHOWING.playerName + " showed you the \"" + Game.SHOWN_CARD.displayName + "\" card", SMALL_FONT, Game.PLAYER_SHOWING.playerColour, (1503, 400))
                        continue_button = Button("Continue", 1503, 780, 60)
                        if continue_button.check_click():
                            Game.NETWORK.send("TurnClick")
                            Game.SHOWN_CARD = "Wait"
                else:
                    draw_text("Suspect: " + Game.PLAYER_GUESS[0].displayName, SMALL_FONT, ORANGE, (1503, 400))
                    draw_text("Weapon: " + Game.PLAYER_GUESS[1].displayName, SMALL_FONT, ORANGE, (1503, 540))
                    draw_text("Location: " + Game.PLAYER_GUESS[2].displayName, SMALL_FONT, ORANGE, (1503, 680))
                    if Game.PLAYER_SHOWING is not None:
                        draw_text(Game.PLAYER_SHOWING.playerName + " has to show a card!", SMALL_FONT, ORANGE, (1503, 750))
                    else:
                        draw_text("Nobody else has the cards accused!", SMALL_FONT, ORANGE, (1503, 750))
                        continue_button = Button("Continue", 1503, 810, 60)
                        if continue_button.check_click():
                            Game.NETWORK.send("TurnClick")
                            Game.SHOWN_CARD = "Wait"
        elif Game.TURN_STAGE == TurnStage.END_TURN:
            if not Game.CLUE_SHEET_OPEN:
                draw_text("Your turn is over now", SMALL_FONT, ORANGE, (1503, 540))
                end_button = Button("End Turn", 1503, 600, 60)
                if end_button.check_click():
                    Game.TURN_STAGE = TurnStage.START
                    if Game.CURRENT_PLAYER == Game.PLAYER_COUNT - 1:
                        Game.CURRENT_PLAYER = 0
                    else:
                        Game.CURRENT_PLAYER += 1
                    Game.NETWORK.send("EndTurn")
                if not current_player.playerDied:
                    final_button = Button("Final Accusation", 1503, 670, 60)
                    if final_button.check_click():
                        Game.TURN_STAGE = TurnStage.FINAL_ACCUSATION
                        Game.NETWORK.send("FinalAccusation")
        elif Game.TURN_STAGE == TurnStage.FINAL_ACCUSATION:
            if Game.WINNER == "Nobody":
                draw_text("Sorry, you got the accusation wrong!", SMALL_FONT, ORANGE, (1503, 100))
                continue_button = Button("Continue", 1503, 600, 60)
                if continue_button.check_click():
                    Game.TURN_STAGE = TurnStage.END_TURN
                    Game.WINNER = None
            else:
                draw_text("You are making a Final Accusation!", SMALL_FONT, ORANGE, (1503, 100))
                if not Game.CLUE_SHEET_OPEN:
                    if Game.ACCUSE_SUSPECT:
                        scarlett_button = Button("Miss Scarlett", 1503, 365, 60)
                        if scarlett_button.check_click():
                            Game.ACCUSE_SUSPECT = False
                            Game.PLAYER_GUESS[0] = MISS_SCARLETT
                        mustard_button = Button("Col. Mustard", 1503, 435, 60)
                        if mustard_button.check_click():
                            Game.ACCUSE_SUSPECT = False
                            Game.PLAYER_GUESS[0] = COL_MUSTARD
                        orchid_button = Button("Dr Orchid", 1503, 505, 60)
                        if orchid_button.check_click():
                            Game.ACCUSE_SUSPECT = False
                            Game.PLAYER_GUESS[0] = DR_ORCHID
                        green_button = Button("Rev. Green", 1503, 575, 60)
                        if green_button.check_click():
                            Game.ACCUSE_SUSPECT = False
                            Game.PLAYER_GUESS[0] = REV_GREEN
                        peacock_button = Button("Mrs Peacock", 1503, 645, 60)
                        if peacock_button.check_click():
                            Game.ACCUSE_SUSPECT = False
                            Game.PLAYER_GUESS[0] = MRS_PEACOCK
                        plum_button = Button("Prof. Plum", 1503, 715, 60)
                        if plum_button.check_click():
                            Game.ACCUSE_SUSPECT = False
                            Game.PLAYER_GUESS[0] = PROF_PLUM
                    elif Game.GUESS_WEAPON:
                        candlestick_button = Button("Candlestick", 1503, 365, 60)
                        if candlestick_button.check_click():
                            Game.GUESS_WEAPON = False
                            Game.PLAYER_GUESS[1] = CANDLESTICK
                        dagger_button = Button("Dagger", 1503, 435, 60)
                        if dagger_button.check_click():
                            Game.GUESS_WEAPON = False
                            Game.PLAYER_GUESS[1] = DAGGER
                        lead_pipe_button = Button("Lead Pipe", 1503, 505, 60)
                        if lead_pipe_button.check_click():
                            Game.GUESS_WEAPON = False
                            Game.PLAYER_GUESS[1] = LEAD_PIPE
                        revolver_button = Button("Revolver", 1503, 575, 60)
                        if revolver_button.check_click():
                            Game.GUESS_WEAPON = False
                            Game.PLAYER_GUESS[1] = REVOLVER
                        rope_button = Button("Rope", 1503, 645, 60)
                        if rope_button.check_click():
                            Game.GUESS_WEAPON = False
                            Game.PLAYER_GUESS[1] = ROPE
                        wrench_button = Button("Wrench", 1503, 715, 60)
                        if wrench_button.check_click():
                            Game.GUESS_WEAPON = False
                            Game.PLAYER_GUESS[1] = WRENCH
                    elif Game.GUESS_LOCATION:
                        ballroom_button = Button("Ballroom", 1503, 260, 60)
                        if ballroom_button.check_click():
                            Game.GUESS_LOCATION = False
                            Game.PLAYER_GUESS[2] = BALLROOM_CARD
                        billiard_button = Button("Billiard Room", 1503, 330, 60)
                        if billiard_button.check_click():
                            Game.GUESS_LOCATION = False
                            Game.PLAYER_GUESS[2] = BILLIARD_ROOM_CARD
                        conservatory_button = Button("Conservatory", 1503, 400, 60)
                        if conservatory_button.check_click():
                            Game.GUESS_LOCATION = False
                            Game.PLAYER_GUESS[2] = CONSERVATORY_CARD
                        dining_button = Button("Dining Room", 1503, 470, 60)
                        if dining_button.check_click():
                            Game.GUESS_LOCATION = False
                            Game.PLAYER_GUESS[2] = DINING_ROOM_CARD
                        hall_button = Button("Hall", 1503, 540, 60)
                        if hall_button.check_click():
                            Game.GUESS_LOCATION = False
                            Game.PLAYER_GUESS[2] = HALL_CARD
                        kitchen_button = Button("Kitchen", 1503, 610, 60)
                        if kitchen_button.check_click():
                            Game.GUESS_LOCATION = False
                            Game.PLAYER_GUESS[2] = KITCHEN_CARD
                        library_button = Button("Library", 1503, 680, 60)
                        if library_button.check_click():
                            Game.GUESS_LOCATION = False
                            Game.PLAYER_GUESS[2] = LIBRARY_CARD
                        lounge_button = Button("Lounge", 1503, 750, 60)
                        if lounge_button.check_click():
                            Game.GUESS_LOCATION = False
                            Game.PLAYER_GUESS[2] = LOUNGE_CARD
                        study_button = Button("Study", 1503, 820, 60)
                        if study_button.check_click():
                            Game.GUESS_LOCATION = False
                            Game.PLAYER_GUESS[2] = STUDY_CARD
                    else:
                        if Game.PLAYER_GUESS[0] is None:
                            suspect_button = Button("Accuse a Suspect", 1503, 400, 60)
                            if suspect_button.check_click():
                                Game.ACCUSE_SUSPECT = True
                        else:
                            draw_text("Suspect: " + Game.PLAYER_GUESS[0].displayName, SMALL_FONT, ORANGE, (1503, 400))
                        if Game.PLAYER_GUESS[1] is None:
                            weapon_button = Button("Guess a Weapon", 1503, 540, 60)
                            if weapon_button.check_click():
                                Game.GUESS_WEAPON = True
                        else:
                            draw_text("Weapon: " + Game.PLAYER_GUESS[1].displayName, SMALL_FONT, ORANGE, (1503, 540))
                        if Game.PLAYER_GUESS[2] is None:
                            location_button = Button("Guess the Location", 1503, 680, 60)
                            if location_button.check_click():
                                Game.GUESS_LOCATION = True
                        else:
                            draw_text("Location: " + Game.PLAYER_GUESS[2].displayName, SMALL_FONT, ORANGE, (1503, 680))
                        back_button = Button("Back", 1503, 750, 60)
                        if back_button.check_click():
                            Game.TURN_STAGE = TurnStage.END_TURN
                            Game.PLAYER_GUESS[0] = None
                            Game.PLAYER_GUESS[1] = None
                            Game.PLAYER_GUESS[2] = None
                            Game.NETWORK.send(("Turn", Game.TURN_STAGE))
                        if Game.PLAYER_GUESS[0] is not None and Game.PLAYER_GUESS[1] is not None and Game.PLAYER_GUESS[2] is not None:
                            continue_button = Button("Make Accusation", 1503, 820, 60)
                            if continue_button.check_click():
                                has_won = Game.NETWORK.send(("Final", Game.PLAYER_GUESS))
                                if has_won:
                                    Game.WINNER = Game.PLAYERS[Game.CLIENT_NUMBER]
                                    Game.TURN_STAGE = TurnStage.GAME_OVER
                                else:
                                    Game.WINNER = "Nobody"
                                    current_player.playerDied = True
                                    Game.NETWORK.send(("JustPlayer", current_player))
                                    players_died = 0
                                    for player in Game.PLAYERS:
                                        if player.playerDied:
                                            players_died += 1
                                    if players_died == Game.PLAYER_COUNT:
                                        Game.TURN_STAGE = TurnStage.GAME_OVER
        elif Game.TURN_STAGE == TurnStage.GAME_OVER:
            draw_text("The Game is now Over!", SMALL_FONT, ORANGE, (1503, 100))
            if Game.WINNER == "Nobody":
                draw_text("Nobody has won the Game!", SMALL_FONT, ORANGE, (1503, 540))
            else:
                draw_text(Game.WINNER.playerName + " has won the Game!", SMALL_FONT, Game.WINNER.playerColour, (1503, 540))
        elif Game.TURN_STAGE == TurnStage.USE_CLUE_CARD:
            draw_text("Using the Clue Card!", SMALL_FONT, ORANGE, (1503, 100))
            if not Game.CLUE_SHEET_OPEN:
                if Game.REVEALING_CARD[0] == "Wait":  # Waiting for Continue
                    draw_text("Waiting for others to continue", SMALL_FONT, ORANGE, (1503, 540))
                elif Game.COMPLETED_PASSAGE:
                    draw_text("A Secret Passage is in the " + Game.SELECTED_LOCATION.displayName, SMALL_FONT, ORANGE, (1503, 540))
                    continue_button = Button("Continue", 1503, 610, 60)
                    if continue_button.check_click():
                        Game.NETWORK.send("TurnClick")
                        Game.REVEALING_CARD[0] = "Wait"
                        Game.SELECTED_LOCATION = None
                        Game.COMPLETED_PASSAGE = False
                elif Game.PLAYER_CHOOSING is not None:  # Waiting for a Player to Choose
                    draw_text("Waiting for " + Game.PLAYER_CHOOSING.playerName + " to choose a card", SMALL_FONT, ORANGE, (1503, 540))
                elif Game.DISPLAYED_CLUE_CARD is not None:
                    if Game.REVEALING_CARD[0] is not None:  # Reveal Card
                        if Game.REVEALING_CARD[1] is None:
                            draw_text("Nobody has the \"" + Game.REVEALING_CARD[0].displayName + "\" card", SMALL_FONT,
                                      ORANGE, (1503, 540))
                        else:
                            draw_text(Game.REVEALING_CARD[1].playerName + " has the \"" + Game.REVEALING_CARD[
                                0].displayName + "\" card", SMALL_FONT, ORANGE, (1503, 540))
                        continue_button = Button("Continue", 1503, 610, 60)
                        if continue_button.check_click():
                            Game.NETWORK.send("TurnClick")
                            Game.REVEALING_CARD[0] = "Wait"
                    elif Game.DISPLAYED_CLUE_CARD.title == "Screeeeam!":  # Go to a Room you Choose
                        draw_text("Click on a Location to Travel There:", SMALL_FONT, ORANGE, (1503, 200))
                        for location in Game.LOCATIONS:
                            if check_click_location(location):
                                Game.SELECTED_LOCATION = location
                        if Game.SELECTED_LOCATION is not None:
                            location_button = Button("Confirm " + Game.SELECTED_LOCATION.displayName, 1503, 540, 60)
                            if location_button.check_click():
                                current_player.location = Game.SELECTED_LOCATION
                                Game.REVEALING_CARD[0] = "Wait"
                                Game.NETWORK.send(("MoveLocation", current_player))
                                Game.SELECTED_LOCATION = None
                    elif Game.DISPLAYED_CLUE_CARD.title == "You Don't Say!":  # Show a Card to the Next Player:
                        if Game.CARD_SENT == 0:
                            draw_text("Choose a Card to Send to the Next Player:", SMALL_FONT, ORANGE, (1503, 200))
                            for x in range(len(current_player.cards)):
                                is_reveal = False
                                card = current_player.cards[x]
                                for reveal in Game.REVEALED_CARDS:
                                    if reveal.displayName == card.displayName:
                                        is_reveal = True
                                        break
                                if is_reveal:
                                    continue
                                button = Button(card.displayName, 1503, 300 + (x * 70), 60)
                                if button.check_click():
                                    Game.CARD_SENT = 1
                                    Game.NETWORK.send(("ShowCard", current_player, card))
                                    break
                        elif Game.CARD_SENT == 1:
                            draw_text("Waiting for the others to choose", SMALL_FONT, ORANGE, (1503, 200))
                        elif Game.CARD_SENT == 2:
                            draw_text(Game.CARDS_FOR_SHOWING[0][0].playerName + " has shown you " + Game.CARDS_FOR_SHOWING[0][1].displayName, SMALL_FONT, Game.CARDS_FOR_SHOWING[0][0].playerColour, (1503, 500))
                            continue_button = Button("Continue", 1503, 560, 60)
                            if continue_button.check_click():
                                Game.CARDS_FOR_SHOWING.clear()
                                Game.CARD_SENT = 0
                                Game.REVEALING_CARD[0] = "Wait"
                                Game.NETWORK.send("TurnClick")
                    elif Game.DISPLAYED_CLUE_CARD.title == "Dun-Dun-Duuun!":  # All Players Reveal a Card
                        if Game.CARD_SENT == 0:
                            draw_text("Choose a Card to Reveal:", SMALL_FONT, ORANGE, (1503, 200))
                            for x in range(len(current_player.cards)):
                                is_reveal = False
                                card = current_player.cards[x]
                                for reveal in Game.REVEALED_CARDS:
                                    if reveal.displayName == card.displayName:
                                        is_reveal = True
                                        break
                                if is_reveal:
                                    continue
                                button = Button(card.displayName, 1503, 300 + (x * 70), 60)
                                if button.check_click():
                                    Game.REVEALED_CARDS.append(card)
                                    Game.CARD_SENT = 1
                                    Game.NETWORK.send(("SentCard", current_player, card))
                                    break
                        elif Game.CARD_SENT == 1:
                            draw_text("Waiting for the others to choose", SMALL_FONT, ORANGE, (1503, 200))
                        elif Game.CARD_SENT == 2:
                            for x in range(len(Game.CARDS_FOR_SHOWING)):
                                player = Game.CARDS_FOR_SHOWING[x][0]
                                card = Game.CARDS_FOR_SHOWING[x][1]
                                draw_text(player.playerName + " has revealed " + card.displayName, SMALL_FONT, ORANGE, (1503, 420 + (x * 40)))
                            continue_button = Button("Continue", 1503, 430 + (len(Game.CARDS_FOR_SHOWING) * 40), 60)
                            if continue_button.check_click():
                                Game.CARDS_FOR_SHOWING.clear()
                                Game.CARD_SENT = 0
                                Game.REVEALING_CARD[0] = "Wait"
                                Game.NETWORK.send("TurnClick")
                    elif Game.DISPLAYED_CLUE_CARD.title == "Creeeeak!":  # Choose a Location to Connect the Passages
                        draw_text("Click a Location to Connect the Passages:", SMALL_FONT, ORANGE, (1503, 200))
                        for location in Game.LOCATIONS:
                            if location.displayName != "Conservatory" and location.displayName != "Lounge" and location.displayName != "Kitchen" and location.displayName != "Study" and check_click_location(location):
                                Game.SELECTED_LOCATION = location
                        if Game.SELECTED_LOCATION is not None:
                            location_button = Button("Confirm " + Game.SELECTED_LOCATION.displayName, 1503, 540, 60)
                            if location_button.check_click():
                                Game.SELECTED_LOCATION.passage.append(CONSERVATORY)
                                Game.SELECTED_LOCATION.passage.append(LOUNGE)
                                Game.SELECTED_LOCATION.passage.append(KITCHEN)
                                Game.SELECTED_LOCATION.passage.append(STUDY)
                                CONSERVATORY.passage.append(Game.SELECTED_LOCATION)
                                LOUNGE.passage.append(Game.SELECTED_LOCATION)
                                KITCHEN.passage.append(Game.SELECTED_LOCATION)
                                STUDY.passage.append(Game.SELECTED_LOCATION)
                                Game.NETWORK.send(("PassageLocation", Game.SELECTED_LOCATION))
                                Game.COMPLETED_PASSAGE = True
                    elif Game.DISPLAYED_CLUE_CARD.title == "Under Pressure!":  # Choose Player to Reveal a Card
                        draw_text("Choose a Player to Reveal a Card:", SMALL_FONT, ORANGE, (1503, 200))
                        for x in range(len(Game.PLAYERS)):
                            if Game.PLAYERS[x].playerIndex != Game.CLIENT_NUMBER:
                                button = Button(Game.PLAYERS[x].playerName, 1503, 360 + (x * 70), 60)
                                if button.check_click():
                                    Game.PLAYER_CHOOSING = Game.PLAYERS[x]
                                    Game.NETWORK.send(("PlayerChoosing", Game.PLAYER_CHOOSING))
                    elif Game.DISPLAYED_CLUE_CARD.title == "Wink Wink!":  # Choose a Location to Reveal
                        draw_text("Click a Location to be Revealed:", SMALL_FONT, ORANGE, (1503, 200))
                        for location in Game.LOCATIONS:
                            if check_click_location(location):
                                Game.SELECTED_LOCATION = location
                        if Game.SELECTED_LOCATION is not None:
                            location_button = Button("Confirm " + Game.SELECTED_LOCATION.displayName, 1503, 540, 60)
                            if location_button.check_click():
                                Game.REVEALING_CARD[0] = Game.SELECTED_LOCATION.ref
                                Game.NETWORK.send(("WeaponReveal", Game.SELECTED_LOCATION.ref))
                                Game.SELECTED_LOCATION = None
                            if Game.REVEALING_CARD[0] is not None:
                                for player in Game.PLAYERS:
                                    for card in player.cards:
                                        if card.displayName == Game.REVEALING_CARD[0].displayName:
                                            Game.REVEALED_CARDS.append(card)
                                            Game.REVEALING_CARD[1] = player
                                            break
                                    if Game.REVEALING_CARD[1] is not None:
                                        break
                    elif Game.DISPLAYED_CLUE_CARD.title == "Airtight Alibi!":  # Choose a Suspect to Reveal
                        draw_text("Choose a Suspect to be Revealed:", SMALL_FONT, ORANGE, (1503, 300))
                        scarlett_button = Button("Miss Scarlett", 1503, 365, 60)
                        if scarlett_button.check_click():
                            Game.REVEALING_CARD[0] = MISS_SCARLETT
                            Game.NETWORK.send(("WeaponReveal", MISS_SCARLETT))
                        mustard_button = Button("Col. Mustard", 1503, 435, 60)
                        if mustard_button.check_click():
                            Game.REVEALING_CARD[0] = COL_MUSTARD
                            Game.NETWORK.send(("WeaponReveal", COL_MUSTARD))
                        orchid_button = Button("Dr Orchid", 1503, 505, 60)
                        if orchid_button.check_click():
                            Game.REVEALING_CARD[0] = DR_ORCHID
                            Game.NETWORK.send(("WeaponReveal", DR_ORCHID))
                        green_button = Button("Rev. Green", 1503, 575, 60)
                        if green_button.check_click():
                            Game.REVEALING_CARD[0] = REV_GREEN
                            Game.NETWORK.send(("WeaponReveal", REV_GREEN))
                        peacock_button = Button("Mrs Peacock", 1503, 645, 60)
                        if peacock_button.check_click():
                            Game.REVEALING_CARD[0] = MRS_PEACOCK
                            Game.NETWORK.send(("WeaponReveal", MRS_PEACOCK))
                        plum_button = Button("Prof. Plum", 1503, 715, 60)
                        if plum_button.check_click():
                            Game.REVEALING_CARD[0] = PROF_PLUM
                            Game.NETWORK.send(("WeaponReveal", PROF_PLUM))
                        if Game.REVEALING_CARD[0] is not None:
                            for player in Game.PLAYERS:
                                for card in player.cards:
                                    if card.displayName == Game.REVEALING_CARD[0].displayName:
                                        Game.REVEALED_CARDS.append(card)
                                        Game.REVEALING_CARD[1] = player
                                        break
                                if Game.REVEALING_CARD[1] is not None:
                                    break
                    elif Game.DISPLAYED_CLUE_CARD.title == "Look What I Found!":  # Choose a Weapon to Reveal
                        draw_text("Choose a Weapon to be Revealed:", SMALL_FONT, ORANGE, (1503, 300))
                        candlestick_button = Button("Candlestick", 1503, 365, 60)
                        if candlestick_button.check_click():
                            Game.REVEALING_CARD[0] = CANDLESTICK
                            Game.NETWORK.send(("WeaponReveal", CANDLESTICK))
                        dagger_button = Button("Dagger", 1503, 435, 60)
                        if dagger_button.check_click():
                            Game.REVEALING_CARD[0] = DAGGER
                            Game.NETWORK.send(("WeaponReveal", DAGGER))
                        lead_pipe_button = Button("Lead Pipe", 1503, 505, 60)
                        if lead_pipe_button.check_click():
                            Game.REVEALING_CARD[0] = LEAD_PIPE
                            Game.NETWORK.send(("WeaponReveal", LEAD_PIPE))
                        revolver_button = Button("Revolver", 1503, 575, 60)
                        if revolver_button.check_click():
                            Game.REVEALING_CARD[0] = REVOLVER
                            Game.NETWORK.send(("WeaponReveal", REVOLVER))
                        rope_button = Button("Rope", 1503, 645, 60)
                        if rope_button.check_click():
                            Game.REVEALING_CARD[0] = ROPE
                            Game.NETWORK.send(("WeaponReveal", ROPE))
                        wrench_button = Button("Wrench", 1503, 715, 60)
                        if wrench_button.check_click():
                            Game.REVEALING_CARD[0] = WRENCH
                            Game.NETWORK.send(("WeaponReveal", WRENCH))
                        if Game.REVEALING_CARD[0] is not None:
                            for player in Game.PLAYERS:
                                for card in player.cards:
                                    if card.displayName == Game.REVEALING_CARD[0].displayName:
                                        Game.REVEALED_CARDS.append(card)
                                        Game.REVEALING_CARD[1] = player
                                        break
                                if Game.REVEALING_CARD[1] is not None:
                                    break
        if Game.HAS_SERVER:
            temp_button = Button("Quit", 1200, 1000, 60)
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
    if Game.CLUE_CARDS_ACTIVE and len(Game.CLUE_CARD_DECK) > 0:
        clue_rect = pygame.Rect((515, 463), (154, 240))
        pygame.draw.rect(WINDOW, BLACK, clue_rect, 0, 10)
        pygame.draw.rect(WINDOW, WHITE, clue_rect, 5, 10)
        draw_text("Clue", SMALL_FONT, WHITE, (592, 553))
        draw_text("Card", SMALL_FONT, WHITE, (592, 613))


def check_updates():
    if Game.SHOWN_CARD == "Wait":
        data = Game.NETWORK.send("!!")
        if data:
            Game.TURN_STAGE = TurnStage.END_TURN
            Game.PLAYER_GUESS[0] = None
            Game.PLAYER_GUESS[1] = None
            Game.PLAYER_GUESS[2] = None
            Game.SHOWN_CARD = None
    elif Game.REVEALING_CARD[0] == "Wait" and not Game.DISPLAYED_CLUE_CARD.title == "Screeeeam!":
        data = Game.NETWORK.send("!!")
        if data:
            Game.REVEALING_CARD[0] = None
            Game.REVEALING_CARD[1] = None
            Game.DISPLAYED_CLUE_CARD = None
            if Game.CLUE_TO_DRAW > 0 and len(Game.CLUE_CARD_DECK) > 0:
                Game.TURN_STAGE = TurnStage.DRAW_CLUE_CARD
            else:
                Game.TURN_STAGE = TurnStage.MOVEMENT
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
            if Game.DISPLAYED_CLUE_CARD is not None and Game.DISPLAYED_CLUE_CARD.title == "Screeeeam!":
                Game.REVEALING_CARD[0] = None
                Game.REVEALING_CARD[1] = None
                Game.DISPLAYED_CLUE_CARD = None
                if Game.CLUE_TO_DRAW > 0 and len(Game.CLUE_CARD_DECK) > 0:
                    Game.TURN_STAGE = TurnStage.DRAW_CLUE_CARD
                else:
                    Game.TURN_STAGE = TurnStage.MOVEMENT
        if "clue" in response:
            if Game.DISPLAYED_CLUE_CARD is None:
                Game.DISPLAYED_CLUE_CARD = Game.CLUE_CARD_DECK.pop()
                if Game.DISPLAYED_CLUE_CARD.card is not None:
                    Game.REVEALING_CARD[0] = Game.DISPLAYED_CLUE_CARD.card
                    for player in Game.PLAYERS:
                        for card in player.cards:
                            if card.displayName == Game.REVEALING_CARD[0].displayName:
                                Game.REVEALED_CARDS.append(card)
                                Game.REVEALING_CARD[1] = player
                                break
                        if Game.REVEALING_CARD[1] is not None:
                            break
            else:
                Game.DISPLAYED_CLUE_CARD = None
        if "card_show" in response:
            Game.PLAYER_SHOWING = response["card_show"][0]
            Game.PLAYER_GUESS = response["card_show"][1]
            print("Revealed Cards: " + str(len(Game.REVEALED_CARDS)))
            for reveal in Game.REVEALED_CARDS:
                print(reveal.displayName)
        if "show_card" in response:
            Game.SHOWN_CARD = response["show_card"]
        if "end_turn" in response:
            if Game.WINNER is not None:
                Game.WINNER = None
            Game.TURN_STAGE = TurnStage.START
            if Game.CURRENT_PLAYER == Game.PLAYER_COUNT - 1:
                Game.CURRENT_PLAYER = 0
            else:
                Game.CURRENT_PLAYER += 1
        if "final" in response:
            Game.TURN_STAGE = TurnStage.FINAL_ACCUSATION
        if "accuse" in response:
            Game.PLAYER_GUESS[0] = None
            Game.PLAYER_GUESS[1] = None
            Game.PLAYER_GUESS[2] = None
            if response["accuse"]:
                Game.WINNER = Game.PLAYERS[Game.CURRENT_PLAYER]
                Game.TURN_STAGE = TurnStage.GAME_OVER
            else:
                Game.WINNER = "Nobody"
                players_died = 0
                for player in Game.PLAYERS:
                    if player.playerDied:
                        players_died += 1
                if players_died == Game.PLAYER_COUNT:
                    Game.TURN_STAGE = TurnStage.GAME_OVER
        if "player_choosing" in response:
            Game.PLAYER_CHOOSING = response["player_choosing"]
        if "chosen_card" in response:
            Game.REVEALING_CARD[0] = response["chosen_card"]
            Game.REVEALING_CARD[1] = Game.PLAYER_CHOOSING
            for x in range(len(Game.PLAYERS[Game.PLAYER_CHOOSING.playerIndex].cards)):
                if Game.PLAYERS[Game.PLAYER_CHOOSING.playerIndex].cards[x].displayName == Game.REVEALING_CARD[0].displayName:
                    Game.REVEALED_CARDS.append(Game.REVEALING_CARD[0])
            Game.PLAYER_CHOOSING = None
        if "weapon_reveal" in response:
            Game.REVEALING_CARD[0] = response["weapon_reveal"]
            for player in Game.PLAYERS:
                for card in player.cards.copy():
                    if card.displayName == Game.REVEALING_CARD[0].displayName:
                        Game.REVEALED_CARDS.append(card)
                        Game.REVEALING_CARD[1] = player
                        break
                if Game.REVEALING_CARD[1] is not None:
                    break
        if "passage_location" in response:
            location = response["passage_location"]
            for loc in Game.LOCATIONS:
                if loc.displayName == location.displayName:
                    loc.passage.append(CONSERVATORY)
                    loc.passage.append(LOUNGE)
                    loc.passage.append(KITCHEN)
                    loc.passage.append(STUDY)
                    CONSERVATORY.passage.append(loc)
                    LOUNGE.passage.append(loc)
                    KITCHEN.passage.append(loc)
                    STUDY.passage.append(loc)
                    Game.COMPLETED_PASSAGE = True
                    Game.SELECTED_LOCATION = loc
        if "cards" in response:
            Game.CARD_SENT = 2
            for pair in response["cards"]:
                if not pair[0].playerName == Game.PLAYERS[Game.CLIENT_NUMBER].playerName:
                    Game.CARDS_FOR_SHOWING.append(pair)
        if "showings" in response:
            Game.CARD_SENT = 2
            if Game.CLIENT_NUMBER == 0:
                target = Game.PLAYER_COUNT - 1
            else:
                target = Game.CLIENT_NUMBER - 1
            for pair in response["showings"]:
                if pair[0].playerIndex == target:
                    Game.CARDS_FOR_SHOWING.append(pair)


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
        for player in Game.PLAYERS:
            if isinstance(player.location, Square) and player.location.square == square.square:
                return None
        finder = AStarFinder()
        if isinstance(Game.PLAYERS[Game.CLIENT_NUMBER].location, Square):
            path = finder.find_path(GRID.node(Game.PLAYERS[Game.CLIENT_NUMBER].location.square[0], Game.PLAYERS[Game.CLIENT_NUMBER].location.square[1]),
                                    GRID.node(square.square[0], square.square[1]), GRID)[0]
            GRID.cleanup()
            if len(path) - 1 > DICE1.value + DICE2.value:
                return len(path) - 1
            else:
                return square
        else:
            shortest_number = 0
            for enter_square in Game.PLAYERS[Game.CLIENT_NUMBER].location.enterSquares:
                path = finder.find_path(GRID.node(enter_square.square[0], enter_square.square[1]), GRID.node(square.square[0], square.square[1]), GRID)[0]
                GRID.cleanup()
                if len(path) - 1 > DICE1.value + DICE2.value:
                    shortest_number = min(shortest_number, len(path) - 1)
                else:
                    return square
            return shortest_number
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
    CONSERVATORY.passage.append(LOUNGE)
    LOUNGE.passage.append(CONSERVATORY)
    STUDY.passage.append(KITCHEN)
    KITCHEN.passage.append(STUDY)
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
                elif event.key == pygame.K_0 and Game.CLUE_SHEET_OPEN and Game.CLUE_SHEET.selectedBox is not None:
                    Game.CLUE_SHEET.selectedBox.dotCount = 0
                elif event.key == pygame.K_1 and Game.CLUE_SHEET_OPEN and Game.CLUE_SHEET.selectedBox is not None:
                    Game.CLUE_SHEET.selectedBox.dotCount = 1
                elif event.key == pygame.K_2 and Game.CLUE_SHEET_OPEN and Game.CLUE_SHEET.selectedBox is not None:
                    Game.CLUE_SHEET.selectedBox.dotCount = 2
                elif event.key == pygame.K_3 and Game.CLUE_SHEET_OPEN and Game.CLUE_SHEET.selectedBox is not None:
                    Game.CLUE_SHEET.selectedBox.dotCount = 3
                elif event.key == pygame.K_4 and Game.CLUE_SHEET_OPEN and Game.CLUE_SHEET.selectedBox is not None:
                    Game.CLUE_SHEET.selectedBox.dotCount = 4
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
