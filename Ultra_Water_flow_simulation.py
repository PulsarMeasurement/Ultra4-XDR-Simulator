import serial
from time import sleep, strftime, time
import logging
import re
# m=10

frmt = logging.Formatter
ser1 = serial.Serial( port='COM13', baudrate=19200,  parity=serial.PARITY_NONE,  stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS,timeout=3)
ser2 = serial.Serial( port='COM11', baudrate=19200,  parity=serial.PARITY_NONE,  stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS,timeout=3)

def parseString(rxData):
    retData = re.sub('\[[^\]]*\]','',rxData)
    print(rxData)
    print(retData)

    return retData

def gotoRunMode():
    print("Going to Run Mode ")
    txString = "/ACCESS:OFF" + '\n\r'
    ser2.write(txString.encode())
    x = ser2.readline()
    x = parseString(x.decode())
    print(x)
    sleep(2)

def gotoProgMode():
    print("Going to Prog Mode ")
    txString = "/ACCESS:552621" + '\n\r'
    ser2.write(txString.encode())
    x = ser2.readline()
    x = parseString(x.decode())
    print(x)
    # sleep(5)

def actualLevel():
    actualLevel = 0

def simWaterFlow(startVal,endVal,upDown):
    with open("log_temp.csv", "a") as log:
        # log.write("Given Distance,XDR Distance, Relay Status\n"))
        # minVal *=abs(upDown)
        # maxVal*=abs(upDown)
        stopPump = 0
        if(startVal<endVal):
            pumpUp = 1
        else:
            pumpUp = 0

        prevPump1Status = checkRelayStatus(0)
        currentVal = float(startVal)
        while(stopPump == 0):
            echoValue = (7299.14 * currentVal) + 24550.3
            print("Simulated Level is: ", '{:.2f}'.format(currentVal))
            # print(x)
            txString = "/NEW_LEVEL:1," +'{:.2f}'.format(echoValue) + '\n\r'
            ser1.write(txString.encode())
            x = ser1.readline()

            sleep(1)
            txString = ("/LEVEL\n\r").encode()
            ser2.write((txString))
            xdrDistance = ser2.readline()
            xdrDistance = parseString(xdrDistance.decode())
            xdrDistance = (xdrDistance).strip()
            print("XDR Distance is; ", xdrDistance)        
            pump1Status = checkRelayStatus(0)
            print("Pump1 ",pump1Status)
            if(pump1Status!= prevPump1Status):
                prevPump1Status = pump1Status
                stopPump = 1
                break
            # log.write("{0},{1},{2},{3},{4},{5},{6}\n".format(strftime("%Y-%m-%d %H:%M:%S"),distance,xdrDistance,relayList[0],relayList[1],relayList[2],relayList[3]))
            # sleep(1)
            currentVal+=upDown
            if(pumpUp == 1 and currentVal > endVal):
                stopPump = 1
            elif(pumpUp == 0 and currentVal<endVal):
                stopPump = 1
            else:
                stopPump = 0






        # for i in range(minVal,maxVal,upDown):

        #     distance = i/(10*abs(upDown))
        #     echoValue = (7299.14 * distance) + 24550.3
        #     txString = "/NEW_LEVEL:1," +'{:.2f}'.format(echoValue) + '\n\r'
        #     ser1.write(txString.encode())
        #     x = ser1.readline()
        #     print("Distance is: ", '{:.2f}'.format(distance))
        #     print(x)
        #     # if(i == minVal):
        #     #     sleep(30)
        #     # else:
        #     sleep(1)
        #     txString = ("/LEVEL\n\r").encode()
        #     ser2.write((txString))
        #     xdrDistance = ser2.readline()
        #     xdrDistance = (xdrDistance.decode()).strip()
        #     print("XDR Distance is; ", xdrDistance)        
        #     # txString = "/REL_STAT\n\r"
        #     # ser1.write(txString.encode())
        #     # relayStatus = ser1.readline()
        #     # relayStatus = (relayStatus.decode()).strip()
        #     # relayList = list(relayStatus)
        #     # relayList = relayList[3:]
        #     pump1Status = checkRelayStatus(0)
        #     print("Pump1 ",pump1Status)
        #     if(pump1Status!= prevPump1Status):
        #         prevPump1Status = pump1Status
        #         break
        #     # log.write("{0},{1},{2},{3},{4},{5},{6}\n".format(strftime("%Y-%m-%d %H:%M:%S"),distance,xdrDistance,relayList[0],relayList[1],relayList[2],relayList[3]))
        #     sleep(1)
        # # return distance

def checkRelayStatus(pumpNumber):
    txString = ("/REL_STAT\n\r").encode()
    ser1.write(txString)
    rxData = ser1.readline()
    # print(rxData)
    relayStatus = (rxData.decode()).strip()
    relayList = list(relayStatus)
    relayList = relayList[3:]
    # print("Relay List: ",relayList)
    # print("pumpNumber is ",pumpNumber)
    print("Relay Status of P",pumpNumber," = ", relayList[pumpNumber])
    sleep(1)
    return int(relayList[pumpNumber])

def getLevel():
    txString = ("/LEVEL\n\r").encode()
    ser2.write((txString))
    xdrDistance = ser2.readline()
    xdrDistance = parseString(xdrDistance.decode())
    xdrDistance = (xdrDistance).strip()
    if(float(xdrDistance)<0.30):
        xdrDistance = 0.30
    if(float(xdrDistance) > 5.5):
        xdrDistance = 5.5
    # print("XDR Distance is; ", xdrDistance)
    return (float(xdrDistance))

def ReadEfficiency():
    txString = ("/P515\n\r").encode()
    ser2.write((txString))
    efficiencyString = ser2.readline()
    efficiencyString = parseString(efficiencyString.decode())
    efficiencyString = efficiencyString.strip()
    print("Efficiency is ", efficiencyString)

def main():

    distance = 3.00
    d2 = 2.5
    gotoRunMode()
    count = 0
    while(1): 
        if(checkRelayStatus(0) == 0):
            # count(30*m,55*m,1)
            print("Counting UP")
            distance = getLevel()
            print("XDR Distance is ", distance)
            s2 = distance + 0.5 
            simWaterFlow(distance,s2,0.02)
            # print("Distance exited is: ",distance)
        else:
            print("Counting DOWN")
            distance = getLevel()
            # sleep(count) #Placed here to simulate reduced efficiecny
            s2 = distance - 0.5
            simWaterFlow(distance,s2,-0.02)

            # count(d2,distance,1,10)
            # print("Distance exited is: /",distance)
    # checkRelayStatus()
        ReadEfficiency()
        count+=1

def keyboardException():
    print("Ctrl-C Pressed")
    gotoProgMode()
    ser2.close()
    sleep(2)

try:
    main()
except KeyboardInterrupt:
    keyboardException()