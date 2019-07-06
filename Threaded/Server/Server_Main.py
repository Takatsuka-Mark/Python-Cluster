import socket
import threading
import time
from Threaded.Server.Server_Thread import *

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


def init():
    global SOCK
    SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SOCK.bind((HOST, PORT))
    SOCK.listen(5)


def main():
    threads = []

    for i in range(0, MAX_CLIENTS):
        client_sock, addr = SOCK.accept()
        print("Connected at: ", addr)
        args = []
        args.append(client_sock)
        args.append(addr)
        thread1 = ServerThread(1, "Thread 1", 1, args)
        thread1.start()
        threads.append(thread1)

    time.sleep(1)


if __name__ == "__main__":
    init()
    main()


