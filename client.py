'''
Client Module

01/23/2020
cristina sewell
'''
from socket import AF_INET, SOCK_STREAM, socket
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from threading import Thread

'''
# make sure you change here so it does not use the hardcoded values
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

def recv_message():
    """Handles receiving messages"""
    while True:
        try:
            message = CLIENT.recv(BUFSIZ).decode("utf-8")
            # send a signal with this message - to be displayed
            # later on, insert it into a list.
            print('trying to receive message....')
           # self.recv_msg_signal.emit(message)
            print(message)
            
        except OSError:
            print('client might have left the chat...')
            # log an error here and display it to the chat
            # send it using a signal? - CRITICAL
            break
        
def send_username(username):
    """Handles sending messages""" 
    # .. get the message you want to send, from the ui put it into a variable
    # .. after the message is saved, you should be clearing the message edit line
    
    # put this into a separate method and check if really connected
    CLIENT.connect(ADDR)

    CLIENT.send(bytes(username, "utf-8"))
    print('before emiting the start_thread_signal')
    #start_thread_signal.emit()
   # self.recv_message()
   # start the recv_thread here, since we might start getting messages
    recv_thread = Thread(target = recv_message)
    recv_thread.start()
    
    
    if username == "{QUIT}": # maybe add {quit} as well
        CLIENT.close()
        # log a message here of Quit request
        # close the application here?
            
def send_data(message):
    CLIENT.send(bytes(message, "utf-8"))
 '''   
    
class Client(QObject):
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
        super().__init__()

        
    recv_msg_signal = pyqtSignal(str)
   # start_thread_signal = pyqtSignal()
        
    # move this to a separate thread
    
    def recv_message(self):
        """Handles receiving messages"""
        while True:
            try:
                message = self.CLIENT.recv(self.BUFSIZ).decode("utf-8")
                # send a signal with this message - to be displayed
                # later on, insert it into a list.
                print('trying to receive message....')
                self.recv_msg_signal.emit(message)
                print(message)
            except OSError:
                print('client might have left the chat...')
                # log an error here and display it to the chat
                # send it using a signal? - CRITICAL
                break
        
    def send_username(self, username):
        """Handles sending messages""" 
        # .. get the message you want to send, from the ui put it into a variable
        # .. after the message is saved, you should be clearing the message edit line
        
        # put this into a separate method and check if really connected
        self.CLIENT.connect(self.ADDR)
  
        self.CLIENT.send(bytes(username, "utf-8"))
        print('before emiting the start_thread_signal')
       # self.start_thread_signal.emit()
       # self.recv_message()
        recv_thread = Thread(target = self.recv_message)
        recv_thread.start()
        
        
        if username == "{QUIT}": # maybe add {quit} as well
            self.CLIENT.close()
            # log a message here of Quit request
            # close the application here?
            
    def send_data(self, message):
        self.CLIENT.send(bytes(message, "utf-8"))
        
    def exit_handler(self):
        """This funtion should do some cleanup before closing"""
        # send a message here that has "{quit}" in it
 
'''
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
                    if '{MSG}cristina' in temp_data:
                        print('the other msg: {}'.format(temp_data))
                    if '{MSG}' and '{CLIENTS}' in temp_data:
                        is_end_message = True
                        break
            except Exception as err:
                print('Some error ', str(err))
                #self.CLIENT.close()
        return full_data


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
                    if '{MSG}cristina' in temp_data:
                        print('the other msg: {}'.format(temp_data))
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
'''