'''
helper class for server process
'''

import re
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QBrush, QLinearGradient
from PyQt5.QtWidgets import (QLabel, QRadioButton, QFormLayout,
                             QSizePolicy, QLineEdit, QDialog, QDialogButtonBox)
from interface import Colors

class ServerDialog(QDialog):
    host_ip = ""
    port = None
    default_host = '127.0.0.1'
    default_port = 33002

    def __init__(self):
        super().__init__()

        self.is_host_valid = False
        self.is_port_valid = False

        self.resize(400, 200)
        self.setWindowTitle("Server Settings")

        self.set_palette()

        self.layout = QFormLayout(self)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self.settings_message = QLabel(self)
        self.use_default_label = QLabel(self)
        self.radio_button = QRadioButton(self)
        self.host_label = QLabel(self)
        self.host_edit_line = QLineEdit(self)
        self.port_label = QLabel(self)
        self.port_edit_line = QLineEdit(self)
        self.button_box = QDialogButtonBox(self)
        self.setup_buttons()

        self.setup_ui()

        self.host_edit_line.textChanged.connect(self.validate_host)
        self.port_edit_line.textChanged.connect(self.validate_port)
        self.radio_button.toggled.connect(self.handle_checked_radiobtn)

    def setup_ui(self):
        self.setup_labels()
        self.setup_edit_lines()
        self.setup_buttons()
        self.setup_radio_btn()

    def setup_labels(self):
        # settings label
        self.settings_message.setFont(QFont('Courier New', 12))
        self.settings_message.setText('Server Settings')
        self.settings_message.setAlignment(Qt.AlignCenter)
        self.layout.setWidget(0, QFormLayout.SpanningRole, self.settings_message)
        # default label
        self.use_default_label.setFont(QFont('Courier New', 12))
        self.use_default_label.setText('use default settings:')
        self.layout.setWidget(1, QFormLayout.LabelRole, self.use_default_label)
        # host label
        self.host_label.setFont(QFont('Courier New', 12))
        self.host_label.setText('HOST: ')
        self.layout.setWidget(2, QFormLayout.LabelRole, self.host_label)
        # port label
        self.port_label.setFont(QFont('Courier New', 12))
        self.port_label.setText('PORT: ')
        self.layout.setWidget(3, QFormLayout.LabelRole, self.port_label)

    def setup_edit_lines(self):
        # host edit line
        self.host_edit_line.setFont(QFont('Courier New', 12))
        self.host_edit_line.setPlaceholderText("127.0.0.1")
        self.host_edit_line.setEnabled(False)
        self.host_edit_line.setSizePolicy(QSizePolicy.MinimumExpanding,
                                          QSizePolicy.MinimumExpanding)
        self.layout.setWidget(2, QFormLayout.FieldRole, self.host_edit_line)
        # port edit line
        self.port_edit_line.setFont(QFont('Courier New', 12))
        self.port_edit_line.setPlaceholderText('33002')
        self.port_edit_line.setEnabled(False)
        self.host_edit_line.setSizePolicy(QSizePolicy.MinimumExpanding,
                                          QSizePolicy.MinimumExpanding)
        self.layout.setWidget(3, QFormLayout.FieldRole, self.port_edit_line)

    def setup_buttons(self):
        self.button_box.setOrientation(Qt.Horizontal)
        self.button_box.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.button_box.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.button_box.setFont(QFont('Courier New', 12))
        self.layout.setWidget(4, QFormLayout.SpanningRole, self.button_box)

        self.button_box.button(QDialogButtonBox.Ok).clicked.connect(self.ok_clicked)
        self.button_box.button(QDialogButtonBox.Cancel).clicked.connect(self.cancel_clicked)

    def setup_radio_btn(self):
        self.radio_button.setChecked(True)
        self.layout.setWidget(1, QFormLayout.FieldRole, self.radio_button)

    def get_settings(self):
        return self.host_ip, self.port

    def handle_checked_radiobtn(self):
        if self.radio_button.isChecked():
            #dissable the input for host and port
            self.host_edit_line.setEnabled(False)
            self.port_edit_line.setEnabled(False)
        elif not self.radio_button.isChecked():
            #enable the input for host and port
            self.button_box.button(QDialogButtonBox.Ok).setEnabled(False)
            self.host_edit_line.setEnabled(True)
            self.port_edit_line.setEnabled(True)

    def validate_host(self):
        patrn = (r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
        ipv4_pattern = re.compile(patrn)
        isa_match = ipv4_pattern.match(self.host_edit_line.text())

        # check to see if the ip match and
        #if the port edit line is not empty
        if isa_match:
            self.host_edit_line.setStyleSheet("""
                QWidget {
                    background-color: rgba(0, 155, 118, 50)
                    }
                """)

            self.is_host_valid = True
        else:
            self.host_edit_line.setStyleSheet("""
                QWidget {
                    background-color: rgba(177, 4, 14, 50)
                    }
                """)
            self.is_host_valid = False

        self.validate_ok_btn()

    def validate_port(self):
        port_str = self.port_edit_line.text()

        if port_str.isnumeric():
            self.port_edit_line.setStyleSheet("""
                QWidget {
                    background-color: rgba(0, 155, 118, 50)
                    }
                """)
            self.is_port_valid = True
        else:
            self.port_edit_line.setStyleSheet("""
                QWidget {
                    background-color: rgba(177, 4, 14, 50)
                    }
                """)
            self.is_port_valid = False

        self.validate_ok_btn()

    def validate_ok_btn(self):
        if self.is_host_valid and self.is_port_valid:
            self.button_box.button(QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.button_box.button(QDialogButtonBox.Ok).setEnabled(False)

    def ok_clicked(self):
        if self.radio_button.isChecked():
            self.host_ip = self.default_host
            self.port = self.default_port
        else:
            self.host_ip = self.host_edit_line.text()
            self.port = self.port_edit_line.text()
        self.done(1)

    def cancel_clicked(self):
        self.done(0)

    def set_palette(self):
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, 100)
        gradient.setColorAt(1.0, Colors.light_sandstone)
        gradient.setColorAt(0.0, Colors.stone)
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)
'''
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    APP = QApplication(sys.argv)
    WINDOW = ServerDialog()
    WINDOW.show()
    sys.exit(APP.exec_())
'''