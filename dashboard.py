#Importing libraries
import matplotlib.pyplot as plt
import mysql.connector

#Create Dashboard
def dash():
        #Connecting to database
        mydb = mysql.connector.connect(user='root', password="Arcana000-", host='localhost', database='isddb')
        mycursor = mydb.cursor()
        check_query = "show tables"
        mycursor.execute(check_query)

        #Gathering the table names in database
        table_list = []
        for table in mycursor:
            tab = table[0]
            table_list.append(tab)

        table_name_axis = []
        avg_helmet_line = []
        avg_goggles_line = []
        avg_jacket_line = []
        avg_gloves_line = []
        avg_footwear_line = []

        #Extractind data from database
        for tables in table_list:
            table_name_axis.append(tables)
            download_query = ("""select time, helmet, goggles, jacket, gloves, footwear from {}""").format(tables)
            
            mycursor.execute(download_query)

            myallData = mycursor.fetchall()

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

            coun_helmet, coun_goggles, coun_jacket, coun_gloves, coun_footwear = 0, 0, 0, 0, 0
            total_helmet, total_goggles, total_jacket, total_gloves, total_footwear = 0, 0, 0, 0, 0

            #Calculating average of classes in each table
            for i in all_helmet:
                if i != '0':
                    coun_helmet +=1
                    total_helmet = total_helmet + float(i)

            for i in all_goggles:
                if i != '0':
                    coun_goggles +=1
                    total_goggles = total_goggles + float(i)
                    
            for i in all_jacket:
                if i != '0':
                    coun_jacket +=1
                    total_jacket = total_jacket + float(i)

            for i in all_gloves:
                if i != '0':
                    coun_gloves +=1
                    total_gloves = total_gloves + float(i)

            for i in all_footwear:
                if i != '0':
                    coun_footwear +=1
                    total_footwear = total_footwear + float(i)

            avg_helmet = (total_helmet/coun_helmet) if coun_helmet != 0 else 0
            avg_goggles = (total_goggles/coun_goggles) if coun_goggles != 0 else 0
            avg_jacket = (total_jacket/coun_jacket) if coun_jacket != 0 else 0
            avg_gloves = (total_gloves/coun_gloves) if coun_gloves != 0 else 0
            avg_footwear = (total_footwear/coun_footwear) if coun_footwear != 0 else 0

            avg_helmet_line.append(avg_helmet)
            avg_goggles_line.append(avg_goggles)
            avg_jacket_line.append(avg_jacket)
            avg_gloves_line.append(avg_gloves)
            avg_footwear_line.append(avg_footwear)

        #Plotting the graph
        plt.plot(table_list, avg_helmet_line, label = "Helmet Accuracy")
        plt.plot(table_list, avg_goggles_line, label = "Goggles Accuracy")
        plt.plot(table_list, avg_jacket_line, label = "Jacket Accuracy")
        plt.plot(table_list, avg_gloves_line, label = "Gloves Accuracy")
        plt.plot(table_list, avg_footwear_line, label = "Footwear Accuracy")
        
        #Showing graph
        plt.legend()
        plt.show()

#Calling function
dash()