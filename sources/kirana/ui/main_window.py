# All Python Built-in Imports Here.
import sys

# All Custom Imports Here.
from PySide6 import QtWidgets

# All Native Imports Here.
from kirana.db.entities.orders import Order
from kirana.db.entities.products import Products
from kirana.ui.entities_ui import products_ui


# All Attributes or Constants Here.


class Window(QtWidgets.QDialog):
    def __init__(self):
        super(Window, self).__init__()
        self._layout = QtWidgets.QVBoxLayout()

        self._category_layout = QtWidgets.QHBoxLayout()
        self._category_label = QtWidgets.QLabel('Select Category')
        self._category_combox = QtWidgets.QComboBox()
        self._category_search_btn = QtWidgets.QPushButton('Search Products')

        self._products_lw = QtWidgets.QListWidget()

        self._add_cart_btn = QtWidgets.QPushButton('Add To Cart')

        self._initialize()

    def _initialize(self):
        self._setup_widget()
        self._setup_widget_connection()

        self.add_categories()

    def _setup_widget(self):
        self.setLayout(self._layout)
        self._layout.addLayout(self._category_layout)

        self._category_layout.addWidget(self._category_label)
        self._category_layout.addWidget(self._category_combox)
        self._category_layout.addWidget(self._category_search_btn)

        self._layout.addWidget(self._products_lw)

        self._layout.addWidget(self._add_cart_btn)

    def _setup_widget_connection(self):
        self._category_search_btn.clicked.connect(self._on_category_searched)

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


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    inst = Window()
    root = QtWidgets.QWidget()
    inst.show()
    app.exec()
