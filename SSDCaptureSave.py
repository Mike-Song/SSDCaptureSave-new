import sys, os
from os import path 
import struct
from socket import *  
import numpy as np
import time
import datetime
import threading
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Ui_SSDCaptureSave import Ui_MainWindow

gSocketHeaderSize = 16
gSocketBodySize = 32 * 1024
gSocketBufSize = gSocketBodySize + gSocketHeaderSize

class UDPSocketClient:
    def __init__(self):
        self.mHost = '192.168.1.6'
        #self.mHost = '127.0.0.1'
        self.mPort = 6000 
        self.mBufSize = gSocketBodySize + gSocketHeaderSize
        self.mAddress = (self.mHost, self.mPort)
        self.mUDPClient = socket(AF_INET, SOCK_DGRAM)
        self.mData = None
        self.mUDPClient.settimeout(5)

    def setBufSize (self,  bufSize):
        self.mBufSize = bufSize
        
    def sendData(self):
        self.mUDPClient.sendto(self.mData,self.mAddress)
        self.mData = None # Clear data after send out

    def receiveData(self):
       self.mData, self.mAddress = self.mUDPClient.recvfrom(gSocketBufSize)
       return self.mData

class SignalThread(threading.Thread):  
    def __init__(self, axes, canvas, fileName, timeout):  
        super(SignalThread, self).__init__()  
        self.axes = axes
        self.canvas = canvas
        self.timeout = timeout 
        self.data = []
        self.stopped = False  
        self.fileName = fileName

    def run(self):  
        def bumatoyuanmaSingle(x):
            if (x > 32767): 
                x = x - 65536 
            return x
              
        def readTxtFile():
            while not self.stopped:
                aiData = []
                aqData = []
                aiFile = open(r'D:\Tasks\Work\SSDCaptureSave\AI-2018-12-08-14-32-35.txt')
                for line in aiFile.readlines(): 
                    aiData.append(int(line))
                
                aqFile = open(r'D:\Tasks\Work\SSDCaptureSave\AQ-2018-12-08-14-32-35.txt')
                for line in aqFile.readlines(): 
                    aqData.append(int(line))

                self.data = combineData(aiData, aqData)
                on_draw(self.axes, self.canvas, self.data)
            
        def readBinFile(datapath):
            if (datapath != None and datapath != ""):
                with open(datapath,'rb') as fileData:
                    while not self.stopped:
                        block = fileData.read(32*1024)
                        if not block:
                            self.stop()
                            break
                            
                        result = parseIQData(block,  False)
                        aiData  = result[0]
                        aqData = result[1]
                        biData  = result[2]
                        bqData = result[3]
                      
                        if( mainWindow.radioButton_CHA.isChecked() == True ):
                            self.data = combineData(aiData, aqData)
                            on_draw(self.axes, self.canvas, self.data)
                        else:
                            self.data = combineData(biData, bqData)
                            on_draw(self.axes, self.canvas, self.data)
            
        def combineData(iData, qData):
             y = []
             for i in range(len(iData)):
               y.append(complex(iData[i],qData[i]))
             yLength = len(y)
             # hanning window
             hanning_window = np.hanning(yLength)
             xf = np.fft.fft(y * hanning_window)
             xf = np.fft.fftshift(abs(xf))
             xf = 20*np.log10(abs(xf)) - 121.5 # -154+35-2.5
             
             skipNum = int(yLength * 100/1500)
             xf = xf[skipNum:yLength-skipNum]
             return xf   

        def get_time_stamp():
            ct = time.time()
            local_time = time.localtime(ct)
            data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
            data_secs = (ct - int(ct)) * 1000
            time_stamp = "%s.%03d" % (data_head, data_secs)
            return time_stamp
            
        def parseIQData(data, withHead):
            if (withHead):
                data = data[40:]                

            # just for testing
            #data = data[40:]
            aiData = []
            aqData = []
            biData = []
            bqData = []
            if (len(data) >= 1024 and len(data) <= 32768):
              # Parse Payload...
                #offsetRegTuple, offsetRegValueTuple, offsetReg, offsetRegValue
                # Save the original payload
                now = datetime.datetime.now()
                currentTime = now.strftime('%Y-%m-%d-%H-%M-%S') 
                ms = get_time_stamp()
                currentTime = currentTime +"-" + ms[-3:]
    #            rawFileName = "RawIQ-" + currentTime + ".dat"
    #            rawFile=open(rawFileName,'wb')
    #            rawFile.write(newdata)
    #            rawFile.close()

               # 32*1024 * 1024bytes,  AIQ/BIQ 4 Byes I Data, 4 Bytes Q data
                times = 0
                for pos in range(0, 32*1024,8):
                    times +=1
                    line = data[pos:pos+8]
                    
                    # 0XFF00, should be unpack one byte by one, 
                    # otherwise, the data will be upack to 0x00FF, 
                    # WE want ti to be still 0XFF00, call ntohs to reverse it
                    if (len(line) == 8):
                        aiData.append(bumatoyuanmaSingle(ntohs(struct.unpack('H',line[0:2])[0])))
                        aqData.append(bumatoyuanmaSingle(ntohs(struct.unpack('H',line[2:4])[0])))
                        biData.append(bumatoyuanmaSingle(ntohs(struct.unpack('H',line[4:6])[0])))
                        bqData.append(bumatoyuanmaSingle(ntohs(struct.unpack('H',line[6:8])[0])))

                # Save the IQ data 
                folderPath = os.path.split(os.path.realpath(__file__))[0]
                aiFileName = folderPath + "\\Data\\AI-" + currentTime + ".txt"
                aqFileName =  folderPath + "\\Data\\AQ-" + currentTime + ".txt"
                biFileName =  folderPath + "\\Data\\BI-" + currentTime + ".txt"   
                bqFileName =  folderPath + "\\Data\\BQ-" + currentTime + ".txt"
                aiFile=open(aiFileName,'w')
                aqFile=open(aqFileName,'w')
                biFile=open(biFileName,'w')
                bqFile=open(bqFileName,'w')
                  
                  # Save the IQ Data
                for i in range(len(aiData)):
                      aiFile.write(str(aiData[i]))
                      aiFile.write('\n');    
                      aqFile.write(str(aqData[i]))
                      aqFile.write('\n')
                      biFile.write(str(biData[i]))
                      biFile.write('\n');    
                      bqFile.write(str(bqData[i]))
                      bqFile.write('\n')

                aiFile.close()
                aqFile.close()
                biFile.close()
                bqFile.close()
            
            return (aiData,aqData,biData,bqData)
        
        def realtimecapture():
          print ("Real Time Capture.......")
          while not self.stopped:
            mainWindow.sendCmdRAW_AD_SAMPLE()
            mainWindow.udpSocketClient.receiveData()

            # Parse Data...
            data = mainWindow.udpSocketClient.mData
            
            print  ("Receive Total Length: ", len(data))
            if data:
              #self.data_shiyu = parseShiyuData(data, True)
              #on_draw(self.axes_shiyu, self.canvas_shiyu, self.data_shiyu)
              
              # Save the data into one folder
              #Save raw data
              folderName = os.path.join(path.dirname(__file__), "Data\\Data-StartTime-" + startTime)
              if (not(os.path.exists(folderName))):
                  os.mkdir(folderName)  
              
              now = datetime.datetime.now()
              currentTime = now.strftime('%Y-%m-%d-%H-%M-%S')
              filename = "Data-" + currentTime + ".txt"
              rawFile=open(folderName + "\\" + filename,'wb')
              rawFile.write(data)
              rawFile.close()
              
              result = parseIQData(data, True)
          
              aiData = result[0]
              aqData = result[1]
              biData = result[2]
              bqData = result[3]
              
              #print (len(aiData))
          
              if( mainWindow.radioButton_CHA_RealTime.isChecked()== True ):
                self.data = combineData(aiData, aqData)
                on_draw(self.axes, self.canvas, self.data)
              else:
                self.data_pinpu = combineData(biData, bqData)
                on_draw(self.axes, self.canvas, self.data)
        
        def readanddraw():
            print ("Read Files to playback...")
            #progressValue = 0
            #readBinFile(r'D:\Tasks\Work\SSDCaptureSave\Data\0_255_83891200285275391_417746534462719.dat')
            readBinFile(self.fileName)
            #readBinFile(r"D:\Tasks\Work\SSDCaptureSave\Data\0_3_196611196611_1966113.dat")
            #readTxtFile()

            self.stop()
