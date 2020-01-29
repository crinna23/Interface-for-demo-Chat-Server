'''
Main - starting point to the Interface for Chat Server

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

    host, port = dialog_app.get_settings()

    main_window = interface.MainWindow()
    main_window.show()
    main_window.run_server_process(host, port)
    app.aboutToQuit.connect(main_window.exit_app_handler)

    sys.exit(app.exec_())
if __name__ == '__main__':
    main(sys.argv)
