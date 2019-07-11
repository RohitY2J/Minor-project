def display(data):
    data_int = int(data)
    i = 4
    while(data_int > 0):
        if (data_int % 10) == 1:
            print(i)
        i = i-1
        data_int = int(data_int / 10)

if __name__ == '__main__':
    data = input("Enter the number: ")
    display(data)


