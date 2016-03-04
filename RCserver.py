import SocketServer
import serial
import getopt
import os
import glob
import socket
import sys
import time
import datetime

class SerialManager():

    def __init__(self):

        self.num_data_vals = 150

        if sys.platform.startswith('win'):
                ports = ['COM' + str(i + 1) for i in range(256)]

        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
                # this is to exclude your current terminal "/dev/tty"
                ports = glob.glob('/dev/ttyACM*')

        elif sys.platform.startswith('darwin'):
                ports = glob.glob('/dev/tty.usb*')

        else:
                raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
                try:
                        s = serial.Serial(port)
                        s.close()
                        result.append(port)
                except (OSError, serial.SerialException):
                        pass

        if len(result) > 1:
                print 'Too many ports to choose from'
                exit(0)
        if len(result) < 1:
                print 'No ports found'
                exit(0)
        if len(result) is 1:
                print 'Found serial port: ', result

        strPort = result[0]
        print 'Found serial port: ', result
        print 'Connecting...'

        try:
                self.ser = serial.Serial(strPort, 9600)
        except:
                print 'Unable to connect to the Arduino via Serial'
                exit(1)

        # wait for port to open
        while self.ser.isOpen() == 0:
                print '...'
                time.sleep(1)
        time.sleep(2)

        print 'Connected!'

    def startDataCapture(self):
        print 'starting data capture'
        #send begin packet
        #print 'sending begin packet'
        self.ser.write("ready\n")  

        s1 = []
        s2 = []
        s3 = []
        s4 = []
        s5 = []
        s6 = []
        s7 = []
        s8 = []

        #read 300 values of each sensor
        i = 0
        while(i < self.num_data_vals):
                if (i % 20) == 0:
                        print '.'
                
                try:
                        line = self.ser.readline()
                        data = [int(val) for val in line.split()]
                        if(len(data) == 8):
                                s1.append(data[0])
                                s2.append(data[1])
                                s3.append(data[2])
                                s4.append(data[3])
                                s5.append(data[4])
                                s6.append(data[5])
                                s7.append(data[6])
                                s8.append(data[7])
                                i += 1
                        #else:
                        #	print 'bad data'
                except:
                        print 'Unable to read data from serial'

        self.ser.write("stop\n")  
        print 'values:'
        print sum(s1)/len(s1)
        print sum(s2)/len(s2)
        print sum(s3)/len(s3)
        print sum(s4)/len(s4)
        print sum(s5)/len(s5)
        print sum(s6)/len(s6)
        print sum(s7)/len(s7)
        print sum(s8)/len(s8)

        #save data to file
        #write to file
        ts = time.time()
        filename = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

        f = open(os.path.join(currentDir, filename), 'w')

        for i in range(0, self.num_data_vals):
            f.write(str(s1[i]))
            f.write(' ')
            f.write(str(s2[i]))
            f.write(' ')
            f.write(str(s3[i]))
            f.write(' ')
            f.write(str(s4[i]))
            f.write(' ')
            f.write(str(s5[i]))
            f.write(' ')
            f.write(str(s6[i]))
            f.write(' ')
            f.write(str(s7[i]))
            f.write(' ')
            f.write(str(s8[i]))
            f.write('\n')
        f.close()

    #def stopDataCapture(self):
        #print 'stopping data capture'

class MyUDPHandler(SocketServer.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """

    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        print "{} wrote:".format(self.client_address[0])
        print data

        global newgest
        global currentGesture
        global currentDir
        if newgest is True:
            currentGesture = data
            currentDir = os.path.join(trainingDir, currentGesture)
            if not os.path.exists(currentDir):
                os.makedirs(currentDir)
            newgest = False
        else:
            if data == "start":
                SM.startDataCapture()
            #if data == "stop":
                #SM.stopDataCapture()
            if data == "exit":
                SM.ser.close()
                #self.server_close()
                #self.shutdown()
                #self.interrupt_main()
                #raise KeyboardInterrupt
            if data == "new":
               # new gesture incoming, set flag
               newgest = True
               
# set filepath and create if necessary 



        #socket.sendto(data.upper(), self.client_address)

if __name__ == "__main__":

    newgest = False
    
    trainingDir = 'TrainingData'
    currentGesture = ''
    currentDir = ''
    
    try:
        trainingDir = sys.argv[1]
    except:
        print 'Using directory "./TrainingData/"'

    if not os.path.exists(trainingDir):
        os.makedirs(trainingDir)


    SM = SerialManager()
   #SM.ser.write("ready\n")

    HOST, PORT = "127.0.0.1", 45454
    server = SocketServer.UDPServer((HOST, PORT), MyUDPHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()


