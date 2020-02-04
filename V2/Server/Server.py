from V2.NetworkingConstants import MAX_CONNECTIONS, IP, PORT
from V2.Logger.Logger import Logger
from V2.Server.ServerNetworking import ServerNetworking
import threading
import socket
import time


class ServerThread(threading.Thread):
    def __init__(self, ip, port, conn, exit_signal, logger, identification):
        super().__init__()
        self.net = ServerNetworking(conn, ip, port)
        self.exit_signal = exit_signal
        self.logger = logger
        self.identification = identification
        print("New Socket Thread Started For: {0}:{1}".format(str(ip), str(port)))
        logger.write_connect(identification, ip)


    def run(self) -> None:
        while not self.exit_signal.is_set():
            data = self.net.receive_data()
            if data is None or not self.net.is_connected():
                self.logger.write_disconnected(self.identification, self.net.port)
                print("Client Disconnected")
                exit(0)

            print("Received Data:", data)
            self.logger.write_recv(self.identification, data)
            self.net.send_str("Received: " + data)


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((IP, PORT))
    threads = []
    exit_signal = threading.Event()
    logger = Logger("Echo Server Test")

    try:
        server_id = 0
        server.listen(4)
        while len(threads) < MAX_CONNECTIONS:
            (conn, (ip, port)) = server.accept()
            temp_thread = ServerThread(ip, port, conn, exit_signal, logger, server_id)
            temp_thread.start()
            threads.append(temp_thread)
            server_id += 1
        while True:
            time.sleep(.5)

    except KeyboardInterrupt:
        print("Keyboard Interrupt Received")
        exit_signal.set()
        logger.close_logger()
        time.sleep(1)

    for t in threads:
        t.join()


if __name__ == '__main__':
    main()
