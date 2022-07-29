# All Python Built-in Imports Here.

# All Custom Imports Here.
from PySide6 import QtGui
from PySide6 import QtWidgets

# All Native Imports Here.
from kirana.db.entities.units import Unit


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
        self._unit_label = QtWidgets.QLabel()
        self._gst_label = QtWidgets.QLabel()

        self.checked_product_list = list()

        self._initialize()

    @property
    def product_info(self):
        return self._product_info

    @property
    def checked(self):
        return self._checkbox.isChecked()

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
        self._layout.addWidget(self._unit_label)
        self._layout.addWidget(self._gst_label)

        self._checkbox.setText(self._product_info['name'])
        self._checkbox.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        # setting price by quantity initial 1.
        self._qty_spb.setValue(1)
        self.pro_price_init = self._product_info["price"]
        self._price_label.setText(f'Rs. {self.pro_price_init}')

        # setting unit like KG for product.
        self.qty_label = Unit().get(return_fields='name', id=self._product_info['unit_id'])
        self._unit_label.setText(self.qty_label)
        # setting GST label initial given.
        _product_gst = self._product_info['gst']
        self._gst_label.setText(f'{_product_gst}% gst')

    def _setup_widget_connections(self):
        self._qty_spb.valueChanged.connect(self._on_change_quantity)

    def _on_change_quantity(self):
        spb_current_value = self._qty_spb.value()
        self.prod_price = spb_current_value * self.pro_price_init
        self._price_label.setText(f'Rs. {self.prod_price}')

    def get_for_cart(self):
        id_ = self._product_info.get('id')
        name = self._product_info.get('name')
        category_id = self._product_info.get('category_id')
        price = self._product_info.get('price')
        gst = self._product_info.get('gst')
        size = self._product_info.get('size')
        unit_id = self._product_info.get('unit_id')
        unit_name = Unit().get(id=unit_id)[0]['name']

        result = dict()
        result.update(id=id_, name=name, category_id=category_id, price=price,
                      size=size, gst_percent=gst, unit_id=unit_id, unit_name=unit_name)

        quantity = self._qty_spb.value()
        result.update(quantity=quantity)

        total = round(price * quantity, 1)
        result.update(total=total)

        gst_price = round((total / 100) * gst, 1)
        result.update(gst=gst_price)

        result.update(grand_total=total + gst_price)
        self.checked_product_list.append(result)

        return result


if __name__ == '__main__':
    pass
