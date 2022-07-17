# All Python Built-in Imports Here.
import sys

# All Custom Imports Here.
from PySide6 import QtGui
from PySide6 import QtWidgets


# All Native Imports Here.
from kirana.db.entities import get_column

# All Attributes or Constants Here.


class ProductWidget(QtWidgets.QWidget):

    def __init__(self, product_info):
        """Product widget to show product for add to cart or else.
        Args:
            product_info (dict): product info returned by the database.
        """
        super(ProductWidget, self).__init__()
        self._product_info = product_info

        self._layout = QtWidgets.QHBoxLayout()
        self._checkbox = QtWidgets.QCheckBox()
        self._qty_spb = QtWidgets.QSpinBox()
        self._price_label = QtWidgets.QLabel()
        self._qty_combox = QtWidgets.QComboBox()

        self._initialize()

    def _initialize(self):
        self._setup_widget()
        self._setup_widget_connections()

    def _setup_widget(self):
        self.setLayout(self._layout)
        self.setAttribute(QtGui.Qt.WA_StyledBackground)

        self._layout.addWidget(self._checkbox)
        self._layout.addWidget(self._price_label)
        self._layout.addWidget(self._qty_spb)
        self._layout.addWidget(self._qty_combox)

        self._checkbox.setText(self._product_info['name'])
        self._price_label.setText(f'Rs. {self._product_info["price"]}')

        _quantities = get_column('units', 'name')
        for each in _quantities:
            self._qty_combox.addItem(each)

    def _setup_widget_connections(self):
        pass


if __name__ == '__main__':
    pass