#          if not self.stopped:
            #if (self.pinpu):
            # aiData = []
            # aqData = []
            # aiData = readFile("D:\\Tasks\\XY\\UI\\AI-2018-01-22-21-04-40.txt")
            # aqData = readFile("D:\\Tasks\\XY\\UI\\AQ-2018-01-22-21-04-40.txt")
            # #self.data_pinpu = combineData(aiData, aqData)
            # #on_draw(self.axes_pinpu, self.canvas_pinpu, self.data_pinpu)
          
            # # if( self.channelA == True ):
              # # self.data_pinpu = combineData(aiData, aqData)
              # # on_draw(self.axes_pinpu, self.canvas_pinpu, self.data_pinpu)
            # # else:
              # # self.data_shiyu = readFile("D:\\Tasks\\XY\\UI\\AI-2018-01-22-21-04-40.txt")
              # # on_draw(self.axes_shiyu, self.canvas_shiyu, self.data_shiyu)
          
            # time.sleep()

            # biData = []
            # bqData = []
            # biData = readFile("D:\\Tasks\\XY\\UI\\BI-2018-01-22-21-04-40.txt")
            # bqData = readFile("D:\\Tasks\\XY\\UI\\BQ-2018-01-22-21-04-40.txt")
            #self.data_pinpu = combineData(biData, bqData)
            #on_draw(self.axes_pinpu, self.canvas_pinpu, self.data_pinpu)
            
            # if( self.channelA == True ):
              # self.data_pinpu = combineData(biData, bqData)
              # on_draw(self.axes_pinpu, self.canvas_pinpu, self.data_pinpu)
            # else:
            # Iterate all files in currentFolder
            
#              for dirpath, dirnames,  filenames in os.walk(self.currentFolder):
#                for file in filenames:
#                    if not self.stopped:
#                      # find the files and start and end time and also all the files size
#                        filePath = os.path.join(dirpath, file)
#                        self.data = readFile(filePath)
#                        on_draw(self.axes, self.canvas, self.data)
#                        progressValue += 1
#                        mainWindow.horizontalSlider.setValue(progressValue)
#                        if progressValue == 100:
#                          progressValue = 0
#                          
#                break # stop
#                self.stop()
        
        def on_draw( axes, canvas, data):
            x = np.linspace(100*1e6, 1.4*1e9, len(data))  
            # clear the axes and redraw the plot anew
            axes.clear()      
            axes.set_title('Signal')
            axes.set_xlabel('Freqs(Hz)')
            axes.set_ylabel('dBm')  
            axes.grid(mainWindow.checkBox_ShowGrid.isChecked())
            axes.plot(x, data)
            canvas.draw()

        now = datetime.datetime.now()
        startTime = now.strftime('%Y-%m-%d-%H-%M-%S')
        subthread = None
#        if (self.replay):
        if (True):
            subthread = threading.Thread(target=readanddraw) 
        else:
            subthread = threading.Thread(target=realtimecapture)
            
        subthread.setDaemon(True)  
        subthread.start()  
        
    def stop(self): 
        print ("Stop thread...")
        self.stopped = True  

    def isStopped(self):  
        return self.stopped  
        
    def bumatoyuanma(self,  x):
      for i in range(len(x)):   
        if (x[i] > 32767):
          x[i]= x[i]-65536
      return x

    def bumatoyuanmaSingle(x):
      if (x > 32767): 
         x = x - 65536 
      return x

class RealTimeThread(threading.Thread):  
    def __init__(self, axes, canvas, timeout):  
        super(RealTimeThread, self).__init__()  
        self.axes = axes
        self.canvas = canvas
        self.timeout = timeout 
        self.data = []
        self.stopped = False  

    def run(self):  
        def combineData(iData, qData):
            y = []
            for i in range(len(iData)):
              y.append(complex(iData[i],qData[i]))
            
            yLength = len(y)
             # hanning window
            hanning_window = np.hanning(yLength)
            xf = np.fft.fft(y * hanning_window)
            xf = np.fft.fftshift(abs(xf))
            xf = 20*np.log10(abs(xf)) - 142.5
         
            #skipNum = int(yLength * 100/1500)
            skipNum = 0
            xf = xf[skipNum:yLength-skipNum]
            return xf   
        
        def bumatoyuanmaSingle(x):
           if (x > 32767): 
               x = x - 65536 
           return x
   
        def get_time_stamp():
            ct = time.time()
            local_time = time.localtime(ct)
            data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
            data_secs = (ct - int(ct)) * 1000
            time_stamp = "%s.%03d" % (data_head, data_secs)
            return time_stamp
   
        def parseIQData(data, withHead):
            if (withHead):
               newdata = data[16:]
              #print ( "New Data Length: ",  len(newdata))

            aiData = []
            aqData = []
            biData = []
            bqData = []

            # Save the original payload
            #now = datetime.datetime.now()
            
            #currentTime = now.strftime('%Y-%m-%d-%H-%M-%S-%ms') 
            now = datetime.datetime.now()
            currentTime = now.strftime('%Y-%m-%d-%H-%M-%S') 
            ms = get_time_stamp()
            currentTime = currentTime +"-" + ms[-3:]
            
            folderPath = os.path.split(os.path.realpath(__file__))[0]
            rawFileName = folderPath + "\\RawIQ-" + currentTime + ".dat"
            rawFile=open(rawFileName,'wb')
            rawFile.write(newdata)
            rawFile.close()

           # 32*1024 bytes AIAQBIBQ ... 
           #  Each data occupy 2 bytes, so iterate one row data by 8 bytes
           
            for pos in range(0, 32*1024,8):
                line = newdata[pos:pos+8]
                
                # 0XFF00, should be unpack one byte by one, 
                # otherwise, the data will be upack to 0x00FF, 
                # WE want ti to be still 0XFF00, call ntohs to reverse it
                if (len(line) == 8):
                    aiData.append(bumatoyuanmaSingle(ntohs(struct.unpack('H',line[0:2])[0])))
                    aqData.append(bumatoyuanmaSingle(ntohs(struct.unpack('H',line[2:4])[0])))
                    biData.append(bumatoyuanmaSingle(ntohs(struct.unpack('H',line[4:6])[0])))
                    bqData.append(bumatoyuanmaSingle(ntohs(struct.unpack('H',line[6:8])[0])))
                else:
                    aiData.append(0)
                    aqData.append(0)
                    biData.append(0)
                    bqData.append(0)


            # Save the IQ data 
            folderPath = os.path.split(os.path.realpath(__file__))[0]
            aiFileName = folderPath + "\\Data\\AI-" + currentTime + ".txt"
            aqFileName =  folderPath + "\\Data\\AQ-" + currentTime + ".txt"
            biFileName =  folderPath + "\\Data\\BI-" + currentTime + ".txt"   
            bqFileName =  folderPath + "\\Data\\BQ-" + currentTime + ".txt"
            
            aiFile=open(aiFileName,'w')
            aqFile=open(aqFileName,'w')
            biFile=open(biFileName,'w')
            bqFile=open(bqFileName,'w')
            
            print (len(aiData))
              # Save the IQ Data
            for i in range(len(aiData)):
              aiFile.write(str(aiData[i]))
              aiFile.write('\n');    
              aqFile.write(str(aqData[i]))
              aqFile.write('\n')
              biFile.write(str(biData[i]))
              biFile.write('\n');    
              bqFile.write(str(bqData[i]))
              bqFile.write('\n')

            aiFile.close()
            aqFile.close()
            biFile.close()
            bqFile.close()
            
            return (aiData,aqData,biData,bqData)
        
        def realtimecapture():
          print ("Real Time Capture.......")
          while not self.stopped:
            mainWindow.sendCmdRAW_AD_SAMPLE()
            mainWindow.udpSocketClient.receiveData()

            # Parse Data...
            data = mainWindow.udpSocketClient.mData
            
            print  ("Receive Total Length: ", len(data))
            if data and len(data) >= 32*1024:
                result = parseIQData(data, True)
                aiData = result[0]
                aqData = result[1]
                biData = result[2]
                bqData = result[3]
          
                if( mainWindow.radioButton_CHA_RealTime.isChecked() == True ):
                    self.data = combineData(aiData, aqData)
                    on_draw(self.axes, self.canvas, self.data)
                else:
                    self.data = combineData(biData, bqData)
                    on_draw(self.axes, self.canvas, self.data)

        def on_draw( axes, canvas, data):
            print (len(data))
            x = np.linspace(100*1e6, 1.4*1e9, len(data))  
            # clear the axes and redraw the plot anew
            axes.clear() 
            axes.set_title('Signal')
            axes.set_xlabel('Freqs(Hz)')
            axes.set_ylabel('dBm')
            refLevel = 0
            refLevelStr = mainWindow.lineEdit_RefLevel.text();
