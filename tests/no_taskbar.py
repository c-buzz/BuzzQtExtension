import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class NoteWindow(QFrame):
    i = 1

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.Tool)
        self.setWindowTitle(str(self.i))
        NoteWindow.i += 1
        self.show()

app = QApplication([])
w1 = NoteWindow()
w2 = NoteWindow()

# close the app after 10 seconds
close_timer = QTimer()
close_timer.singleShot(10000, app.quit)

sys.exit(app.exec())