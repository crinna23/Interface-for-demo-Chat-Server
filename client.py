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
    REGISTER = '{REGISTER}'
    QUIT = '{QUIT}'

    data_received = ""
    clients = ""
    hello_msg = ""

    CLIENT = socket(AF_INET, SOCK_STREAM)
    
    recv_msg_signal = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
    
   # start_thread_signal = pyqtSignal()
        
    # move this to a separate thread
    
    def recv_message(self):
        """Handles receiving messages"""
        while True:
            try:
                message = self.CLIENT.recv(self.BUFSIZ).decode("utf-8")
                # send a signal with this message - to be displayed
                # later on, insert it into a list.
              #  print('trying to receive message....')
                self.recv_msg_signal.emit(message)
               # print(message)
            except OSError:
                print('client might have left the chat...')
                # log an error here and display it to the chat
                # send it using a signal? - CRITICAL
                break
            except self.CLIENT.timeout:
                print('socket timeout')
                break
            except:
                print('Some other type of error that i dont know')
        
    def send_username(self, username):
        """Handles sending messages""" 
        # .. get the message you want to send, from the ui put it into a variable
        # .. after the message is saved, you should be clearing the message edit line
        
        # put this into a separate method and check if really connected
        self.CLIENT.connect(self.ADDR)
        self.CLIENT.send(bytes(username, "utf-8"))
        
        # check if successfully connected

       #start the revc thread here, since we are expecting a
       #message back from the server
        recv_thread = Thread(target=self.recv_message)
        recv_thread.start()
        
            
    def send_message_data(self, message):
        self.CLIENT.send(bytes(message, "utf-8"))
        
    def exit_handler(self):
        """This funtion should do some cleanup before closing"""
        # send a message here that has "{quit}" in it
 