#            print (refLevelStr)
            if (('-' )  == refLevelStr or "" == refLevelStr):
                refLevel = 0
            else:
                refLevel = int(refLevelStr)
            
            scaleStr = mainWindow.lineEdit_Scale.text()
            scale = 10
            if (('-' )  == scaleStr or "" == scaleStr):
                scale = 10
            else:
                scale = int(scaleStr)

            axes.set_ylim(refLevel -10*scale,refLevel)
            ymajorLocator = MultipleLocator(10) 
            yminorLocator = MultipleLocator(5) 
            axes.yaxis.set_major_locator(ymajorLocator)
            axes.yaxis.set_minor_locator(yminorLocator)
            
            axes.grid(mainWindow.checkBox_ShowGrid_RealTime.isChecked())
            axes.plot(x, data)
            canvas.draw()

        now = datetime.datetime.now()
        startTime = now.strftime('%Y-%m-%d-%H-%M-%S')
        subthread = threading.Thread(target=realtimecapture)
        subthread.setDaemon(True)  
        subthread.start()  
        
    def stop(self): 
        print ("Stop thread...")
        self.stopped = True  

    def isStopped(self):  
        return self.stopped  

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.selectFolder = None
        self.tableView_Local_Init()
        self.tableView_SSD_Init()
        self.replay = False

        self.dpi = 100
        self.signalframe = self.widget_Signal
        self.figure = Figure((9, 5), dpi=self.dpi)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setParent(self.signalframe)
        self.axes = self.figure.add_subplot(111)
        self.axes.set_title('Signal')
        self.axes.set_xlabel('Freqs(Hz)')
        self.axes.set_ylabel('dBm')
        plt.subplots_adjust(left=0.2, bottom=0.2, right=0.8, top=0.8, hspace=0.2, wspace=0.3)
        self.figure.tight_layout()# Adjust spaces

        self.signalframe_RealTime = self.widget_Signal_RealTime
        self.figure_RealTime = Figure((8, 5), dpi=self.dpi)
        self.canvas_RealTime = FigureCanvas(self.figure_RealTime)
        self.canvas_RealTime.setParent(self.signalframe_RealTime)
        self.axes_RealTime = self.figure_RealTime.add_subplot(111)
        self.axes_RealTime.set_title('Signal')
        self.axes_RealTime.set_xlabel('Freqs(Hz)')
        self.axes_RealTime.set_ylabel('dBm')
        plt.subplots_adjust(left=0.2, bottom=0.2, right=0.8, top=0.8, hspace=0.2, wspace=0.3)
        self.figure_RealTime.tight_layout()# Adjust spaces

        # Init Socket
        self.udpSocketClient = UDPSocketClient()
     
        # Init...
        self.preSNLow = 0
        self.preSNHigh = 0
        self.preTimeLow = 0
        self.preTimeHigh = 0
        # Columns for data
        self.adidCol = 5
        self.snLowCol = 6
        self.snHighCol = 7
        self.timeLowCol = 8
        self.timeHighCol = 9
        self.startAddrLowCol = 10
        self.startAddrHighCol = 11
        self.ssdNumCol = 12
        self.localFileNameCol = 13
        
        #self.onInitSSDInfo()
       
       # Add custom context menu
        self.tableView_SSD.setContextMenuPolicy(Qt.CustomContextMenu)
        
        # Create context menu for SSD files
        self.createSSDContextMenu()
    
    # For Test Now
    def actionHandler(self):
        '''
        菜单中的具体action调用的函数
        '''
        print ('action handler')
    
    def showSSDContextMenu(self,  pos):
        print (pos)
        self.SSD_ContextMenu.move(pos)
        self.SSD_ContextMenu.show()
        
    def createSSDContextMenu(self):
        self.tableView_SSD.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableView_SSD.customContextMenuRequested.connect(self.showSSDContextMenu)
 
        self.SSD_ContextMenu = QtWidgets.QMenu(self)
        self.SSD_ActionA = self.SSD_ContextMenu.addAction(u'动作A')
        self.SSD_ActionB = self.SSD_ContextMenu.addAction(u'动作B')
        self.SSD_ActionC = self.SSD_ContextMenu.addAction(u'动作C')
        self.SSD_ActionA.triggered.connect(self.actionHandler)
        self.SSD_ActionB.triggered.connect(self.actionHandler)
        self.SSD_ActionC.triggered.connect(self.actionHandler)

    def onInitSSDInfo(self):
        print (sys._getframe().f_code.co_name)
        global gSocketBodySize
        gSocketBodySize = 64 # SSD Info, 64 Bytes + 16 header
        self.udpSocketClient.setBufSize(gSocketBodySize + gSocketHeaderSize) #  = 64 + 16 
        self.sendCmdSSD_INFO()
        self.udpSocketClient.receiveData(); #  Do nothing for the data for now
        
    def tableView_SSD_Init(self): 
        print (sys._getframe().f_code.co_name)
        # Readonly
        self.tableView_SSD.setEditTriggers(QTableWidget.NoEditTriggers)
          
        #添加表头：  
        self.SSDModel = QtGui.QStandardItemModel(self.tableView_SSD)  
  
        #设置表格属性：  
        self.SSDModel.setRowCount(0)    
        self.SSDModel.setColumnCount(13)   
          
        #设置表头  
        self.SSDModel.setHeaderData(0,QtCore.Qt.Horizontal,("File Name"))  
        self.SSDModel.setHeaderData(1,QtCore.Qt.Horizontal,("Start Time"))  
        self.SSDModel.setHeaderData(2,QtCore.Qt.Horizontal,("End Time"))  
        self.SSDModel.setHeaderData(3,QtCore.Qt.Horizontal,("Size(MByte)"))  
        self.SSDModel.setHeaderData(4,QtCore.Qt.Horizontal,("Total Time"))  
        
        self.tableView_SSD.setModel(self.SSDModel)  
           
        #设置列宽  
        self.tableView_SSD.setColumnWidth(0,280)  
        self.tableView_SSD.setColumnWidth(1,180)  
        self.tableView_SSD.setColumnWidth(2,180)  
        self.tableView_SSD.setColumnWidth(3,80) 
        self.tableView_SSD.setColumnWidth(4,100) 
          
        # Hidden the other colmumns
        self.tableView_SSD.setColumnHidden(5,  True)
        self.tableView_SSD.setColumnHidden(6,  True)
        self.tableView_SSD.setColumnHidden(7,  True)
        self.tableView_SSD.setColumnHidden(8,  True)
        self.tableView_SSD.setColumnHidden(9,  True)
        self.tableView_SSD.setColumnHidden(10,  True)
        self.tableView_SSD.setColumnHidden(11,  True)
        self.tableView_SSD.setColumnHidden(12,  True)
        
        #设置单元格禁止更改  
        #self.tableView_Local.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)  
          
        #表头信息显示居左  
        #self.tableView_Local.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft)  
          
        #表头信息显示居中  
        self.tableView_SSD.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignCenter)  
  
    def tableView_SSD_InsertData(self, data):
        print (sys._getframe().f_code.co_name)
                
        # Get Current Index
        # data:  rowdata = [fileName,  adid, snLow, snHigh, timeLow, timeHigh, startAddrLow, startAddrHigh, ssdNum ]
        # only show file name
        rowcount = self.SSDModel.rowCount()
        self.SSDModel.setItem(rowcount,0,QtGui.QStandardItem(data[0]))
        self.SSDModel.setItem(rowcount,self.adidCol,QtGui.QStandardItem(str(data[1])))
        self.SSDModel.setItem(rowcount,self.snLowCol,QtGui.QStandardItem(str(data[2])))
        self.SSDModel.setItem(rowcount,self.snHighCol,QtGui.QStandardItem(str(data[3])))
        self.SSDModel.setItem(rowcount,self.timeLowCol,QtGui.QStandardItem(str(data[4])))
        self.SSDModel.setItem(rowcount,self.timeHighCol,QtGui.QStandardItem(str(data[5])))
        self.SSDModel.setItem(rowcount,self.startAddrLowCol,QtGui.QStandardItem(str(data[6])))
        self.SSDModel.setItem(rowcount,self.startAddrHighCol,QtGui.QStandardItem(str(data[7])))
        self.SSDModel.setItem(rowcount,self.ssdNumCol,QtGui.QStandardItem(str(data[8])))
        
        self.tableView_SSD.setModel(self.SSDModel) 


    def tableView_Local_Init(self):  
        print (sys._getframe().f_code.co_name)
        # Readonly
        self.tableView_Local.setEditTriggers(QTableWidget.NoEditTriggers)
          
        #添加表头：  
        self.LocalModel = QtGui.QStandardItemModel(self.tableView_Local)  
  
        #设置表格属性：  
        #self.LocalModel.setRowCount(10)    
        self.LocalModel.setColumnCount(14)   
          
        #设置表头  
        self.LocalModel.setHeaderData(0,QtCore.Qt.Horizontal,("File Name"))  
        self.LocalModel.setHeaderData(1,QtCore.Qt.Horizontal,("Start Time"))  
        self.LocalModel.setHeaderData(2,QtCore.Qt.Horizontal,("End Time"))  
        self.LocalModel.setHeaderData(3,QtCore.Qt.Horizontal,("Size(MByte)"))  
        self.LocalModel.setHeaderData(4,QtCore.Qt.Horizontal,("Total Time"))  
          
        self.tableView_Local.setModel(self.LocalModel)  
           
        #设置列宽  
        self.tableView_Local.setColumnWidth(0,280)  
        self.tableView_Local.setColumnWidth(1,180)  
        self.tableView_Local.setColumnWidth(2,180)  
        self.tableView_Local.setColumnWidth(3,80) 
        self.tableView_Local.setColumnWidth(4,100) 
        
        # Hidden the other colmumns
        self.tableView_Local.setColumnHidden(5,  True)
        self.tableView_Local.setColumnHidden(6,  True)
        self.tableView_Local.setColumnHidden(7,  True)
        self.tableView_Local.setColumnHidden(8,  True)
        self.tableView_Local.setColumnHidden(9,  True)
        self.tableView_Local.setColumnHidden(10,  True)
        self.tableView_Local.setColumnHidden(11,  True)
        self.tableView_Local.setColumnHidden(12,  True)
        self.tableView_Local.setColumnHidden(13,  True)
          
        #设置单元格禁止更改  
        #self.tableView_Local.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)  
          
        #表头信息显示居左  
        #self.tableView_Local.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft)  
          
        #表头信息显示居中  
        self.tableView_Local.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignCenter)  
  

    def tableView_Local_InsertData(self,  data):
        print (sys._getframe().f_code.co_name)
                
        # Get Current Index
        # data:  rowdata = [fileName,  adid, snLow, snHigh, timeLow, timeHigh, startAddrLow, startAddrHigh, ssdNum, folderName ]
        # only show file name
        rowcount = self.LocalModel.rowCount()
        self.LocalModel.setItem(rowcount,0,QtGui.QStandardItem(data[0]))
        self.LocalModel.setItem(rowcount,self.adidCol,QtGui.QStandardItem(str(data[1])))
        self.LocalModel.setItem(rowcount,self.snLowCol,QtGui.QStandardItem(str(data[2])))
        self.LocalModel.setItem(rowcount,self.snHighCol,QtGui.QStandardItem(str(data[3])))
        self.LocalModel.setItem(rowcount,self.timeLowCol,QtGui.QStandardItem(str(data[4])))
        self.LocalModel.setItem(rowcount,self.timeHighCol,QtGui.QStandardItem(str(data[5])))
        self.LocalModel.setItem(rowcount,self.startAddrLowCol,QtGui.QStandardItem(str(data[6])))
        self.LocalModel.setItem(rowcount,self.startAddrHighCol,QtGui.QStandardItem(str(data[7])))
        self.LocalModel.setItem(rowcount,self.ssdNumCol,QtGui.QStandardItem(str(data[8])))
        self.LocalModel.setItem(rowcount,self.localFileNameCol,QtGui.QStandardItem(str(data[9])))
        
        self.tableView_Local.setModel(self.LocalModel) 

    def startReplay(self,  fullFilePath):
        print (sys._getframe().f_code.co_name)
        
        # Set Foucs on the tab_Play
        #self.tab_Play.setForeground()
        self.tabWidget.setCurrentIndex(3);

