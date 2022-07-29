# All Python Built-in Imports Here.
import sys
from PySide6 import QtWidgets
from PySide6.QtCore import QCoreApplication

# All Custom Imports Here.
from kirana.ui import get_stylesheet
from kirana.ui import prompts
from kirana.db.entities import customers


# All Native Imports Here.

# All Attributes or Constants Here.


class UserRegister(QtWidgets.QDialog):
    def __init__(self, phone_number):
        super(UserRegister, self).__init__()
        self._phone_number = phone_number
        self._layout = QtWidgets.QFormLayout()
        self._f_name_lb = QtWidgets.QLabel('First Name')
        self._f_name_le = QtWidgets.QLineEdit()
        self._l_name_lb = QtWidgets.QLabel('Last Name')
        self._l_name_le = QtWidgets.QLineEdit()
        self._phone_lb = QtWidgets.QLabel('Phone Number')
        self._phone_le = QtWidgets.QLineEdit()
        self._phone_le.setText(str(self._phone_number))
        self._address_lb = QtWidgets.QLabel('Address')
        self._address_le = QtWidgets.QLineEdit()
        self._pin_lb = QtWidgets.QLabel('Postal Code')
        self._pin_le = QtWidgets.QLineEdit()

        self._submit_btn = QtWidgets.QPushButton('Submit')
        self._initialize()

        self.setFixedWidth(500)
        self.setFixedHeight(200)
        self.setWindowTitle('Customer Registration')

    def _initialize(self):
        self._setup_ui()
        self.apply_stylesheet()
        self.setup_connections()

    def _setup_ui(self):
        self.setLayout(self._layout)
        self._layout.addRow(self._f_name_lb, self._f_name_le)
        self._layout.addRow(self._l_name_lb, self._l_name_le)
        self._layout.addRow(self._phone_lb, self._phone_le)
        self._layout.addRow(self._address_lb, self._address_le)
        self._layout.addRow(self._pin_lb, self._pin_le)
        self._layout.addWidget(self._submit_btn)

    def apply_stylesheet(self):
        self.setStyleSheet(get_stylesheet('register_user'))

    def setup_connections(self):
        self._submit_btn.clicked.connect(self._on_submit)
        self._submit_btn.clicked.connect(prompts.registration_done)

    def _on_submit(self):
        f_name = self._f_name_le.text()
        l_name = self._l_name_le.text()
        phone = self._phone_le.text()
        address = self._address_le.text()
        pincode = self._pin_le.text()
        values = list()
        values.append((f_name, l_name, phone, address, pincode))
        customers.Customer().insert(values[0])
        self.close()


if __name__ == '__main__':
    pass
    # app = QtWidgets.QApplication(sys.argv)
    # inst = UserRegister(7715809262)
    # root = QtWidgets.QWidget()
    # inst.show()
    # app.exec()
