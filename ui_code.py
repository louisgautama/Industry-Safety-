import sys
import cv2
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QDialog, QInputDialog
from PyQt5.uic import loadUi
import os

from datetime import datetime
import mysql.connector
import pandas as pd
import numpy as np
import os.path

now = datetime.now()
date_str = now.strftime("%Y%m%d") 
date_str2 = now.strftime("%d/%m/%Y") 
print(date_str2)
passwrd_correct = False
csv_pass_correct = False
image_pass_correct = False

coun = 0



class Connect(QInputDialog):
    def __init__(self):
        super(Connect,self).__init__()
                
    
    def conn(self):
        dialog_text = "Input database password: "
        global passwrd_correct
        while passwrd_correct == False:
            try:
                text, ok = self.getText(self, 'Password', dialog_text)
                global passwrd
                passwrd = text
                if ok:
                    mydb = mysql.connector.connect(user='root', password=passwrd, host='localhost')
                    global mycursor
                    mycursor = mydb.cursor()
                    passwrd_correct = True
                else:
                    sys.exit()
            except Exception as e:
                print(e)
                dialog_text = "Wrong Password! Input correct password: "
        
        #Creating database if not exist
        mycursor.execute("CREATE DATABASE IF NOT EXISTS isddb")

        #Establishing database connection
        db = mysql.connector.connect(user='root', password=passwrd, host='localhost', database='isddb')

        if db.is_connected():
            print("Database is connected\n")

        #Creating a cursor object using the cursor() method
        global cursor
        cursor = db.cursor()

        #Create table with name based on the date the file is created
        sql = ("""CREATE TABLE IF NOT EXISTS `""" +"s_"+ date_str + """` (photo LONGBLOB NOT NULL, time varchar(255), helmet varchar(255), goggles varchar(255), jacket varchar(255), gloves varchar(255), footwear varchar(255));""")
        cursor.execute(sql)
        print("Database Table is created\n")
        return passwrd


class ISDetection(QDialog):
    def __init__(self):
        super(ISDetection,self).__init__()
        loadUi('ISD.ui',self)
        self.downloadCsv.clicked.connect(self.download_csv)
        self.downloadImages.clicked.connect(self.download_images)
        self.StopScan.clicked.connect(self.stop_webcam)
        self.DateLabel_2.setText(date_str2)
        self.logFill.setText("Initializing...")

    def stop_webcam(self):
        sys.exit()

    def displayImage(self,im0,window=1):
        qformat=QImage.Format_Indexed8
        if len(im0.shape)==3:
            if im0.shape[2]==4:
                qformat=QImage.Format_RGBA8888
            else:
                qformat=QImage.Format_RGB888

        outImage=QImage(im0,im0.shape[1],im0.shape[0],im0.strides[0],qformat)
        #BGR>>RGB
        outImage=outImage.rgbSwapped()

        if window==2:
            self.processedImgLabel.setPixmap(QPixmap.fromImage(outImage))
            self.processedImgLabel.setScaledContents(True)

    #Download csv of detection data from database
    def download_csv(self):
        self.logFill.setText("Downloading csv")
        global csv_pass_correct
        db = mysql.connector.connect(user='root', password=passwrd, host='localhost', database='isddb')
        cursor = db.cursor()
        dialog_text = "Input database password: "
        while csv_pass_correct == False:
            text, ok = QInputDialog.getText(self, 'Password', dialog_text)
            if ok:
                download_csv_pass = text
                if download_csv_pass == passwrd:
                    csv_pass_correct = True
                else:
                    dialog_text = "Wrong Password! Input correct password: "
            else:
                return
       
        print("Downloading csv file...\n")
        table_name = "s_" + date_str
        suffix2 = ".csv"
        check_query = "show tables"
        cursor.execute(check_query)
        table_list = []
        for table in cursor:
            tab = table[0]
            table_list.append(tab)
            
        if table_name not in table_list:
            print('Table not found!\n')
        else: 
            download_query = ("""select helmet, goggles, jacket, gloves, footwear from {}""").format(table_name)
            cursor.execute(download_query)

            myallData = cursor.fetchall()

            all_helmet = []
            all_goggles = []
            all_jacket = []
            all_gloves = []
            all_footwear = []

            for helmet, goggles, jacket, gloves, footwear in myallData:
                all_helmet.append(helmet)
                all_goggles.append(goggles)
                all_jacket.append(jacket)
                all_gloves.append(gloves)
                all_footwear.append(footwear)

            dic = {'Helmet' : all_helmet, 'Goggles': all_goggles, 'Jacket': all_jacket, 'Gloves':all_gloves, 'Footwear': all_footwear}
            df = pd.DataFrame(dic)
            download_path_o = 'data/csv_files/{}'.format(table_name)
            suffix2 = ".csv"

            if os.path.isfile(download_path_o+suffix2) == True:
                number = 1

                download_path1 = download_path_o + "_({})".format(number)
                download_path = download_path1 + suffix2

                while os.path.isfile(download_path) == True:
                    num = int(download_path[-6])
                    num += 1

                    download_path2 = download_path_o + "_({})".format(str(num))
                    download_path = download_path2 + suffix2
            else:
                download_path = download_path_o + suffix2

            df_csv = df.to_csv(download_path)

            print("Downloaded csv file into data/csv_files folder\n")

            csv_pass_correct = False
            

    #Download images of detection
    def download_images(self):
        self.logFill.setText("Downloading images")
        global image_pass_correct
        db = mysql.connector.connect(user='root', password=passwrd, host='localhost', database='isddb')
        cursor = db.cursor()
        dialog_text = "Input database password: "
        while image_pass_correct == False:
            text, ok = QInputDialog.getText(self, 'Password', dialog_text)
            if ok:
                download_image_pass = text
                if download_image_pass == passwrd:
                    image_pass_correct = True
                else:
                    dialog_text = "Wrong Password! Input correct password: "
            else:
                return
        while image_pass_correct == False:
            download_image_pass = input("Input database password to download images: ")
            if download_image_pass == passwrd:
                image_pass_correct = True
        
        print("Downloading images from database...\n")
        table_name = "s_" + date_str
        suffix3 = ".jpg"
        check_query = "show tables"
        cursor.execute(check_query)
        table_list = []
        for table in cursor:
            tab = table[0]
            table_list.append(tab)
            
        if table_name not in table_list:
            print('Table not found!\n')
        else: 
            download_image_query = ("""SELECT photo FROM {}""").format(table_name)
            cursor.execute(download_image_query)

            myResult = cursor.fetchall()
            myRes = myResult[:]

            for myR in myRes:
                myd1 = myR[0]
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

            print("Downloaded images from database into data\image_files_from_database folder\n")
            image_pass_correct = False