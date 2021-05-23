#!/usr/bin/python3
from PyQt5.QtCore import QSize,Qt
from PyQt5.QtWidgets import QHBoxLayout, QInputDialog, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QWidget , QApplication
from PyQt5.QtGui import QIcon
import sys
import socket 
from threading import Thread

tcpConnection = None

class myWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.top = 80
        self.left = 400
        self.win_width = 450 
        self.win_height = 625
        
        self.setWindowTitle("S-Chat | Python PYQt5 Project")
        self.setWindowIcon(QIcon("messenger.ico"))
        self.setGeometry(self.left,self.top,self.win_width,self.win_height)
        self.setMinimumSize(self.win_width,self.win_height)
        

        # set the nickname 
        self.nickname,self.bool_value = QInputDialog.getText(self,"Text Input Dialog","Enter Your Nickname:>") 
        print(self.nickname)
        if self.bool_value == False:
            sys.exit()

        # Set the layouts
        self.vbox_layout = QVBoxLayout()
        self.hbox = QHBoxLayout()
        
        self.label = QLabel()
        self.label.setText(f"User: {self.nickname}")
        self.label.move(10,10)
        self.label.setStyleSheet("background-color:grey; color:rgb(255,255,255); font-size:18px; width:300px; height:20px;")
        self.label.setAlignment(Qt.AlignCenter)
    
        # set the Chat Box  
        self.chatBox = QTextEdit()
        self.chatBox.setGeometry(10,10,400,500)
        self.chatBox.setReadOnly(True)
        self.chatBox.setStyleSheet("background-color:rgb(52, 50, 50);color:rgb(255,255,255);margin:5px 5px;border:2px solid white;border-radius:5px;font-size:15px;")
        self.vbox_layout.addWidget(self.label)
        self.vbox_layout.addWidget(self.chatBox)
        self.setLayout(self.vbox_layout)

        
        # set Send Button
        self.sendBtn = QPushButton()
        self.sendBtn.setIcon(QIcon("send.ico"))
        self.sendBtn.setIconSize(QSize(25,25))
        self.sendBtn.setStyleSheet("background-color:rgb(18, 81, 225);")
        self.sendBtn.clicked.connect(self.sendMsg)

        # set Chat Message
        self.chatMsg = QLineEdit()
        self.chatMsg.setPlaceholderText("Enter Message Here :)")
        self.chatMsg.setStyleSheet("background-color:rgb(52, 50, 50);color:rgb(251, 251, 251);border:1.5px solid white;border-radius:7px;width:350;height:33px;padding:0px 10px;font-size:16px;font-weight:bold;")
        self.chatMsg.setText('')

        self.hbox.addWidget(self.chatMsg)
        self.hbox.addWidget(self.sendBtn)
        self.vbox_layout.addLayout(self.hbox)

    def sendMsg(self):
        msg = self.chatMsg.text()
        tcpConnection.send(msg.encode("utf-8"))
        self.chatMsg.setText('')


class clientThread(Thread):
    def __init__(self,window):
        Thread.__init__(self)
        self.window = window

    def run(self):
        global tcpConnection
        host = '127.0.0.1'
        port = 9090
        BUFFER_SIZE = 2048
        tcpConnection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        tcpConnection.connect((host,port))

        while True:
            data = tcpConnection.recv(BUFFER_SIZE).decode("utf-8")
            if "NAME" in data:
                tcpConnection.send(self.window.nickname.encode("utf-8"))

            else:
                if data.startswith(self.window.nickname):
                    data = str(data)
                    data = data.replace(self.window.nickname,"Me")
                    self.window.chatBox.append(data)
                else:
                    self.window.chatBox.append(data)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = myWindow()
    window.show()
    clientThreading = clientThread(window)
    clientThreading.start()
    sys.exit(app.exec())