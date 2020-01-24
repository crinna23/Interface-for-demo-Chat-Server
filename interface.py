'''
Chat Interface
'''
import sys
import signal
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QSize, QRect, Qt, QTimer
from PyQt5.QtWidgets import ( QApplication, QLineEdit, QPushButton, 
    QWidget, QGridLayout, QVBoxLayout, QStackedLayout, QStyle, QLabel, QComboBox, 
    QScrollArea, QMessageBox, QApplication )


class MainWindow(QWidget):
    
    # signals 
    trigger = pyqtSignal(str)
    error_signal = pyqtSignal(str)

     
    def __init__(self):
        super().__init__()

        min_width = 1200
        min_height = 1200
        self.title = "SLAC Chat"
    
        self.setWindowTitle(self.title)
        self.setMinimumSize(QSize(min_width, min_height))

        palette = QPalette()
        #palette.setColor(QPalette.Window, QColor(155, 28, 49))
        palette.setColor(QPalette.Window, QColor(84,73,72))
        self.setPalette(palette)

        self.setupUi()
    
    # defines the main area where the messages
    # will be exchanged or displayed
    def setup_chat_area(self):
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setContentsMargins(2, 2, 2, 2)
       # self.scrollArea.setMaximumWidth(650)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(249,246,239))
        self.scrollArea.setPalette(palette)

        widget = QWidget()
        self.scrollArea.setWidget(widget)
        self.scrollAreaLayout = QVBoxLayout(widget)
        # maybe add a message widget here???
        #self.scrollAreaLayout.addWidget()
        self.scrollAreaLayout.addStretch(1)

   
    #combo box that will hold the list of
    #clients that are currently participating
    def setup_combobox(self):
        self.comboBox = QComboBox()
        self.comboBox.setGeometry(QRect(40, 40, 300, 35))
    
    # push button that will allow the user to connect or disconnect
    def setup_button(self):
        self.connectButton = QPushButton('Connect')
        self.connectButton.setFont(QFont('Calibri', 12))

        self.connectButton.setStyleSheet(""" 
            QWidget {
                border: 3px solid black;
                color: rgb(249,246,239);
                background-color: rgb(47, 36, 36);
                border-radius:3;
                min-width: 10em;
                } 
            """)

        self.connectButton.clicked.connect(self.button_clicked)
    
    def setup_username_line_edit(self):
        self.usernameLineEdit = QLineEdit(self)
        self.usernameLineEdit.setFont(QFont('Calibri', 12))
        self.usernameLineEdit.setEnabled(True)


    def setup_labels(self):
        self.username_label = QLabel('Username: ')
        self.status_label = QLabel('Status.........................')
        

    def setup_layout(self):
        self.gridLayout = QGridLayout(self)

        self.gridLayout.setSpacing(30)

        self.gridLayout.addWidget(self.scrollArea, 1, 2, -1, -1)
        self.gridLayout.addWidget(self.usernameLineEdit, 2, 0)
        self.gridLayout.addWidget(self.connectButton, 4, 0)
        self.gridLayout.addWidget(self.comboBox, 6, 0)
        self.gridLayout.addWidget(self.username_label, 1, 0)
        self.gridLayout.addWidget(self.status_label, 5, 0)

        self.gridLayout.setColumnStretch(2, 1)
        self.setLayout(self.gridLayout)

    def setupUi(self):        
        self.setup_chat_area()
        self.setup_combobox()
        self.setup_button()
        self.setup_labels()
        self.setup_username_line_edit()
        self.setup_layout()

        self.trigger.connect(self.connect_to_server)


   # @pyqtSlot(int, name = 'name')
    def some_method(self, arg1):
        pass

    def button_clicked(self):
        self.trigger.emit('REGISTER')
        
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
    #QTimer::singleShot(1000, &app, sigint_handler)
    #timer = QTimer()
   # timer.start(500)
   # timer.timeout.connect(lambda: None)
    window = MainWindow()
    #window.resize(600, 800)
    window.show()

    sys.exit(app.exec_())
        