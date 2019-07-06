import threading
import time


class ServerThread(threading.Thread):
    def __init__(self, threadID, name, counter, *args):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.args = args

    def run(self):
        print("printing args")
        print(self.args)
        client(self, self.args[0], self.args[1])
        return


def client(self, client_socket, addr):
    print("Client thread started")
    run = True
    while run:
        data = client_socket.recv(1024)
        if not data:
            run = False
            break
        client_socket.send(data)
    client_socket.close()

