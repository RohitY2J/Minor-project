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

y_var = np.array(np.zeros([20]))
fig = ""
ax = ""
line =""
times = 1
arr = []
ser = ""

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
    try:
        ser_bytes = ser.readline()
        decoded_bytes = ser_bytes.decode('utf-8')
        print("\n"+str(decoded_bytes))
        arr.append(decoded_bytes)
        print(len(arr))  
        print("============="+str(times))
        if len(arr) == 5:
            print(type(arr[2]))
            print("Data needed:"+str(arr[2]))
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

#main function
def main():
    #window description    
    window = tk.Tk(screenName="Main",  baseName="What is this??",  useTk=1)          
    window.title('Hello, Tkinter!')
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
    action_menu.add_command(label="Read", command=donothing)
    action_menu.add_command(label="Show database", command=donothing)
    menubar.add_cascade(label="Action", menu=action_menu) 

    img = ImageTk.PhotoImage(Image.open("dave.jpg")) #icon image
    panel = tk.Label(window, image = img) #set the image
    panel.place(relx = 0.44, rely = 0.1)

    #label and entry defining
    port_number_label = tk.Label(window, text="Port Number")
    port_number_label.place(relx = 0.05, rely = 0.4)
    port_number_entry = tk.Entry(window, width = 29)
    port_number_entry.place(relx=0.3, rely=0.4)

    baudrate_label = tk.Label(window, text="Baudrate")
    baudrate_label.place(relx = 0.05, rely = 0.47)
    baudrate_entry = tk.Entry(window, width = 29)
    baudrate_entry.place(relx=0.3, rely=0.47)

    date_label = tk.Label(window, text = "Enter date:")
    date_label.place(relx = 0.05, rely = 0.54)
    date_entry = tk.Entry(window, width = 29)
    date_entry.place(relx = 0.3, rely = 0.54)

    #button defining
    button_read = tk.Button(window, text = "Read", width = 25, bg = 'green', command = lambda: read(window,port_number_entry.get(),baudrate_entry.get()))
    button_read.place(relx = 0.25, rely = 0.63)
    button_show_data = tk.Button(window, text='Show data', width=25, bg = 'green',command = lambda: open_data(window))
    button_show_data.place(relx=0.25, rely=0.72)
    button_stop = tk.Button(window, text='Stop', width=25, bg = 'green',command=window.destroy)
    button_stop.place(relx=0.25, rely=0.81)

    #defining the font of the button and label
    myFont = font.Font(family='Helvetica', size=10, weight='bold')

    button_stop['font'] = myFont
    button_read['font'] = myFont
    button_show_data['font'] = myFont
    port_number_entry['font'] = myFont
    baudrate_entry['font'] = myFont
    date_entry['font'] = myFont

    window.config(menu = menubar)
    window.mainloop()   

if __name__ == "__main__":
    main()
