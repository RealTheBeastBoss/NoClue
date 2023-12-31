import socket
from _thread import *
import pickle
from player import Player
import random
from game import *

port = 5555

class Server:
    sock = None
    added_players = 0
    player_count = 0
    client_addresses = []
    players = []
    clue_cards = []
    clue_cards_active = False
    game_cards = None
    final_cards = None
    quits_to_send = []
    locations_to_send = []
    locations = []
    turn_stage = None
    turn_stages_to_send = []
    dice_values = None
    dice_to_send = []
    players_to_send = []
    clue_to_send = []
    card_showings_to_send = []
    card_showns_to_send = []
    card_showing_data = None
    turn_stages_to_get = []
    turns_to_end = []
    finals_to_send = []
    final_succeeded = False
    accuse_to_send = []
    player_choosing = None
    player_choosing_to_send = []
    chosen_card = None
    chosen_card_to_send = []
    weapon_revealed = None
    weapon_reveals_to_send = []
    passage_location = None
    passages_to_send = []
    temp_players = []
    temp_players_to_send = []
    temp_cards = []
    temp_cards_to_send = []
    temp_showings = []
    temp_showings_to_send = []

def threaded_client(conn, ip):
    while True:  # Send and Receive Data
        try:
            data = pickle.loads(conn.recv(2048*5))
            if not data:
                print(ip[0] + " Disconnected")
                break
            else:
                if len(Server.locations_to_send) == 0:
                    Server.locations.clear()
                if data == "!":
                    data = {}
                    if ip in Server.quits_to_send:
                        data["quit"] = True
                        Server.quits_to_send.remove(ip)
                    if ip in Server.locations_to_send:
                        data["locations"] = Server.locations
                        Server.locations_to_send.remove(ip)
                    if ip in Server.turn_stages_to_send:
                        data["turn"] = Server.turn_stage
                        Server.turn_stages_to_send.remove(ip)
                    if ip in Server.dice_to_send:
                        data["dice"] = Server.dice_values
                        Server.dice_to_send.remove(ip)
                    if ip in Server.players_to_send:
                        data["players"] = Server.players
                        Server.players_to_send.remove(ip)
                    if ip in Server.clue_to_send:
                        data["clue"] = 1
                        Server.clue_to_send.remove(ip)
                    if ip in Server.card_showings_to_send:
                        data["card_show"] = Server.card_showing_data
                        Server.card_showings_to_send.remove(ip)
                    if ip in Server.card_showns_to_send:
                        data["show_card"] = Server.card_showing_data
                        Server.card_showns_to_send.remove(ip)
                    if ip in Server.turns_to_end:
                        data["end_turn"] = True
                        Server.turns_to_end.remove(ip)
                    if ip in Server.finals_to_send:
                        data["final"] = True
                        Server.finals_to_send.remove(ip)
                    if ip in Server.accuse_to_send:
                        data["accuse"] = Server.final_succeeded
                        Server.accuse_to_send.remove(ip)
                    if ip in Server.player_choosing_to_send:
                        data["player_choosing"] = Server.player_choosing
                        Server.player_choosing_to_send.remove(ip)
                    if ip in Server.chosen_card_to_send:
                        data["chosen_card"] = Server.chosen_card
                        Server.chosen_card_to_send.remove(ip)
                    if ip in Server.weapon_reveals_to_send:
                        data["weapon_reveal"] = Server.weapon_revealed
                        Server.weapon_reveals_to_send.remove(ip)
                    if ip in Server.passages_to_send:
                        data["passage_location"] = Server.passage_location
                        Server.passages_to_send.remove(ip)
                    if ip in Server.temp_players_to_send:
                        data["players"] = Server.temp_players
                        Server.temp_players_to_send.remove(ip)
                    if ip in Server.temp_cards_to_send:
                        data["cards"] = Server.temp_cards
                        Server.temp_cards_to_send.remove(ip)
                    if ip in Server.temp_showings_to_send:
                        data["showings"] = Server.temp_showings
                        Server.temp_showings_to_send.remove(ip)
                elif data == "?":
                    if Server.added_players == Server.player_count:
                        data = (Server.players, Server.clue_cards, Server.clue_cards_active)
                    else:
                        data = False
                elif data == "!!":
                    data = False
                    if len(Server.turn_stages_to_get) == 0:
                        data = True
                elif data == "quit":
                    Server.quits_to_send = Server.client_addresses.copy()
                    Server.quits_to_send.remove(ip)
                    data = False
                elif data == "EndTurn":
                    Server.turns_to_end = Server.client_addresses.copy()
                    Server.turns_to_end.remove(ip)
                    data = False
                elif data == "FinalAccusation":
                    print("From " + str(ip[0]) + ", Received: " + str(data))
                    Server.finals_to_send = Server.client_addresses.copy()
                    Server.finals_to_send.remove(ip)
                    data = False
                elif data == "TurnClick":
                    print("From " + str(ip[0]) + ", Received Turn Click")
                    Server.turn_stages_to_get.remove(ip)
                    data = False
                elif data[0] == "WeaponReveal":
                    print("From " + str(ip[0]) + ", Received: " + str(data))
                    Server.weapon_revealed = data[1]
                    Server.weapon_reveals_to_send = Server.client_addresses.copy()
                    Server.weapon_reveals_to_send.remove(ip)
                    Server.turn_stages_to_get = Server.client_addresses.copy()
                    data = False
                elif data[0] == "PassageLocation":
                    print("From " + str(ip[0]) + ", Received: " + str(data))
                    Server.passage_location = data[1]
                    Server.passages_to_send = Server.client_addresses.copy()
                    Server.passages_to_send.remove(ip)
                    Server.turn_stages_to_get = Server.client_addresses.copy()
                    data = False
                elif data[0] == "ChosenCard":
                    print("From " + str(ip[0]) + ", Received: " + str(data))
                    Server.chosen_card = data[1]
                    Server.chosen_card_to_send = Server.client_addresses.copy()
                    Server.chosen_card_to_send.remove(ip)
                    Server.turn_stages_to_get = Server.client_addresses.copy()
                    data = False
                elif data[0] == "PlayerChoosing":
                    print("From " + str(ip[0]) + ", Received: " + str(data))
                    Server.player_choosing = data[1]
                    Server.player_choosing_to_send = Server.client_addresses.copy()
                    Server.player_choosing_to_send.remove(ip)
                    data = False
                elif data[0] == "Clue":
                    print("From " + str(ip[0]) + ", Received: " + str(data))
                    Server.clue_to_send = Server.client_addresses.copy()
                    Server.clue_to_send.remove(ip)
                    if data[1].card is not None:
                        Server.turn_stages_to_get = Server.client_addresses.copy()
                    data = False
                elif data[0] == "Final":
                    print("From " + str(ip[0]) + ", Received: " + str(data))
                    if Server.final_cards[0].displayName == data[1][0].displayName and Server.final_cards[1].displayName == data[1][1].displayName and Server.final_cards[2].displayName == data[1][2].displayName:
                        data = True
                        Server.final_succeeded = True
                    else:
                        data = False
                        Server.final_succeeded = False
                    Server.accuse_to_send = Server.client_addresses.copy()
                    Server.accuse_to_send.remove(ip)
                elif data[0] == "Turn":
                    print("From " + str(ip[0]) + ", Received: " + str(data))
                    Server.turn_stage = data[1]
                    Server.turn_stages_to_send = Server.client_addresses.copy()
                    Server.turn_stages_to_send.remove(ip)
                    data = False
                elif data[0] == "ShownCard":
                    print("From " + str(ip[0]) + ", Received: " + str(data))
                    Server.card_showing_data = data[1]
                    Server.card_showns_to_send = Server.client_addresses.copy()
                    Server.card_showns_to_send.remove(ip)
                    Server.turn_stages_to_get = Server.client_addresses.copy()
                    data = False
                elif data[0] == "CardShowing":
                    print("From " + str(ip[0]) + ", Received: " + str(data))
                    Server.turn_stage = data[1]
                    Server.turn_stages_to_send = Server.client_addresses.copy()
                    Server.turn_stages_to_send.remove(ip)
                    Server.card_showing_data = (data[3], data[2])
                    Server.card_showings_to_send = Server.client_addresses.copy()
                    Server.card_showings_to_send.remove(ip)
                    if data[3] is None:
                        Server.turn_stages_to_get = Server.client_addresses.copy()
                    data = False
                elif data[0] == "MoveLocation":
                    print("From " + str(ip[0]) + ", Received: " + str(data))
                    Server.temp_players.append(data[1])
                    if len(Server.temp_players) == Server.player_count:
                        Server.temp_players_to_send = Server.client_addresses.copy()
                    data = False
                elif data[0] == "SentCard":
                    print("From " + str(ip[0]) + ", Received: " + str(data))
                    Server.temp_cards.append((data[1], data[2]))
                    if len(Server.temp_cards) == Server.player_count:
                        Server.temp_cards_to_send = Server.client_addresses.copy()
                        Server.turn_stages_to_get = Server.client_addresses.copy()
                    data = False
                elif data[0] == "ShowCard":
                    print("From " + str(ip[0]) + ", Received: " + str(data))
                    Server.temp_showings.append((data[1], data[2]))
                    if len(Server.temp_showings) == Server.player_count:
                        Server.temp_showings_to_send = Server.client_addresses.copy()
                        Server.turn_stages_to_get = Server.client_addresses.copy()
                    data = False
                elif data[0] == "TurnPlayer":
                    print("From " + str(ip[0]) + ", Received: " + str(data))
                    Server.turn_stage = data[1]
                    Server.turn_stages_to_send = Server.client_addresses.copy()
                    Server.turn_stages_to_send.remove(ip)
                    Server.players[data[2].playerIndex] = data[2]
                    Server.players_to_send = Server.client_addresses.copy()
                    Server.players_to_send.remove(ip)
                    data = False
                elif data[0] == "TurnDice":
                    print("From " + str(ip[0]) + ", Received: " + str(data))
                    Server.turn_stage = data[1]
                    Server.turn_stages_to_send = Server.client_addresses.copy()
                    Server.turn_stages_to_send.remove(ip)
                    Server.dice_values = (data[2], data[3])
                    Server.dice_to_send = Server.client_addresses.copy()
                    Server.dice_to_send.remove(ip)
                    data = False
                elif data[0] == "JustPlayer":
                    print("From " + str(ip[0]) + ", Received: " + str(data))
                    Server.players[data[1].playerIndex] = data[1]
                    Server.players_to_send = Server.client_addresses.copy()
                    Server.players_to_send.remove(ip)
                    data = False
                elif data[0] == "Player":
                    print("From " + str(ip[0]) + ", Received Player: " + str(data[1]))
                    for player in Server.players:
                        if player.playerNumber == data[1]:
                            data = False
                            break
                    if data:
                        Server.players.append(Player(data[1]))
                        data = Server.player_count
                        Server.added_players += 1
                        if Server.added_players == Server.player_count:
                            Server.games_to_start = Server.client_addresses.copy()
                            suspect_cards = []
                            weapon_cards = []
                            location_cards = []
                            for card in Server.game_cards:
                                if card.cardType == CardType.SUSPECT:
                                    suspect_cards.append(card)
                                elif card.cardType == CardType.WEAPON:
                                    weapon_cards.append(card)
                                else:
                                    location_cards.append(card)
                            random.shuffle(suspect_cards)
                            random.shuffle(weapon_cards)
                            random.shuffle(location_cards)
                            Server.final_cards = (suspect_cards.pop(), weapon_cards.pop(), location_cards.pop())
                            cards = suspect_cards + weapon_cards + location_cards
                            random.shuffle(cards)
                            if Server.player_count == 2:
                                location_indexes = []
                                while len(location_indexes) != 4:
                                    number = random.randrange(0, 9)
                                    if number not in location_indexes:
                                        location_indexes.append(number)
                                for index in location_indexes:
                                    Game.LOCATIONS[index].card = cards.pop()
                                    Server.locations.append(Game.LOCATIONS[index])
                                    Server.locations_to_send = Server.client_addresses.copy()
                            selected_player = 0
                            while len(cards) > 0:
                                Server.players[selected_player].cards.append(cards.pop())
                                if selected_player == Server.player_count - 1:
                                    selected_player = 0
                                else:
                                    selected_player += 1
                            random.shuffle(Server.clue_cards)
                            players = Server.players.copy()
                            Server.players.clear()
                            Server.game_cards.clear()
                            players.sort(key=sort_by_number)
                            for x in range(len(players)):
                                players[x].playerIndex = x
                                Server.players.append(players[x])
                if data:
                    print("Sending " + str(data) + " to " + ip[0])
                conn.sendall(pickle.dumps(data))
        except error:
            break
    print(ip[0] + " Lost Connection")
    conn.close()


def sort_by_number(e):
    return e.playerNumber


def check_server(server):
    Server.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        Server.sock.bind((server, port))
        return True
    except socket.error:
        return False


def start_server(count, server):
    Server.player_count = count
    Server.clue_cards = Game.CLUE_CARD_DECK
    Server.clue_cards_active = Game.CLUE_CARDS_ACTIVE
    Server.game_cards = GAME_CARDS
    Server.sock.listen(Server.player_count)
    print("Waiting for Connection, Server Started at " + server)
    while True:
        connect, addr = Server.sock.accept()
        print(addr[0] + " has Connected")
        Server.client_addresses.append(addr)
        start_new_thread(threaded_client, (connect, addr))


def close_server():
    Server.sock.close()
