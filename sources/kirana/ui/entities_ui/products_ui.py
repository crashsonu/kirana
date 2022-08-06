# All Python Built-in Imports Here.

# All Custom Imports Here.
from PySide6 import QtGui
from PySide6 import QtCore
import os

# All Native Imports Here.
from kirana.db.entities.units import Unit

# ModifyProducts imports here
from kirana.db.entities import products_category
from kirana.db.entities import products
from kirana.ui import get_stylesheet
from kirana.db.entities import units
from PySide6 import QtWidgets
from kirana.ui.prompt import prompts
from kirana import ui


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


class AddNewProduct(QtWidgets.QDialog):
    category_names = products_category.ProductsCategory().all()
    unit_names = units.Unit().all()

    def __init__(self):
        super(AddNewProduct, self).__init__()
        self._layout1 = QtWidgets.QVBoxLayout()
        self._layout = QtWidgets.QFormLayout()
        self._layout.setContentsMargins(200, 50, 120, 0)

        self.add_pro_label = QtWidgets.QLabel('ADD NEW PRODUCT DETAILS')

        self.add_prod_lw = QtWidgets.QListWidget()
        self.pro_name_lb = QtWidgets.QLabel('Product Name')
        self.prod_name_le = QtWidgets.QLineEdit()
        self.prod_name_le.setFixedSize(400, 40)
        self.pro_cat_label = QtWidgets.QLabel("Select Product Category")
        self.prod_cat_cb = QtWidgets.QComboBox()
        self.prod_cat_cb.setFixedSize(400, 40)
        self.pro_price_lb = QtWidgets.QLabel('Price in Rs.')
        self.prod_price_cb = QtWidgets.QLineEdit()
        self.prod_price_cb.setFixedSize(400, 40)
        self.pro_gst_label = QtWidgets.QLabel('GST Percentage')
        self.prod_gst_le = QtWidgets.QLineEdit()
        self.prod_gst_le.setFixedSize(400, 40)
        self.prod_gst_le.setPlaceholderText('GST Percentage')
        self.pro_size_lb = QtWidgets.QLabel('Size Of Packet related to Unit')
        self.prod_size_cb = QtWidgets.QLineEdit()
        self.prod_size_cb.setFixedSize(400, 40)
        self.prod_size_cb.setPlaceholderText('Ex. 1, 2')
        self.pro_unit_lb = QtWidgets.QLabel('Select Unit')
        self.prod_unit_cb = QtWidgets.QComboBox()
        self.prod_unit_cb.setFixedSize(400, 40)
        self.add_prod_btn = QtWidgets.QPushButton("Add Product")
        self._spacer = QtWidgets.QSpacerItem(150, 10, QtWidgets.QSizePolicy.Expanding)

        self._layout.setVerticalSpacing(45)
        self._layout.setHorizontalSpacing(20)

        self._initialize()

    def _initialize(self):
        self._setup_ui()
        self._setup_connections()
        self.add_category()
        self.add_unit()
        self.apply_stylesheet()

    def _setup_ui(self):
        self.setLayout(self._layout1)
        self._layout1.addLayout(self._layout)
        self._layout.addRow(self.pro_name_lb, self.prod_name_le)
        self._layout.addRow(self.pro_cat_label, self.prod_cat_cb)
        self._layout.addRow(self.pro_size_lb, self.prod_size_cb)
        self._layout.addRow(self.pro_unit_lb, self.prod_unit_cb)
        self._layout.addRow(self.pro_price_lb, self.prod_price_cb)
        self._layout.addRow(self.pro_gst_label, self.prod_gst_le)

        self._layout1.addWidget(self.add_prod_btn)

    def _setup_connections(self):
        self.add_prod_btn.clicked.connect(self._on_add_product)

    def add_category(self):
        for each in self.category_names:
            self.prod_cat_cb.addItem(each['name'])

    def add_unit(self):
        for each in self.unit_names:
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
        null_check_list = {'Product Name': name, 'category': category, 'Packet Size': size, 'unit': unit, 'price': price, 'GST_percentage': gst}
        for k, v in null_check_list.items():
            if len(v) == 0:
                prompts.field_required(k)
                return

        for each in self.category_names:
            if each['name'] == category:
                category_id.append(each['id'])
        for each in self.unit_names:
            if each['name'] == unit:
                unit_id.append(each['id'])

        values_ls = list()
        values_ls.append((name, category_id[0], price, gst, size, unit_id[0]))

        products.Products().insert(values_ls[0])
        prompts.product_added()
        line_edit_clear_list = [self.prod_name_le, self.prod_gst_le, self.prod_size_cb, self.prod_price_cb]
        for x in line_edit_clear_list:
            x.clear()

    def apply_stylesheet(self):
        self.setStyleSheet(get_stylesheet('products/add_product'))


