# All Python Built-in Imports Here.
import sys
from datetime import datetime

# All Custom Imports Here.
from PySide6 import QtWidgets

# All Native Imports Here.
from kirana.db import db_connection
from kirana.ui import get_stylesheet
from kirana.ui.entities_ui import products_ui
from kirana.db.entities.products import Products
from kirana.db.entities.customers import Customer


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

        return total_cart_value

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


class Window(QtWidgets.QDialog):
    def __init__(self):
        super(Window, self).__init__()
        self._layout = QtWidgets.QVBoxLayout()
        self._layout2 = QtWidgets.QHBoxLayout()
        self._add_cart_layout = QtWidgets.QVBoxLayout()

        # add category widgets
        self._category_label = QtWidgets.QLabel('All Products')
        self._products_lw = QtWidgets.QListWidget()
        self._add_cart_btn = QtWidgets.QPushButton('Add Products To Cart')

        # cart widget
        self._cart_layout = QtWidgets.QVBoxLayout()
        self._cart_le_layout = QtWidgets.QHBoxLayout()
        self._cart_label = QtWidgets.QLabel('Cart')
        self._customer_verify = QtWidgets.QLineEdit()
        self._customer_verify.setPlaceholderText('Enter Registered Phone Number...')
        self._customer_verify_button = QtWidgets.QPushButton('Verify Me')
        self._cart_tw = CartTableWidget()
        self._grand_total_label = QtWidgets.QLabel()
        self._cart_btn_layout = QtWidgets.QHBoxLayout()
        self._place_order_btn = QtWidgets.QPushButton('Place Order')
        self._clear_cart_btn = QtWidgets.QPushButton('Clear Cart')

        # checked product info to add cart
        self._info_to_add_cart = list()

        self._initialize()

    def _initialize(self):
        self._setup_widget()
        self._setup_widget_connection()

        self.add_all_products()
        self.apply_stylesheet()

    def _setup_widget(self):
        self.setLayout(self._layout)
        self.setWindowTitle('Place Order.')
        self._layout.addLayout(self._layout2)
        self.setLayout(self._layout2)
        self._layout2.addLayout(self._add_cart_layout)

        # setting up select category and add products list
        self._add_cart_layout.addWidget(self._category_label)

        self._add_cart_layout.addWidget(self._products_lw)

        self._add_cart_layout.addWidget(self._add_cart_btn)

        # cart layout
        self._layout2.addLayout(self._cart_layout)
        self._cart_layout.addLayout(self._cart_le_layout)
        self._cart_layout.addWidget(self._cart_label)
        self._cart_le_layout.addWidget(self._customer_verify)
        self._cart_le_layout.addWidget(self._customer_verify_button)
        self._cart_layout.addWidget(self._cart_tw)
        self._cart_layout.addWidget(self._grand_total_label)
        self._cart_layout.addLayout(self._cart_btn_layout)
        self._cart_btn_layout.addWidget(self._place_order_btn)
        self._cart_btn_layout.addWidget(self._clear_cart_btn)

        self._products_lw.setSpacing(2)

    def _setup_widget_connection(self):
        pass
        self._add_cart_btn.clicked.connect(self._on_add_cart)
        self._place_order_btn.clicked.connect(self._on_place_order)
        self._customer_verify_button.clicked.connect(self._on_verify_me)
        self._clear_cart_btn.clicked.connect(self._on_clear_cart)

    def add_all_products(self):
        all_products = Products().all()
        for each in all_products:
            product_widget = products_ui.ProductWidget(each)
            lwi = QtWidgets.QListWidgetItem()
            lwi.setSizeHint(product_widget.sizeHint())
            self._products_lw.addItem(lwi)
            self._products_lw.setItemWidget(lwi, product_widget)

    def _on_add_cart(self):
        for i in range(self._products_lw.count()):
            item = self._products_lw.item(i)
            wid = self._products_lw.itemWidget(item)
            if not wid.checked:
                continue

            res = wid.get_for_cart()

            self._info_to_add_cart.append(res)
            self._cart_tw.add_product(res)

        self._grand_total_label.setText(f"CART TOTAL : RS. {self._cart_tw.cart_total} ")

    def _on_verify_me(self):
        self._phone_number = self._customer_verify.text()
        self._customer_id = Customer().get(return_fields='id', mobile=self._phone_number)
        if len(self._phone_number) == 0:
            print('Please verify Yourself, to Place an Order.')
            return
        if len(self._phone_number) != 10:
            print('Please enter valid Phone Number.')
            return

        return self._customer_id

    @db_connection
    def _on_place_order(self, **kwargs):
        connection = kwargs.pop('connection')
        cursor = connection.cursor()

        product_info = self._info_to_add_cart
        products_dict = dict()
        for each in product_info:
            products_dict[each['id']] = each['quantity']
        customer_id = self._on_verify_me()
        if customer_id is None:
            return

        ordered_on = datetime.now()
        # products dict in json
        products_dict_json = dict()
        for k, v in products_dict.items():
            products_dict_json[f"{k}"] = f"{v}"

        products_dict_json_str = f'"{products_dict_json}"'

        msg = f'insert into orders(customer_id, products, ordered_on) values(%s, %s, %s)'
        values = (customer_id, products_dict_json_str, ordered_on)
        cursor.execute(msg, values)
        connection.commit()
        print('Order placed successfully.')

    def _on_clear_cart(self):
        self._cart_tw.setRowCount(0)
        self._grand_total_label.setText('CART TOTAL : Rs. 0')

    def apply_stylesheet(self):
        self.setStyleSheet(get_stylesheet('stylesheet'))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    inst = Window()
    root = QtWidgets.QWidget()
    inst.show()
    app.exec()
