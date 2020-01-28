'''
Client Module

01/23/2020
cristina sewell
'''
from socket import AF_INET, SOCK_STREAM, socket

class Client():
    # have an option to configure these values if necessary
    HOST = '127.0.0.1'
    PORT = 33002
    BUFSIZ = 2048
    ADDR = (HOST, PORT)
    REGISTER = '{REGISTER}'
    QUIT = '{QUIT}'

    data_received = ""
    clients = ""
    hello_msg = ""

    CLIENT = socket(AF_INET, SOCK_STREAM)

    def __init__(self):
        pass


    def connect_to_server(self, username):
        try:
            self.CLIENT.connect(self.ADDR)
            # provide the server with an username
            register_msg = self.REGISTER + username
            register_msg = register_msg.encode('utf-8')

            # after we register we should expect some
            # messages comming back from the server
            server_resp = self.send_dataaa(register_msg)
            return server_resp
        except ConnectionRefusedError:
            print("Could not make connection, the target might not be online.")
        except OSError:
            print("No request or received allowed.")
        


    def send_dataaa(self, msg):
        full_data = ""
        is_end_message = False
        while not is_end_message:
            print('first loop - sending message')
            self.CLIENT.send(msg)
            try:
                while True:
                    data = self.CLIENT.recv(self.BUFSIZ)
                    print('receiving data - second loop')
                    full_data += data.decode('utf-8')

                    print('full data: {}'.format(data.decode('utf-8')))
                    temp_data = data.decode("utf-8")
                    if '{CLIENTS}' in temp_data:
                        #is_end_message = True
                        # empty the message
                        #full_data = ""
                        self.clients = temp_data.split("}")[1]
                        self.set_clients(self.clients)
                        #handle_combobox_selection(clients)
                        print('clients msg: {}'.format(temp_data))
                        #break
                    if '{MSG}' in temp_data:
                        print("broadcast msg: {}".format(temp_data))
                    if '{MSG}' and '{CLIENTS}' in temp_data:
                        is_end_message = True
                        break
            except Exception as err:
                print('Some error ', str(err))
                #self.CLIENT.close()
        return full_data

    #getter - gets the current active clients in the chat
    def get_clients(self):
        return self.clients

    def set_clients(self, str_clients):
        self.clients = str_clients

    def close(self):
        self.CLIENT.close()