#        currentFolder = None
#        if (self.selectFolder != None):
#            #print (self.LocalModel.item(self.tableView_Local.currentIndex().row(), 4).data(Qt.DisplayRole))
#            currentFolder = os.path.join(self.selectFolder, self.LocalModel.item(self.tableView_Local.currentIndex().row(), 0).data(Qt.DisplayRole))
        
        self.pushButton_StartReplay.setEnabled(False)

        self.signalThread = SignalThread(self.axes, self.canvas, fullFilePath, 1.0)
        self.signalThread.setDaemon(True)
        self.signalThread.start()
    
    def stopReplay (self):
        print (sys._getframe().f_code.co_name)
        self.signalThread.stop()
        self.pushButton_StartReplay.setEnabled(True)
        # self.action_exit.triggered.connect(self.onExitTriggered)
        # self.action_copy.triggered.connect(self.onCopyTriggered)
        # self.action_paste.triggered.connect(self.onPasteTriggered)
        # self.action_cut.triggered.connect(self.onCutTriggered)
        
    def sendcommand(self, cmdid, status, msgid, len, type, offset, apiversion, pad, CRC16, cmdData):
          cmdid=struct.pack('H',htons(cmdid))
          status=struct.pack('H',htons(status))
          msgid=struct.pack('H',htons(msgid))
          len=struct.pack('H',htons(len))
          type=struct.pack('H',htons(type))
          offset=struct.pack('H',htons(offset))
          apiversion=struct.pack('B',apiversion) # 1 Byte unsigned char
          pad=struct.pack('B',pad) # 1 Byte unsigned char
          CRC16=struct.pack('H',htons(CRC16)) # 2 Byte unsigned short
          cmdHeader = cmdid + status + msgid + len + type + offset + apiversion + pad + CRC16
          
          if (cmdData != None):
              self.udpSocketClient.mData = cmdHeader + cmdData
          else:
              self.udpSocketClient.mData = cmdHeader
          
          self.udpSocketClient.sendData()
        
    def sendCmdRAW_AD_SAMPLE(self):
        print (sys._getframe().f_code.co_name)
        self.sendcommand(0x5a04,0x0000,0x5a04,0x0000,0x0000,0x0000,0x00,0x00,0x0000, None)
          
    def sendCmdRDREG(self,  regAddress,  regValue):
        #print (sys._getframe().f_code.co_name)
