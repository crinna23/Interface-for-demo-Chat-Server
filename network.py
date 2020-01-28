'''
Network Module
This module handles some of the communication between
the Gui interface and the Client

01/23/2020
cristina sewell
'''
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget
import client

class Network(QWidget):
    send_clients_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.client = client.Client()

    def handle_username_input(self, username):
        print('before connect_to_server')
        server_response = self.client.connect_to_server(username)
        if server_response:
            print('data: {}'.format(server_response))
            self.handle_combobox_selection()

    def handle_combobox_selection(self):
        clients = self.client.get_clients()
        print('Can i print the clients here? {}'.format(clients))
        self.send_clients_signal.emit(clients)

    def handle_message_input(self, message):
        temp_m = '{ALL}' + message
        temp_m = temp_m.encode('utf-8')
        self.client.send_dataaa(temp_m)

    def handle_connect(self, username):
        print("I am in Network, I have received the connect signal: {}".format(username))
        # pack the message here in the right format
        # send it to
    def handle_disconnect(self):
       # temp_message = '{QUIT}'
       #r = self.client.send_data(temp_message)
        #print('in closing {} '.format(r))
        self.client.close()
