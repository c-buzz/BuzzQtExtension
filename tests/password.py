from qtpy.QtWidgets import QInputDialog, QApplication, QMainWindow, QPushButton

app = QApplication()
mw = QMainWindow()
inp = QInputDialog(mw)

btn = QPushButton("Click")

btn.clicked.connect()

def on_btn_clicked():
    QInputDialog.getText(mw, "Password", "Type a password")