#        global gSocketBodySize
#        gSocketBodySize = 8
#        self.udpSocketClient.setBufSize(gSocketBodySize + gSocketHeaderSize)
        cmdData  =  struct.pack('L', htonl(regAddress)) +  struct.pack('L', htonl(regValue))
        self.sendcommand(0x5a01,0x0000,0x5a01,0x0008,0x0000,0x0000,0x00,0x00,0x0000, cmdData)
        
    def sendCmdSSD_INFO(self):
        print (sys._getframe().f_code.co_name)
        self.sendcommand(0x5a05,0x0000,0xa505,0x0000,0x0000,0x0000,0x00, 0x00,0x0000, None)
          
    def sendCmdSSD_AD_PROFILE(self,  updateAddr, ssdNum,  startAddrLow,  startAddrHigh):
        print (sys._getframe().f_code.co_name)
        
          # Send AD Profile Data
        cmdData = None
        if updateAddr == True:
            cmdData =  struct.pack('B', 0x02) +  struct.pack('B', int(ssdNum)) + struct.pack('2B', 0x00, 0x00) 
        else:
           cmdData  =  struct.pack('B', 0x00) +  struct.pack('B', int(ssdNum))+ struct.pack('2B', 0x00, 0x00) 
         
        cmdData = cmdData + struct.pack('L',  int(startAddrLow)) +  struct.pack('L',  int(startAddrHigh))  #Start Address [0:63]
        # End Address for testing
        cmdData = cmdData + struct.pack('L',  int(0)) +  struct.pack('L',  int(0)) 
        
        self.sendcommand(0x5a06,0x0000,0xa506,0x0000,0x0000,0x0000,0x00,0x00,0x0000, cmdData)
        
        # Receive data and return 
        global gSocketBufSize
        gSocketBufSize = 52
        self.udpSocketClient.setBufSize(gSocketBufSize);
        self.udpSocketClient.receiveData()
        data = self.udpSocketClient.mData 
        return data 
        

    def sendCmdSSD_AD_DATA(self,  flag,  adid, snLow, snHigh, timeLow, timeHigh, len, ssdNum):
        #print (sys._getframe().f_code.co_name)
        
#        cmdData =  struct.pack('B', 0x00) + struct.pack('B', 0x00) + struct.pack('H', 0x0000) \
#        + struct.pack('L', 0x0000) + struct.pack('L', 0x0000)   + struct.pack('L', 0x0000) + struct.pack('L', 0x0000) \
#        + struct.pack('Q',  0x8000) + struct.pack('H',  0x0000)
        
#        cmdData =  struck.pack('B',  0x00)  \ # flag
#        + struck.pack('B',  adid) \ # adid
#        + struck.pack('H',  snLow) \  # snLow
#        + struck.pack('L',  snHigh) \ # snHigh
#        + struck.pack('L',  timeLow) \ # timeLow
#        + struck.pack('L',  timeHigh) \ # timeHigh
#        + struck.pack('L',  0x00) \ # Offset
#        + struck.pack('H',  len) \ # len
#        + struck.pack('B',  0x00) \ # reseverd + SSD Num
#        + struck.pack('B',  0x00) # reseverd
        cmdData =  struct.pack('B',  0x00)  \
        + struct.pack('B',  adid) \
        + struct.pack('H',  htons(int(snLow))) \
        + struct.pack('L',  htonl(int(snHigh))) \
        + struct.pack('L',  htonl(int(timeLow))) \
        + struct.pack('L',  htonl(int(timeHigh))) \
        + struct.pack('L',  htons(0x00)) \
        + struct.pack('H',  htons(len)) \
        + struct.pack('B',  int(ssdNum)) \
        + struct.pack('B',  0x00) 
        
        self.sendcommand(0x5a07,0x0000,0x5a07,0x0000,0x0000,0x0000,  0x00, 0x00,  0x0000,  cmdData)

    def sendCmdSSD_RW_AD(self, CMD, ADid, FLAG,  RSVD,  StartAddr):
        print (sys._getframe().f_code.co_name)
        
        cmdData  =  struct.pack('B', CMD) +  struct.pack('B', ADid) + struct.pack('B', FLAG ) + struct.pack('B',  RSVD) + struct.pack('Q', StartAddr)
        self.sendcommand(0x5a08,0x0000,0x5a08,0x0000, 0x0000, 0x0000,  0x00, 0x00,  0x0000,  cmdData)
        
    def sendCmdTime(self):
        print (sys._getframe().f_code.co_name)
        
        t = int(time.time()) # in second
        cmdData  =  struct.pack('L', htonl(t))# +  struct.pack('L', t >> 32)
        self.sendcommand(0xd0e0,0x0000,0xd0e0,0x0000, 0x0000, 0x0000,  0x00, 0x00,  0x0000,  cmdData)

        # Recevie back, but do nothing
#        global gSocketBufSize
#        gSocketBufSize = 24 + 16
#        self.udpSocketClient.setBufSize(gSocketBufSize);
        self.udpSocketClient.receiveData()


    def parseSSD_AD_Profile(self, data):
        # The first 16 Bytes are the message header
        # The first 4 Bytes in payload is reseverd....
        # 1-4 Reseverd
        # 5-8 StartAddress[31:0]
        # 9-12 StartAddress[63:32]
        # 13-16 EndAddress[31:0]
        # 17-20 EndAddress[63:32]
        # 21 Adid
        # 22 CRC
        # 23-24 SerialNumber[15:0]
        # 25-28 SerialNumber[47:16]
        # 29-32 Timestamp[31:0]
        # 33-36 Timestamp[63:32]
        print ("Data Length: ",  len(data))
        data = data[16:]
