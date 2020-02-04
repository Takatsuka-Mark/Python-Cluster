from threading import Thread
from V2.Client.ClientNetworking import ClientNetworking

NUM_CLIENTS = 3


# class Client(Thread):
#     def __init__(self):
#         super().__init__()
#         self.responseLoops = 4
#
#     def run(self) -> None:
#         pass


class Client:
    def __init__(self):
        self.response_loops = 4

    def run(self):
        net = ClientNetworking()
        net.connect_to_server()

        if not net:
            return False

        for i in range(self.response_loops):
            text = input()
            net.send_info(text)
            data = net.receive_info()
            print(data)

        return True


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
