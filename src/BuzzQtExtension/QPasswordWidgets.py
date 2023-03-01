from enum import Enum, auto
from typing import Optional, Tuple, Union

from qtpy.QtGui import QIcon
from qtpy.QtWidgets import *
from qtpy.QtCore import Qt
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


class QPasswordDialog(QDialog):
    class Mode(Enum):
        ChangePassword = auto()
        TypePassword = auto() # <-- Used when needed to type a pre-existing password
        CreatePassword = auto()  # <-- Used when needed to create a new password: confirm is present

    def __init__(self, parent: QWidget = None, old_password: str = None, mode = Mode.TypePassword):
        QDialog.__init__(self, parent)

        v_layout = QVBoxLayout(self)

        if mode == QPasswordDialog.Mode.CreatePassword:
            self.setWindowTitle("Set a password")
        elif mode == QPasswordDialog.Mode.ChangePassword:
            self.setWindowTitle("Change the password")
        elif mode == QPasswordDialog.Mode.TypePassword:
            self.setWindowTitle("Type a password")
        else:
            raise ValueError("Password Mode unknown")


        # Password 1
        self.old_password_label = QLabel("Old password: ", self)
        self.old_password_edit = QPasswordLineEdit(self)
        if not mode == QPasswordDialog.Mode.ChangePassword:
            self.old_password_edit.setVisible(False)
            self.old_password_label.setVisible(False)

        # Password 2
        self.master_password_label = QLabel("Type a password")
        self.master_password_edit = QPasswordLineEdit(self)
        if mode == QPasswordDialog.Mode.ChangePassword:
            self.master_password_label.setText("Type a new password")

        # Password 3
        self.password_confim_label = QLabel("Confirm password")
        self.password_confirm_edit = QPasswordLineEdit(self)
        if mode == QPasswordDialog.Mode.TypePassword:
            self.password_confirm_edit.setVisible(False)
            self.password_confim_label.setVisible(False)

        self.password_mode = mode

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel,
                                           Qt.Orientation.Horizontal)

        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        v_layout.addWidget(self.old_password_label)
        v_layout.addWidget(self.old_password_edit)
        v_layout.addWidget(self.master_password_label)
        v_layout.addWidget(self.master_password_edit)
        v_layout.addWidget(self.password_confim_label)
        v_layout.addWidget(self.password_confirm_edit)
        v_layout.addWidget(self.button_box)

        self.old_password_to_match = old_password

    @property
    def master_password(self):
        return  self.master_password_edit.text()

    @property
    def old_password(self):
        return self.old_password_edit.text()

    @property
    def password_confirm(self):
        return self.password_confirm_edit.text()

    def is_valid(self) -> bool:
        Mode = QPasswordDialog.Mode
        mandatory_pwd_list = [self.master_password]
        if self.password_mode == Mode.ChangePassword:
            mandatory_pwd_list.append(self.old_password)
            mandatory_pwd_list.append(self.password_confirm)
        elif self.password_mode == Mode.CreatePassword:
            mandatory_pwd_list.append(self.password_confirm)

        if '' in mandatory_pwd_list:
            QMessageBox.critical(self, "Error", "Empty password not allowed")
            return False

        if self.password_mode == Mode.ChangePassword:
            if self.old_password_to_match:
                if not self.old_password == self.old_password_to_match:
                    QMessageBox.critical(self, "Error", 'The old password is not correct')
                    return False
        if self.password_mode in [Mode.ChangePassword, Mode.CreatePassword]:
            if not self.master_password == self.password_confirm:
                QMessageBox.critical(self, "Error", "The two passwords do not match")
                return False

        return True

    def accept(self) -> None:
        if self.is_valid():
            QDialog.accept(self)

    @staticmethod
    def get_password(parent: QWidget, mode=Mode.TypePassword, old_password: str = None) -> Optional[str]:
        dialog = QPasswordDialog(parent, old_password, mode=mode)
        if dialog.exec_() == QDialog.DialogCode.Accepted:
            return \
                (dialog.master_password, dialog.old_password) \
                if mode == QPasswordDialog.Mode.ChangePassword and not old_password \
                else dialog.master_password
        return None

    @staticmethod
    def get_change_password(parent: QWidget, old_password: str = None) -> Optional[Union[str, Tuple[str, str]]]:
        """

        :param parent: QWidget parent of QPasswordDialog created
        :param old_password:
        :return: If old_password is provided, the check is performed internally and the method returns only the new
                password; otherwise, the method return a tuple as (new_password, old_password).
                Returns None if any error occurred
        """
        return QPasswordDialog.get_password(parent, QPasswordDialog.Mode.ChangePassword, old_password)

    @staticmethod
    def get_create_password(parent: QWidget) -> Optional[str]:
        return QPasswordDialog.get_password(parent, QPasswordDialog.Mode.CreatePassword)

