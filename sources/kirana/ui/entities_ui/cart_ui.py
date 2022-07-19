# All Python Built-in Imports Here.
import sys

# All Custom Imports Here.
from PySide6 import QtWidgets
from kirana.ui.entities_ui.products_ui import ProductWidget


# All Native Imports Here.

# All Attributes or Constants Here.


class CartWidget(QtWidgets.QWidget, ProductWidget):
    def __init__(self, product_info):
        super(CartWidget, self).__init__()
        self._product_info = product_info
        self._layout = QtWidgets.QHBoxLayout()
        self._product_label = QtWidgets.QLabel()
        self._pro_count_lb = QtWidgets.QLabel()
        self._product_final_price_lb = QtWidgets.QLabel()
        self._pro_total_gst_lb = QtWidgets.QLabel()

        self._initialize()

    def _initialize(self):
        self._setup_widget()
        self._setup_widget_connection()

    def _setup_widget(self):
        self.setLayout(self._layout)
        self._layout.addWidget(self._product_lable)
        self._layout.addWidget(self._pro_count_lb)
        self._layout.addWidget(self._pro_total_gst_lb)
        self._layout.addWidget(self._product_final_price_lb)

    def _setup_widget_connection(self):
        pass


if __name__ == '__main__':
    pass
