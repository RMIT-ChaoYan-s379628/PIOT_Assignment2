import pymysql

connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='65390057y',
                                 db='library')
with connection.cursor() as cursor:
    cursor.execute("UPDATE `library`.`Users` SET `UserPassword` = '13' WHERE (`UserId` = 'test')")
    res=connection.affected_rows()
    print(res)