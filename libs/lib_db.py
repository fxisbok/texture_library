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

if __name__ == "__main__":
    with OpenDB() as database:
        database.cursor.execute('DESC assets')
        print(database.cursor.fetchall())