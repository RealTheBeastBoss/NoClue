import socket
from _thread import *
import pickle
from player import Player

port = 5555

class Server:
    sock = None
    added_players = 0
    player_count = 0
    client_addresses = []
    players = []


def threaded_client(conn, ip):
    while True:  # Send and Receive Data
        try:
            data = pickle.loads(conn.recv(2048))
            if not data:
                print(ip[0] + " Disconnected")
                break
            else:
                if data == "?":
                    if Server.added_players == Server.player_count:
                        data = (Server.players, 1)
                    else:
                        data = False
                elif data[0] == "Name":
                    print("From " + str(ip[0]) + ", Received Player Name: " + str(data[1]))
                    Server.players.append(Player(Server.added_players, data[1]))
                    data = (Server.added_players, Server.player_count)
                    Server.added_players += 1
                if data:
                    print("Sending " + str(data) + " to " + ip[0])
                conn.sendall(pickle.dumps(data))
        except error:
            break
    print(ip[0] + " Lost Connection")
    conn.close()


def check_server(server):
    Server.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        Server.sock.bind((server, port))
        return True
    except socket.error:
        return False


def start_server(count, server):
    Server.player_count = count
    Server.sock.listen(Server.player_count)
    print("Waiting for Connection, Server Started at " + server)
    while True:
        connect, addr = Server.sock.accept()
        print(addr[0] + " has Connected")
        Server.client_addresses.append(addr)
        start_new_thread(threaded_client, (connect, addr))


def close_server():
    Server.sock.close()
