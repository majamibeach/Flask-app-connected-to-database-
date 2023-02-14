from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTextEdit, QPushButton, QDialog, QWidget, QStackedWidget
from PyQt5 import uic 
from PyQt5 import QtWidgets
from PyQt5.QtGui import QMovie
import sys
import MQTT
import facial_req
import servo
import qr_scann


class LoginUi(QMainWindow):
    def __init__(self):
        super(LoginUi, self).__init__()
        # Load the ui file
        uic.loadUi("login.ui", self)

        # set qmovie as label
        #self.label.setStyleSheet("border: 10px solid gray;")
        #self.label.setStyleSheet("border-radius:10")
        self.movie = QMovie("login.gif")
        self.label.setMovie(self.movie)
        self.movie.start()
#         rgb(170, 228, 255);
        self.pushButton.clicked.connect(self.FaceReq)
        self.pushButton.setStyleSheet("QPushButton"
                             "{"
                             "background-color : rgb(170, 228, 255);"
                             "}"
                             "QPushButton::pressed"
                             "{"
                             "background-color : rgb(92, 132, 197);"
                             "}"
                             )
        
        #self.show()
        
    def FaceReq(self):
        servo.Servo.FaceScan()
        MainWindow.label_2.setText(facial_req.start_req())
        widget.setCurrentWidget(MainWindow)
        
        #facial_req.start_req.user = ""
        
class MainUi(QMainWindow):
    def __init__(self):
        super(MainUi, self).__init__()
        # Load the ui file
        uic.loadUi("main.ui", self)
        
        self.pushButton.clicked.connect(self.Logout)
        self.pushButton_2.clicked.connect(self.ScanQR)
        self.pushButton_3.clicked.connect(self.GetMass)
    
    def Logout(self):
        MainWindow.label_2.setText("")
        widget.setCurrentWidget(LoginWindow)
        
    def ScanQR(self):
        servo.Servo.QrScan()
        self.label_5.setText("")
        self.label_5.setText(qr_scann.Scanner.scan())
        
    def GetMass(self):
        self.label_6.setText(MQTT.get_mass())

app = QApplication(sys.argv)
MQTT.main()
s = servo.Servo()
widget = QtWidgets.QStackedWidget()
LoginWindow = LoginUi()
MainWindow = MainUi()
widget.addWidget(LoginWindow)
widget.addWidget(MainWindow)

widget.showMaximized()

app.exec_()