# All Python Built-in Imports Here.
import mysql.connector


# All Custom Imports Here.

# All Native Imports Here.

# All Attributes or Constants Here.


def db_connection(func):
    def wrapper(*args, **kwargs):
        connection = mysql.connector.connect(
            host='192.168.0.231',
            user='sonali',
            password='Sonali@123',
            database='kirana'
        )
        try:
            kwargs.update(connection=connection)
            _result = func(*args, **kwargs)
            return _result

        except Exception as ex:
            print(ex)

        finally:
            connection.close()

    return wrapper


if __name__ == '__main__':
    pass
