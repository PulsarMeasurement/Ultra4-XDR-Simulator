import csv
import serial
import sys
ser2 = serial.Serial( port='COM11', baudrate=19200,  parity=serial.PARITY_NONE,  stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS,timeout=100)


def gotoRunMode():
    print("Going to Run Mode ")
    txString = "/ACCESS:OFF" + '\n\r'
    ser2.write(txString.encode())
    x = ser2.readline()
    print(x.decode())

def gotoProgMode():
    print("Going to Prog Mode ")
    txString = "/ACCESS:552621" + '\n\r'
    ser2.write(txString.encode())
    x = ser2.readline()
    print(x.decode())

def sendValuesFromCsv():
    with open('U5_Advanced_Efficiency_params.csv') as csvFile:
        # csvFile.seek(15)
        readFile = csv.reader(csvFile,delimiter=',')
        for row in readFile:
            temp = list(row)
            txString = "/P%s:%s\r\n" % (temp[0],temp[1])
            print(txString)
            ser2.write(txString.encode())
            x = ser2.readline()
            print(x.decode())


def main():
    gotoProgMode()
    sendValuesFromCsv()


main()