import pickle
from V2.NetworkingConstants import BUFF_SIZE


class ServerNetworking:
    def __init__(self, conn, ip, port):
        self.conn = conn
        self.ip = ip
        self.port = port
        self.connected = True

    def send_str(self, data):
        self.conn.sendall(pickle.dumps(data))

    def receive_data(self):
        try:
            data = self.conn.recv(BUFF_SIZE)
            if data:
                data = pickle.loads(data)

                return data
        except ConnectionResetError:
            self.connected = False
            return None

    def is_connected(self):
        return self.connected
