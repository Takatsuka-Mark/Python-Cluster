import datetime


class Logger:
    def __init__(self, instance_name):
        self.instance_name = instance_name
        self.log = open("../Logs/" + datetime.datetime.now().strftime("%m-%d-%y %H-%M-%S") + " " + str(instance_name) + ".txt", "w")

    def close_logger(self):
        self.log.close()

    def write_connect(self, server_id, port):
        self.__write_str(str(server_id) + " Connected on Port: " + str(port))

    def write_disconnected(self, server_id, port):
        self.__write_str(str(server_id) + " Disconnected from Port: " + str(port))

    def write_recv(self, server_id, size):
        self.__write_str(str(server_id) + " Received data " + str(size))

    def write_send(self, server_id, size):
        self.__write_str(str(server_id) + " Sending data " + str(size))

    def __write_str(self, string):
        self.log.writelines(datetime.datetime.now().strftime("%m-%d-%y %H-%M-%S") + "\t\t" + string + "\n")
        self.log.flush()

