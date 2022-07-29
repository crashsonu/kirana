# All Python Built-in Imports Here.
import sys

# All Custom Imports Here.
from PySide6 import QtWidgets
from PySide6.QtWidgets import QMessageBox
from PySide6 import QtCore
from kirana.db.entities import products
from kirana.db.entities import products_category
from kirana.db.entities import units
from kirana.ui import get_stylesheet
from kirana.ui import prompts


# All Native Imports Here.

# All Attributes or Constants Here.


class ProductsWid(QtWidgets.QDialog):
    def __init__(self, data):
        super(ProductsWid, self).__init__()
        self._layout = QtWidgets.QHBoxLayout()
        self._check_box = QtWidgets.QCheckBox()
        self._check_box.setText(data['name'])
        self.id = data['id']
        size = str(data['size'])
        self._size = QtWidgets.QLabel()
        unit_id = data['unit_id']
        unit_name = units.Unit().get(return_fields='name', id=unit_id)
        self._unit = QtWidgets.QLabel()
        price = str(data['price'])
        self._price = QtWidgets.QLabel()
        self._price.setText(price)
        self._size.setText(size)
        self._unit.setText(unit_name)

        self._initialize()

    def _initialize(self):
        self._setup_ui()

    def _setup_ui(self):
        self.setLayout(self._layout)
        self._layout.addWidget(self._check_box)
        self._layout.addWidget(self._size)
        self._layout.addWidget(self._unit)
        self._layout.addWidget(self._price)

    @property
    def checked(self):
        return self._check_box.isChecked()

    @property
    def chek_box_id(self):
        return self.id


class ModifyProducts(QtWidgets.QDialog):
    category_names = products_category.ProductsCategory().all()
    unit_names = units.Unit().all()

    def __init__(self):
        super(ModifyProducts, self).__init__()
        self._layout = QtWidgets.QVBoxLayout()
        self._layout2 = QtWidgets.QHBoxLayout()
        self.lw_layout = QtWidgets.QHBoxLayout()
        self.del_pro_layout = QtWidgets.QVBoxLayout()
        self.add_prod_layout = QtWidgets.QFormLayout()
        self.products_lw = QtWidgets.QListWidget()
        self.pro_chk_box = QtWidgets.QCheckBox()
        self.del_prod_btn = QtWidgets.QPushButton("Delete Product")

        self.add_pro_label = QtWidgets.QLabel('ADD NEW PRODUCT DETAILS')
        self.del_pro_label = QtWidgets.QLabel('DELETE SELECTED PRODUCT')

        self.add_prod_lw = QtWidgets.QListWidget()
        self.pro_name_lb = QtWidgets.QLabel('Product Name')
        self.prod_name_le = QtWidgets.QLineEdit()
        self.pro_cat_label = QtWidgets.QLabel("Select Product Category")
        self.prod_cat_cb = QtWidgets.QComboBox()
        self.pro_price_lb = QtWidgets.QLabel('Price in Rs.')
        self.prod_price_cb = QtWidgets.QLineEdit()
        self.pro_gst_label = QtWidgets.QLabel('GST Percentage')
        self.prod_gst_le = QtWidgets.QLineEdit()
        self.prod_gst_le.setPlaceholderText('GST Percentage')
        self.pro_size_lb = QtWidgets.QLabel('Size Of Packet related to Unit')
        self.prod_size_cb = QtWidgets.QLineEdit()
        self.prod_size_cb.setPlaceholderText('Ex. 1, 2')
        self.pro_unit_lb = QtWidgets.QLabel('Select Unit')
        self.prod_unit_cb = QtWidgets.QComboBox()
        self.add_prod_btn = QtWidgets.QPushButton("Add Product")
        self._spacer = QtWidgets.QSpacerItem(150, 10, QtWidgets.QSizePolicy.Expanding)

        self._initialize()

    def _initialize(self):
        self._setup_widget()
        self._setup_widget_connections()
        self.add_products_lw()
        self.add_category()
        self.apply_stylesheet()

    def _setup_widget(self):
        self.setLayout(self._layout)
        self._layout.addLayout(self._layout2)

        # add product section
        self._layout2.addLayout(self.add_prod_layout)
        self.add_prod_layout.addWidget(self.add_pro_label)
        self.add_prod_layout.addRow(self.pro_name_lb, self.prod_name_le)
        self.add_prod_layout.addRow(self.pro_cat_label, self.prod_cat_cb)
        self.add_prod_layout.addRow(self.pro_size_lb, self.prod_size_cb)
        self.add_prod_layout.addRow(self.pro_unit_lb, self.prod_unit_cb)
        self.add_prod_layout.addRow(self.pro_price_lb, self.prod_price_cb)
        self.add_prod_layout.addRow(self.pro_gst_label, self.prod_gst_le)

        self.add_prod_layout.addWidget(self.add_prod_btn)

        # delete product section
        self._layout2.addLayout(self.del_pro_layout)
        self.del_pro_layout.addWidget(self.del_pro_label)
        self.del_pro_layout.addWidget(self.products_lw)
        self.del_pro_layout.addWidget(self.del_prod_btn)

        self.setWindowState(QtCore.Qt.WindowMaximized)

        # products_lw header

    def _setup_widget_connections(self):
        self.add_prod_btn.clicked.connect(self._on_add_product)
        self.del_prod_btn.clicked.connect(self._on_delete_product)
        self.add_prod_btn.clicked.connect(prompts.product_added)

    def add_products_lw(self):
        all_products = products.Products().all()
        for each in all_products:
            product_widget = ProductsWid(each)
            lwi = QtWidgets.QListWidgetItem()
            lwi.setSizeHint(product_widget.sizeHint())
            self.products_lw.addItem(lwi)
            self.products_lw.setItemWidget(lwi, product_widget)

    def add_category(self):
        category_names = products_category.ProductsCategory().all()
        for each in category_names:
            self.prod_cat_cb.addItem(each['name'])

        unit_names = units.Unit().all()
        for each in unit_names:
            self.prod_unit_cb.addItem(each['name'])

    def _on_add_product(self):
        name = self.prod_name_le.text()
        category = self.prod_cat_cb.currentText()
        price = self.prod_price_cb.text()
        gst = self.prod_gst_le.text()
        size = self.prod_size_cb.text()
        unit = self.prod_unit_cb.currentText()
        category_id = list()
        unit_id = list()
        for each in self.category_names:
            if each['name'] == category:
                category_id.append(each['id'])
        for each in self.unit_names:
            if each['name'] == unit:
                unit_id.append(each['id'])

        values_ls = list()
        values_ls.append((name, category_id[0], price, gst, size, unit_id[0]))

        products.Products().insert(values_ls[0])

    def _on_delete_product(self):
        for i in range(self.products_lw.count()):
            item = self.products_lw.item(i)
            wid = self.products_lw.itemWidget(item)
            if not wid.checked:
                continue
            product_id = wid.chek_box_id
            products.Products().delete(product_id=product_id)

    def apply_stylesheet(self):
        self.setStyleSheet(get_stylesheet('modify_products'))


if __name__ == '__main__':
    pass
    # app = QtWidgets.QApplication(sys.argv)
    # inst = ModifyProducts()
    # root = QtWidgets.QWidget()
    # inst.show()
    # app.exec()
