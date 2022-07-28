# All Python Built-in Imports Here.
import sys
from PySide6.QtWidgets import *


# All Custom Imports Here.

# All Native Imports Here.

# All Attributes or Constants Here.

def product_added():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("Product Added to DATABASE Successfully!!")
    msg.setWindowTitle("Message")
    msg.exec()


if __name__ == '__main__':
    pass
