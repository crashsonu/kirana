# All Python Built-in Imports Here.
from PySide6 import QtWidgets, QtCore
from pprint import pprint

# All Custom Imports Here.
from kirana.db import db_connection
from kirana.ui.prompt import prompts
from kirana.db.entities.orders import Order
from kirana.db.entities.customers import Customer
from kirana.db.entities.order_status import OrderStatus


# All Native Imports Here.

# All Attributes or Constants Here.

class OrdersStatusWidget(QtWidgets.QTableWidget):
    MAPPED_HEADERS = {'delivery_status': 0, 'order_id': 1, 'customer_name': 2, 'address': 3, 'products': 4,
                      'ordered_on': 5,
                      }

    def __init__(self):
        super(OrdersStatusWidget, self).__init__()
        self.order_status_names = OrderStatus().all(column_name='name')
        self.all_orders = Order().all()
        self.orders_status_data = OrderStatus().all()
        self.save_changes = QtWidgets.QPushButton()

        self._initialize()

    def _initialize(self):
        self.setRowCount(0)
        self.setColumnCount(len(self.MAPPED_HEADERS))
        self.setHorizontalHeaderLabels(list(self.MAPPED_HEADERS.keys()))
        self.setup_ui()
        self.add_orders()

        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)

    def setup_ui(self):
        pass

    def add_orders(self):
        for each in self.all_orders:
            _order_id = each['id']
            _customer_id = each['customer_id']
            _customer_name = Customer().get(return_fields=['first_name', 'last_name'], id=_customer_id)
            _customer_address = Customer().get(return_fields='address', id=_customer_id)
            _order_date = each['ordered_on']
            del each['customer_id']
            del each['id']
            del each['ordered_on']
            each['order_id'] = str(_order_id)
            each['customer_name'] = _customer_name
            each['address'] = _customer_address
            each['ordered_on'] = str(_order_date)
            row = self.rowCount()
            self.setRowCount(row + 1)
            for key, value in each.items():
                column = self.MAPPED_HEADERS.get(key)
                if column is None:
                    continue

                val = f'{value}'

                item = QtWidgets.QTableWidgetItem(val)
                self._combox = QtWidgets.QComboBox()
                self._combox.addItems(self.order_status_names)
                self.setItem(row, column, item)
                self.setCellWidget(row, 0, self._combox)
                status_id = each['status']
                self.orders_status_data = OrderStatus().all()
                for x in self.orders_status_data:
                    if status_id != x['id']:
                        continue
                    self.orders_status_name = x['name']
                self._combox.setCurrentText(self.orders_status_name)



class OrderStatusUi(QtWidgets.QDialog):
    def __init__(self):
        super(OrderStatusUi, self).__init__()
        self._layout = QtWidgets.QVBoxLayout()
        self.save_changes_btn = QtWidgets.QPushButton('Save Status Changes')
        self.orders_status_data = OrderStatus().all()
        self.orders_status_widget = OrdersStatusWidget()
        self.setLayout(self._layout)
        self._layout.addWidget(self.orders_status_widget)
        self._layout.addWidget(self.save_changes_btn)

        self.setup_ui_connections()

    def setup_ui_connections(self):
        self.save_changes_btn.clicked.connect(self.update_status)

    def set_combox_text(self, text):
        for row in range(self.orders_status_widget.rowCount()):
            status_chk = self.orders_status_widget.cellWidget(row, 5)
            status_chk.setCurrentText(text)

    @db_connection
    def update_status(self, **kwargs):
        connection = kwargs.pop('connection')
        cursor = connection.cursor()
        for row in range(self.orders_status_widget.rowCount()):
            status_chk = self.orders_status_widget.cellWidget(row, 5)
            status_text = status_chk.currentText()
            order_id = self.orders_status_widget.item(row, 0)
            order_id_txt = int(order_id.text())
            for each in self.orders_status_data:
                if status_text != each['name']:
                    continue
                self.orders_status_id = each['id']

            msg = f'update orders set status = {self.orders_status_id} where id = {order_id_txt}'
            cursor.execute(msg)
            connection.commit()
        prompts.delivery_status_updated()


if __name__ == '__main__':
    pass
    #
    # app = QtWidgets.QApplication(sys.argv)
    # inst = OrderStatusUi()
    # root = QtWidgets.QWidget()
    # inst.show()
    # app.exec()
