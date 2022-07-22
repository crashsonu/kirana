# All Python Built-in Imports Here.

# All Custom Imports Here.
from kirana.db.entities import BaseEntity


# All Native Imports Here.

# All Attributes or Constants Here.


class Products(BaseEntity):
    TABLE_NAME = 'products'
    COLUMN_NAME = BaseEntity().get_all_column_names(table_name=TABLE_NAME)

    def __init__(self):
        super(Products, self).__init__()


if __name__ == '__main__':
    inst = Products()
    res = inst.get(category_id=2)
    from pprint import pprint

    pprint(res)

    pass
