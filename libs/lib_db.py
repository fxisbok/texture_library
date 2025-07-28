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

# CRUD methods
class CRUD:
    class INSERT:
        def __init__(self):
            self.__table = str()
            self.__columns = []  # 컬럼명을 리스트로 관리
            self.__values_placeholders = []  # 값 대신 `%s` 플레이스홀더를 위한 리스트
            self.__actual_values = []  # 실제 값들을 저장할 리스트

        @property
        def prefix(self) -> str:
            return "INSERT INTO"

        @property
        def table(self) -> str:
            return self.__table

        @table.setter
        def table(self, name: str) -> None:
            self.__table = name

        # columns는 이제 tuple이 아닌 list of strings를 받습니다.
        @property
        def columns(self) -> list:
            return self.__columns

        @columns.setter
        def columns(self, colm: str | tuple | list):
            if isinstance(colm, str):
                self.__columns = [colm]
            elif isinstance(colm, (tuple, list)):
                self.__columns = list(colm)
            else:
                raise TypeError("Columns must be a string, tuple, or list of strings.")

            # 컬럼 개수에 맞춰 플레이스홀더 (%s)를 생성합니다.
            self.__values_placeholders = ["%s"] * len(self.__columns)

        # values는 이제 실제 값들을 직접 받습니다.
        @property
        def actual_values(self) -> list:
            return self.__actual_values

        @actual_values.setter
        def actual_values(self, vals: tuple | list) -> None:
            if isinstance(vals, (tuple, list)):
                self.__actual_values = list(vals)
            else:
                # 단일 값이라도 리스트에 담도록 강제
                self.__actual_values = [vals]

            if len(self.__actual_values) != len(self.__columns):
                raise ValueError("Number of values must match the number of columns.")

        # get_query가 이제 쿼리 문자열과 값 튜플을 반환합니다.
        def get_query(self, table: str, columns: str | tuple | list, values: tuple | list) -> tuple[str, tuple]:
            self.table = table
            self.columns = columns  # columns setter가 values_placeholders를 초기화합니다.
            self.actual_values = values  # actual_values setter가 값 개수를 검증합니다.

            columns_str = f"({', '.join(self.__columns)})"
            values_str = f"({', '.join(self.__values_placeholders)})"

            result_query = f"{self.prefix} {self.table}{columns_str} VALUES {values_str}"
            return result_query, tuple(self.__actual_values)


    class SELECT:
        def __init__(self):
            self.__table = str()
            self.__columns = "*"
            self.__where_conditions_str = []  # SQL 조건 문자열 부분 (플레이스홀더 포함)
            self.__where_values = []  # 조건에 바인딩될 실제 값들
            self.__order_by_columns = []
            self.__limit_row = None
            self.__offset_row = None

        @property
        def prefix(self) -> str:
            return "SELECT"

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
        def columns(self, cols: str | tuple | list) -> None:
            if isinstance(cols, str):
                self.__columns = cols
            elif isinstance(cols, (tuple, list)):
                self.__columns = ", ".join(cols)
            else:
                raise TypeError("Columns must be a string, tuple, or list of strings.")

        # where는 이제 (조건 문자열, 값 튜플/리스트)의 리스트를 받습니다.
        # 예: [("column1 = %s", "value1"), ("column2 > %s", 10)]
        @property
        def where_clauses(self) -> list:
            return list(zip(self.__where_conditions_str, self.__where_values))

        @where_clauses.setter
        def where_clauses(self, conditions: list[tuple[str, tuple | list]]) -> None:
            self.__where_conditions_str = []
            self.__where_values = []
            for condition_str, vals in conditions:
                if not isinstance(condition_str, str):
                    raise TypeError("Each condition string must be a string.")
                if not isinstance(vals, (tuple, list)):
                    raise TypeError("Values for conditions must be a tuple or list.")
                self.__where_conditions_str.append(condition_str)
                self.__where_values.extend(vals)

        @property
        def order_by(self) -> list:
            return self.__order_by_columns

        @order_by.setter
        def order_by(self, cols: str | tuple | list) -> None:
            if isinstance(cols, str):
                self.__order_by_columns = [cols]
            elif isinstance(cols, (tuple, list)):
                self.__order_by_columns = list(cols)
            else:
                raise TypeError("Order by columns must be a string, tuple, or list of strings.")

        @property
        def limit(self) -> int | None:
            return self.__limit_row

        @limit.setter
        def limit(self, row_count: int) -> None:
            if not isinstance(row_count, int) or row_count < 0:
                raise ValueError("Limit must be a non-negative integer.")
            self.__limit_row = row_count

        @property
        def offset(self) -> int | None:
            return self.__offset_row

        @offset.setter
        def offset(self, row_offset: int) -> None:
            if not isinstance(row_offset, int) or row_offset < 0:
                raise ValueError("Offset must be a non-negative integer.")
            self.__offset_row = row_offset

        def get_query(self, table: str, columns: str | tuple | list = "*",
                      where: list[tuple[str, tuple | list]] | None = None,  # (조건 문자열, 값) 쌍의 리스트
                      order_by: str | tuple | list | None = None,
                      limit: int | None = None, offset: int | None = None) -> tuple[str, tuple]:

            self.table = table
            self.columns = columns

            if where is not None:
                self.where_clauses = where  # setter 호출

            if order_by is not None:
                self.order_by = order_by
            if limit is not None:
                self.limit = limit
            if offset is not None:
                self.offset = offset

            query_parts = [self.prefix, self.columns, "FROM", self.table]

            if self.__where_conditions_str:
                query_parts.append("WHERE")
                query_parts.append(" AND ".join(self.__where_conditions_str))

            if self.__order_by_columns:
                query_parts.append("ORDER BY")
                query_parts.append(", ".join(self.__order_by_columns))

            if self.__limit_row is not None:
                query_parts.append(f"LIMIT {self.__limit_row}")

            if self.__offset_row is not None:
                query_parts.append(f"OFFSET {self.__offset_row}")

            return " ".join(query_parts), tuple(self.__where_values)


    class UPDATE:
        def __init__(self):
            self.__table = str()
            self.__set_clauses_str = []  # SET 절의 `컬럼 = %s` 문자열 부분
            self.__set_values = []  # SET 절에 바인딩될 실제 값들
            self.__where_conditions_str = []  # WHERE 절 조건 문자열 부분
            self.__where_values = []  # WHERE 절에 바인딩될 실제 값들

        @property
        def prefix(self) -> str:
            return "UPDATE"

        @property
        def table(self) -> str:
            return self.__table

        @table.setter
        def table(self, name: str) -> None:
            self.__table = name

        # set_data는 이제 딕셔너리를 받습니다. (컬럼: 값)
        @property
        def set_data(self) -> dict:
            # 역으로 딕셔너리 형태로 반환하기는 어려우므로, 이 속성은 직접 사용하지 않고 setter만 활용하는 것이 좋습니다.
            # 내부적으로는 self.__set_clauses_str과 self.__set_values를 사용합니다.
            return {}  # 더미 반환

        @set_data.setter
        def set_data(self, data: dict) -> None:
            if not isinstance(data, dict):
                raise TypeError("Set data must be a dictionary (column: value).")
            self.__set_clauses_str = []
            self.__set_values = []
            for col, val in data.items():
                self.__set_clauses_str.append(f"{col} = %s")
                self.__set_values.append(val)

        # where는 SELECT와 동일하게 (조건 문자열, 값 튜플/리스트)의 리스트를 받습니다.
        @property
        def where_clauses(self) -> list:
            return list(zip(self.__where_conditions_str, self.__where_values))

        @where_clauses.setter
        def where_clauses(self, conditions: list[tuple[str, tuple | list]]) -> None:
            self.__where_conditions_str = []
            self.__where_values = []
            for condition_str, vals in conditions:
                if not isinstance(condition_str, str):
                    raise TypeError("Each condition string must be a string.")
                if not isinstance(vals, (tuple, list)):
                    raise TypeError("Values for conditions must be a tuple or list.")
                self.__where_conditions_str.append(condition_str)
                self.__where_values.extend(vals)

        def get_query(self, table: str, set_data: dict,
                      where: list[tuple[str, tuple | list]] | None = None) -> tuple[str, tuple]:

            self.table = table
            self.set_data = set_data  # setter 호출

            if not self.__set_clauses_str:  # set_data가 비어있으면 오류
                raise ValueError("SET data cannot be empty for an UPDATE query.")

            if where is not None:
                self.where_clauses = where  # setter 호출

            query_parts = [self.prefix, self.table, "SET", ", ".join(self.__set_clauses_str)]

            if self.__where_conditions_str:
                query_parts.append("WHERE")
                query_parts.append(" AND ".join(self.__where_conditions_str))

            # SET 값들과 WHERE 값들을 합쳐서 반환
            return " ".join(query_parts), tuple(self.__set_values + self.__where_values)


    class DELETE:
        def __init__(self):
            self.__table = str()
            self.__where_conditions_str = []
            self.__where_values = []

        @property
        def prefix(self) -> str:
            return "DELETE FROM"

        @property
        def table(self) -> str:
            return self.__table

        @table.setter
        def table(self, name: str) -> None:
            self.__table = name

        # where는 SELECT와 동일하게 (조건 문자열, 값 튜플/리스트)의 리스트를 받습니다.
        @property
        def where_clauses(self) -> list:
            return list(zip(self.__where_conditions_str, self.__where_values))

        @where_clauses.setter
        def where_clauses(self, conditions: list[tuple[str, tuple | list]]) -> None:
            self.__where_conditions_str = []
            self.__where_values = []
            for condition_str, vals in conditions:
                if not isinstance(condition_str, str):
                    raise TypeError("Each condition string must be a string.")
                if not isinstance(vals, (tuple, list)):
                    raise TypeError("Values for conditions must be a tuple or list.")
                self.__where_conditions_str.append(condition_str)
                self.__where_values.extend(vals)

        def get_query(self, table: str,
                      where: list[tuple[str, tuple | list]] | None = None) -> tuple[str, tuple]:

            self.table = table

            if where is not None:
                self.where_clauses = where  # setter 호출

            query_parts = [self.prefix, self.table]

            if self.__where_conditions_str:
                query_parts.append("WHERE")
                query_parts.append(" AND ".join(self.__where_conditions_str))

            return " ".join(query_parts), tuple(self.__where_values)



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



if __name__ == "__main__":
    add_assets("python_test_01")
    # with OpenDB() as database:
    #     _select = CRUD.get_query_select(table="assets")
    #     database.cursor.execute(_select)
    #     print(database.cursor.fetchall())