import mysql.connector
import os.path
from datetime import datetime
import pandas as pd
import numpy as np
now = datetime.now()


date_str = now.strftime("%Y%m%d") #tambah ini di dalam kurung untuk waktu %H:%M:%S")
time_str = now.strftime("%H%M%S")
date_time_str = now.strftime("%Y%m%d%H%M%S")

mydb = mysql.connector.connect(user='root', password='Arcana000-', host='localhost')
mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS isddb")

#Establishing database connection
db = mysql.connector.connect(user='root', password='Arcana000-', host='localhost', database='isddb')

if db.is_connected():
    print("Database is connected\n")

#Creating a cursor object using the cursor() method
cursor = db.cursor()

#Create table with name based on the date the file is created
sql = ("""CREATE TABLE IF NOT EXISTS `""" +"s_"+ "sd" + """` (photo LONGBLOB NOT NULL, time varchar(255), helmet varchar(255), goggles varchar(255), jacket varchar(255), gloves varchar(255), footwear varchar(255));""")
cursor.execute(sql)
print("database is created\n")

def download_images():
    table_name = "s_" + date_str
    suffix3 = ".jpg"
    #"""SELECT * FROM information_schema.tables WHERE table_schema = 'isddb' AND table_name = '{}' LIMIT 1;"""
    check_query = "show tables"
    cursor.execute(check_query)
    table_list = []
    for table in cursor:
        tab = table[0]
        table_list.append(tab)
        
    if table_name not in table_list:
        print('Table not found!')
    else: 
        download_image_query = ("""SELECT photo FROM {}""").format(table_name)
        cursor.execute(download_image_query)

        myResult = cursor.fetchall()
        myRes = myResult[:]

        for myR in myRes:
            myd1 = myR[0]
            # print(myd1)
            global coun
            coun +=1
            StoreFilePath_o = "data/image_files_from_database/" + table_name + "_" + str(coun)
            StoreFilePath = StoreFilePath_o + suffix3

            if os.path.isfile(StoreFilePath_o+suffix3) == True:
                number = 1

                StoreFilePath1 = StoreFilePath_o + "_({})".format(number)
                StoreFilePath = StoreFilePath1 + suffix3

                while os.path.isfile(StoreFilePath) == True:
                    num = int(StoreFilePath[-6])
                    num += 1

                    StoreFilePath2 = StoreFilePath_o + "_({})".format(str(num))
                    StoreFilePath = StoreFilePath2 + suffix3
            else:
                StoreFilePath = StoreFilePath_o + suffix3

            with open(StoreFilePath, "wb") as Fil:
                Fil.write(myd1)

        print("downloaded")
download_images()
# download_images()
