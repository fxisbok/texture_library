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
    @staticmethod
    def get_query_insert(table: str, fields: tuple="*", vals: tuple="", filters: str=""):
        """
        C for CRUD. combine query command based on arguments.
        :param table: data table name
        :param fields: column to read
        :param vals: input values
        :param filters: where state ment
        :return: combined query command
        """
        if len(vals) == 1 or isinstance(vals, str):
            vals = f'("{vals}")'
        result = f"INSERT INTO {table}"
        if filters:
            result += f" WHERE {filters} GROUP BY {fields}"
        else:
            result += f"{fields}"
        result += f" VALUES {vals}"
        return result

    @staticmethod
    def get_query_select(table: str, fields: str="*", filters: str = ""):
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

    @staticmethod
    def get_query_update(table: str, vals: tuple, filters: tuple = ""):
        """
        U for CRUD. combine query command based on arguments.
        :param table: data table name
        :param vals: (column, equation, value) value to update
        :param filters: (column, equation, value) value for indexing
        :return: combined query command
        """
        result = f"UPDATE {table} SET {vals[0]} {vals[1]} {vals[2]} WHERE {filters[0]} {filters[1]} {filters[2]}"
        return result

    @staticmethod
    def get_query_delete(table: str, filters: str = ""):
        """
        D for CRUD. combine query command based on arguments.
        :param table: data table name
        :param filters: filter for search
        :return: combined query command
        """
        result = f"DELETE FROM {table} WHERE {filters}"
        return result

def add_assets(name: str):
    """
    query: INSERT INTO assets(asset_name) VALUES('test_asset_04');
    :param name:
    :return:
    """
    # asset_create_query = CRUD.get_query_insert(
    #     table="assets",
    #     fields='("asset_name")',
    #     vals=(name),
    # )
    ins = INSERT()
    asset_create_query = ins.get_query(
        "assets",
        "asset_name",
        name
    )
    print("commands:",asset_create_query)
    with OpenDB() as db:
        db.cursor.execute(asset_create_query)
        print(db.cursor.fetchall())


# TODO :: 원시 클래스를 만들고, 이를 상속받아 디벨롭 해야할듯
class INSERT:
    def __init__(self):
        self.__table = str()
        self.__columns = str()
        self.__values = str()

    @property
    def prefix(self) -> str:
        return "INSERT INTO"

    @property
    def table(self) -> str:
        return self.__table

    @table.setter
    def table(self, name: str) -> None:
        self.__table = name

    @property
    def columns(self) -> str:
        return self.__columns

    @columns.setter
    def columns(self, colm: str|tuple):
        if isinstance(colm, str):
            self.__columns = f'({colm})'
            return
        self.__columns = str(colm)

    @property
    def values(self) -> str:
        return self.__values

    @values.setter
    def values(self, vals: str|tuple|list[tuple]) -> None:
        if isinstance(vals, tuple):
            self.__values = str(vals)
        elif isinstance(vals, str):
            self.__values = f"('{vals}')"
        else:
            tmp_vals = (str(v) for v in vals)
            self.__values = ",".join(tmp_vals)

    def get_query(self, table, column, values) -> str:
        self.table = table
        self.columns = column
        self.values = values
        result = f"INSERT INTO {self.table}{self.columns} VALUES {self.values}"
        return result

class SELECT:
    def __init__(self):
        self.__table =  str()
        self.__columns = str()
        self.__filters = str()

    @property
    def table(self) -> str:
        return self.__table

    @table.setter
    def table(self, name: str):
        self.__table = name

    @property
    def columns(self) -> str:
        return self.__columns

    @columns.setter
    def columns(self, colm: str|tuple) -> str:
        if isinstance(colm, str):
            self.__columns = f"({colm})"
        else:
            self.__columns = str(colm)

    @property
    def filters(self) -> str:
        return self.__filters

    @filters.setter
    def filters(self, filter_expression: str) -> str:
        self.__filters = filter_expression

    def get_query(self, ):
        pass

if __name__ == "__main__":
    add_assets("python_test_01")
    # with OpenDB() as database:
    #     _select = CRUD.get_query_select(table="assets")
    #     database.cursor.execute(_select)
    #     print(database.cursor.fetchall())