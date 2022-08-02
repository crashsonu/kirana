# All Python Built-in Imports Here.
import sys
from PySide6 import QtWidgets, QtCore

# All Custom Imports Here.
from kirana.db.entities.orders import Order
from kirana.db.entities.customers import Customer
from kirana.db.entities.order_status import OrderStatus


# All Native Imports Here.

# All Attributes or Constants Here.

class OrdersLwWidget(QtWidgets.QDialog):
    def __init__(self, data):
        super(OrdersLwWidget, self).__init__()
        self._layout = QtWidgets.QHBoxLayout()
        self._order_id_label = QtWidgets.QLabel(data['id'])
        self._customer_name_label = QtWidgets.QLabel(data['customer_name'])
        self._address_label = QtWidgets.QLabel(data['address'])
        self._products_label = QtWidgets.QLabel(data['products'])
        self._order_status_cb = QtWidgets.QComboBox()
        self._order_date_label = QtWidgets.QLabel(data['ordered_on'])

        self.order_status_names = OrderStatus().all(column_name='name')

        self._initialize()

    def _initialize(self):
        self.setup_ui()

    def setup_ui(self):
        self.setLayout(self._layout)
        self._layout.addWidget(self._order_id_label)
        self._layout.addWidget(self._customer_name_label)
        self._layout.addWidget(self._products_label)
        self._layout.addWidget(self._address_label)
        self._layout.addWidget(self._order_date_label)
        self._layout.addWidget(self._order_status_cb)

        self._order_status_cb.addItems(self.order_status_names)


class OrdersStatusWid(QtWidgets.QDialog):
    def __init__(self):
        super(OrdersStatusWid, self).__init__()
        self.setWindowState(QtCore.Qt.WindowMaximized)
        self._layout = QtWidgets.QVBoxLayout()
        self._orders_lw = QtWidgets.QListWidget()
        self._save_changes_btn = QtWidgets.QPushButton('Save Changes')
        self.all_orders = Order().all()
        for each in self.all_orders:
            _order_id = each['id']
            _customer_id = each['customer_id']
            _customer_name = Customer().get(return_fields=['first_name', 'last_name'], id=_customer_id)
            _customer_address = Customer().get(return_fields='address', id=_customer_id)
            _order_date = each['ordered_on']
            del each['customer_id']
            del each['id']
            del each['ordered_on']
            each['id'] = str(_order_id)
            each['customer_name'] = _customer_name
            each['address'] = _customer_address
            each['ordered_on'] = str(_order_date)
            orders_widget = OrdersLwWidget(each)
            lwi = QtWidgets.QListWidgetItem()
            lwi.setSizeHint(orders_widget.sizeHint())
            self._orders_lw.addItem(lwi)
            self._orders_lw.setItemWidget(lwi, orders_widget)

        self._initialize()

    def _initialize(self):
        self.setup_ui()

    def setup_ui(self):
        self.setLayout(self._layout)
        self._layout.addWidget(self._orders_lw)
        self._layout.addWidget(self._save_changes_btn)

    def setup_connections(self):
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    inst = OrdersStatusWid()
    root = QtWidgets.QWidget()
    inst.show()
    app.exec()
