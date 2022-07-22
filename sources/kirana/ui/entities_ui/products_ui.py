# All Python Built-in Imports Here.
import sys

# All Custom Imports Here.
from PySide6 import QtGui
from PySide6 import QtWidgets

# All Native Imports Here.
from kirana.db.entities import get_field


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
        self._qty_label = QtWidgets.QLabel()
        self._gst_label = QtWidgets.QLabel()

        self._initialize()

    @property
    def product_info(self):
        return self._product_info

    @property
    def checked(self):
        return self._checkbox.isChecked()

    @property
    def quantity(self):
        return self._qty_spb.value()

    @property
    def unit(self):
        return self.qty_label['id']

    @property
    def price(self):
        return self.pro_price

    def _initialize(self):
        self._setup_widget()
        self._setup_widget_connections()

    def _setup_widget(self):
        self.setLayout(self._layout)
        self.setObjectName('ProductWidget')
        self.setAttribute(QtGui.Qt.WA_StyledBackground)

        self._layout.addWidget(self._checkbox)
        self._layout.addWidget(self._price_label)
        self._layout.addWidget(self._qty_spb)
        self._layout.addWidget(self._qty_label)
        self._layout.addWidget(self._gst_label)

        self._checkbox.setText(self._product_info['name'])
        self._checkbox.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        # setting price by quantity initial 1.
        self._qty_spb.setValue(1)
        self.pro_price = self._product_info["price"]
        self._price_label.setText(f'Rs. {self.pro_price}')

        # setting unit like KG for product.
        self.qty_label = get_field('units', 'id', self._product_info['unit_id'], get_column='name')
        self._qty_label.setText(self.qty_label['id'])

        # setting GST label initial given.
        _product_gst = self._product_info['gst']
        self._gst_label.setText(f'{_product_gst}% gst')

    def _spb_value(self):
        spb_current_value = self._qty_spb.value()
        self.pro_price = spb_current_value * self._product_info['price']
        self._price_label.setText(f'Rs. {self.pro_price}')

    def _setup_widget_connections(self):
        self._qty_spb.valueChanged.connect(self._spb_value)


if __name__ == '__main__':
    pass
