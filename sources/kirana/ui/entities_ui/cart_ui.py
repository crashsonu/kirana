# All Python Built-in Imports Here.

# All Custom Imports Here.
from PySide6 import QtWidgets


# All Native Imports Here.

# All Attributes or Constants Here.


class CartTableWidget(QtWidgets.QTableWidget):
    MAPPED_HEADERS = {'name': 0, 'price': 1, 'size': 2, 'unit_name': 3, 'gst_percent': 4,
                      'quantity': 5, 'total': 6, 'gst': 7, 'grand_total': 8}

    def __init__(self):
        super(CartTableWidget, self).__init__()
        self.product_data_list = list()

        self._initialize()

    def _initialize(self):
        self.setRowCount(0)
        self.setColumnCount(len(self.MAPPED_HEADERS))
        self.setHorizontalHeaderLabels(list(self.MAPPED_HEADERS.keys()))

    @property
    def cart_total(self):
        total_cart_value = 0
        for each in self.product_data_list:
            total_cart_value += each['grand_total']

        return round(total_cart_value, 2)

    def add_product(self, data):
        row = self.rowCount()
        self.setRowCount(row + 1)
        for key, value in data.items():
            column = self.MAPPED_HEADERS.get(key)
            if column is None:
                continue

            val = f'{value}'
            item = QtWidgets.QTableWidgetItem(val)
            self.setItem(row, column, item)

        self.product_data_list.append(data)

    def confirm_order(self):
        pass

    def _setup_widget_connection(self):
        pass


if __name__ == '__main__':
    pass
