'''
Network Module
This module handles some of the communication between
the Gui interface and the Client

01/23/2020
cristina sewell
'''
#from socket import socket, SHUT_WR
import socket
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget
import client

class Network(QWidget):

    send_clients_signal = pyqtSignal(str)
    send_connected_signal = pyqtSignal(bool)
    display_msg_signal = pyqtSignal(str)
    send_log_signal = pyqtSignal(str, str)
    send_disconnected = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.client = client.Client()

        self.client.recv_msg_signal.connect(self.handle_msg_revc)
        self.client.send_status_signal.connect(self.handle_status)

    def connection_settings(self, host, port):
        """This is a slot that captures the user info about host/port"""
        self.client.HOST = host
        self.client.PORT = port

    def handle_status(self, status):
        self.send_log_signal.emit(status, None)

    def handle_username_input(self, username):
        """Initiates the communication with the server by providing
        a username for registration"""
        register_msg = "{REGISTER}" + username
        self.client.send_username(register_msg)

    def handle_message_input(self, message, recipient):
        if not message or 'QUIT' in message:
            self.handle_quit()
        else:
            if 'ALL-Broadcast' in recipient:
                all_users = 'ALL'
                temp_m = '{%s}'%(all_users) + message
            else:
                temp_m = '{%s}'%(recipient) + message
            self.client.send_message_data(temp_m)

    def handle_quit(self):
        temp_m = '{QUIT}'
        self.display_msg_signal.emit("Goodbye :)")
        self.client.send_message_data(temp_m)
        self.send_disconnected.emit()

    def handle_msg_revc(self, message):
        """Slot to catch the messages received from the client.
           Processes the messages and sends info for display"""
        # process clients
        self.process_clients(message)
        # process messages
        self.process_message(message)

    def process_clients(self, message):
        #send a signal to the combo_box to populate the clients
        if '{CLIENTS}' in message:
            clients = str(message.split('{CLIENTS}')[-1])
            self.send_clients_signal.emit(clients)

            #if we recieved a clients list from the server and it is not empty
            #it is a good indication we are connected to the server
            #send a signal to indicate that we are connected - i don't like doing it here though
            self.send_connected_signal.emit(True)

    def process_message(self, message):
        if '{QUIT}' in message:
            self.display_msg_signal.emit("Goodbye :)")
        elif '{MSG}' and ':' in message:
            # take the {MSG} out, this is a broadcast message from a user
            msg = str(message.split('{MSG}')[-1])
            if msg != "":
                self.display_msg_signal.emit(msg)
        elif ':' in message:
            #just display it the way it is, this is coming from an active user, not from the server
            self.display_msg_signal.emit(message)
        elif '{MSG}' and '{CLIENTS}' in message:
            # get only what i in the middle of them
            msg = message.split('{MSG}')[-1].split('{CLIENTS}')[0]
            if msg != "":
                print('this is the inner split: {}'.format(msg))
                self.display_msg_signal.emit(msg)
        elif '{MSG}' and not '{CLIENTS}' in message:
            msg = str(message.split('{MSG}')[-1])
            #send a signal to the scroll_are to populate the message
            if msg != "":
                self.display_msg_signal.emit(msg)

    def handle_usr_disconnect(self):
        """Called when the user clicks on the Disconnect button"""
        self.client.CLIENT.shutdown(socket.SHUT_WR)
        self.client.CLIENT.close()

    def handle_disconnect(self):
        """Called when the application is about to close"""
        try:
            self.client.CLIENT.shutdown(socket.SHUT_WR)
            self.client.CLIENT.close()
        except:
            print('The clients is probably already closed...')

