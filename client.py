# client module
from socket import AF_INET, SOCK_STREAM, socket

class Client():
    # have an option to configure these values if necessary
    HOST = '127.0.0.1'
    PORT = 33002
    BUFSIZ = 2048
    ADDR = (HOST, PORT)
    
    CLIENT = socket(AF_INET, SOCK_STREAM)
    
    # should i have a client  as param here? to create a client per name?
    def __init__(self):
        #self.ip_addr = ip_addr
        #self.port = port

    def connect_to_server(self, ip_addr = HOST, port = PORT):
        self.CLIENT.connect((self.ip_addr, self.port ))
        return "The client has successfully connected on port == %s" %(self.HOST)

    def send_data(self, message):
        try:
            #register - see what type of data you need to send?
            message = message.encode("utf-8")
            self.CLIENT.send(message)
            receive = self.CLIENT.recv(self.BUFSIZ)
            receive = receive.decode("utf-8")
            
            # while received < expected:???
        except CLIENT.error as err:
            return str(err)

    def close(self):
        self.CLIENT.shutdown(SHUT_WR)
        self.CLIENT.close()

    def create_client(self):
        client = Client()
        return client