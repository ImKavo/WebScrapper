from db_config import host, user, password, db_name
import mysql.connector

try:
    mydb = mysql.connector.connect(
        host=host,
        user=user,
        passwd=password,
        database=db_name
    )
    print('MySQL: Successfully connected!')
    print('#' * 20)
    mycursor = mydb.cursor()
    sql = "INSERT INTO test_3 (id, name, password) VALUES (%s, %s, %s)"
    val = ("1", "max", "12345")
    mycursor.execute(sql, val)

    mydb.commit()
    # myresult = mycursor.fetchall()

    # for x in myresult:
    #     print(x)
    # print(myresult)
except Exception as ex:
    print('MySQL: Connection refused...')
    print(ex)
