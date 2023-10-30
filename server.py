import socket
from _thread import *
import pickle

port = 5555

class Server:
    sock = None
    client_addresses = []


def threaded_client(conn, ip):
    while True:  # Send and Receive Data
        try:
            data = pickle.loads(conn.recv(2048))
            if not data:
                print(ip[0] + " Disconnected")
                break
            else:
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
