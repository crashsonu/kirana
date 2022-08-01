# All Python Built-in Imports Here.
from datetime import datetime

# All Custom Imports Here.

# All Native Imports Here.
from kirana.db.entities import BaseEntity
from kirana.db import db_connection
from kirana.db.entities import BaseEntity


# All Attributes or Constants Here.


class Order(BaseEntity):
    TABLE_NAME = 'orders'
    COLUMN_NAME = BaseEntity().get_all_column_names(TABLE_NAME)

    def __init__(self):
        super(Order, self).__init__()


if __name__ == '__main__':
    inst = Order()
    inst.delete([18, 19])
