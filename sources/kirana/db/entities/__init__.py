# All Python Built-in Imports Here.

# All Custom Imports Here.

# All Native Imports Here.
from kirana.db import db_connection


# All Attributes or Constants Here.


class BaseEntity:
    TABLE_NAME = ''
    COLUMN_NAME = ''

    def __init__(self):
        pass

    @staticmethod
    def zip_method(table_columns, values):
        result = list()
        for i in values:
            _records = dict()
            for key, value in zip(table_columns, i):
                _records[key] = value
            result.append(_records)
        return result

    @db_connection
    def get_all_column_names(self, table_name, **kwargs):
        """

        Args:
            table_name: table name whose columns you want.
            **kwargs: for wrapper function.

        Returns: list of all column names present in given table.

        """
        connection = kwargs.get('connection')
        cursor = connection.cursor()
        cursor.execute(f'show columns from {table_name}')
        table_column_names = list()
        for column_name in cursor.fetchall():
            table_column_names.append(column_name[0])

        cursor.close()
        return table_column_names

    @db_connection
    def get_table_field(self, table_name, column_name, column_value, get_column='*', **kwargs):
        connection = kwargs.pop('connection')
        cursor = connection.cursor()

        cursor.execute(f'select {get_column} from {table_name} where {column_name} = "{column_value}"')
        data = dict()
        for attr, value in zip(self.get_all_column_names(table_name), cursor.fetchall()[0]):
            data[attr] = value
        self.get_all_column_names(table_name)
        cursor.close()
        return data

    # @db_connection
    # def get_column(self, table_name, column_name, **kwargs):
    #     conn = kwargs.pop('connection')
    #     cursor = conn.cursor()
    #
    #     cursor.execute(f'select {column_name} from {table_name}')
    #     _result = list()
    #     for i in cursor.fetchall():
    #         _result.append(i[0])
    #     return _result

    @db_connection
    def all(self, column_name=None, ** kwargs):
        """
        returns all table data with their columns names row in table is a dict.
        Args:
            column_name: when want particular column data. eg - name
            **kwargs:

        Returns:

        """

        conn = kwargs.get('connection')
        cursor = conn.cursor()

        table_data = list()
        if column_name is None:
            column_name = '*'
            cursor.execute(f'select {column_name} from {self.TABLE_NAME}')
            for each in cursor.fetchall():
                table_data.append(each)
            # zipping customer details with columns.
            return self.zip_method(self.COLUMN_NAME, table_data)

        else:
            cursor.execute(f'select {column_name} from {self.TABLE_NAME}')
            for each in cursor.fetchall():
                table_data.append(each)
            return table_data

    @db_connection
    def filter(self, **kwargs):
        conn = kwargs.pop('connection')
        cursor = conn.cursor()
        result = list()

        msg_str = ''
        for k, v in kwargs.items():
            if type(v) == int:
                _msg_str = f'{k} = {v} and '
                msg_str += _msg_str
                continue
            else:
                _msg_str = f'{k} = "{v}" and '
                msg_str += _msg_str
        _msg_str = msg_str.strip(' and ')

        msg = f"select * from {self.TABLE_NAME} where {_msg_str} "
        cursor.execute(msg)
        for i in cursor.fetchall():
            result.append(i)

        return self.zip_method(self.COLUMN_NAME, result)

    @db_connection
    def get(self, return_fields=None, **kwargs):
        connection = kwargs.pop('connection')
        cursor = connection.cursor()
        column_name = list(kwargs.keys())[0]
        column_value = list(kwargs.values())[0]

        if return_fields is not None:
            cursor.execute(f'select {return_fields} from {self.TABLE_NAME} where {column_name} = "{column_value}"')
            _fetched = (cursor.fetchall())[0][0]
            return _fetched

        cursor.execute(f'select * from {self.TABLE_NAME} where {column_name} = "{column_value}"')
        _result = self.zip_method(self.COLUMN_NAME, cursor.fetchall())

        cursor.close()
        return _result


if __name__ == '__main__':
    pass
