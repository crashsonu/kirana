# All Python Built-in Imports Here.
import sys

# All Custom Imports Here.
from kirana.ui.entities_ui import products_ui
from kirana.ui.entities_ui import order_ui
from kirana.ui.entities_ui import order_status_ui
from PySide6 import QtWidgets
from PySide6 import QtCore

# All Native Imports Here.


# All Attributes or Constants Here.


class WindowKiranaManager(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        print(1111111111111111)
        self._place_order_wid = order_ui.OrderWidget()
        self._all_orders_wid = order_ui.AllOrdersTableWidget()
        self._modification_wid = products_ui.ModifyProducts()
        self._add_order_status_wid = order_status_ui.OrderStatusUi()
        # self._test_wid = ModifyProducts()
        self._layout = QtWidgets.QVBoxLayout()
        self.tab_widget = QtWidgets.QTabWidget()
        print(9999999999999)

        self._initialize()

    def _initialize(self):
        self._setup_ui()
        self._setup_connections()

    def _setup_ui(self):
        self.setLayout(self._layout)
        self._layout.addWidget(self.tab_widget)
        print(4444444444)
        self.tab_widget.addTab(self._modification_wid, 'ADD OR DELETE PRODUCTS')
        print(555555555)
        self.tab_widget.addTab(self._place_order_wid, 'PLACE ORDER')
        print(666666666666)
        self.tab_widget.addTab(self._all_orders_wid, 'ORDERS HISTORY')
        print(77777777777)
        self.tab_widget.addTab(self._add_order_status_wid, 'SET ORDER DELIVERY STATUS')
        print(8888888888888)
        # self.tab_widget.addTab(self._test_wid, 'TEST TAB')
        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.setWindowTitle('KIRANA MANAGER')

    def _setup_connections(self):
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    inst = WindowKiranaManager()
    root = QtWidgets.QWidget()
    inst.show()
    app.exec()
