# All Python Built-in Imports Here.
import sys
from datetime import datetime

# All Custom Imports Here.
from PySide6 import QtWidgets
from PySide6 import QtCore

# All Native Imports Here.
from kirana.ui.entities_ui.cart_ui import CartTableWidget
from kirana.db.entities.customers import Customer
from kirana.db.entities.products import Products
from kirana.db.entities.orders import Order
from kirana.ui.entities_ui import products_ui
from kirana.ui.entities_ui import customer_ui
from kirana.ui import get_stylesheet
from kirana.db import db_connection
from kirana.ui.prompt import prompts


# All Attributes or Constants Here.

class OrderWidget(QtWidgets.QDialog):
    def __init__(self):
        super(OrderWidget, self).__init__()
        self._layout = QtWidgets.QVBoxLayout()
        self._layout2 = QtWidgets.QHBoxLayout()
        self._search_layout = QtWidgets.QHBoxLayout()
        self._add_cart_layout = QtWidgets.QVBoxLayout()

        # add category widgets
        self._category_label = QtWidgets.QLabel('All Products')
        self._search_le = QtWidgets.QLineEdit()
        self._search_le.setPlaceholderText('search product....')
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

        self.all_products = Products().all()

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
        self.setLayout(self._add_cart_layout)

        # setting up select category and add products list
        self._add_cart_layout.addWidget(self._category_label)
        self._add_cart_layout.addLayout(self._search_layout)
        self._search_layout.addWidget(self._search_le)
        self._add_cart_layout.addWidget(self._products_lw)
        self._add_cart_layout.addWidget(self._add_cart_btn)

        # cart layout
        self._layout2.addLayout(self._cart_layout)
        self._cart_layout.addWidget(self._cart_label)
        self._cart_layout.addLayout(self._cart_le_layout)
        self._cart_le_layout.addWidget(self._customer_verify)
        self._cart_le_layout.addWidget(self._customer_verify_button)
        self._cart_layout.addWidget(self._cart_tw)
        self._cart_layout.addWidget(self._grand_total_label)
        self._cart_layout.addLayout(self._cart_btn_layout)
        self._cart_btn_layout.addWidget(self._place_order_btn)
        self._cart_btn_layout.addWidget(self._clear_cart_btn)

        self._customer_verify_button.setObjectName('CUSTOMER_VERIFY_PB')

        self._products_lw.setSpacing(2)
        self.setWindowState(QtCore.Qt.WindowMaximized)

    def _setup_widget_connection(self):
        pass
        self._add_cart_btn.clicked.connect(self._on_add_cart)
        self._place_order_btn.clicked.connect(self._on_place_order)
        self._customer_verify_button.clicked.connect(self._on_verify_me)
        self._clear_cart_btn.clicked.connect(self._on_clear_cart)
        self._search_le.returnPressed.connect(self._on_search_products)

    def add_all_products(self):
        for each in self.all_products:
            product_widget = products_ui.ProductWidget(each)
            lwi = QtWidgets.QListWidgetItem()
            lwi.setSizeHint(product_widget.sizeHint())
            self._products_lw.addItem(lwi)
            self._products_lw.setItemWidget(lwi, product_widget)

    def _on_search_products(self):
        search_name = self._search_le.text().lower()
        for i in range(self._products_lw.count()):
            item = self._products_lw.item(i)
            wid = self._products_lw.itemWidget(item)
            product_name = wid.product_info.get('name').lower()
            if product_name.count(search_name):
                item.setHidden(False)
            else:
                item.setHidden(True)

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
        _phone_number = int(self._phone_number)
        existing_phone_numbers = Customer().all(column_name='mobile')
        if self._phone_number in existing_phone_numbers:
            prompts.customer_verified()
            self._customer_id = Customer().get(return_fields='id', mobile=self._phone_number)
            return self._customer_id

        if len(self._phone_number) == 10 and self._phone_number not in existing_phone_numbers:
            w = customer_ui.UserRegister(phone_number=self._phone_number)
            w.show()
            w.exec()
            self._customer_id = Customer().get(return_fields='id', mobile=self._phone_number)
            return self._customer_id

        if len(self._phone_number) == 0:
            print('Please verify Yourself, to Place an Order.')
            return

        if len(self._phone_number) != 10:
            print('Please enter valid Phone Number.')
            return

    @property
    def verified_customer_id(self):
        return self._customer_id

    @db_connection
    def _on_place_order(self, **kwargs):
        connection = kwargs.pop('connection')
        cursor = connection.cursor()

        product_info = self._info_to_add_cart
        products_dict = dict()
        for each in product_info:
            products_dict[each['id']] = each['quantity']
        customer_id = self.verified_customer_id
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
        prompts.order_placed()
        print('Order placed successfully.')

    def _on_clear_cart(self):
        self._cart_tw.setRowCount(0)
        self._grand_total_label.setText('CART TOTAL : Rs. 0')

    def apply_stylesheet(self):
        self.setStyleSheet(get_stylesheet('order'))


class AllOrdersTableWidget(QtWidgets.QTableWidget):
    MAPPED_HEADERS = {'Customer Name': 0, 'Products': 1, 'Ordered Date': 2}

    def __init__(self):
        super(AllOrdersTableWidget, self).__init__()
        self.orders_list = list()
        self.all_orders = Order().all()

        self._initialize()

    def _initialize(self):
        self.setRowCount(0)
        self.setColumnCount(len(self.MAPPED_HEADERS))
        self.setHorizontalHeaderLabels(list(self.MAPPED_HEADERS.keys()))
        self.provide_data()

    def _setup_ui(self):
        pass

    def _setup_connections(self):
        pass

    def add_orders(self, data):
        row = self.rowCount()
        self.setRowCount(row+1)
        for key, value in data.items():
            column = self.MAPPED_HEADERS.get(key)

            val = f'{value}'
            item = QtWidgets.QTableWidgetItem(val)
            self.setItem(row, column, item)

    def provide_data(self):
        for each in self.all_orders:
            print(each)
            customer_name = Customer().get(return_fields='first_name', id=each['customer_id'])
            get_pr_id = each['products']
            print(get_pr_id)
            # product_name = Products().get(return_fields='name', id=each[] )
            print(customer_name)
            # print(product_name)


if __name__ == '__main__':
    pass
