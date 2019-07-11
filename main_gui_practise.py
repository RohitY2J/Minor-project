import tkinter as tk           #importing tkinter
import tkinter.font as font
from PIL import ImageTk, Image
import os
from datas import database
from tkinter import Menu

import serial
import time
import csv
import matplotlib
matplotlib.use("tkAgg")
import matplotlib.pyplot as plt
import numpy as np
import mysql.connector
from mysql.connector import Error

y_var = np.array(np.zeros([20]))
fig = ""
ax = ""0
line = ""
times = 1
arr = []
ser = ""
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

def insert_into_database(arr):
    global new_connection
    new_cursor = new_connection.cursor()
    try:
        val = int(arr[0])
        bin_data = str(bin(int(arr[0])))
        combination = int(bin_data[slice(2,6)])
    except:
        print("Not a number")
        return
    if val > 15:
        print("Value out of range")
        return
    print('Combination: '+str(combination))
    length = len(arr)
    index = []
    i = 4
    
    while combination > 0:
        if (combination % 10) == 1:
            index.append(i)
            print("Appended "+str(i))
        i = i-1
        combination = int(combination / 10)

    i = 0
    columns = ""
    data_value = ""
    values = []
    
    if len(index) > 0: 
        columns = "sensor"+str(index[len(index)-i-1])
        data_value = "%s"
        values.append(int(arr[i+1]))
    i = i + 1

    while i < len(index):
        x = ",sensor"+str(index[len(index)-i-1])
        columns = columns+x
        data_value = data_value + "," + "%s"
        values.append(int(arr[i+1]))
        i = i + 1
    sql = "INSERT INTO transmitter1("+columns+") values("+data_value+")"
    sql1 = "INSERT INTO minor_project.transmitter1(sensor1) values(%s)"
    new_cursor.execute(sql,tuple(values))
    new_connection.commit()
    print("Columns:" + columns)
    print("Data: " +  data_value)
    print("Sql: "+ sql)
    print("Values: "+ str(values))
                       
                
def serial_read(root,port_num, baud_rate):
    global ser
    ser = serial.Serial()
    ser.baudrate = baud_rate
    ser.port = port_num
    ser.port : port_num
    ser.open()
    root.after(2, serial_read2(root))

def serial_read2(root):
    global y_var, arr, fig, ax, line, times, ser
    '''ser_bytes = ser.readline()
    decoded_bytes = ser_bytes.decode('utf-8')
    print("\n"+str(decoded_bytes))
    arr.append(decoded_bytes)
    print(len(arr))  
    print("============="+str(times))
    if len(arr) == 5:
        insert_into_database(arr)
        y_var = np.append(y_var,int(arr[2]))
        y_var = y_var[1:20+1]
        line.set_ydata(y_var)
        ax.relim()
        ax.autoscale_view()
        fig.canvas.draw()
        fig.canvas.flush_events()
        arr = []
        times = times + 1
    root.after(1, serial_read2(root))
    '''
    try:
        ser_bytes = ser.readline()
        decoded_bytes = ser_bytes.decode('utf-8')
        print("\n"+str(decoded_bytes))
        arr.append(decoded_bytes)
        print(len(arr))  
        print("============="+str(times))
        if len(arr) == 5:
            insert_into_database(arr) 
            y_var = np.append(y_var,int(arr[2]))
            y_var = y_var[1:20+1]
            line.set_ydata(y_var)
            ax.relim()
            ax.autoscale_view()
            fig.canvas.draw()
            fig.canvas.flush_events()
            arr = []
            times = times + 1
        root.after(1, serial_read2(root))
    except:
    	print("Keyboard Interrupt")
    	y_var = np.array(np.zeros([20]))
    	fig = ""
    	ax = ""
    	line =""
    	times = 1
    	arr = []
    	ser = ""
	

def open_data(window):
    database(window)

def donothing():
    return

#start reading the data from serial port
def read(window,port_num, baud_rate):
    global fig, ax, line
    y_var = np.array(np.zeros([20]))
    plt.ion()
    fig, ax = plt.subplots()
    line, = ax.plot(y_var)
    serial_read(window,port_num, baud_rate) #read the data



