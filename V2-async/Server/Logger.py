from datetime import date


class Logger:
    def __init__(self, instance_name):
        self.instance_name = instance_name
        self.log = open(date.today().strftime("%m-%d-%y") + " " + str(instance_name), "w")

    def close_logger(self):
        self.log.close()

    def write_connect(self, server_id, port):
        self.__write_str(str(server_id) + " Connected on Port: " + str(port))

    def __write_str(self, string):
        self.log.write(string)

