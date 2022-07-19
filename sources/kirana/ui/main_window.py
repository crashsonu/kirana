# All Python Built-in Imports Here.
import os
import sys

# All Custom Imports Here.
from PySide6 import QtWidgets

# All Native Imports Here.
from kirana.ui import get_stylesheet
from kirana.db.entities.orders import Order
from kirana.ui.entities_ui import products_ui
from kirana.db.entities.products import Products


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
        self._cart_le = QtWidgets.QLineEdit('Cart')
        self._cart_lw = QtWidgets.QListWidget()
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
        self._cart_layout.addWidget(self._cart_le)
        self._cart_layout.addWidget(self._cart_lw)
        self._cart_layout.addLayout(self._cart_btn_layout)
        self._cart_btn_layout.addWidget(self._place_order_btn)
        self._cart_btn_layout.addWidget(self._clear_cart_btn)

        self._products_lw.setSpacing(2)

    def _setup_widget_connection(self):
        self._category_search_btn.clicked.connect(self._on_category_searched)
        self._add_cart_btn.clicked.connect(self._on_add_cart)

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
        for i in range(self._products_lw.count()):
            item = self._products_lw.item(i)
            wid = self._products_lw.itemWidget(item)
            if wid.checked:
                _prod_info = wid._product_info
                _info_to_pop = ['id', 'category_id', 'size', 'unit_id']
                for k in _info_to_pop:
                    _prod_info.pop(k)

                qty_unit = wid._qty_combox.currentText()
                prod_qty = wid._qty_spb.value()
                _prod_info['Quantity'] = f"{prod_qty}{qty_unit}"

    def apply_stylesheet(self):
        self.setStyleSheet(get_stylesheet('stylesheet'))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    inst = Window()
    root = QtWidgets.QWidget()
    inst.show()
    app.exec()
