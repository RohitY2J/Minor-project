import serial
import tkinter as tk
import time
import csv
import matplotlib
matplotlib.use("tkAgg")
import matplotlib.pyplot as plt
import numpy as np



#np.zeros creates 20 0 vector.
y_var = np.array(np.zeros([20]))
fig = ""
ax = ""
line =""
times = 1
arr = []
ser = ""


def serial_read(port_num, baud_rate):
    try:
        global ser
        ser = serial.Serial()
        ser.baudrate = baud_rate
        ser.port = port_num
        ser.port : port_num
        ser.open()
        root.after(1, serial_read2)
            
    except:
        print("Keyboard InterruptXX")
        ser.close()

   

def serial_read2():
    try:
        global y_var, arr, fig, ax, line, times
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
        root.after(1, serial_read2)
    except:
    	print("Keyboard Interrupt")
    	ser.close()
    	root.destroy()
    	main()

'''if __name__ == '__main__':
    root = tk.Tk(screenName="Serial data Read",  baseName="What is this??",  useTk=1)          
    root.title('Serial Data!')
    root.geometry('500x400') # Size 200, 200
    root.resizable(False, False) #dont resize the window
    x = 1
    plt.ion()
    fig, ax = plt.subplots()
    line, = ax.plot(y_var)
    root.after(1, serial_read('COM11', 9600))
    print(x)
    root.mainloop()
    '''

def serial_read_main(window, port_num, baud_rate):
    root = tk.Tk(screenName="Serial data Read",  baseName="What is this??",  useTk=1)          
    root.title('Serial Data!')
    root.geometry('500x400') # Size 200, 200
    root.resizable(False, False) #dont resize the window
    root.after(1, serial_read('COM11', 9600))
    plt.ion()
    fig, ax = plt.subplots()
    line, = ax.plot(y_var)
    print(port_num)
    print(type(port_num))
    print(baud_rate)
    print(type(baud_rate))
    root.mainloop()

