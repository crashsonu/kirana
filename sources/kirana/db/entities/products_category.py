# All Python Built-in Imports Here.

# All Custom Imports Here.
from kirana.db.entities import BaseEntity

# All Native Imports Here.

# All Attributes or Constants Here.


class ProductsCategory(BaseEntity):
    TABLE_NAME = 'products_category'
    COLUMN_NAME = BaseEntity().get_all_column_names(TABLE_NAME)

    def __init__(self):
        super(ProductsCategory, self).__init__()


if __name__ == '__main__':
    pass
