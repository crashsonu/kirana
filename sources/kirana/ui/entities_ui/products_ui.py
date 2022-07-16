# All Python Built-in Imports Here.
import sys

# All Custom Imports Here.
from PySide6 import QtWidgets


# All Native Imports Here.


# All Attributes or Constants Here.


class ProductWidget(QtWidgets.QWidget):
    product_name = ''

    def __init__(self):
        super(ProductWidget, self).__init__()
        self._layout = QtWidgets.QVBoxLayout()
        self.setLayout(self._layout)
        self._layout2 = QtWidgets.QHBoxLayout()
        self.setLayout(self._layout2)
        self._layout.addLayout(self._layout2)
        self._chk_box = QtWidgets.QCheckBox()
        self._spin_box = QtWidgets.QSpinBox()
        self._label = QtWidgets.QLabel()

        self._layout2.addWidget(self._chk_box)
        self._layout2.addWidget(self._label)
        self._label.setText(self.product_name)
        self._layout2.addWidget(self._spin_box)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    inst = ProductWidget()
    inst.show()
    app.exec()
