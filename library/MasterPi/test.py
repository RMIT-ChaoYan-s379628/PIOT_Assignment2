import pymysql

connection = pymysql.connect(host='35.244.109.255',
                                 user='root',
                                 password='65390057y',
                                 db='LMS')
with connection.cursor() as cursor:
    cursor.execute("INSERT INTO `LMS`.`LmsUser` (`LmsUserID`, `UserName`, `Name`) VALUES ('1', 'test2', 'test2');")
    connection.commit()
