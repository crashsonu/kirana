# All Python Built-in Imports Here.

# All Custom Imports Here.

# All Native Imports Here.
from kirana.db.entities import BaseEntity


# All Attributes or Constants Here.

class Unit(BaseEntity):
    TABLE_NAME = 'units'
    COLUMN_NAME = BaseEntity().get_all_column_names(TABLE_NAME)

    def __init__(self):
        super(Unit, self).__init__()


if __name__ == '__main__':
    pass
