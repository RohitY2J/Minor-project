import tkinter as tk
import mysql.connector
from mysql.connector import Error
import tkinter.font as font
import csv

def write_to_csv(myresult, col_names):
    myresult.insert(0, col_names)
    
    with open('data.csv', 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(myresult)
    writeFile.close()

def return_to_main():
    return

def database(window):
    win = tk.Tk()
    #heading names for database columns
    col_names = ("Sensor 1","Sensor 2","Sensor 3","Sensor 4","Sensor 5","Sensor 6") 
    row = 0  #to keep track of the rows
    
    win.title("Datas from the database")
    window.destroy()   #destroying previous window
    myFont = font.Font(win, family='Helvetica', size=10, weight='bold')
    
    heading = tk.Label(win, text = "Database data") #heading text
    heading.grid(row = 0,column = 2)
    heading['font'] = myFont

    blank = tk.Label(win, text = "") #leave one row
    blank.grid(row = 1,column = 1)

    try:
        #try to develop connection
        connection = mysql.connector.connect(host = 'localhost', database = 'giraffe',
                                             user = 'root', password = 'rohitkauri123')
        if connection.is_connected():
            db_Info = connection.get_server_info() #get the information about the db
            print("Connected to mysql database with version ",db_Info)
            cursor = connection.cursor() #defining cursor object
            cursor.execute("Select * from giraffe.tickets;")
            myresult = cursor.fetchall() #fetch the returned data;
            
            height = len(myresult)+1  #number of rows + heading
            width = len(myresult[0]) #number of columns
            for i in range(height): #Rows
                for j in range(width): #Columns
                    if i == 0:
                        # for putting headings
                        b = tk.Label(win, text=col_names[j],
                                     fg = "light green",
                                     bg = "dark green",
                                     width = 20)
                        b.grid(row=i+2, column=j)
                    else:
                        #copying data from database to table
                        b = tk.Label(win, text=myresult[i-1][j], width = 20)
                        b.grid(row=i+2, column=j)
                row = i+3 #next row
            blank2 = tk.Label(win, text = "") #leave one row
            blank2.grid(row = row, column = 0)
            row = row+1
            #button to save the table to csv
            save = tk.Button(win, text = "Save to csv", bg = 'green', command = lambda: write_to_csv(myresult, col_names), width = 15)
            save.grid(row = row, column =4)
            
            #button to return
            returnn = tk.Button(win,text = "Return", bg = 'green', command = return_to_main, width = 15)
            returnn.grid(row = row, column = 5)
            

    except Error as e:
        print("Error while connecting to MYSQL",e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MYSQL is disconnected")

    
    win.mainloop()

if __name__ == '__main__':
    database(tk.Tk())
