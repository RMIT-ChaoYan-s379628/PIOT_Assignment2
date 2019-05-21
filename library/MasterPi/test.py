import pymysql

connection = pymysql.connect(host='35.244.109.255',
                                 user='root',
                                 password='65390057y',
                                 db='LMS')
with connection.cursor() as cursor:
    cursor.execute("select * from Book;")
    row=cursor.fetchall()
    for item in row:
        print(item[1])
    connection.commit()
