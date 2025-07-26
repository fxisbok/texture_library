import typing
import pymysql

class OpenDB:
    def __enter__(self):
        self.connector = pymysql.connect(
            host='172.30.1.63',
            port=3306,
            user='root',
            password='1523',
            db='texture_library',
            charset='utf8'
        )
        self.cursor = self.connector.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.execute('COMMIT')
        self.cursor.close()

class CRUD:
    def get_query_insert(self, table: str, fields: str="*", vals: str = ""):
        """
        C for CRUD. combine query command based on arguments.
        :param table: data table name
        :param fields: column to read
        :param vals: input values
        :return: combined query command
        """
        result = f"INSERT INTO {table} {fields} VALUES {vals}"
        return result

    def get_query_select(self, table: str, fields: str="*", filters: str = ""):
        """
        R for CRUD. combine query command based on arguments.
        :param table: data table name
        :param fields: column to read
        :param filters: filter for search
        :return: combined query command
        """
        result = f"SELECT {fields} FROM {table}"
        if filters:
            result += f" WHERE {filters}"
        return result

    def get_query_update(self, table: str, fields: str="*", filters: str = ""):
        """
        U for CRUD. combine query command based on arguments.
        :param table: data table name
        :param fields: column to read
        :param filters: filter for search
        :return: combined query command
        """
        result = f"UPDATE {table} SET {fields} WHERE {filters}"
        return result

    def get_query_delete(table: str, filters: str = ""):
        """
        D for CRUD. combine query command based on arguments.
        :param table: data table name
        :param filters: filter for search
        :return: combined query command
        """
        result = f"DELETE FROM {table} WHERE {filters}"
        return result


if __name__ == "__main__":
    with OpenDB() as database:
        database.cursor.execute('DESC assets')
        print(database.cursor.fetchall())