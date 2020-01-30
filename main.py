'''
Main - starting point to the Interface for Chat Server
- executes the dialog box for Server Settings
- executes the main application window

01/28/2020
cristina sewell
'''
import sys
import signal
from PyQt5.QtWidgets import QApplication
import interface
import serverdialog

def main(argv):
    interface.signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(argv)

    dialog_app = serverdialog.ServerDialog()
    if not dialog_app.exec_():
        sys.exit(0)

    # get the server ip_addr and port
    host, port = dialog_app.get_settings()

    main_window = interface.MainWindow()
    main_window.set_connection_settings(host, port)
    main_window.show()
    app.aboutToQuit.connect(main_window.exit_app_handler)

    sys.exit(app.exec_())

if __name__ == '__main__':
    main(sys.argv)
