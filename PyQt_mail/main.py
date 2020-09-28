from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import *
import sys
from mailTransactions import get_inbox, send_mail


class MailUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.my_ui = uic.loadUi("main_window.ui", self)

        self.popup = QMessageBox()
        self.popup.setWindowTitle("MessageBox demo")
        self.popup.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        # for sending
        self.toEdit = self.my_ui.toEdit
        self.subjectEdit = self.my_ui.subjectEdit
        self.bodyEdit = self.my_ui.bodyEdit
        self.sendBtn = self.my_ui.sendButton

        # for receiving
        self.fromLabel = self.my_ui.fromLabel
        self.subjectLabel = self.my_ui.subjectLabel
        self.receivedMsg = self.my_ui.receivedEdit
        self.searchBtn = self.my_ui.searchButton

        self.my_ui.setFixedSize(659, 438)
        self.show()

        self.sendBtn.clicked.connect(self.send_mail)
        self.searchBtn.clicked.connect(self.show_inbox)

    def send_mail(self):
        self.toPerson = self.toEdit.toPlainText()
        self.toSubject = self.subjectEdit.toPlainText()
        self.Msg = self.bodyEdit.toPlainText()

        try:
            send_mail(text=self.Msg, subject=self.toSubject, to_email=[self.toPerson])
            self.popup.setIcon(QMessageBox.Information)
            self.popup.setText("Mail has been successfully sent.")
            self.popup.exec_()
        except:
            self.popup.setIcon(QMessageBox.Warning)
            self.popup.setText("Something went wrong! :(")
            self.popup.exec_()

    def show_inbox(self):
        inbox_data = get_inbox()

        self.fromLabel.setText(inbox_data['From'])
        self.subjectLabel.setText(inbox_data['Subject'])
        self.receivedMsg.setPlainText(inbox_data['Body'])


app = QtWidgets.QApplication(sys.argv)
screen = MailUI()
sys.exit(app.exec_())



