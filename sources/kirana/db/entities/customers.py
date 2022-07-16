# All Python Built-in Imports Here.

# All Custom Imports Here.

# All Native Imports Here.
from kirana.db.entities import BaseEntity
from kirana.db.entities import get_table_column_names


# All Attributes or Constants Here.


class Customer(BaseEntity):
    TABLE_NAME = 'customers'
    COLUMN_NAME = get_table_column_names(TABLE_NAME)

    def __init__(self):
        super(Customer, self).__init__()


if __name__ == '__main__':
    inst = Customer()
    res = inst.filter(postal_code=410209)
    print(inst.all())
    print(inst.get(id=1))
