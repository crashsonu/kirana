# All Python Built-in Imports Here.
from datetime import datetime

# All Custom Imports Here.

# All Native Imports Here.
from kirana.db.entities import BaseEntity
from kirana.db import db_connection
from kirana.db.entities import get_table_column_names


# All Attributes or Constants Here.


class Order(BaseEntity):
    TABLE_NAME = 'orders'
    COLUMN_NAME = get_table_column_names(TABLE_NAME)

    def __init__(self):
        super(Order, self).__init__()

    @staticmethod
    @db_connection
    def get(table_name, column_name, column_value, get_column='*', **kwargs):
        connection = kwargs.pop('connection')
        cursor = connection.cursor()

        cursor.execute(f'select {get_column} from {table_name} where {column_name} = "{column_value}"')
        data = dict()
        for attr, value in zip(get_table_column_names(table_name), cursor.fetchall()[0]):
            data[attr] = value
        get_table_column_names(table_name)
        cursor.close()
        return data

    @db_connection
    def insert_into_db(self, **kwargs):
        connection = kwargs.pop('connection')
        cursor = connection.cursor()
        self.COLUMN_NAME.pop(0)
        col_str = ''
        for column in self.COLUMN_NAME:
            col = f'{column}, '
            col_str += col

        columns_str = col_str.strip(', ')

        customer_id = kwargs.get('customer_id')
        products_info = kwargs.get('products')
        # products info data in json
        products_info_dict = {}
        for k, v in products_info.items():
            products_info_dict[f"{k}"] = f"{v}"

        products_info_dict_str = f'"{products_info_dict}"'

        ordered_on = datetime.now()

        _str = ('%s, ' * len(self.COLUMN_NAME)).strip(', ')
        msg = f'insert into {self.TABLE_NAME}({columns_str}) values({_str})'
        values = (customer_id, products_info_dict_str, ordered_on)
        cursor.execute(msg, values)
        connection.commit()
        print(cursor.rowcount, "record inserted.")
        cursor.close()

    def place_order(self, **kwargs):
        _result = dict()
        products_data = list()

        # getting given kwarg customer_id
        _customer_id = list(kwargs.values())[0]

        customer_data = self.get('customers', 'id', _customer_id)
        _result['customer'] = customer_data

        # kwarg products is dictionary of key product_id and value quantity.
        for pro_id, qty in kwargs.get('products').items():
            product_data = self.get('products', 'id', pro_id)
            product_data.pop('id')
            product_data.pop('category_id')
            product_data.setdefault('quantity', qty)
            products_data.append(product_data)

        # getting price according to quantity and gst

        order_total_of_products = 0
        order_total_of_gst = 0
        for product in products_data:
            product['gst_percent'] = product['gst']
            pro_qua_price = product['price'] * product['quantity']
            product['product_gst'] = round(pro_qua_price * product['gst_percent'] / 100, 2)
            product['total'] = round(pro_qua_price + product['product_gst'], 2)
            _units = self.get('units', 'id', product['unit_id'], get_column='name')
            product['size_unit'] = list(_units.values())[0]
            product.pop('gst')
            product.pop('unit_id')

            order_total_of_products += product['total']
            order_total_of_gst += round(product['product_gst'], 2)

        _result['products'] = products_data
        _result['grand_total'] = order_total_of_products
        _result['GST'] = order_total_of_gst

        self.insert_into_db(**kwargs)

        return _result

    @staticmethod
    @db_connection
    def get_column(table_name, column_name, **kwargs):
        conn = kwargs.pop('connection')
        cursor = conn.cursor()

        cursor.execute(f'select {column_name} from {table_name}')
        _result = list()
        for i in cursor.fetchall():
            _result.append(i[0])
        return _result

    @staticmethod
    @db_connection
    def get_column_by_cond(table_name, column_name, column_value, get_column='*', **kwargs):
        conn = kwargs.pop('connection')
        cursor = conn.cursor()

        cursor.execute(f'select {get_column} from {table_name} where {column_name}={column_value}')
        _result = list()
        for i in cursor.fetchall():
            _result.append(i[0])
        return _result


if __name__ == '__main__':
    kw = dict(customer_id=1,
              products={1: 5, 4: 2},
              )
    inst = Order()
    # result = inst.place_order(**kw)
    inst.get_column('products_category', 'name')
    from pprint import pprint
    # pprint(result)
