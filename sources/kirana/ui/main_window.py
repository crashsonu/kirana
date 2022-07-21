# All Python Built-in Imports Here.
import sys
from datetime import datetime

# All Custom Imports Here.
from PySide6 import QtWidgets

# All Native Imports Here.
from kirana.db import db_connection
from kirana.ui import get_stylesheet
from kirana.db.entities.orders import Order
from kirana.ui.entities_ui import products_ui
from kirana.db.entities.products import Products
from kirana.db.entities import get_field


# All Attributes or Constants Here.


class Window(QtWidgets.QDialog):
    def __init__(self):
        super(Window, self).__init__()
        self._layout = QtWidgets.QVBoxLayout()
        self._layout2 = QtWidgets.QHBoxLayout()
        self._add_cart_layout = QtWidgets.QVBoxLayout()

        # add category widgets
        self._category_layout = QtWidgets.QHBoxLayout()
        self._category_label = QtWidgets.QLabel('Select Category')
        self._category_combox = QtWidgets.QComboBox()
        self._category_search_btn = QtWidgets.QPushButton('Search Products')

        self._products_lw = QtWidgets.QListWidget()

        self._add_cart_btn = QtWidgets.QPushButton('Add Products To Cart')

        # cart widget
        self._cart_layout = QtWidgets.QVBoxLayout()
        self._cart_le_layout = QtWidgets.QHBoxLayout()
        self._cart_label = QtWidgets.QLabel('Cart')
        self._customer_verify = QtWidgets.QLineEdit()
        self._customer_verify.setPlaceholderText('Enter Registered Phone Number...')
        self._customer_verify_button = QtWidgets.QPushButton('Verify Me')
        self._cart_tw = QtWidgets.QTableWidget()
        self._grand_total_label = QtWidgets.QLabel()
        self._cart_btn_layout = QtWidgets.QHBoxLayout()
        self._place_order_btn = QtWidgets.QPushButton('Place Order')
        self._clear_cart_btn = QtWidgets.QPushButton('Clear Cart')

        self._initialize()

    def _initialize(self):
        self._setup_widget()
        self._setup_widget_connection()

        self.add_categories()
        self.apply_stylesheet()

    def _setup_widget(self):
        self.setLayout(self._layout)
        self.setWindowTitle('Place Order.')
        self._layout.addLayout(self._layout2)
        self.setLayout(self._layout2)
        self._layout2.addLayout(self._add_cart_layout)
        self._add_cart_layout.addLayout(self._category_layout)

        # setting up select category and add products list
        self._category_layout.addWidget(self._category_label)
        self._category_layout.addWidget(self._category_combox)
        self._category_layout.addWidget(self._category_search_btn)

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
        self._category_search_btn.clicked.connect(self._on_category_searched)
        self._add_cart_btn.clicked.connect(self._on_add_cart)
        self._place_order_btn.clicked.connect(self._on_place_order)
        self._customer_verify_button.clicked.connect(self._on_verify_me)

    def add_categories(self):
        _categories = Order.get_column(table_name='products_category', column_name='name')
        for each in _categories:
            self._category_combox.addItem(each)

    def _on_category_searched(self):
        self._products_lw.clear()

        category = self._category_combox.currentText()
        catagory_id = Order.get('products_category', 'name', category, get_column='id')
        _id = catagory_id.get('id')
        _products = Products().filter(category_id=_id)
        # add widget to QListWidget
        for each in _products:
            product_widget = products_ui.ProductWidget(each)
            lwi = QtWidgets.QListWidgetItem()
            lwi.setSizeHint(product_widget.sizeHint())
            self._products_lw.addItem(lwi)
            self._products_lw.setItemWidget(lwi, product_widget)

    def _on_add_cart(self):
        product_already_in_cart = list()
        products_in_cart = list()
        product_already_in_cart.append(products_in_cart)
        self.gra_total = 0
        self.place_order_pro_info = list()

        for i in range(self._products_lw.count()):
            item = self._products_lw.item(i)
            wid = self._products_lw.itemWidget(item)
            _prod_info = wid._product_info
            _info_to_add_cart = dict()
            if wid.checked:
                qty_unit = wid.unit
                prod_qty = wid.quantity
                _prod_info['Quantity'] = prod_qty
                _prod_info['price'] = wid.price
                pro_gst = round(_prod_info['price']) * round(_prod_info['gst']) / 100
                pro_total = _prod_info['price'] + pro_gst
                self.gra_total += pro_total

                _info_to_add_cart['name'] = _prod_info['name']
                _info_to_add_cart['quantity'] = f"{prod_qty}{qty_unit}"
                _info_to_add_cart['price'] = f'{_prod_info["price"]}'
                _info_to_add_cart['total_gst'] = f'{pro_gst}'
                _info_to_add_cart['total'] = f"{pro_total}"
                products_in_cart.append(_info_to_add_cart)

                self.place_order_pro_info.append(_prod_info)
        row_count = len(products_in_cart)
        self._cart_tw.setRowCount(row_count)
        self._cart_tw.setColumnCount(5)
        self._cart_tw.setHorizontalHeaderLabels(["Product", "Quantity", "Price", "GST", "Total"])
        self._grand_total_label.setText(f"GRAND TOTAL : Rs. {round(self.gra_total)}")

        for i in range(row_count):
            name = QtWidgets.QTableWidgetItem(products_in_cart[i]['name'])
            price = QtWidgets.QTableWidgetItem(products_in_cart[i]['price'])
            gst = QtWidgets.QTableWidgetItem(products_in_cart[i]['total_gst'])
            quantity = QtWidgets.QTableWidgetItem(products_in_cart[i]['quantity'])
            total = QtWidgets.QTableWidgetItem(products_in_cart[i]['total'])
            self._cart_tw.setItem(i, 0, name)
            self._cart_tw.setItem(i, 1, quantity)
            self._cart_tw.setItem(i, 2, price)
            self._cart_tw.setItem(i, 3, gst)
            self._cart_tw.setItem(i, 4, total)
            self._cart_tw.resizeColumnsToContents()
        return self.place_order_pro_info

    def _on_verify_me(self):
        self._phone_number = self._customer_verify.text()
        self._customer_id = get_field('customers', 'mobile', self._phone_number, 'id')
        if len(self._phone_number) != 10:
            print('Please enter valid Phone Number.')
        return self._customer_id['id']

    @db_connection
    def _on_place_order(self, **kwargs):
        connection = kwargs.pop('connection')
        cursor = connection.cursor()

        product_info = self._on_add_cart()
        products_dict = dict()
        for each in product_info:
            products_dict[each['id']] = each['Quantity']
        customer_id = self._on_verify_me()
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

    def apply_stylesheet(self):
        self.setStyleSheet(get_stylesheet('stylesheet'))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    inst = Window()
    root = QtWidgets.QWidget()
    inst.show()
    app.exec()
