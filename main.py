'''
Main - starting point to the Interface for Chat Server
- executes the dialog box for Server Settings
- executes the main application window
- executes a Qprocess that starts the server

01/28/2020
cristina sewell
'''
import sys
import signal
from PyQt5.QtWidgets import QApplication
#from PyQt5.QtCore import QProcess
import interface
import serverdialog

#SERVER_PROCESS = QProcess()

#def exit_app_handler():
 #   try:
 #       print('terminating server process')
 #       SERVER_PROCESS.waitForFinished()
 #       SERVER_PROCESS.terminate()
 #   except:
 #       print('problems closing the server process')
 #       self.SERVER_PROCESS.kill()    
    
def main(argv):
    interface.signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(argv)
  #  SERVER_PROCESS = QProcess()

    
    dialog_app = serverdialog.ServerDialog()
    if not dialog_app.exec_():
        sys.exit(0)

    # get the server ip_addr and port
    host, port = dialog_app.get_settings()
  
    
    #create a QProcess where the server will run
 #   SERVER_PROCESS.setProcessChannelMode(QProcess.ForwardedChannels)
    
 #   process  = "python server.py --host %s --port %s" %(host, port)
 #   print(process)
    
 #   try:
        # check if the server is not running already
 #       SERVER_PROCESS.start(process)
 #       SERVER_PROCESS.waitForStarted()
 #   except QProcess.FailedToStart:
 #       print('Server process failed to start')
 #   except QProcess.Timedout:
  #      print('Server process timedout')
  #  except QProcess.Crashed:
  #      print('Server process crashed')
  #  except QProcess.UnknownError:
 #       print('Server Process - Unknown Error')
 #   except QProcess.WriteError:
 #       print('Server process write error')
 #   except QProcess.ReadError:
  #      print('Server process read error')
    
  #  process_stdout = str(SERVER_PROCESS.readAllStandardOutput())
    # prints what the server is writing on to the console
 #   print(process_stdout)
         
    main_window = interface.MainWindow()
    main_window.set_connection_settings(host, port)
    main_window.show()
    #app.aboutToQuit.connect(main_window.exit_app_handler)

    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main(sys.argv)

