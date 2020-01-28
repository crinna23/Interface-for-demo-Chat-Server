'''
Chat Interface

01/23/2020
cristina sewell

'''
import sys
import signal
from enum import Enum
from PyQt5.QtGui import QFont, QPalette, QColor, QBrush, QLinearGradient
from PyQt5.QtCore import pyqtSignal, QRect, Qt
from PyQt5.QtWidgets import (QApplication, QLineEdit, QPushButton,
                             QWidget, QGridLayout, QVBoxLayout, QLabel,
                             QComboBox, QScrollArea, QSizePolicy)
import network

# supporting the status loggin function 
class Status(Enum):
    CRITICAL = 1
    WARNING = 2
    INFO = 3

# supporting the QPalette, can be expanded so it
# could support the setStyleSheet method as well
class Colors():
    # Note: the colors bellow have been borrowed from
    # https://identity.stanford.edu/color.html
    stone = QColor(84, 73, 72)
    light_sandstone = QColor(249, 246, 239)
    light_sage = QColor(199, 209, 197)
    chocolate = QColor(47, 36, 36)
    lagunita = QColor(0, 124, 146)
    teal = QColor(0, 80, 92)
    mint = QColor(0, 155, 118)
    bright_red = QColor(177, 4, 14)
    gold = QColor(178, 111, 22)

