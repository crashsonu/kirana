# All Python Built-in Imports Here.
import sys

# All Custom Imports Here.
from PySide6 import QtWidgets

# All Native Imports Here.
from kirana.db.entities.orders import Order
from kirana.ui.entities_ui import products_ui


# All Attributes or Constants Here.


class Window(QtWidgets.QDialog):
    def __init__(self):
        super(Window, self).__init__()
        self._layout = QtWidgets.QVBoxLayout()
        self._combox_lbl = QtWidgets.QLabel()
        self._combox_lbl.setText('Select Category')
        self._combox = QtWidgets.QComboBox()
        self.setLayout(self._layout)
        self._layout2 = QtWidgets.QHBoxLayout()
        self.setLayout(self._layout2)
        self._layout.addLayout(self._layout2)
        self._push_btn = QtWidgets.QPushButton()
        self._push_btn.setText('Search Products')
        self._layout2.addWidget(self._combox_lbl)
        self._layout2.addWidget(self._combox)
        self._layout2.addWidget(self._push_btn)

        self._products_lw = QtWidgets.QListWidget()
        self._layout.addWidget(self._products_lw)

        # QListWidgetItem
        self.qls_widget_item = QtWidgets.QListWidgetItem()
        # creating widget

        # self._widget_layout = QtWidgets.QHBoxLayout()
        # self._chk_box = QtWidgets.QCheckBox()
        # self._lable = QtWidgets.QLabel()
        # self._spin_box = QtWidgets.QSpinBox()
        # # add to layout
        # self._widget_layout.addWidget(self._chk_box)
        # self._widget_layout.addWidget(self._lable)
        # self._widget_layout.addWidget(self._spin_box)
        # self.setLayout(self._widget_layout)

        # lw layout
        # self._lw_layout = QtWidgets.QVBoxLayout()
        # self._ls_widget.setLayout(self._lw_layout)
        #
        # self._ls_widget.addItem(self.qls_widget_item)
        # self._ls_widget.setItemWidget(self.qls_widget_item, self._spin_box)
        # self._ls_widget.addItem(self.qls_widget_item)
        # self._ls_widget.setItemWidget(self.qls_widget_item, self._chk_box)

        self.compute()

    def add_categories(self):
        _categories = Order.get_column(table_name='products_category', column_name='name')
        for each in _categories:
            self._combox.addItem(each)

    def add_selected_cat_products(self):
        _sel_category = self._combox.currentText()
        _sel_catagory_id = Order.get('products_category', 'name', _sel_category, get_column='id')
        _id = _sel_catagory_id.get('id')
        _products_of_sel_category = Order.get_column_by_cond('products', 'category_id', _id, get_column='name')
        # add widget to QListWidget
        for each in _products_of_sel_category:
            product_widget = products_ui.ProductWidget()
            product_widget.product_name = each
            lwi = QtWidgets.QListWidgetItem()
            lwi.setSizeHint(product_widget.sizeHint())
            self._products_lw.addItem(lwi)
            self._products_lw.setItemWidget(lwi, product_widget)

    def clear_listwidget(self):
        self._products_lw.clear()

    def compute(self):
        self.add_categories()
        # self._push_btn.clicked.connect(self.clear_listwidget)
        self._push_btn.clicked.connect(self.add_selected_cat_products)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    inst = Window()
    root = QtWidgets.QWidget()
    inst.show()
    app.exec()
