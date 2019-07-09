import mysql.connector
from mysql.connector import Error

connection = mysql.connector.connect(host = 'localhost',
                                     user = 'root', password = 'rohitkauri123')

mycursor = connection.cursor()
mycursor.execute("SHOW DATABASES LIKE 'minor_project';")
myresult = mycursor.fetchall()
if not len(myresult) == 0:
    database_name = myresult[0][0]
    print(database_name)
    new_connection = mysql.connector.connect(host = 'localhost', database = database_name,
                                             user = 'root', password = 'rohitkauri123')
else:
    mycursor.execute("CREATE DATABASE minor_project;")
    new_connection = mysql.connector.connect(host = 'localhost', database = 'minor_project',
                                             user = 'root', password = 'rohitkauri123')
    new_cursor = new_connection.cursor()
    new_cursor.execute("CREATE TABLE transmitter1 (SN int(255) auto_increment primary key, sensor1 int(255), sensor2 int(255), sensor3 int(255), sensor4 int(255));")
    new_cursor.execute("CREATE TABLE transmitter2 (SN int(255) auto_increment primary key, sensor1 int(255), sensor2 int(255), sensor3 int(255), sensor4 int(255));")
    new_cursor.execute("CREATE TABLE transmitter3 (SN int(255) auto_increment primary key, sensor1 int(255), sensor2 int(255), sensor3 int(255), sensor4 int(255));")



