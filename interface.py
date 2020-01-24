'''
Chat Interface
'''
import sys
import signal
from PyQt5.QtGui import QFont, QPalette, QColor, QBrush, QLinearGradient
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QSize, QRect, Qt
from PyQt5.QtWidgets import ( QApplication, QLineEdit, QPushButton,
    QWidget, QGridLayout, QVBoxLayout, QStackedLayout, QStyle, QLabel, QComboBox, 
    QScrollArea, QMessageBox, QApplication, QFrame, QSpacerItem, QSizePolicy)


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

        self.widget_style = " QWidget { border: 2px solid black; color: rgb(47, 36, 36); border-radius:10 }"
        palette = QPalette()
        #palette.setColor(QPalette.Window, QColor(155, 28, 49))
        gradient = QLinearGradient(0, 0, 0, 300)
        # Chocolate
        gradient.setColorAt(1.0, QColor(47, 36, 36))
        # Stone
        gradient.setColorAt(0.0, QColor(87, 73, 72))
        #palette.setColor(QPalette.Background, QColor(249,246,220))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        # Stone
       # palette.setColor(QPalette.Window, QColor(84,73,72))
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
        gradient = QLinearGradient(0, 0, 0, 300)
        # Light Sandstone
        gradient.setColorAt(0.0, QColor(249, 246, 239))
        # Light Sage
        gradient.setColorAt(1.0, QColor(199, 209, 197))
 
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.scrollArea.setPalette(palette)

        self.scrollArea.setFont(QFont('Courier New', 12))

        self.scrollArea.setStyleSheet(self.widget_style)

        # the widget with messages can have a small opacity baground color
        # one color for client, one for server

        widget = QWidget()
        self.scrollArea.setWidget(widget)
        self.scrollAreaLayout = QVBoxLayout(widget)
        # maybe add a message widget here???
        #label = QLabel('this is a message')
        #self.scrollAreaLayout.addWidget(label)
        #self.scrollAreaLayout.addWidget()
        widget.setStyleSheet(self.widget_style)
        #self.scrollAreaLayout.addStretch(1)

    #combo box that will hold the list of
    #clients that are currently participating
    def setup_combobox(self):
        self.comboBox = QComboBox()
        self.comboBox.setFont(QFont('Courier New', 12))

        self.comboBox.setStyleSheet(""" 
            QWidget {
                border: 1px solid black;
                color: rgb(47, 36, 36);
                background-color: rgb(249, 246, 239);
                border-radius:10;
                } 
            """)
        #self.comboBox.setGeometry(QRect(40, 40, 300, 35))
    
    # push button that will allow the user to connect or disconnect
    def setup_button(self):
        self.connectButton = QPushButton('Connect')
        self.connectButton.setFont(QFont('Courier New', 12))

        self.connectButton.setStyleSheet(""" 
            QWidget {
                border: 4px solid black;
                color: rgb(47, 36, 36);
                background-color: rgb(182, 177, 169);
                border-radius:10;
                min-width: 10em
                } 
            """)

        self.connectButton.clicked.connect(self.button_clicked)
    
    def setup_username_line_edit(self):
        self.usernameLineEdit = QLineEdit(self)
        self.usernameLineEdit.setEnabled(True)
        self.usernameLineEdit.setFont(QFont('Courier New', 12))

        self.usernameLineEdit.setStyleSheet(""" 
            QWidget {
                border: 1px solid black;
                color: rgb(47, 36, 36);
                background-color: rgb(249, 246, 239);
                border-radius:10;
                min-width: 10em
                } 
            """)


    def setup_labels(self):
        self.username_label = QLabel('Username: ')
        self.username_label.setFont(QFont('Courier New', 12))
        self.username_label.setStyleSheet(""" 
            QLabel{ 
                color: white;
                qproperty-alignment: AlignVCenter;
                font-family: Courier New;
                color: white
                } 
            """)

        self.status_label = QLabel('Status.........................')
        self.status_label.setFont(QFont('Courier New', 12))
        self.top_label = QLabel(self)
        self.middle_label = QLabel(self)
        self.buttom_label = QLabel(self)
        self.combobox_label = QLabel("Send message to: ")
        self.combobox_label.setFont(QFont('Courier New', 12))
        self.combobox_label.setStyleSheet(""" QLabel{ color: white } """)

        self.top_label.setFrameShape(QFrame.NoFrame)
        self.middle_label.setFrameShape(QFrame.NoFrame)
        self.buttom_label.setFrameShape(QFrame.NoFrame)

        self.status_label.setStyleSheet("""
            QLabel {
                qproperty-alignment: AlignJustify;
                font-family: Courier New;
                color: white;
                font: bold 16em
            }""")

    def setup_layout(self):
        self.gridLayout = QGridLayout(self)

        self.gridLayout.addWidget(self.top_label, 0, 0, 1, -1)
        self.gridLayout.addWidget(self.middle_label, 4, 0, 1, -1)
        self.gridLayout.addWidget(self.buttom_label, 8, 0, 1, -1)
        self.gridLayout.addWidget(self.username_label, 1, 0)
        self.gridLayout.addWidget(self.usernameLineEdit, 1, 1)
        self.gridLayout.addWidget(self.combobox_label, 3, 0)
        self.gridLayout.addWidget(self.comboBox, 3, 1)
        self.gridLayout.addWidget(self.status_label, 6, 0, 1, -1)
        self.gridLayout.addWidget(self.connectButton, 1, 2)
        self.gridLayout.addWidget(self.scrollArea, 7, 0, 1, -1)
       
        self.gridLayout.setColumnStretch(1, 1)

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
    
    window.show()

    sys.exit(app.exec_())
        