#        print ("Data Length: ",  len(data))
#        print ("Data4:8",  data[4:8])
#        print ("Data8:12",  data[8:12])
#        print ("Data12:16",  data[12:16])
#        print ("Data16:20",  data[16:20])
#        print ("Data20:21",  data[20:21])
#        print ("Data21:22",  data[21:22])
#        print ("Data22:24",  data[22:24])
#        print ("Data24:28",  data[24:28])
#        print ("Data28:32",  data[28:32])
#        print ("Data32:36",  data[32:36])
        ssdNum =  (struct.unpack('B',data[1:2])[0]) # ssdNum
        print ("SSDNum: ",  ssdNum)
        startAddrLow = (ntohl(struct.unpack('L',data[4:8])[0]))
        print ("startAddr Low ", hex(startAddrLow))
        startAddrHigh = (ntohl(struct.unpack('L',data[8:12])[0]))
        print ("startAddr High ", hex(startAddrHigh))
        #print ("struct.unpack('L',data[12:16])[0]:",  struct.unpack('L',data[12:16])[0])
        endAddrLow = (ntohl(struct.unpack('L',data[12:16])[0]))
        print ("endAddrLow ", hex(endAddrLow))
        endAddrHigh = (ntohl(struct.unpack('L',data[16:20])[0]))
        print ("endAddrHigh ", hex(endAddrHigh))
        adid = struct.unpack('B',data[20:21])[0]
        adid = int(str(adid), 10)
        print ("adid: ",  adid)
        
        crc = struct.unpack('B',data[21:22])
        snLow =(ntohs(struct.unpack('H',data[22:24])[0]))
        print ("snLow ", hex(snLow))
        snHigh = (ntohl(struct.unpack('L',data[24:28])[0]))
        print ("snHigh ", hex(snHigh))
        timeLow = (ntohl(struct.unpack('L',data[28:32])[0]))
        print ("timeLow ", hex(timeLow))
        timeHigh = (ntohl(struct.unpack('L',data[32:36])[0]))
        print ("timeHigh ", hex(timeHigh))
        
        #Compare with Previous one, if they are same, then return false to stop it.
        if (snLow == self.preSNLow and snHigh == self.preSNHigh \
            and timeLow == self.preTimeLow  and timeHigh == self.preTimeHigh):
           return False;
        else:
            fileName = str(ssdNum) + "_" + str(adid) + "_" + str(timeHigh)+str(timeLow) +"_" + str(snHigh)+str(snLow) + ".dat"
            
            self.preSNLow = snLow
            self.preSNHigh = snHigh
            self.preTimeLow = timeLow
            self.preTimeHigh = timeHigh
            
            # Add into SSD File TableView
            rowdata = [fileName,  adid, snLow, snHigh, timeLow, timeHigh, startAddrLow, startAddrHigh, ssdNum ]
            self.tableView_SSD_InsertData(rowdata)

#        fileName = str(adid) + "_" + str(timeHigh)+str(timeLow) +"_" + str(snHigh)+str(snLow) + ".dat"
#        
#        # Add into SSD File TableView
#        rowdata = [fileName, adid, snLow, snHigh, timeLow, timeHigh, startAddrLow,  startAddrHigh ]
#        self.tableView_SSD_InsertData(rowdata)
#
#        return True;
        
    
    def saveSSD_AD_DATA(self, fileIO,  lastFrame):
        # Receive Data
        global gSocketBufSize
        gSocketBufSize = 32*1024 + 24 + 16
        self.udpSocketClient.setBufSize(gSocketBufSize);
        self.udpSocketClient.receiveData()
        data = self.udpSocketClient.mData  
        #print  ("Receive Total Length: ", len(data))
        data  = data[16+24:]
        
        # Save the file to local
        # Save the original payload
        if (not lastFrame):
            fileIO.write(data)
        else:
            fileIO.write(data[0:len(data)-16])
            fileIO.close()
            
    @pyqtSlot()
    def on_pushButton_StartReplay_clicked(self):
        """
        Slot documentation goes here.
        """

        folderPath = os.path.split(os.path.realpath(__file__))[0] + "\\Data\\"
        selectFilePath,  filtType = QFileDialog.getOpenFileName(mainWindow, "Open Bin File", folderPath, "Binary File (*.dat)");
        if (selectFilePath != None):
            self.startReplay(selectFilePath)
    
    @pyqtSlot()
    def on_pushButton_PauseReplay_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.stopReplay()
    
    @pyqtSlot()
    def on_pushButton_StopReply_clicked(self):
        """
        Slot documentation goes here.
        """
        self.stopReplay()
    
    @pyqtSlot()
    def on_pushButton_Local_Browse_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.selectFolder=QFileDialog.getExistingDirectory(self,'Select Folder:',path.dirname(__file__))
        self.lineEdit_LocalFolder.setText(self.selectFolder)
#        self.tableView_Local_InsertData()
    
    
    @pyqtSlot()
    def on_pushButton_SSD_Search_clicked(self):
        """
        Slot documentation goes here.
        """
        # Should send many times.....
        # Get Current SSD Files
        
        firstTime = True
        
        # Receive Data
#        global gSocketBodySize
#        gSocketBodySize = 36
#        self.udpSocketClient.setBufSize(gSocketBodySize + gSocketHeaderSize)
        
        testtime = 10
        
        #while (True):
        for ssdNum in range(0, 2):
            #Reset Regist 0x4, bit 0 to 0
            self.sendCmdResetAll()
            
            # Start to Read....
            self.sendCmdSSD_RW_AD(0x08, 0x00, 0x02, 0x00, 0x0000)
            
            updateAddr = True
            i = 0
            while ( i < testtime  ):
           # while ( True ):
                i = i+1
                self.sendCmdSSD_AD_PROFILE(updateAddr, ssdNum,  0,  0)
                updateAddr = False
                
                data = self.udpSocketClient.mData  
               # print  ("Receive Total Length: ", len(data))
                
                # if SN/Time are same, do not insert data
                if (self.parseSSD_AD_Profile(data)== False):
                    #Reset Regist 0x4, bit 0 to 0
#                    regAddr= 0x4 # 0x2, Bit[0], 0: Reset
#                    self.sendCmdRDREG(0x04,  0x00)
#                    data = self.udpSocketClient.receiveData()
#                    currentValue = ntohl(int(struct.unpack('L',data[20:24])[0]))
#                    mask = 0b1111111111111110
#                    currentValue = currentValue & mask
#                    self.sendCmdWRREG(regAddr,  currentValue) 
                    break;
                    
    @pyqtSlot()
    def on_pushButton_StartCapture_clicked(self):
        """
        Slot documentation goes here.
        """
        # Disable StartCapture Button
        self.pushButton_StartCapture.setEnabled(False)
        
        # Send Time first
        self.sendCmdTime()
        
        self.sendCmdResetAll()
        
        # Start Capture...
        self.sendCmdSSD_RW_AD(0x02, 0x00, 0x02, 0x00, 0x0000)
        #sendCmdSSD_RW_AD(self, CMD, ADid, FLAG,  RSVD,  StartAddr):
        
#        global gSocketBodySize
#        gSocketBodySize = 12
#        self.udpSocketClient.setBufSize(gSocketBodySize + gSocketHeaderSize)
        self.udpSocketClient.receiveData() # Do nothing
    
    @pyqtSlot()
    def on_pushButton_StopCapture_clicked(self):
        """
        Slot documentation goes here.
        """
        self.pushButton_StartCapture.setEnabled(True)
                
        self.sendCmdSSD_RW_AD(0x01, 0x00, 0x02, 0x00, 0x0000)
         #sendCmdSSD_RW_AD(self, CMD, ADid, FLAG,  RSVD,  StartAddr):
        
        global gSocketBodySize
        gSocketBodySize = 12
        self.udpSocketClient.setBufSize(gSocketBodySize + gSocketHeaderSize)
        self.udpSocketClient.receiveData() # Do nothing
        
        # Refresh table view
        # self.sendCmdSSD_AD_PROFILE(True,  0, 0,  0) # SSDNum 0
        #s elf.sendCmdSSD_AD_PROFILE(True,  1,  0,  0) # SSDNum 1

    
    
    
    def readDataTest(self):
        # Reset
        #self.sendCmdResetAll()
        
        # Start to Read....
        #self.sendCmdSSD_RW_AD(0x08, 0x00, 0x02, 0x00, 0x0000)
         #sendCmdSSD_RW_AD(self, CMD, ADid, FLAG,  RSVD,  StartAddr):
        
        # 1 - GetProfile for the start addrss
        #self.sendCmdSSD_AD_PROFILE(True, ssdNum, startAddrLow,  startAddrHigh)
        #self.sendCmdSSD_AD_PROFILE(True, 0, 0,  0)
        
        
        # Mannual send the register value 
