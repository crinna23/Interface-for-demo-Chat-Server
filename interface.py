'''
Chat Interface

01/23/2020
cristina sewell

ToDo: setObjectName??
'''
import sys
import signal
from PyQt5.QtGui import QFont, QPalette, QColor, QBrush, QLinearGradient
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QSize, QRect, Qt 
from PyQt5.QtWidgets import (QApplication, QLineEdit, QPushButton,
    QWidget, QGridLayout, QVBoxLayout, QStackedLayout, QStyle, QLabel, QComboBox, 
    QScrollArea, QMessageBox, QFrame, QSpacerItem, QSizePolicy, QTextEdit)
import network

class MainWindow(QWidget):     
     # signals 

    error_signal = pyqtSignal(str)
    connect_signal = pyqtSignal(str)
    text_changed_signal = pyqtSignal(str, str)

    user_input = ""

    def __init__(self):
        super().__init__()

        min_width = 600
        min_height = 1000
        self.title = "SLAC Chat"
        self.resize(min_width, min_height)
        self.setWindowTitle(self.title)

        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        
        self.centralwidget = QWidget(self)
        self.gridLayoutWidget = QWidget(self.centralwidget)

        self.gridLayoutWidget.setGeometry(QRect(0, 0, 600, 300))

        
        self.style_colors()

        palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, 300)
        gradient.setColorAt(1.0, self.chocolate)
        gradient.setColorAt(0.0, self.stone)
        
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)
        
        #create an instance of Network Module
        self.network = network.Network()
     #   self.setup_communication(self.network)

        self.setupUi()
        self.setup_signal_slots()

   # def setup_communication(self, module):
   #     self.connect_signal.connect(self.network.handle_connect)

        #self.push_import.clicked.connect(self.import_data)
        #self.push_cancel.clicked.connect(self.close_app)
        #self.push_ok.clicked.connect(self.process_input)        
    
    def setup_signal_slots(self):
        self.connect_button.clicked.connect(self.button_clicked)
        self.username_line_edit.textChanged.connect(self.check_username_text)
        
    # Note: the colors bellow have been borrowed from 
    # https://identity.stanford.edu/color.html
    def style_colors(self):
        self.stone = QColor(84, 73, 72)
        self.light_sandstone = QColor(249, 246, 239)
        self.light_sage = QColor(199, 209, 197)
        self.chocolate = QColor(47, 36, 36)
        self.lagunita = QColor(0, 124, 146)
        self.teal = QColor(0, 80, 92)

    # defines the main area where the messages
    # will be exchanged or displayed
    def setup_chat_area(self):
        self.scrollArea = QScrollArea(self.gridLayoutWidget)
        self.scrollArea.setContentsMargins(2, 2, 2, 2)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, 300)
        gradient.setColorAt(0.0, self.light_sandstone)
        gradient.setColorAt(1.0, self.light_sage)
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.scrollArea.setPalette(palette)

        self.scrollArea.setFont(QFont('Courier New', 12))
        
        # the widget with messages can have a small opacity baground color
        # one color for client, one for server

        widget = QWidget()
        self.scrollArea.setWidget(widget)
        self.scrollAreaLayout = QVBoxLayout(widget)
        self.scrollAreaLayout.setAlignment(Qt.AlignTop)
      
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.verticalScrollBar().setSingleStep(20)

        for i in range(30):
            i = QLabel('start------------------------------------------------------------end')
         #   i.setWordWrap(True)
           # i.setMinimumWidth(1)
            l = self.scrollAreaLayout.layout()
            l.insertWidget(l.count() - 1, i)


        

        # maybe add a message widget here???
        label = QLabel('this is a message')
        self.scrollAreaLayout.addWidget(label)
        #self.scrollAreaLayout.addWidget()
       # widget.setStyleSheet(self.widget_style)
        #self.scrollAreaLayout.addStretch(1)

    #combo box that holds the list of
    #clients that are currently participating
    def setup_combobox(self):
        self.combo_box = QComboBox(self.gridLayoutWidget)
        self.combo_box.setFont(QFont('Courier New', 12))
        self.combo_box.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)

        self.combo_box.setStyleSheet(""" 
            QWidget {
                border: 1px solid black;
                color: QColor(47, 36, 36);
                background-color: rgb(249, 246, 239);
                border-radius:10;
                } 
            """)
        #self.comboBox.setGeometry(QRect(40, 40, 300, 35))
    
    # push button that will allow the user to connect or disconnect
    def setup_button(self):
        self.connect_button = QPushButton(self.gridLayoutWidget)
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
        
       # self.trigger.connect(self.connect_to_server)
        self.connect_signal.connect(self.network.handle_username_input)
       # self.connectButton.clicked.connect(self.button_clicked)
    
    def setup_username_line_edit(self):
        self.username_line_edit = QLineEdit(self.gridLayoutWidget)
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

        self.user_input = self.username_line_edit.text()
        # connecting to 'check_username_text' anytime somethins is added or removed 
        # from the QLineEdit
       
    
    # enables/dissables the 'connect' button and updates the 'user_inpu' with current info
    def check_username_text(self):
        self.connect_button.setEnabled(True)
        if self.user_input != self.username_line_edit.text():
            self.user_input = self.username_line_edit.text()
       # dissable the 'connect' button if no imput in username edit line
        if self.username_line_edit.text() == "":
            self.connect_button.setEnabled(False)

    def setup_labels(self):
        # username:
        self.username_label = QLabel(self.gridLayoutWidget)
        self.username_label.setText("username:")
        self.username_label.setAlignment(Qt.AlignCenter)
        self.username_label.setFont(QFont('Courier New', 12))
        self.username_label.setStyleSheet(""" QLabel{ color: white} """)
 
        # connection status
        self.status_label = QLabel('Status..')
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFont(QFont('Courier New', 12))
        self.status_label.setStyleSheet(""" QLabel{ color: white } """)
        
        # message to:
        self.combobox_label = QLabel("message to: ")
        self.combobox_label.setFont(QFont('Courier New', 12))
        self.combobox_label.setStyleSheet(""" QLabel{ color: white; border-radius: 7} """)

        self.status_label.setStyleSheet(""" QLabel { color: white }""")

    def setup_layout(self):
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(2, 2, 2, 2)
        self.gridLayout.setHorizontalSpacing(24)
        self.gridLayout.setVerticalSpacing(7)
        self.gridLayout.setRowStretch(0, 1)
        self.gridLayout.setRowStretch(1, 1)
        self.gridLayout.setRowStretch(6, 8)
        self.gridLayout.setRowStretch(4, 2)

        self.gridLayout.addWidget(self.username_label, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.username_line_edit, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.combobox_label, 3, 0, 1, 1)
        self.gridLayout.addWidget(self.combo_box, 3, 1, 1, 1)
        self.gridLayout.addWidget(self.status_label, 4, 0, 1, -1)
        self.gridLayout.addWidget(self.connect_button, 1, 2, 1, 1)
        self.gridLayout.addWidget(self.scrollArea, 6, 0, 1, -1)

        self.setLayout(self.gridLayout)

    def setupUi(self):        
        self.setup_chat_area()
        self.setup_combobox()
        self.setup_button()
        self.setup_labels()
        self.setup_username_line_edit()
        self.setup_layout()

   


   # @pyqtSlot(int, name = 'name')
    def some_method(self, arg1):
        pass

    def button_clicked(self):
        self.connect_signal.emit(self.user_input)
        self.connect_button.setText('Disconenct')
        self.connect_button.setStyleSheet(""" 
            QWidget {
                border: 4px solid black;
                color: rgb(47, 36, 36);
                background-color: rgb(0, 155, 118);
                border-radius:10
                } 
            """)
        
    def connect_to_server(self, client):
        print('Is trying to connect...')
        # connect to server
    
    def add_items_to_combobox(self, item):
        print('we will be adding a list of clients here')

    def sigint_handler(*args):
        sys.stderr.write('\r')
        if(QMessageBox.question(None, '', "Are you sure you want to quit?", 
                                QMessageBox.Yes | QMessageBox.No, 
                                QMessageBox.Yes) == QMessageBox.Yes):
            QMessageBox.raise_
            QApplication.quit()

  #  def keyPressEvent(cls, self, QKeyEvent):
   #     return super().keyPressEvent(self, QKeyEvent)

 # instatiating the MainWindow
if __name__ == "__main__":
    signal.signal(signal.SIGINT, MainWindow.sigint_handler)
    app = QApplication(sys.argv)
    window = MainWindow() 
    window.show()
    sys.exit(app.exec_())
        