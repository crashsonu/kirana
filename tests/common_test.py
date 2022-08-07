import os
from kirana.ui import IMAGES_PATH

icon_file = os.path.join(IMAGES_PATH, 'add.png')
print(icon_file)
print(os.path.exists(icon_file))

self._layout1 = QtWidgets.QVBoxLayout()
self.del_category_name_label = QtWidgets.QLabel("Category Name")
self.category_combox = QtWidgets.QComboBox()
self.category_combox.setFixedSize(400, 40)
self.category_combox.setCurrentText('select category....')
self.del_cat_btn = QtWidgets.QPushButton('Delete Category')