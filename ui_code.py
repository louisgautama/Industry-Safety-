#Import libraries
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from PyQt5.uic import loadUi

from datetime import datetime
import mysql.connector
import pandas as pd
import os.path

#Creating variables
now = datetime.now()
date_str = now.strftime("%Y%m%d") 
date_str2 = now.strftime("%d/%m/%Y") 
passwrd_correct = False
csv_pass_correct = False
image_pass_correct = False
date_picked = False
count = 0

class Connect(QInputDialog):
    #Initialization
    def __init__(self):
        super(Connect,self).__init__()
                
    #Connecting to database
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
    #Initialization
    def __init__(self):
        super(ISDetection,self).__init__()
        self.w = None
        self.ui = uic.loadUi('ISD.ui',self)
        self.ui.closeEvent = self.closeEvent
        self.ui.downloadCsv.clicked.connect(self.download_csv)
        self.ui.downloadImages.clicked.connect(self.download_images)
        self.ui.StopScan.clicked.connect(self.stop_webcam)
        self.ui.DateLabel_2.setText(date_str2)
        self.ui.logFill.setText("Initializing...")        
        self.ui.logDownloaded.setText(" ")     

    #Pop-up message before quitting the system  
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
            "Are you sure you want to quit?", QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
            sys.exit()
        else:
            event.ignore()

    #Closes the window and stops the system
    def stop_webcam(self):
        reply = QMessageBox.question(self, 'Message',
            "Are you sure you want to quit?", QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            sys.exit()
        else:
            return

    #Display the detection screen on GUI
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

        #Prompts input dialog to input password before downloading
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

        self.logDownloaded.setText("Downloading csv file")

        #Pick the date of the table to be downloaded
        date = self.date_picker()
        table_name = "s_" + date
        suffix2 = ".csv"
        check_query = "show tables"
        cursor.execute(check_query)

        #Check if table exists
        table_list = []
        for table in cursor:
            tab = table[0]
            table_list.append(tab)
            
        if table_name not in table_list:
            self.logDownloaded.setText('Table not found!')

        #Downloading csv
        else: 
            #Getting data from database
            download_query = ("""select time, helmet, goggles, jacket, gloves, footwear from {}""").format(table_name)
            cursor.execute(download_query)

            myallData = cursor.fetchall()

            all_time = []
            all_helmet = []
            all_goggles = []
            all_jacket = []
            all_gloves = []
            all_footwear = []

            for time, helmet, goggles, jacket, gloves, footwear in myallData:
                all_time.append(time)
                all_helmet.append(helmet)
                all_goggles.append(goggles)
                all_jacket.append(jacket)
                all_gloves.append(gloves)
                all_footwear.append(footwear)

            dic = {'Time' : all_time, 'Helmet' : all_helmet, 'Goggles': all_goggles, 'Jacket': all_jacket, 'Gloves':all_gloves, 'Footwear': all_footwear}
            df = pd.DataFrame(dic)
            download_path_o = 'data/csv_files/{}'.format(table_name)
            suffix2 = ".csv"

            #Create a new file if file with same name exists when downloading
            if os.path.isfile(download_path_o+suffix2) == True:
                number = 1
            
                download_path1 = download_path_o + "_({})".format(number)
                download_path = download_path1 + suffix2
                while os.path.isfile(download_path) == True:
                    download_path1 = download_path.split("(")
                    download_path2 = download_path1[1]
                    download_path3 = int(download_path2[0:-5])
                    download_path3+=1
                    download_path3 = (str(download_path3))
                    download_path1[1] ="("+download_path3+")"
                    download_path1 = ''.join(download_path1)
                    
                    download_path = download_path1 + suffix2
            else:
                download_path = download_path_o + suffix2

            #Downloads the csv file
            df_csv = df.to_csv(download_path)
            self.logDownloaded.setText("Downloaded csv file")
            csv_pass_correct = False

    #Download images of detection
    def download_images(self):
        global image_pass_correct
        db = mysql.connector.connect(user='root', password=passwrd, host='localhost', database='isddb')
        cursor = db.cursor()
        dialog_text = "Input database password: "

        #Prompts input dialog to input password before downloading
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
        
        self.logFill.setText("Downloading images")
        
        #Pick the date of the table to be downloaded
        date = self.date_picker()
        table_name = "s_" + date
        suffix3 = ".jpg"

        #Check if table exists
        check_query = "show tables"
        cursor.execute(check_query)
        table_list = []
        for table in cursor:
            tab = table[0]
            table_list.append(tab)
            
        if table_name not in table_list:
            self.logDownloaded.setText('Images not found!\n')

        #Downloading images
        else: 
            #Getting data from database
            download_image_query = ("""SELECT photo FROM {}""").format(table_name)
            cursor.execute(download_image_query)

            myResult = cursor.fetchall()
            myRes = myResult[:]

            for myR in myRes:
                myd1 = myR[0]
                global count
                count +=1
                StoreFilePath_o = "data/image_files_from_database/" + table_name + "_" + str(count)
                StoreFilePath = StoreFilePath_o + suffix3

                #Create a new file if file with same name exists when downloading
                if os.path.isfile(StoreFilePath_o+suffix3) == True:
                    number = 1
                
                    StoreFilePath1 = StoreFilePath_o + "_({})".format(number)
                    StoreFilePath = StoreFilePath1 + suffix3
                    while os.path.isfile(StoreFilePath) == True:
                        StoreFilePath1 = StoreFilePath.split("(")
                        StoreFilePath2 = StoreFilePath1[1]
                        StoreFilePath3 = int(StoreFilePath2[0:-5])
                        StoreFilePath3+=1
                        StoreFilePath3 = (str(StoreFilePath3))
                        StoreFilePath1[1] ="("+StoreFilePath3+")"
                        StoreFilePath1 = ''.join(StoreFilePath1)
                        
                        StoreFilePath = StoreFilePath1 + suffix3
                else:
                    StoreFilePath = StoreFilePath_o + suffix3

                #Downloads the imagaes
                with open(StoreFilePath, "wb") as Fil:
                    Fil.write(myd1)

            self.logDownloaded.setText("Images Downloaded")
            image_pass_correct = False
    
    #Date picker to pick the date of the dataset to be downloaded
    def date_picker(self):

        #Returns picked date
        def date_method():
            # getting the date
            value = date.date()
            value = value.toString('yyyyMMdd')
            return value   

        #Creating date picker window frame
        dlg = QDialog(self)
        dlg.setWindowTitle("Date Pick")
        dlg.layout = QVBoxLayout()
        message = QLabel("Pick a date: ")
        dlg.layout.addWidget(message)        
        dlg.setLayout(dlg.layout)
        date = QtWidgets.QDateEdit(dlg, calendarPopup = True)
        date.setGeometry(100, 100, 150, 40)

        #Setting default time to current day
        date.setDateTime(QtCore.QDateTime.currentDateTime())

        #Formatting date
        date.setDisplayFormat("dd MMM yyyy")

        #Showing date picker window frame
        dlg.layout.addWidget(date)
        date.show()
        dlg.exec()

        #Returns picked date
        val = date_method()
        return val