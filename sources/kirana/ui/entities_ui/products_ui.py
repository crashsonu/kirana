# All Python Built-in Imports Here.

# All Custom Imports Here.
from PySide6 import QtGui

# All Native Imports Here.
from kirana.db.entities.units import Unit

# ModifyProducts imports here
from kirana.db.entities import products_category
from kirana.db.entities import products
from kirana.ui import get_stylesheet
from kirana.db.entities import units
from PySide6 import QtWidgets
from kirana.ui.prompt import prompts
from PySide6 import QtCore


# All Attributes or Constants Here.


class ProductWidget(QtWidgets.QWidget):
    """For adding products list for place order tab."""
    def __init__(self, product_info):
        """Product widget to show product for add to cart or else.
        Args:
            product_info (dict): product info returned by the database.
        """
        super(ProductWidget, self).__init__()
        self._product_info = product_info

        self._layout = QtWidgets.QHBoxLayout()
        self._checkbox = QtWidgets.QCheckBox()
        self._qty_spb = QtWidgets.QSpinBox()
        self._price_label = QtWidgets.QLabel()
        self._unit_label = QtWidgets.QLabel()
        self._gst_label = QtWidgets.QLabel()

        self.checked_product_list = list()

        self._initialize()

    @property
    def product_info(self):
        return self._product_info

    @property
    def checked(self):
        return self._checkbox.isChecked()

    def _initialize(self):
        self._setup_widget()
        self._setup_widget_connections()

    def _setup_widget(self):
        self.setLayout(self._layout)
        self.setObjectName('ProductWidget')
        self.setAttribute(QtGui.Qt.WA_StyledBackground)

        self._layout.addWidget(self._checkbox)
        self._layout.addWidget(self._price_label)
        self._layout.addWidget(self._qty_spb)
        self._layout.addWidget(self._unit_label)
        self._layout.addWidget(self._gst_label)

        self._checkbox.setText(self._product_info['name'])
        self._checkbox.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        # setting price by quantity initial 1.
        self._qty_spb.setValue(1)
        self.pro_price_init = self._product_info["price"]
        self._price_label.setText(f'Rs. {self.pro_price_init}')

        # setting unit like KG for product.
        self.qty_label = Unit().get(return_fields='name', id=self._product_info['unit_id'])
        self._unit_label.setText(self.qty_label)
        # setting GST label initial given.
        _product_gst = self._product_info['gst']
        self._gst_label.setText(f'{_product_gst}% gst')

    def _setup_widget_connections(self):
        self._qty_spb.valueChanged.connect(self._on_change_quantity)

    def _on_change_quantity(self):
        spb_current_value = self._qty_spb.value()
        self.prod_price = spb_current_value * self.pro_price_init
        self._price_label.setText(f'Rs. {self.prod_price}')

    def get_for_cart(self):
        id_ = self._product_info.get('id')
        name = self._product_info.get('name')
        category_id = self._product_info.get('category_id')
        price = self._product_info.get('price')
        gst = self._product_info.get('gst')
        size = self._product_info.get('size')
        unit_id = self._product_info.get('unit_id')
        unit_name = Unit().get(id=unit_id)[0]['name']

        result = dict()
        result.update(id=id_, name=name, category_id=category_id, price=price,
                      size=size, gst_percent=gst, unit_id=unit_id, unit_name=unit_name)

        quantity = self._qty_spb.value()
        result.update(quantity=quantity)

        total = round(price * quantity, 1)
        result.update(total=total)

        gst_price = round((total / 100) * gst, 1)
        result.update(gst=gst_price)

        result.update(grand_total=total + gst_price)
        self.checked_product_list.append(result)

        return result



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
        product_ids = list()
        for i in range(self.products_lw.count()):
            item = self.products_lw.item(i)
            wid = self.products_lw.itemWidget(item)
            if not wid.checked:
                continue
            product_id = wid.chek_box_id
            product_ids.append(product_id)
        products.Products().delete(product_ids=product_ids)
        prompts.product_deleted()

    def apply_stylesheet(self):
        self.setStyleSheet(get_stylesheet('product'))


if __name__ == '__main__':
    pass
    # app = QtWidgets.QApplication(sys.argv)
    # inst = ModifyProducts()
    # root = QtWidgets.QWidget()
    # inst.show()
    # app.exec()