def main_read(win):
    win.destroy()
    #window description    
    window = tk.Tk(screenName="Main",  baseName="What is this??",  useTk=1)          
    window.title('Telemetry!')
    window.geometry('500x300') # Size 200, 200
    window.resizable(False, False) #dont resize the window

    #creating menubar
    menubar = Menu(window)
    filemenu = Menu(menubar, tearoff=0)
    #add submenu
    filemenu.add_command(label="New", command=donothing)
    filemenu.add_command(label="Open", command=donothing)
    filemenu.add_command(label="Save", command=donothing)
    menubar.add_cascade(label="File", menu=filemenu) #add the menu
    #action submenu
    action_menu = Menu(menubar, tearoff=0)
    action_menu.add_command(label="Read", command= lambda: main_read(window))
    action_menu.add_command(label="Show database", command= lambda: main_database(window))
    menubar.add_cascade(label="Action", menu=action_menu) 

    img = ImageTk.PhotoImage(Image.open("dave_80.jpg")) #icon image
    panel = tk.Label(window, image = img) #set the image
    panel.place(relx = 0.44, rely = 0.1)

    #label and entry defining
    port_num = tk.Label(window, text="Port Number")
    port_num.place(relx = 0.05, rely = 0.42)
    port_num_entry = tk.Entry(window, width = 29)
    port_num_entry.place(relx=0.3, rely=0.42)

    baud_rate_label = tk.Label(window, text="Baudrate")
    baud_rate_label.place(relx = 0.05, rely = 0.52)
    baud_rate_entry = tk.Entry(window, width = 29)
    baud_rate_entry.place(relx=0.3, rely=0.52)

    #button defining
    button_read = tk.Button(window, text = "Read", width = 25, bg = 'green', command = lambda: read(window,port_num_entry.get(),baud_rate_entry.get()))
    button_read.place(relx = 0.25, rely = 0.65)
    button_stop = tk.Button(window, text='Stop', width=25, bg = 'green',command=window.destroy)
    button_stop.place(relx=0.25, rely=0.78)

    #defining the font of the button and label
    myFont = font.Font(family='Helvetica', size=10, weight='bold')

    button_stop['font'] = myFont
    button_read['font'] = myFont
    port_num_entry['font'] = myFont
    baud_rate_entry['font'] = myFont

    window.config(menu = menubar)
    window.mainloop()

def main_database(win):
    win.destroy()
    #window description    
    window = tk.Tk(screenName="Main",  baseName="What is this??",  useTk=1)          
    window.title('Telemetry!')
    window.geometry('500x400') # Size 200, 200
    window.resizable(False, False) #dont resize the window

    #creating menubar
    menubar = Menu(window)
    filemenu = Menu(menubar, tearoff=0)
    #add submenu
    filemenu.add_command(label="New", command=donothing)
    filemenu.add_command(label="Open", command=donothing)
    filemenu.add_command(label="Save", command=donothing)
    menubar.add_cascade(label="File", menu=filemenu) #add the menu
    #action submenu
    action_menu = Menu(menubar, tearoff=0)
    action_menu.add_command(label="Read", command= lambda: main_read(window))
    action_menu.add_command(label="Show database", command= lambda: main_database(window))
    menubar.add_cascade(label="Action", menu=action_menu) 

    img = ImageTk.PhotoImage(Image.open("dave_80.jpg")) #icon image
    panel = tk.Label(window, image = img) #set the image
    panel.place(relx = 0.44, rely = 0.1)

    #label and entry defining
    database_hostName = tk.Label(window, text="Database Hostname:")
    database_hostName.place(relx = 0.05, rely = 0.4)
    database_hostName_entry = tk.Entry(window, width = 29)
    database_hostName_entry.place(relx=0.3, rely=0.4)

    database_username_label = tk.Label(window, text="Database Username:")
    database_username_label.place(relx = 0.05, rely = 0.47)
    database_username_entry = tk.Entry(window, width = 29)
    database_username_entry.place(relx=0.3, rely=0.47)

    password_label = tk.Label(window, text = "Database Password:")
    password_label.place(relx = 0.05, rely = 0.54)
    password_entry = tk.Entry(window, width = 29)
    password_entry.place(relx = 0.3, rely = 0.54)
    
    date_label = tk.Label(window, text = "Enter date:")
    date_label.place(relx = 0.05, rely = 0.61)
    date_entry = tk.Entry(window, width = 29)
    date_entry.place(relx = 0.3, rely = 0.61)

    #button defining
    button_show_data = tk.Button(window, text='Show data', width=25, bg = 'green',command = lambda: open_data(window))
    button_show_data.place(relx=0.25, rely=0.69)
    button_stop = tk.Button(window, text='Stop', width=25, bg = 'green',command=window.destroy)
    button_stop.place(relx=0.25, rely=0.78)

    #defining the font of the button and label
    myFont = font.Font(family='Helvetica', size=10, weight='bold')

    button_stop['font'] = myFont
    
    button_show_data['font'] = myFont
    database_hostName_entry['font'] = myFont
    database_username_entry['font'] = myFont
    password_entry['font'] = myFont
    date_entry['font'] = myFont

    window.config(menu = menubar)
    window.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    main_database(root)
