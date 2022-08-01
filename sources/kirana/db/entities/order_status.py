# All Python Built-in Imports Here.

# All Custom Imports Here.

# All Native Imports Here.
from kirana.db.entities import BaseEntity


# All Attributes or Constants Here.


class OrderStatus(BaseEntity):
    TABLE_NAME = 'order_status'
    COLUMN_NAME = BaseEntity().get_all_column_names(TABLE_NAME)

    def __init__(self):
        super(OrderStatus, self).__init__()


if __name__ == '__main__':
    inst = OrderStatus()
    res = inst.filter(postal_code=410209)
    print(inst.all())
    print(inst.get(id=1))
