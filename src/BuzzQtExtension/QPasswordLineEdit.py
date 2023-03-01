from qtpy.QtGui import QIcon
from qtpy.QtWidgets import QLineEdit, QWidget
from BuzzQtExtension.res.ui import resource_rc


class QPasswordLineEdit(QLineEdit):
    def __init__(self, parent: QWidget):
        QLineEdit.__init__(self, parent)

        self.visible_icon = QIcon(":/icon/eye_visible")
        self.hidden_icon = QIcon(":/icon/eye_hidden")

        self.setEchoMode(QLineEdit.EchoMode.Password)
        self.toggle_password_action = self.addAction(self.visible_icon, QLineEdit.ActionPosition.TrailingPosition)
        self.toggle_password_action.triggered.connect(self.on_toggle_password_action_triggered)

    def on_toggle_password_action_triggered(self):
        if self.echoMode() == QLineEdit.EchoMode.Normal:
            self.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_password_action.setIcon(self.visible_icon)
        else:
            self.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_password_action.setIcon(self.hidden_icon)