from datetime import datetime
import mysql.connector

now = datetime.now()
date_time_str = now.strftime("%Y%m%d") #tambah ini di dalam kurung untuk waktu %H:%M:%S")

#establishing the connection
db = mysql.connector.connect(user='root', password='Arcana000-', host='localhost', database='isddb')

if db.is_connected():
    print("database connected")

#Creating a cursor object using the cursor() method
cursor = db.cursor()

#create table with name based on the date the file is created
sql = ("""CREATE TABLE IF NOT EXISTS `""" +"s_"+ date_time_str + """` (ala varchar(255), asdk varchar(255));""") #, strikeprice int, put_ask float
cursor.execute(sql)

## defining the Query
query = ("""INSERT INTO `"""+ "s_" + date_time_str + """`(ala, asdk) VALUES (%s, %s);""")
## storing values in a variable
values = ("Hafeez", "hafeez")

## executing the query with values
cursor.execute(query, values)

## to make final output we have to run the 'commit()' method of the database object
db.commit()

print(cursor.rowcount, "record inserted")
