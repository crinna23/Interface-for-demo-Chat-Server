'''
Network Module
This module handles some of the communication between
the Gui interface and the Client

01/23/2020
cristina sewell
'''
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThread
from PyQt5.QtWidgets import QWidget
#from client import send_username, recv_message, send_data
#import server
import client

class Network(QWidget):
    send_clients_signal = pyqtSignal(str)
    send_connected_signal = pyqtSignal(bool)
    display_msg_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.client = client.Client()
         
        self.client.recv_msg_signal.connect(self.handle_msg_revc)
    
    def connection_settings(self, host, port):
        self.client.HOST = host
        self.client.PORT = port

        
       # client_socket = server.find_client_socket('cristina')
       # print('find client socket from server: {}'.format(client_socket))
    def handle_username_input(self, username):
        print('before connect_to_server')
        #server_response = self.client.connect_to_server(username)
        #if server_response:
        #    # send something here to show that it is connected
        #    self.send_connected_signal.emit(True)
        #    print('data: {}'.format(server_response))
        #    self.handle_combobox_selection()
        register_msg = "{REGISTER}" + username
        self.client.send_username(register_msg)
        #self.hanle_recv_thread()
        #self.handle_msg_revc()
        
    def handle_msg_revc(self, message):
        """Slot to catch the recv_msg_signal from client"""        
        # send it to the display....
        #msg_list = [i for i in message.split("}"))
        #msg = message.split('{')[1]
        clients = message.split('{CLIENTS}')
        print(clients)
      
       # print('in network: {}'.format(msg_list))
        #for i in range msg_list
        self.display_msg_signal.emit(message)
                 
    def handle_combobox_selection(self):
        clients = self.client.get_clients()
        print('Can i print the clients here? {}'.format(clients))
        send_clients_signal.emit(clients)

    def handle_message_input(self, message, username):
        if 'ALL-Broadcast' in username:
            all_users = 'ALL'
            temp_m = '{%s}'%(all_users) + message 
        else:
            temp_m = '{%s}'%(username) + message 
       # temp_m = temp_m.encode('utf-8')
        self.client.send_data(temp_m)
        

    def handle_connect(self, username):
        print("I am in Network, I have received the connect signal: {}".format(username))
        # pack the message here in the right format
        # send it to
        
    def handle_usr_disconnect(self):
        temp_message = '{QUIT}'.encode("utf-8")
        #self.client.send_dataaa(temp_message)
        client.CLIENT.send(temp_message)
       #r = self.client.send_data(temp_message)
        #print('in closing {} '.format(r))
        #self.client.close()
        
    def handle_disconnect(self):
        client.close()
        

