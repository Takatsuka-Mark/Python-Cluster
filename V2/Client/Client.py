from threading import Thread
from V2.Client.ClientNetworking import ClientNetworking
from V2.Problem.Primality import PrimalityTest
import time

NUM_CLIENTS = 3

class Client:
    def __init__(self):
        self.response_loops = 4

    def run(self):
        net = ClientNetworking()
        net.connect_to_server()

        if not net:
            return False

        """Echo Implementation"""
        # for i in range(self.response_loops):
        #     text = input(">\t")
        #     net.send_info(text)
        #     data = net.receive_info()
        #     print(data)
        try:
            while True:
                net.send_info("READY")
                data = net.receive_info()
                print(data)
                data = data.split(" ")

                start = int(data[0])
                end = int(data[1])
                problem = PrimalityTest()
                res = self.solveProblem(problem, start, end)
                net.send_info(res)
                print(res)
                time.sleep(1)

        except KeyboardInterrupt:
            return False

    def solveProblem(self, problem, start, end):
        problem.run(start, end)
        return problem.res


def main():
    clients = []
    # for i in range(NUM_CLIENTS):
    #     temp_thread = Client()
    #     temp_thread.start()
    #     clients.append(temp_thread)
    # temp_thread = Client()
    # temp_thread.start()
    client = Client()
    client.run()


if __name__ == '__main__':
    main()
