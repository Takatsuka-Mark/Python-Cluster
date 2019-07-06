import socket
import _thread
import time


HOST = '127.0.0.1'
PORT = 6666
MAX_CLIENTS = 5

"""
Steps
    
    Create Socket
    
    Bind
    
    Listen
    
    Accept
    
        Client connects after
        
    then send and receive pairing
    
    close

"""

def client(client_socket, addr):
    print("Client thread started")
    run = True
    while run:
        data = client_socket.recv(1024)
        if not data:
            run = False
            break
        client_socket.send(data)
    client_socket.close()


def init():
    global SOCK
    SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SOCK.bind((HOST, PORT))
    SOCK.listen(5)


def main():
    for i in range(0, MAX_CLIENTS):
        client_sock, addr = SOCK.accept()
        print("Connected at: ", addr)
        _thread.start_new_thread(client, (client_sock, addr))
    time.sleep(1)


if __name__ == "__main__":
    init()
    main()