class DeleteProduct(QtWidgets.QDialog):
    def __init__(self):
        super(DeleteProduct, self).__init__()
        self._layout = QtWidgets.QVBoxLayout()
        self.pro_chk_box = QtWidgets.QCheckBox()
        self.pro_lw = QtWidgets.QListWidget()
        self.del_prod_btn = QtWidgets.QPushButton("Delete Product")
        self.del_pro_label = QtWidgets.QLabel('DELETE SELECTED PRODUCT')

        self._initialize()

    def _initialize(self):
        self._setup_ui()
        self.apply_stylesheet()
        self._setup_connections()

    def _setup_ui(self):
        self.setLayout(self._layout)
        self._layout.addWidget(self.del_pro_label)
        self._layout.addWidget(self.pro_lw)
        self.add_all_products()
        self._layout.addWidget(self.del_prod_btn)

    def _setup_connections(self):
        self.del_prod_btn.clicked.connect(self._on_delete_product)

    def add_all_products(self):
        all_products = products.Products().all()
        for each in all_products:
            product_widget = ProductsWid(each)
            lwi = QtWidgets.QListWidgetItem()
            lwi.setSizeHint(product_widget.sizeHint())
            self.pro_lw.addItem(lwi)
            self.pro_lw.setItemWidget(lwi, product_widget)

    def _on_delete_product(self):
        product_ids = list()
        for i in range(self.pro_lw.count()):
            item = self.pro_lw.item(i)
            wid = self.pro_lw.itemWidget(item)
            if not wid.checked:
                continue
            product_id = wid.chek_box_id
            product_ids.append(product_id)
        products.Products().delete(product_ids=product_ids)
        prompts.product_deleted()

    def apply_stylesheet(self):
        self.setStyleSheet(get_stylesheet('products/delete_product'))


class AddNewCategory(QtWidgets.QDialog):
    def __init__(self):
        super(AddNewCategory, self).__init__()
        self._layout = QtWidgets.QFormLayout()
        self.add_cat_layout = QtWidgets.QFormLayout()
        self.add_cat_label = QtWidgets.QLabel('ADD CATEGORY')
        self.category_name_label = QtWidgets.QLabel("Category Name")
        self.category_name_le = QtWidgets.QLineEdit()
        self.category_name_le.setPlaceholderText('category name....')
        self.add_cat_btn = QtWidgets.QPushButton('Add Category')

        self._initialize()

    def _initialize(self):
        self._setup_ui()
        self._setup_connections()

    def _setup_ui(self):
        self.setLayout(self._layout)
        self._layout.addRow(self.add_cat_label)
        self._layout.addRow(self.category_name_label, self.category_name_le)
        self._layout.addWidget(self.add_cat_btn)

    def _setup_connections(self):
        self.add_cat_btn.clicked.connect(self._on_add_category)

    def _on_add_category(self):
        category_name = [self.category_name_le.text()]
        products_category.ProductsCategory().insert(category_name)
        prompts.category_added()
        self.category_name_le.clear()


class DeleteCategory(QtWidgets.QDialog):
    category_names = products_category.ProductsCategory().all()

    def __init__(self):
        super(DeleteCategory, self).__init__()
        self._layout = QtWidgets.QFormLayout()
        self.delete_cat_label = QtWidgets.QLabel('DELETE CATEGORY')
        self.del_category_name_label = QtWidgets.QLabel("Category Name")
        self.category_combox = QtWidgets.QComboBox()
        self.category_combox.setCurrentText('select category....')
        self.del_cat_btn = QtWidgets.QPushButton('Delete Category')

        self._initialize()

    def _initialize(self):
        self._setup_ui()
        self.add_category()
        self._setup_connections()

    def _setup_ui(self):
        self.setLayout(self._layout)
        self._layout.addRow(self.delete_cat_label)
        self._layout.addRow(self.del_category_name_label, self.category_combox)
        self._layout.addWidget(self.del_cat_btn)

    def _setup_connections(self):
        self.del_cat_btn.clicked.connect(self._on_delete_category)

    def add_category(self):
        for each in self.category_names:
            self.category_combox.addItem(each['name'])

    def _on_delete_category(self):
        category_name = self.category_combox.currentText()
        products_category.ProductsCategory().delete(category_name)
        print('Category deleted!')


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


class ModifyProducts(QtWidgets.QTabWidget):

    def __init__(self):
        super(ModifyProducts, self).__init__()
        self.add_product_wid = AddNewProduct()
        self.delete_prod_wid = DeleteProduct()
        self.add_cat_wid = AddNewCategory()
        self.delete_cat_wid = DeleteCategory()

        self._initialize()

    def _initialize(self):
        self._setup_ui()

    def _setup_ui(self):
        # self.addTab(self.add_product_wid, "ADD NEW PRODUCT")
        self.addTab(self.delete_prod_wid, "DELETE PRODUCT")
        # self.addTab(self.add_cat_wid, "ADD NEW CATEGORY")
        # self.addTab(self.delete_cat_wid, "DELETE CATEGORY")
        self.tabs = {0: 'add.png', 1: 'delete.png', 2: 'add.png', 3: 'delete.png'}
        for k, v in self.tabs.items():
            self.image_path = os.path.join(ui.IMAGES_PATH, v)
            self.setTabIcon(k, QtGui.QIcon(self.image_path))
            self.setIconSize(QtCore.QSize(50, 30))

    def apply_stylesheet(self):
        self.setStyleSheet(get_stylesheet('modify_products'))


if __name__ == '__main__':
    pass
    # app = QtWidgets.QApplication(sys.argv)
    # inst = ModifyProducts()
    # root = QtWidgets.QWidget()
    # inst.show()
    # app.exec()
