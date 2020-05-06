from V2.NetworkingConstants import MAX_CONNECTIONS, IP, PORT
from V2.Logger.Logger import Logger
from V2.Server.ServerNetworking import ServerNetworking
from V2.Problem.Pi import pi_sum
from multiprocessing.pool import ThreadPool
from decimal import *
import threading
import socket
import time
import asyncio

global batchLock
global currentBatch
global results
global resLock


def server_loop(reader, writer, exit_signal, logger, identification, batch_size, problem_type):
    net = ServerNetworking(reader, writer)


class ServerThread(threading.Thread):
    def __init__(self, reader, writer, exit_signal, logger, identification, batch_size, problem_type):
        super().__init__()
        self.net = ServerNetworking(reader, writer)
        self.exit_signal = exit_signal
        self.logger = logger
        self.identification = identification
        self.batchSize = batch_size
        self.problem_type = problem_type
        print("New Socket Thread Started For: {0}:{1}".format(str(ip), str(port)))
        logger.write_connect(identification, ip)

    def run(self) -> None:
        first_contact = True
        while not self.exit_signal.is_set():
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
                if first_contact:
                    first_contact = False
                    self.net.send_str(str(self.problem_type))
                    continue

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
                    if self.problem_type == 0:
                        results.extend(data)
                        print("Current Results Last 10:", results[-10:])
                    else:
                        results += pi_sum(True, data)
                        print("{0:.50f}".format(results))
                        # print(results)
                    resLock.release()


async def main():
    # server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # server.bind((IP, PORT))
    threads = []
    exit_signal = threading.Event()

    global batchLock
    batchLock = threading.Lock()

    global currentBatch
    currentBatch = 0

    global resLock
    resLock = threading.Lock()

    batch_size = 100

    print_bars()
    print("\t0:\tPrime Calculator")
    print("\t1:\tPi Calculator")
    print_bars()

    global results
    problemType = int(input("Select the kind of problem to solve (default 0):\t"))
    logger = None
    if problemType == 0:
        logger = Logger("Prime Server")
        results = list()
    else:
        logger = Logger("Pi Server")
        results = 3

    try:
        server = await asyncio.start_server(lambda reader, writer: server_loop(reader, writer, exit_signal, logger, 0, batch_size, problemType),
                                      IP, PORT)







        # server_id = 0
        # server.listen(4)
        # while len(threads) < MAX_CONNECTIONS:
        #     (conn, (ip, port)) = server.accept()
        #     temp_thread = ServerThread(ip, port, conn, exit_signal, logger, server_id, batch_size, problemType)
        #     temp_thread.start()
        #     threads.append(temp_thread)
        #     server_id += 1
        # while True:
        #     time.sleep(.5)

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


def print_bars():
    for i in range(0, 80):
        print("=", end='')
    print("")


if __name__ == '__main__':
    asyncio.run(main())