# All Python Built-in Imports Here.
import sys

# All Custom Imports Here.
from kirana.ui.entities_ui import products_ui
from kirana.ui.entities_ui import order_ui
from kirana.ui.entities_ui import order_status_ui
from PySide6 import QtWidgets
from PySide6 import QtGui

# All Native Imports Here.


# All Attributes or Constants Here.


class WindowKiranaManager(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(1300)
        self.setFixedHeight(700)
        qtRectangle = self.frameGeometry()
        cp = QtGui.QGuiApplication.primaryScreen().availableGeometry().center()
        qtRectangle.moveCenter(cp)
        self.move(qtRectangle.topLeft())

        self._place_order_wid = order_ui.OrderWidget()
        self._all_orders_wid = order_ui.AllOrdersTableWidget()
        self._modification_wid = products_ui.ModifyProducts()
        self._add_order_status_wid = order_status_ui.OrderStatusUi()
        # self._test_wid = ModifyProducts()
        self._layout = QtWidgets.QVBoxLayout()
        self.tab_widget = QtWidgets.QTabWidget()

        self._initialize()

    def _initialize(self):
        self._setup_ui()
        self._setup_connections()

    def _setup_ui(self):
        self.setLayout(self._layout)
        self._layout.addWidget(self.tab_widget)
        self.tab_widget.addTab(self._modification_wid, 'ADD OR DELETE PRODUCTS')
        self.tab_widget.addTab(self._place_order_wid, 'PLACE ORDER')
        self.tab_widget.addTab(self._all_orders_wid, 'ORDERS HISTORY')
        self.tab_widget.addTab(self._add_order_status_wid, 'SET ORDER DELIVERY STATUS')
        # self.tab_widget.addTab(self._test_wid, 'TEST TAB')
        self.setWindowTitle('KIRANA MANAGER')

    def _setup_connections(self):
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    inst = WindowKiranaManager()
    root = QtWidgets.QWidget()
    inst.show()
    app.exec()
