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

def category_added():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("Product Category Added to DATABASE Successfully!!")
    msg.setWindowTitle("category Added")
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

def delivery_status_updated():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("Successfully Updated delivery status!!")
    msg.setWindowTitle("Updated")
    msg.exec()

def field_required(field_name):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText(f"{field_name} is required!")
    msg.setWindowTitle("Fill all the fields!")
    msg.exec()

def select_atleast_onefield():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText(f"Select at least one field for further process!")
    msg.setWindowTitle("check at least one Field!")
    msg.exec()

if __name__ == '__main__':
    pass