#        currentValue = ntohl(int(struct.unpack('L',data[20:24])[0]))
#        mask = 0b100
#        currentValue = currentValue | mask   
#        self.sendCmdWRREG(regAddr,  currentValue) 
#        
#        self.sendCmdWRREG(0x4,  ntohs(0x20))
#        self.sendCmdWRREG(0x4,  ntohs(0x21))
#        self.sendCmdWRREG(0x4,  ntohs(0x23))
        #/////////////////wr
#./fpga_tool wr_reg 0x4 0x20
#./fpga_tool wr_reg 0x4 0x21
#./fpga_tool wr_reg 0x4 0x23
#
#./fpga_tool wr_reg 0x200A 0x1111
#./fpga_tool wr_reg 0x200A 0x1700
#./fpga_tool wr_reg 0x200C 0x1208
#./fpga_tool wr_reg 0x200E 0x2018
#./fpga_tool wr_reg 0x2102 0x3
#./fpga_tool wr_reg 0x2100 0x0
#./fpga_tool wr_reg 0x2018 0x10
#
#./fpga_tool wr_reg 0x300A 0x2222
#./fpga_tool wr_reg 0x300A 0x1700
#./fpga_tool wr_reg 0x300C 0x1208
#./fpga_tool wr_reg 0x300E 0x2018
#./fpga_tool wr_reg 0x3102 0x3
#./fpga_tool wr_reg 0x3100 0x0
#./fpga_tool wr_reg 0x3018 0x10
#
#./fpga_tool wr_reg 0x4 0x27
#
#
#/////////////////////rd
#./fpga_tool wr_reg 0x4 0x20
#./fpga_tool wr_reg 0x4 0x21
#./fpga_tool wr_reg 0x4 0x23
#
#./fpga_tool wr_reg 0x200A 0x1111
#./fpga_tool wr_reg 0x200A 0x1700
#./fpga_tool wr_reg 0x200C 0x1208
#./fpga_tool wr_reg 0x200E 0x2018
#./fpga_tool wr_reg 0x2102 0x3
#./fpga_tool wr_reg 0x2100 0x0
#./fpga_tool wr_reg 0x2018 0xa
#
#./fpga_tool wr_reg 0x300A 0x2222
#./fpga_tool wr_reg 0x300A 0x1700
#./fpga_tool wr_reg 0x300C 0x1208
#./fpga_tool wr_reg 0x300E 0x2018
#./fpga_tool wr_reg 0x3102 0x3
#./fpga_tool wr_reg 0x3100 0x0
#./fpga_tool wr_reg 0x3018 0xa
#
#./fpga_tool rd_reg 0x201A
#./fpga_tool rd_reg 0x201C
#./fpga_tool rd_reg 0x201E
#./fpga_tool rd_reg 0x2020
#./fpga_tool rd_reg 0x2022
#./fpga_tool rd_reg 0x2024
#./fpga_tool rd_reg 0x2026
#./fpga_tool rd_reg 0x2028
#
#./fpga_tool rd_reg 0x301A
#./fpga_tool rd_reg 0x301C
#./fpga_tool rd_reg 0x301E
#./fpga_tool rd_reg 0x3020
#./fpga_tool rd_reg 0x3022
#./fpga_tool rd_reg 0x3024
#./fpga_tool rd_reg 0x3026
#./fpga_tool rd_reg 0x3028
#
#
#/////////////////////rd index
#./fpga_tool wr_reg 0x4 0x20
#./fpga_tool wr_reg 0x4 0x21
#./fpga_tool wr_reg 0x4 0x23
#
#./fpga_tool wr_reg 0x200A 0x1111
#./fpga_tool wr_reg 0x200A 0x1700
#./fpga_tool wr_reg 0x200C 0x1208
#./fpga_tool wr_reg 0x200E 0x2018
#./fpga_tool wr_reg 0x2102 0x3
#./fpga_tool wr_reg 0x2100 0x0
#./fpga_tool wr_reg 0x2018 0xb
#
#./fpga_tool wr_reg 0x300A 0x2222
#./fpga_tool wr_reg 0x300A 0x1700
#./fpga_tool wr_reg 0x300C 0x1208
#./fpga_tool wr_reg 0x300E 0x2018
#./fpga_tool wr_reg 0x3102 0x3
#./fpga_tool wr_reg 0x3100 0x0
#./fpga_tool wr_reg 0x3018 0xb
#
#./fpga_tool rd_reg 0x201A
#./fpga_tool rd_reg 0x201C
#./fpga_tool rd_reg 0x201E
#./fpga_tool rd_reg 0x2020
#./fpga_tool rd_reg 0x2022
#./fpga_tool rd_reg 0x2024
#./fpga_tool rd_reg 0x2026
#./fpga_tool rd_reg 0x2028
#
#./fpga_tool rd_reg 0x301A
#./fpga_tool rd_reg 0x301C
#./fpga_tool rd_reg 0x301E
#./fpga_tool rd_reg 0x3020
#./fpga_tool rd_reg 0x3022
#./fpga_tool rd_reg 0x3024
#./fpga_tool rd_reg 0x3026
#./fpga_tool rd_reg 0x3028

        
        # 2 - Get data, only need the ssd number and Len
        folderName = os.path.join(path.dirname(__file__), "Data\\")
        ssdNum = '0'
        adid = '0'
        timeHigh = '0'
        timeLow = '0'
        snHigh = '0'
        snLow = '0'
        
        
        fileName = ssdNum + "_" + adid + "_" + timeHigh+timeLow +"_" + snHigh+snLow + ".dat"
        if (not os.path.exists(folderName)):
            os.makedirs(folderName) 
        fullFilePath = folderName +fileName
        fileIO=open(fullFilePath,'wb')

        # Send 1024 time for each file to save it
        length = 32*1024;
        iter = 0
        while (iter < 10):
            iter += 1
            #self.sendCmdSSD_AD_DATA(adid, 0x00,  snLow,  snHigh,  timeLow, timeHigh, length, ssdNum  )
            self.sendCmdSSD_AD_DATA(0, 0x00,  0,  0,  0, 0, length, 0  )
            self.saveSSD_AD_DATA(fileIO, False)
        
        # Send for the last frame
        #self.sendCmdSSD_AD_DATA(adid, 0x00,  snLow,  snHigh,  timeLow, timeHigh, length,  ssdNum )
        self.sendCmdSSD_AD_DATA(0, 0x00,  0,  0,  0, 0, length,  0 )
        self.saveSSD_AD_DATA(fileIO, True)
        
        # Add into the local view
        startAddrLow = ""
        startAddrHigh = ""
        rowdata = [fileName,  adid, snLow, snHigh, timeLow, timeHigh, startAddrLow, startAddrHigh, ssdNum, fullFilePath ]
        self.tableView_Local_InsertData(rowdata)
        
    @pyqtSlot(QModelIndex)
    def on_tableView_SSD_doubleClicked(self, index):
        """
        Slot documentation goes here.
        
        @param index DESCRIPTION
        @type QModelIndex
        """
        # Start to Send command to get data from SSD
        # fileName = adid_timestamp_sn.dat
        #print (self.SSDModel.rowCount())
        #fileName = self.SSDModel.item(self.tableView_SSD.currentIndex().row(), 0).data(Qt.DisplayRole)
        rowNum = self.tableView_SSD.currentIndex().row()
        adid = self.SSDModel.item(rowNum, self.adidCol).data(Qt.DisplayRole)
        snLow = self.SSDModel.item(rowNum, self.snLowCol).data(Qt.DisplayRole)
        snHigh = self.SSDModel.item(rowNum, self.snHighCol).data(Qt.DisplayRole)
        timeLow = self.SSDModel.item(rowNum, self.timeLowCol).data(Qt.DisplayRole)
        timeHigh = self.SSDModel.item(rowNum, self.timeHighCol).data(Qt.DisplayRole)
        startAddrLow = self.SSDModel.item(rowNum, self.startAddrLowCol).data(Qt.DisplayRole)
        startAddrHigh = self.SSDModel.item(rowNum, self.startAddrHighCol).data(Qt.DisplayRole)
        ssdNum = self.SSDModel.item(rowNum, self.ssdNumCol).data(Qt.DisplayRole)
        
        # Reset
        self.sendCmdResetAll()
        
        # Start to Read....
        self.sendCmdSSD_RW_AD(0x08, 0x00, 0x02, 0x00, 0x0000)
         #sendCmdSSD_RW_AD(self, CMD, ADid, FLAG,  RSVD,  StartAddr):
        
        # 1 - GetProfile for the start addrss
        #self.sendCmdSSD_AD_PROFILE(True, ssdNum, startAddrLow,  startAddrHigh)
        self.sendCmdSSD_AD_PROFILE(True, ssdNum, startAddrLow,  startAddrHigh)
        
        # 2 - Get data, only need the ssd number and Len
        folderName = os.path.join(path.dirname(__file__), "Data\\")
        fileName = ssdNum + "_" + adid + "_" + timeHigh+timeLow +"_" + snHigh+snLow + ".dat"
        if (not os.path.exists(folderName)):
            os.makedirs(folderName) 
        fullFilePath = folderName +fileName
        fileIO=open(fullFilePath,'wb')

        # Send 1024 time for each file to save it
        length = 32*1024;
        iter = 0
        while (iter < 1023):
            iter += 1
            #self.sendCmdSSD_AD_DATA(adid, 0x00,  snLow,  snHigh,  timeLow, timeHigh, length, ssdNum  )
            self.sendCmdSSD_AD_DATA(0, 0x00,  0,  0,  0, 0, length, 0  )
            self.saveSSD_AD_DATA(fileIO, False)
        
        # Send for the last frame
        #self.sendCmdSSD_AD_DATA(adid, 0x00,  snLow,  snHigh,  timeLow, timeHigh, length,  ssdNum )
        self.sendCmdSSD_AD_DATA(0, 0x00,  0,  0,  0, 0, length,  0 )
        self.saveSSD_AD_DATA(fileIO, True)
        
        # Add into the local view
        rowdata = [fileName,  adid, snLow, snHigh, timeLow, timeHigh, startAddrLow, startAddrHigh, ssdNum, fullFilePath ]
        self.tableView_Local_InsertData(rowdata)
        
    
    @pyqtSlot(QModelIndex)
    def on_tableView_Local_doubleClicked(self, index):
        # check file number
        #print (self.LocalModel.rowCount())
        # 13 is the fullFilePath
        fullFilePath = self.LocalModel.item(self.tableView_Local.currentIndex().row(), 13).data(Qt.DisplayRole)
        #self.label_TotalTime.setText(str(fileNum))
        
        self.replay = True
        self.startReplay(fullFilePath)
        #self.replay = False
     
    @pyqtSlot()
    def on_pushButton_SSDADData_clicked(self):
        """
        Slot documentation goes here.
        """
        
        # TODO: not implemented yet
        self.sendCmdSSD_AD_DATA()
        
        # Receive Data
        global gSocketBufSize
        gSocketBufSize = 32*1024 + 24 + 16
        self.udpSocketClient.receiveData()
        
        data = self.udpSocketClient.mData  
        #print  ("Receive Total Length: ", len(data))
        
        data  = data[16+24:]
        
    @pyqtSlot()
    def on_pushButton_SSDRWAD_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.sendCmdSSD_RW_AD()
        # Receive Data
        global gSocketBufSize
        gSocketBufSize = 12 + 16
        self.udpSocketClient.receiveData()
        
        data = self.udpSocketClient.mData  
        #print  ("Receive Total Length: ", len(data))
        
        data  = data[16+24:]
        
    @pyqtSlot()
    def on_pushButton_Time_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.sendCmdTime()
        
    def sendCmdWRREG(self,  regAddress,  regValue):
        #print (sys._getframe().f_code.co_name)
        #global gSocketBodySize
        #gSocketBodySize = 8
        #self.udpSocketClient.setBufSize(gSocketBodySize + gSocketHeaderSize)
        cmdData  =  struct.pack('L', htonl(regAddress)) +  struct.pack('L', htonl(regValue))
        self.sendcommand(0x5a02,0x0000,0x5a02,0x0008,0x0000,0x0000,0x00,0x00,0x0000, cmdData)
        self.udpSocketClient.receiveData() # Do nothing
        
    def sendCmdStartRealTime(self,): 
        regAddr= 0x4 # 0x2, Bit[2], 0: Auto, 1: External
        self.sendCmdRDREG(0x04,  0x00)
        data = self.udpSocketClient.receiveData()
        currentValue = ntohl(int(struct.unpack('L',data[20:24])[0]))
        mask = 0b100
        currentValue = currentValue | mask   
        self.sendCmdWRREG(regAddr,  currentValue) 
            
    def sendCmdResetAll(self,): 
        regAddr= 0x4 # 0x2, Bit[0], 0: Reset
        self.sendCmdRDREG(0x04,  0x00)
        data = self.udpSocketClient.receiveData()
        currentValue = ntohl(int(struct.unpack('L',data[20:24])[0]))
        mask = 0b1111111111111110
        currentValue = currentValue & mask
        self.sendCmdWRREG(regAddr,  currentValue) 
        
    def sendCmdStopRealTime(self,): 
        regAddr= 0x4 # 0x2, Bit[2], 0: Auto, 1: External
        self.sendCmdRDREG(0x04,  0x00)
        data = self.udpSocketClient.receiveData()
        currentValue = ntohl(int(struct.unpack('L',data[20:24])[0]))
        mask = 0b1111111111111011
        currentValue = currentValue & mask
        self.sendCmdWRREG(regAddr,  currentValue) 
        
    @pyqtSlot()
    def on_pushButton_Start_RealTime_clicked(self):
        """
        Slot documentation goes here.
        """
        
        self.sendCmdStartRealTime()
        time.sleep(0.1) # Sleep 100 ms to wait the start cmd has been received.
        
        self.pushButton_Start_RealTime.setEnabled(False)
        
        self.realTimeThread = RealTimeThread(self.axes_RealTime, self.canvas_RealTime, 1.0)
        self.realTimeThread.setDaemon(True)
        self.realTimeThread.start()
    
    @pyqtSlot()
    def on_pushButton_Stop_RealTime_clicked(self):
        """
        Slot documentation goes here.
        """
        self.sendCmdStopRealTime()
        
        print (sys._getframe().f_code.co_name)
        self.realTimeThread.stop()
        self.pushButton_Start_RealTime.setEnabled(True)
        
    @pyqtSlot()
    def on_pushButton_Save_RealTime_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: Save the last one data
        pass
        
    @pyqtSlot(int)
    def on_comboBox_TriggerDomain_currentIndexChanged(self, index):
        """
        Slot documentation goes here.
        
        @param index DESCRIPTION
        @type int
        """
        # TODO: not implemented yet
        print (index)
        
    @pyqtSlot()
    def on_pushButton_ReadTest_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.readDataTest()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