class MainWindow(QWidget):
    '''Setup the main window along with all the other attributes'''
    error_signal = pyqtSignal(str)
    connect_signal = pyqtSignal(str)
    text_changed_signal = pyqtSignal(str, str)
    send_message_signal = pyqtSignal(str)

    user_username = ""
    user_message = ""

    def __init__(self):
        super().__init__()

        min_width = 600
        min_height = 1200
        self.title = "SLAC Chat"
        self.resize(min_width, min_height)
        self.setWindowTitle(self.title)

        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.centralwidget = QWidget(self)
        self.grid_layout_widget = QWidget(self.centralwidget)

        self.grid_layout_widget.setGeometry(QRect(0, 0, 600, 300))

        #self.style_colors()
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, 300)
        gradient.setColorAt(1.0, Colors.chocolate)
        gradient.setColorAt(0.0, Colors.stone)
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

        #create an instance of Network Module
        self.network = network.Network()

        # define attributes here to be part of the __init__
        self.scroll_area = QScrollArea(self.grid_layout_widget)
        self.combo_box = QComboBox(self.grid_layout_widget)
        self.connect_button = QPushButton(self.grid_layout_widget)
        self.username_line_edit = QLineEdit(self.grid_layout_widget)
        self.username_label = QLabel(self.grid_layout_widget)
        self.status_label = QLabel('Status..')
        self.combobox_label = QLabel("chat users: ")
        self.send_button = QPushButton(self.grid_layout_widget)
        self.grid_layout = QGridLayout(self.grid_layout_widget)
        self.message_line_edit = QLineEdit(self.grid_layout_widget)

        self.setup_ui()
        self.setup_signal_slots()

    #setup multiple components of the app ui
    def setup_ui(self):
        self.setup_chat_area()
        self.setup_combobox()
        self.setup_button()
        self.setup_labels()
        self.setup_username_line_edit()
        self.setup_message_area()
        self.setup_send_button()
        self.setup_layout()
        self.log_status('Please provide a username to connect.', Status.INFO)

    # defines the main area where the messages
    # will be exchanged or displayed
    def setup_chat_area(self):
        self.scroll_area.setContentsMargins(2, 2, 2, 2)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.scroll_area.setStyleSheet("""
            QWidget {
                 border: 1px solid black;
                 border-radius:7;
                } 
            """)

        palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, 300)
        gradient.setColorAt(0.0, Colors.light_sandstone)
        gradient.setColorAt(1.0, Colors.light_sage)
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.scroll_area.setPalette(palette)

        self.scroll_area.setFont(QFont('Courier New', 12))

        widget = QWidget()
        self.scroll_area.setWidget(widget)
        scroll_area_layout = QVBoxLayout(widget)
        scroll_area_layout.setAlignment(Qt.AlignTop)

        self.scroll_area.setWidgetResizable(True)

        self.scroll_area.verticalScrollBar().setSingleStep(20)

        for i in range(40):
            i = QLabel('start----------------------------------------------------------end')
            i.setStyleSheet(""" QLabel { background-color: rgba(0, 23, 43, 80)}""")
            i.setFixedHeight(60)
           # i.adjustSize()
           # i.setMinimumWidth(1)
            i.wordWrap()
           # l = scroll_area_layout.layout()
           # l.insertWidget(l.count() - 1, i)

    # combo box that holds the list of
    # clients that are currently participating in the chat
    def setup_combobox(self):
        self.combo_box.setFont(QFont('Courier New', 12))
        self.combo_box.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)

        self.combo_box.setStyleSheet("""
            QComboBox {
                border: 2px solid black;
                color: QColor(47, 36, 36);
                background-color: rgb(249, 246, 239);
                border-radius:7
                } 
            """)
        #self.combo_box.addItem('username1')
        #self.combo_box.addItem('username2')

    # push button that will allow the user to connect or disconnect
    def setup_button(self):
        self.connect_button.setText('Connect')
        self.connect_button.setFont(QFont('Courier New', 12))
        self.connect_button.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        self.connect_button.setEnabled(False)

        self.connect_button.setStyleSheet("""
            QWidget {
                border: 4px solid black;
                color: QColor(47, 36, 36);
                background-color: rgb(182, 177, 169);
                border-radius:10;
                min-width: 10em
                } 
            """)

        self.connect_signal.connect(self.network.handle_username_input)

    def setup_username_line_edit(self):
        self.username_line_edit.setEnabled(True)
        self.username_line_edit.setFont(QFont('Courier New', 12))
        self.username_line_edit.setStyleSheet(""" QLabel { border-radius:10} """)
        self.username_line_edit.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)

        self.username_line_edit.setStyleSheet("""
            QWidget {
                border: 2px solid black;
                color: rgb(0, 80, 92);
                background-color: rgb(249, 246, 239);
                border-radius:10;
                font: bold
                } 
            """)

        self.user_username = self.username_line_edit.text()

    def setup_labels(self):
        # username:
        self.username_label.setText("username:")
        self.username_label.setAlignment(Qt.AlignCenter)
        self.username_label.setFont(QFont('Courier New', 12))
        self.username_label.setStyleSheet(""" QLabel{ color: white} """)

        # connection status
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFont(QFont('Courier New', 12))
        self.status_label.setStyleSheet(""" QLabel{ color: white } """)

        # chat users:
        self.combobox_label.setFont(QFont('Courier New', 12))
        self.combobox_label.setStyleSheet(""" QLabel{ color: white; border-radius: 7} """)

        self.status_label.setStyleSheet(""" QLabel { color: white }""")

    # the area where the user will write a text
    def setup_message_area(self):
        self.message_line_edit.setObjectName("MessageLineEdit")
        self.message_line_edit.setEnabled(True)
        self.message_line_edit.setPlaceholderText("....")
        self.message_line_edit.setFont(QFont('Courier New', 12))
        self.message_line_edit.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)

        self.message_line_edit.setStyleSheet("""
            QWidget {
                border: 4px solid black;
                color: QColor(47, 36, 36);
                background-color: rgb(249, 246, 239);
                border-radius:10;
                } 
            """)
        #self.message_line_edit.setWordWrap(True)
        print(self.message_line_edit.width())

    # button to send a message
    def setup_send_button(self):
        self.send_button.setEnabled(True)
        self.send_button.setText("Send")
        self.send_button.setFont(QFont('Courier New', 12))

        self.send_button.setStyleSheet("""
            QPushButton {
                border: 4px solid black;
                color: QColor(47, 36, 36);
                background-color: rgb(199, 209, 197);
                border-radius:10;
                min-width: 10em
                } 
            """)

        self.send_message_signal.connect(self.network.handle_message_input)

    # arrange and add the components on the grid_layout
    def setup_layout(self):
        self.grid_layout.setHorizontalSpacing(24)
        self.grid_layout.setContentsMargins(7, 7, 7, 7, )
        self.grid_layout.setVerticalSpacing(7)
        self.grid_layout.setRowStretch(0, 1)
        self.grid_layout.setRowStretch(1, 1)
        self.grid_layout.setRowStretch(6, 8)
        self.grid_layout.setRowStretch(4, 2)
        self.grid_layout.setRowStretch(8, 2)

        self.grid_layout.addWidget(self.username_label, 1, 0, 1, 1)
        self.grid_layout.addWidget(self.username_line_edit, 1, 1, 1, 1)
        self.grid_layout.addWidget(self.combobox_label, 3, 0, 1, 1)
        self.grid_layout.addWidget(self.combo_box, 3, 1, 1, 1)
        self.grid_layout.addWidget(self.status_label, 4, 0, 1, -1)
        self.grid_layout.addWidget(self.connect_button, 1, 2, 1, 1)
        self.grid_layout.addWidget(self.scroll_area, 6, 0, 1, -1)
        self.grid_layout.addWidget(self.message_line_edit, 8, 0, 1, 3)
        self.grid_layout.addWidget(self.send_button, 9, 1, 1, 1)

        self.setLayout(self.grid_layout)

    def setup_signal_slots(self):
        self.connect_button.clicked.connect(self.connect_clicked)
        self.username_line_edit.textChanged.connect(self.check_username_text)
        self.message_line_edit.textChanged.connect(self.check_message_text)
        self.send_button.clicked.connect(self.send_button_clicked)
        self.network.send_clients_signal.connect(self.update_combobox)
            
    def connect_clicked(self):
        self.connect_signal.emit(self.user_username)
        self.connect_button.setText('Disconenct')
        self.connect_button.setStyleSheet("""
            QWidget {
                border: 4px solid black;
                color: rgb(47, 36, 36);
                background-color: rgb(0, 155, 118);
                border-radius:10
                } 
            """)
    # do not allow the user to send any mesasges if no active users
    def send_button_clicked(self):
        if self.get_current_users() <= 0:
            self.log_status('There are no active users, you cannot send a message!', Status.WARNING)
        else:
            self.send_message_signal.emit(self.user_message)
            self.user_message = ""
            self.message_line_edit.clear()
        
    # gets the current users in the combo_box, this is usefull
    # when trying to see if there are any active users 
    def get_current_users(self):
        return self.combo_box.count()
        
    # takes a string message that represents the current status of some components
    
    def log_status(self, msg, status):
        self.status_label.setText(msg)
        self.status_label.setWordWrap(True)
        
        if status == Status.CRITICAL:          
            self.status_label.setStyleSheet("""QLabel {color: rgb(177, 4, 14)}""")
        elif status == Status.WARNING:
            self.status_label.setStyleSheet("""QLabel {color: rgb(178, 111, 22)}""")
        elif status == Status.INFO:
            self.status_label.setStyleSheet("""QLabel {color: rgb(0, 124, 146)}""")
        
    # enables/dissables the 'connect' button and updates the 'user_inpu' with current info
    def check_username_text(self):
        self.connect_button.setEnabled(True)
        if self.user_username != self.username_line_edit.text():
            self.user_username = self.username_line_edit.text()
       # dissable the 'connect' button if no imput in username edit line
        if self.username_line_edit.text() == "":
            self.connect_button.setEnabled(False)

    def check_message_text(self):
        if self.user_message != self.message_line_edit.text():
            self.user_message = self.message_line_edit.text()
        print(self.user_message)

    def update_combobox(self, str_clients):
        #self.network.handle_combobox_selection()
        clients = list(str_clients.split('|'))
        self.combo_box.addItems(clients)
        self.combo_box.addItem('All')
        print('clients list: {}'.format(clients))

    # this signal handler can be implemented in place of the SIG_DFL
    # to allo for more control when application is closed using Ctrl+C
    #def sigint_handler(self, *args):
    #    sys.stderr.write('\r')
    #    if(QMessageBox.question(None, '', "Are you sure you want to quit?",
    #                            QMessageBox.Yes | QMessageBox.No,
    #                            QMessageBox.Yes) == QMessageBox.Yes):
    #        QMessageBox.setWindowFlags(Qt.WindowStaysOnTopHint)
    #        QApplication.quit()

    # handle anything you have to hanle
    # before the application closes
    def exit_app_handler(self):
        print('I am about to exit')
        # close the client here
        self.network.handle_disconnect()
        # add more cleanup if necessary

 # instatiating the MainWindow
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    APP = QApplication(sys.argv)
    WINDOW = MainWindow()
    WINDOW.show()

    APP.aboutToQuit.connect(WINDOW.exit_app_handler)

    sys.exit(APP.exec_())
        