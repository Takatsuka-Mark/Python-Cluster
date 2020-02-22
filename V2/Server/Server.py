from V2.NetworkingConstants import MAX_CONNECTIONS, IP, PORT
from V2.Logger.Logger import Logger
from V2.Server.ServerNetworking import ServerNetworking
from multiprocessing.pool import ThreadPool
import threading
import socket
import time

global batchLock
global currentBatch
global results
global resLock


class ServerThread(threading.Thread):
    def __init__(self, ip, port, conn, exit_signal, logger, identification, batch_size):
        super().__init__()
        self.net = ServerNetworking(conn, ip, port)
        self.exit_signal = exit_signal
        self.logger = logger
        self.identification = identification
        self.batchSize = batch_size
        print("New Socket Thread Started For: {0}:{1}".format(str(ip), str(port)))
        logger.write_connect(identification, ip)

    def run(self) -> None:
        # while not self.exit_signal.is_set():
        for i in range(5 * 2):
            data = self.net.receive_data()

            # TODO implement this in Server Networking
            if data is None or not self.net.is_connected():
                self.logger.write_disconnected(self.identification, self.net.port)
                print("Client Disconnected")
                exit(0)

            print("Received Data:", data)
            self.logger.write_recv(self.identification, data)

            # client is ready to start its next task
            if data == "READY":

                calc_range = 0
                # get the current batch that we should calculate
                global batchLock
                global currentBatch
                batchLock.acquire()
                calc_range = currentBatch
                currentBatch += 1
                batchLock.release()

                calc_range = (calc_range * self.batchSize, (calc_range + 1) * self.batchSize)
                self.net.send_str("{0} {1}".format(calc_range[0], calc_range[1]))

            else:
                # We have received some results
                if isinstance(data, list):
                    global resLock
                    global results
                    resLock.acquire()
                    results.extend(data)
                    print("Current Results:", results)
                    resLock.release()




def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((IP, PORT))
    threads = []
    exit_signal = threading.Event()
    logger = Logger("Echo Server Test")

    global batchLock
    batchLock = threading.Lock()

    global currentBatch
    currentBatch = 0

    global resLock
    resLock = threading.Lock()

    global results
    results = list()

    batch_size = 100

    try:
        server_id = 0
        server.listen(4)
        while len(threads) < MAX_CONNECTIONS:
            (conn, (ip, port)) = server.accept()
            temp_thread = ServerThread(ip, port, conn, exit_signal, logger, server_id, batch_size)
            temp_thread.start()
            threads.append(temp_thread)
            server_id += 1
        while True:
            time.sleep(.5)

    except KeyboardInterrupt:
        print("Keyboard Interrupt Received")
        exit_signal.set()
        time.sleep(1)
        logger.close_logger()
        for thread in threads:
            thread.join()
        print("Our final results are as follows")
        print(results)


    for t in threads:
        t.join()


if __name__ == '__main__':
    main()
