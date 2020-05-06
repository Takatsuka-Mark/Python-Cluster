import pickle
import socket
import asyncio
from V2.NetworkingConstants import IP, PORT, BUFF_SIZE


class ClientNetworking:
    def __init__(self):
        self.reader = asyncio.StreamReader()
        self.writer = asyncio.StreamWriter()
        # self.s = socket.socket()

    def connect_to_server(self):
        try:
            self.reader, self.writer = await asyncio.open_connection(IP, PORT)
            # self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # self.s.connect((IP, PORT))
            return True
        except socket.error:
            print("Socket creation failed with error")
        return False

    def disconnect_from_server(self):
        self.writer.close()
        await self.writer.wait_closed()
        return 1

    def send_info(self, data):
        # first send the data type
        # then send the actual data pickled
        # TODO send the data type before sending the data

        data_string = pickle.dumps(data)
        self.writer.write(data_string)
        return await self.writer.drain()

    def receive_info(self):
        data_string = await self.reader.read(-1)  # will read until EOF and return all read bytes
        data_string = pickle.loads(data_string)
        # data_string = self.s.recv(BUFF_SIZE)
        # data_string = pickle.loads(data_string)
        return data_string
