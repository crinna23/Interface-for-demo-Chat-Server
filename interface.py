'''
Chat Interface - handles the Main GUI Application

01/23/2020
cristina sewell
'''
import signal
from enum import Enum
from PyQt5.QtGui import QFont, QPalette, QColor, QBrush, QLinearGradient
from PyQt5.QtCore import pyqtSignal, QRect, Qt
from PyQt5.QtWidgets import (QLineEdit, QPushButton,
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

    error_signal = pyqtSignal(str)
    connect_signal = pyqtSignal(str)
    text_changed_signal = pyqtSignal(str, str)
    send_message_signal = pyqtSignal(str, str)
    disconnect_signal = pyqtSignal()
    conn_settings_signal = pyqtSignal(str, int)

    def __init__(self):
        super().__init__()

        min_width = 600
        min_height = 1200
        title = "SLAC Chat"
        self.resize(min_width, min_height)
        self.setWindowTitle(title)

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

    def set_connection_settings(self, addr, port):
        """Setting the HOST Address and the PORT for connection with the server"""
        self.conn_settings_signal.emit(addr, port)

    def setup_ui(self):
        """Setup multiple components of the ui by calling their setup functions"""
        self.setup_chat_area()
        self.setup_combobox()
        self.setup_connect_button(False)
        self.setup_labels()
        self.setup_username_line_edit()
        self.setup_message_area()
        self.setup_send_button()
        self.setup_layout()
        self.log_status('Please provide a username to connect.', Status.INFO)

    def setup_chat_area(self):
        """Defines the main area where the messages will be displayed"""
        self.scroll_area.setContentsMargins(2, 40, 2, 2)
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

        widget = QWidget()
        self.scroll_area.setWidget(widget)
        self.scroll_area_layout = QVBoxLayout(widget)
        self.scroll_area_layout.setAlignment(Qt.AlignTop)

    def setup_combobox(self):
        """Combo box that holds the list of currently active clients"""
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

    def setup_connect_button(self, state):
        """Push button that will allow the user to connect or disconnect
           state: 1 - connected; state:0 - not connected"""
        self.connect_button.setEnabled(False)
        self.connect_button.setFont(QFont('Courier New', 12))
        self.connect_button.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        if state == 0:
        # user connected to the server
            self.connect_button.setText('Connect')
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

        elif state == 1:
            self.connect_button.setText('Disconnect')
            self.connect_button.setEnabled(True)
            self.connect_button.setStyleSheet("""
                QWidget {
                    border: 4px solid black;
                    color: rgb(47, 36, 36);
                    background-color: rgb(0, 155, 118);
                    border-radius:10
                    } 
                """)
            self.disconnect_signal.connect(self.network.handle_usr_disconnect)

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

        self.username_line_edit.returnPressed.connect(self.connect_clicked)

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

    def setup_message_area(self):
        """The area where the user will write a message to be sent"""
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
        self.message_line_edit.returnPressed.connect(self.send_button_clicked)

    def setup_send_button(self):
        """Button to send a message"""
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
        self.conn_settings_signal.connect(self.network.connection_settings)

    def setup_layout(self):
        """Organizes and adds the components of the grid layout"""
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
        self.send_button.clicked.connect(self.send_button_clicked)
        self.network.send_clients_signal.connect(self.update_combobox)
        self.network.send_connected_signal.connect(self.update_connect_btn)
        self.network.display_msg_signal.connect(self.display_message)
        self.network.send_log_signal.connect(self.log_status)
        self.network.send_disconnected.connect(self.update_quit_status)

    def update_quit_status(self):
        self.update_connect_btn(False)
        self.log_status('You have disconnected...', Status.WARNING)

    def display_message(self, message):
        msg_label = QLabel(message)
        msg_label.setFont(QFont('Courier New', 12))
        msg_label.setWordWrap(True)
        msg_label.setStyleSheet("""
            QLabel{ 
                border: 2px solid black;
                background-color: rgba(0, 155, 118, 50)
                }
            """)
        # this needs some fixing, the scroll bar is still not going all the way to the bottom
        self.scroll_area_layout.addWidget(msg_label)
        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())

    def connect_clicked(self):
        # this is not a very good practice here...
        if self.connect_button.text() == "Connect":
            self.log_status('connecting...', Status.INFO)
            # we will send a signal so we can connect
            self.connect_signal.emit(self.username_line_edit.text())
        elif self.connect_button.text() == "Disconnect":
            # send a signal to disconnect
            self.log_status('disconnecting...', Status.INFO)
            self.disconnect_signal.emit()
            self.update_connect_btn(False)


    # do not allow the user to send any mesasges if no active users
    def send_button_clicked(self):
        if self.get_current_users() <= 0:
            self.log_status('You must connect before you can send a message!', Status.WARNING)
        else:
            recipient = str(self.combo_box.currentText())
            self.send_message_signal.emit(self.message_line_edit.text(), recipient)
            self.message_line_edit.clear()
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
        else:
            self.status_label.setStyleSheet("""QLabel {color: rgb(177, 4, 14)}""")

    # enables/dissables the 'connect' button and updates the 'user_input' with current info
    def check_username_text(self):
        self.connect_button.setEnabled(True)
       # dissable the 'connect' button if no imput in username edit line
        if self.username_line_edit.text() == "":
            self.connect_button.setEnabled(False)

    def update_combobox(self, str_clients):
        """Clear the combo box every time the server sends a list
           of clients, this way we have the latest updated list and no duplicates"""
        self.combo_box.clear()

        clients = str_clients.split('|')
        for i in clients:
            self.combo_box.addItem(i)
        self.combo_box.addItem('ALL-Broadcast')

    def update_connect_btn(self, is_connected):
        if is_connected:
            self.log_status("Connected", Status.INFO)
            self.setup_connect_button(True)
        elif not is_connected:
            self.log_status("Not Connected", Status.WARNING)
            self.setup_connect_button(False)
            self.username_line_edit.clear()

    def exit_app_handler(self):
        """Handle here anything you have to handle before closing the main application"""
        # add more cleanup if necessary
        self.network.handle_disconnect()

#if __name__ == "__main__":
#    import sys
#    import signal
#    from PyQt5.QtWidgets import QApplication
#    signal.signal(signal.SIGINT, signal.SIG_DFL)
#    APP = QApplication(sys.argv)
#
#    WINDOW = MainWindow()
#    WINDOW.show()
#    WINDOW.run_server_process()
#    APP.aboutToQuit.connect(WINDOW.exit_app_handler)
#
#    sys.exit(APP.exec_())
