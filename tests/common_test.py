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


class AddNewProduct(QtWidgets.QFormLayout):
    category_names = products_category.ProductsCategory().all()
    unit_names = units.Unit().all()

    def __init__(self):
        super(AddNewProduct, self).__init__()

        self.add_pro_label = QtWidgets.QLabel('ADD NEW PRODUCT DETAILS')

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

    def _setup_ui(self):
        self.addWidget(self.add_pro_label)
        self.addRow(self.pro_name_lb, self.prod_name_le)
        self.addRow(self.pro_cat_label, self.prod_cat_cb)
        self.addRow(self.pro_size_lb, self.prod_size_cb)
        self.addRow(self.pro_unit_lb, self.prod_unit_cb)
        self.addRow(self.pro_price_lb, self.prod_price_cb)
        self.addRow(self.pro_gst_label, self.prod_gst_le)

        self.addWidget(self.add_prod_btn)

    def _setup_connection(self):
        self.add_prod_btn.clicked.connect(self._on_add_product)

    def add_category(self):
        for each in self.category_names:
            self.prod_cat_cb.addItem(each['name'])

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
        prompts.product_added()


class DeleteProduct(QtWidgets.QListWidget):
    def __init__(self):
        super(DeleteProduct, self).__init__()
        self.pro_chk_box = QtWidgets.QCheckBox()
        self.del_prod_btn = QtWidgets.QPushButton("Delete Product")
        self.del_pro_label = QtWidgets.QLabel('DELETE SELECTED PRODUCT')

    def _setup_ui(self):
        self.addWidget(self.del_pro_label)
        self.addWidget(self.del_prod_btn)

    def _setup_connections(self):
        self.del_prod_btn.clicked.connect(self._on_delete_product)

    def add_all_products(self):
        all_products = products.Products().all()
        for each in all_products:
            product_widget = ProductsWid(each)
            lwi = QtWidgets.QListWidgetItem()
            lwi.setSizeHint(product_widget.sizeHint())
            self.addItem(lwi)
            self.setItemWidget(lwi, product_widget)

    def _on_delete_product(self):
        product_ids = list()
        for i in range(self.count()):
            item = self.item(i)
            wid = self.itemWidget(item)
            if not wid.checked:
                continue
            product_id = wid.chek_box_id
            product_ids.append(product_id)
        products.Products().delete(product_ids=product_ids)
        prompts.product_deleted()


class AddNewCategory(QtWidgets.QFormLayout):
    def __init__(self):
        super(AddNewCategory, self).__init__()
        self.add_cat_layout = QtWidgets.QFormLayout()
        self.add_cat_label = QtWidgets.QLabel('ADD CATEGORY')
        self.category_name_label = QtWidgets.QLabel("Category Name")
        self.category_name_le = QtWidgets.QLineEdit()
        self.category_name_le.setPlaceholderText('category name....')
        self.add_cat_btn = QtWidgets.QPushButton('Add Category')

    def _setup_ui(self):
        self.addRow(self.add_cat_label)
        self.addRow(self.category_name_label, self.category_name_le)
        self.addWidget(self.add_cat_btn)

    def _setup_connections(self):
        self.add_cat_btn.clicked.connect(self._on_add_category)

    def _on_add_category(self):
        category_name = [self.category_name_le.text()]
        products_category.ProductsCategory().insert(category_name)
        prompts.category_added()
        self.category_name_le.clear()


class DeleteCategory(QtWidgets.QFormLayout):
    category_names = products_category.ProductsCategory().all()

    def __init__(self):
        super(DeleteCategory, self).__init__()
        self.delete_cat_label = QtWidgets.QLabel('DELETE CATEGORY')
        self.del_category_name_label = QtWidgets.QLabel("Category Name")
        self.category_combox = QtWidgets.QComboBox()
        self.category_combox.setCurrentText('select category....')
        self.del_cat_btn = QtWidgets.QPushButton('Delete Category')

    def _setup_ui(self):
        self.addRow(self.delete_cat_label)
        self.addRow(self.del_category_name_label, self.category_combox)
        self.addWidget(self.del_cat_btn)

    def add_category(self):
        for each in self.category_names:
            self.category_combox.addItem(each['name'])

        # unit_names = units.Unit().all()
        # for each in unit_names:
        #     self.prod_unit_cb.addItem(each['name'])

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

    def apply_stylesheet(self):
        self.setStyleSheet(get_stylesheet('product'))


if __name__ == '__main__':
    pass
    # app = QtWidgets.QApplication(sys.argv)
    # inst = ModifyProducts()
    # root = QtWidgets.QWidget()
    # inst.show()
    # app.exec()
