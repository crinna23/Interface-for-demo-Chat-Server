# Network Module

from PyQt5.QtCore import pyqtSignal, pyqtSlot

class Network():
    def __init__(self):
        pass
    
    def handle_username_input(self):
        pass
     
    def handle_combobox_selection(self, selection):
        pass
    
    def handle_connect(self, username):
        print("I am in Network, I have received the connect signal: {}".format(username))
     
    def handle_disconnect(self):
        pass
        
