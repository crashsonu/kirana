# All Python Built-in Imports Here.
import os
import sys

# All Custom Imports Here.
from PySide6 import QtWidgets
from PySide6 import QtCore
from kirana.ui import place_order_widget
from kirana.ui import modify_products

from kirana.ui.entities_ui import products_ui


# All Native Imports Here.


# All Attributes or Constants Here.


class WindowKiranaManager(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self._place_order_wid = place_order_widget.OrderWidget()
        self._modification_wid = modify_products.ModifyProducts()
        self._layout = QtWidgets.QVBoxLayout()
        self.tab_widget = QtWidgets.QTabWidget()

        self._initialize()

    def _initialize(self):
        self._setup_ui()
        self._setup_connections()

    def _setup_ui(self):
        self.setLayout(self._layout)
        self._layout.addWidget(self.tab_widget)
        self.tab_widget.addTab(self._modification_wid, 'ADD OR DELETE PRODUCTS')
        self.tab_widget.addTab(self._place_order_wid, 'PLACE ORDER')
        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.setWindowTitle('KIRANA MANAGER')

    def _setup_connections(self):
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    inst = WindowKiranaManager()
    root = QtWidgets.QWidget()
    inst.show()
    app.exec()
