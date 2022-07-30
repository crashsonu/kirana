# All Python Built-in Imports Here.
import sys
from PySide6.QtWidgets import *
from PySide6.QtWidgets import QMessageBox


# All Custom Imports Here.

# All Native Imports Here.

# All Attributes or Constants Here.

def product_added():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("Product Added to DATABASE Successfully!!")
    msg.setWindowTitle("Product Added")
    msg.exec()

def product_deleted():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("Product deleted from DATABASE Successfully!!")
    msg.setWindowTitle("Deletion completed")
    msg.exec()


def registration_done():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("Successfully Registered!")
    msg.setInformativeText('Now customer can place order, with Auths.')
    msg.setWindowTitle("Registration Completed.")
    msg.exec()


def customer_verified():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("Customer verified!")
    msg.setWindowTitle("verification completed.")
    msg.exec()


def order_placed():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("Order Placed!")
    msg.setWindowTitle("Order completed.")
    msg.exec()


if __name__ == '__main__':
    pass
