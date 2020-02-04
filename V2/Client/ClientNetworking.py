import pickle
import socket
from V2.NetworkingConstants import IP, PORT, BUFF_SIZE


class ClientNetworking:
    def __init__(self):
        self.s = socket.socket()

    def connect_to_server(self):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((IP, PORT))
            return True
        except socket.error as err:
            print("socket creation failed with error " + str(err))
        return False

    def disconnect_from_server(self):
        self.s.shutdown()
        self.s.close()
        return 1

    def send_info(self, data):
        # first send the data type
        # then send the actual data pickled
        # TODO send the data type before sending the data

        data_string = pickle.dumps(data)
        return self.s.sendall(data_string)

    def receive_info(self):
        data_string = self.s.recv(BUFF_SIZE)
        data_string = pickle.loads(data_string)
        return data_string
