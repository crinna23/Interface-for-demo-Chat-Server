'''
Client Module

01/23/2020
cristina sewell
'''
from threading import Thread
from socket import AF_INET, SOCK_STREAM, socket
from PyQt5.QtCore import QObject, pyqtSignal

class Client(QObject):
    HOST = '127.0.0.1'
    PORT = 33002
    BUFSIZ = 2048
    ADDR = (HOST, PORT)

    data_received = ""
    clients = ""
    hello_msg = ""

    recv_msg_signal = pyqtSignal(str)
    send_status_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    CLIENT = socket(AF_INET, SOCK_STREAM)

    # move this to a separate thread
    def recv_message(self):
        """Handles receiving messages"""
        while True:
            try:
                message = self.CLIENT.recv(self.BUFSIZ).decode("utf-8")
                self.recv_msg_signal.emit(message)
            except OSError:
                print('Client probably left the chat')
                self.send_status_signal.emit('The Client probably left the chat...')
                # log an error here and display it to the chat
                # send it using a signal? - CRITICAL
                break


    def send_username(self, username):
        """Handles starting the connection by registering the username"""
        try:
            self.CLIENT.connect(self.ADDR)
            self.CLIENT.send(bytes(username, "utf-8"))
        except ConnectionRefusedError:
            print("Server Refused Connection. The server migth not be running..")
            self.send_status_signal.emit('Server Refused Connection. The server migth not be running..')
        except OSError:
            print('No request allowed')
        except:
            print('Something went wrong when trying to conenct to the server')
        #start the revc thread here, since we are expecting a
        #message back from the server
        recv_thread = Thread(target=self.recv_message)
        recv_thread.start()

    def send_message_data(self, message):
        try:
            self.CLIENT.send(bytes(message, "utf-8"))
        except OSError:
            print('Could not send the message')

    def exit_handler(self):
        """This funtion should do some cleanup before closing"""
        # send a message here that has "{quit}" in it
 