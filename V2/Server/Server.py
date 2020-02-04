from threading import Thread
from V2.NetworkingConstants import BUFF_SIZE, MAX_CONNECTIONS, IP, PORT
from V2.Server.ServerNetworking import ServerNetworking
import socket


class ServerThread(Thread):
    def __init__(self, ip, port, conn):
        Thread.__init__(self)
        self.net = ServerNetworking(conn, ip, port)
        print("New Socket Thread Started For: {0}:{1}".format(str(ip), str(port)))

    def run(self) -> None:
        while self.net.is_connected():
            data = self.net.receive_data()
            if data is None or not self.net.is_connected():
                print("Client Disconnected")
                exit(0)

            print("Received Data:", data)
            self.net.send_str("Received: " + data)


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((IP, PORT))
    threads = []

    while len(threads) < MAX_CONNECTIONS:
        server.listen(4)
        (conn, (ip, port)) = server.accept()

        temp_thread = ServerThread(ip, port, conn)
        temp_thread.start()
        threads.append(threads)

    for t in threads:
        t.join()


if __name__ == '__main__':
    main()
