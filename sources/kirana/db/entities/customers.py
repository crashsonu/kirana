# All Python Built-in Imports Here.

# All Custom Imports Here.

# All Native Imports Here.
from kirana.db.entities import BaseEntity


# All Attributes or Constants Here.


class Customer(BaseEntity):
    TABLE_NAME = 'customers'
    COLUMN_NAME = BaseEntity().get_all_column_names(TABLE_NAME)

    def __init__(self):
        super(Customer, self).__init__()


if __name__ == '__main__':
    pass
    # inst = Customer()
    # res = inst.get(return_fields='id', mobile=7715809262)
    # print(res)

