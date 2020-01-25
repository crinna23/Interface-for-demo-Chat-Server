# Network Module
# This module handles some of the communication between 
# the Gui interface and the Client
from PyQt5.QtCore import pyqtSignal, pyqtSlot
import client

class Network():
    def __init__(self):
        self.client = client.Client()
    
    def handle_username_input(self, username):
        print('I am in the network moduel, username: {}'.format(username))
        temp_user = '{REGISTER}' + username
        print(temp_user)
        self.client.connect_to_server()
        self.client.send_data(temp_user)
        
    def handle_combobox_selection(self, selection):
        pass
    
    def handle_connect(self, username):
        print("I am in Network, I have received the connect signal: {}".format(username))
        # pack the message here in the right format
        # send it to 
    def handle_disconnect(self):
        pass
        
