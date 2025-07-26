import pymysql

conn = pymysql.connect(
    host='172.30.1.63',
    port=3306,
    user='root',
    password='1523',
    db='texture_library',
    charset='utf8'
)

cursor = conn.cursor()
cursor.execute(
    'DESC assets',
)
print(cursor.fetchall())
