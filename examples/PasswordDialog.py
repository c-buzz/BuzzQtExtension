import sys

from qtpy.QtWidgets import *
from BuzzQtExtension.QPasswordWidgets import QPasswordDialog

def main():
    app = QApplication([])

    mw = QMainWindow()

    simple_type_password_btn = QPushButton("Type a password", mw)
    change_password_btn = QPushButton("Change password", mw)
    change_password_no_old_btn = QPushButton("Change password without old", mw)
    create_password_btn = QPushButton("Create a new password", mw)


    def on_simple_type_password_requested():
        pwd = QPasswordDialog.get_password(mw)
        mw.statusBar().showMessage(f"Typed Password: {pwd}")

    def on_change_password_requested():
        pwd = QPasswordDialog.get_change_password(mw, 'my_old_password')
        mw.statusBar().showMessage(f"Typed Password: {pwd}")

    def on_change_password_no_old_requested():
        pwd = QPasswordDialog.get_change_password(mw)
        mw.statusBar().showMessage(f"New Password: {pwd[0]}. Old password: {pwd[1]}")

    def on_create_password_requested():
        pwd = QPasswordDialog.get_create_password(mw)
        mw.statusBar().showMessage(f"Created Password: {pwd}")

    simple_type_password_btn.clicked.connect(on_simple_type_password_requested)
    change_password_btn.clicked.connect(on_change_password_requested)
    change_password_no_old_btn.clicked.connect(on_change_password_no_old_requested)
    create_password_btn.clicked.connect(on_create_password_requested)

    w = QWidget()
    mw.setCentralWidget(w)

    layout = QVBoxLayout(w)
    layout.addWidget(simple_type_password_btn)
    layout.addWidget(change_password_btn)
    layout.addWidget(change_password_no_old_btn)
    layout.addWidget(create_password_btn)

    mw.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()