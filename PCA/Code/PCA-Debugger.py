# Python file for debugging PCA-Version3.ipynb

import sys
import os
from PySide import QtCore
from PySide import QtGui
import pyqtgraph as pg
from functools import partial
import pandas as pd
import numpy as np
from pyqtgraph import PlotWidget
from mainwindow import Ui_MainWindow

class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    
    seriesData = {}
    attemptsDistributionData = {}
    deliveriesDistributionData = {}
    previousPlot = ''
    
    def __init__(self):
        super(MainWindow, self).__init__()
        pg.setConfigOption('background','w')
        pg.setConfigOption('foreground','k')

        self.setupUi(self)
        self.createActions()
        self.assignWidgets()
        
        # Need to move to a more appropriate place.
        labelStyle = {'color':(255,255,255),'font-size':'30px'}
        self.main_plot.setLabel('bottom', '<span style="color: black;font-size: 16pt">Time(s)</span>')
        self.main_plot.setLabel('left', '<span style="color: black;font-size: 16pt">Activity(N/A)</span>')
        
        '''Test plot data (Remove when finished)'''
        
        #testX = np.arange(0,100)
        #testY = np.random.normal(loc=2, scale=4.7, size=100)
        #item = pg.ScatterPlotItem(testX,testY,pen='w',size=10)
        #self.main_plot.addItem(item)
        #testZ = np.random.normal(loc=3, scale = 2.2, size=100)
        #p = pg.mkPen(color=(0,0,0), width=5)
        #self.main_plot.getAxisItem().setPen(p)
        #self.main_plot.plot(testX,testY,pen={'color':(0,0,0),'width':3})
        
        #self.main_plot.plot(testX,testY,pen=(0,0,255))
        #self.main_plot.plot(testX,testZ,pen=(255,165,0))
        #self.main_plot.show()
        # Zoom Plot
        #self.zoom_plot.plot(testX,testY)
        #self.zoom_plot.show()
        # Example Histogram (tab 2)
        vals = np.hstack([np.random.normal(size=500), np.random.normal(size=500, loc=8, scale=2.0)])
        y,x = np.histogram(vals, bins=np.linspace(-3, 8, 40))
        self.graphicsView.plot(x, y, stepMode=True, fillLevel=0, brush=(0,0,255,150))
        #print(x.size,y.size)
        # Example HIstogram (tab 3)
        y = pg.pseudoScatter(vals, spacing=0.15)
        self.graphicsView_2.plot(vals, y, pen=None, symbol='o', symbolSize=5, symbolPen=(255,255,255,200), symbolBrush=(0,0,255,150))
        # Example Histogram (tab 4) - Rest period
        
        # Create sample seriesData dictionary.
        for each in range(1,7):
            x = range(1,30)
            y = np.random.normal(loc=3, scale=1.5, size=len(x))
            temp = pd.DataFrame({'x':x, 'y':y})
            self.seriesData[str(each)] = temp
        
        # Add sample seriesDictionary keys to listbox
        for each in sorted(self.seriesData.keys()):
            item = QtGui.QListWidgetItem(each)
            self.list_files.addItem(item)
        
        # Plot first entry in main and zoom plots
        #self.main_plot.plot(self.seriesData['1']['x'],self.seriesData['1']['y'],pen={'color':(0,0,0),'width':3})
        #self.zoom_plot.plot(self.seriesData['1']['x'],self.seriesData['1']['y'],pen={'color':(0,0,0),'width':3})
        
        # Test bar graph plotting
        '''
        x = range(1,10)
        y = [i * 3 for i in range(1,10)]
        # NOTE: Need to have separate BarGraphItem object, otherwise zoom graph does not work properly.
        temp = pg.BarGraphItem(x = x, height = y, width = 0.3, brush='r')
        temp1 = pg.BarGraphItem(x = x, height = y, width = 0.3, brush='r')
        self.main_plot.addItem(temp)
        self.zoom_plot.addItem(temp1)
        '''
        '''End Test Plot Data'''
        
        self.show()
    
    def createActions(self):
        self.exitAct = QtGui.QAction('E&xit', self, shortcut='Ctrl+Q',statusTip='Exit the application',triggered=self.close)
        self.importAct = QtGui.QAction('&Open', self, shortcut='Ctrl+O', statusTip='Open a file')
        self.importAct.triggered.connect(partial(self.openFileDialog, self.tb_stats, self.list_files, self.main_plot, self.zoom_plot))
        # TODO:
        self.zoomViewAct = QtGui.QAction('Zoom', self, statusTip='View zoomed plot tab',triggered=self.tab_distributions.setCurrentWidget(self.tab_1))        
        #self.clearAct = QtGui.QAction('Clear Data', self, shortcut='Ctrl+D', statusTip='Clear loaded data', triggered=)
        #self.helpAct = QtGui.QAction('Help', self, shortcut='Ctrl+H', statusTip='Help', triggered=os.)
    
    # Assign functionality to widgets created from the UI Layout
    def assignWidgets(self):
        # Checkboxes
        self.cb_attempts.toggle()
        self.cb_attempts.stateChanged.connect(partial(self.updateMainPlot, self.list_files, self.main_plot, self.zoom_plot, self.rb_bar, self.rb_line, self.rb_scatter, self.cb_attempts, self.cb_deliveries))
        self.cb_deliveries.stateChanged.connect(partial(self.updateMainPlot, self.list_files, self.main_plot, self.zoom_plot, self.rb_bar, self.rb_line, self.rb_scatter, self.cb_attempts, self.cb_deliveries))
        # Push Buttons
        self.pb_add.clicked.connect(partial(self.openFileDialog, self.tb_stats, self.list_files, self.main_plot, self.zoom_plot))
        self.pb_remove.clicked.connect(partial(self.removeListItem, self.list_files))
        # Radio Buttons
        self.rb_bar.toggle()
        self.rb_line.toggled.connect(self.lineChanged)
        self.rb_scatter.toggled.connect(self.scatterChanged)
        self.rb_bar.toggled.connect(self.barChanged)
        # Menu Items
        self.menuFile.addAction(self.importAct)
        self.menuFile.addAction(self.exitAct)
        self.menuView.addAction(self.zoomViewAct)
        # Main plot
        self.main_plot.setLabel('bottom', 'Time')
        self.main_plot.setLabel('left', 'Status')
        self.lr = pg.LinearRegionItem([20,30])
        self.main_plot.addItem(self.lr)
        # Zoom plot
        self.zoom_plot.setLabel('bottom', 'Time')
        self.zoom_plot.setLabel('left', 'Status')
        self.lr.sigRegionChanged.connect(self.updateZoomPlot)
        self.zoom_plot.sigXRangeChanged.connect(self.updateZoomRegion)
        # ID list box
        self.list_files.itemSelectionChanged.connect(partial(self.updateMainPlot, self.list_files, self.main_plot, self.zoom_plot, self.rb_bar, self.rb_line, self.rb_scatter, self.cb_attempts, self.cb_deliveries))
        
    
    def updateZoomPlot(self):
        self.zoom_plot.setXRange(*self.lr.getRegion(), padding=0)
        self.zoom_plot.show()
        
    def updateZoomRegion(self):
        self.lr.setRegion(self.zoom_plot.getViewBox().viewRange()[0])
        self.zoom_plot.show()
    
    
    def updateMainPlot(self, list_files, main_plot, zoom_plot, rb_bar, rb_line, rb_scatter, cb_attempts, cb_deliveries, plotType=''):
        
        # Clear existing main plot and zoom plot
        for each in main_plot.allChildItems():
            if type(each) == type(pg.BarGraphItem()):
                main_plot.removeItem(each)
        for each in zoom_plot.allChildItems():
            if type(each) == type(pg.BarGraphItem()):
                zoom_plot.removeItem(each)
        for each in self.main_plot.listDataItems():
            main_plot.removeItem(each)
        for each in self.zoom_plot.listDataItems():
            zoom_plot.removeItem(each)
        main_plot.show()
        zoom_plot.show()
        
        # Get current selected item to plot
        CUTOFF = 2 # The cutoff limit used to differentiate between attempt and delivery datapoints.
        selectedItem = list_files.selectedItems()
        for each in selectedItem:
            
            temp_df = self.seriesData[each.text()] # NEW
            
            # Determine correct plot type and plot data:
            if self.previousPlot == '':
                self.previousPlot = 'bar'
            if plotType == '':
                plotType = self.previousPlot
            #TODO
            if cb_attempts.isChecked() and cb_deliveries.isChecked(): #NEW
                attempt_X = temp_df[temp_df['y'] <= CUTOFF]['x']
                attempt_Y = temp_df[temp_df['y'] <= CUTOFF]['y']
                delivery_X = temp_df[temp_df['y'] > CUTOFF]['x']
                delivery_Y = temp_df[temp_df['y'] > CUTOFF]['y']

                if plotType == 'bar':
                    att_main = pg.BarGraphItem(x = attempt_X, height = attempt_Y, width = 0.3, brush=(43,140,190))
                    att_zoom = pg.BarGraphItem(x = attempt_X, height = attempt_Y, width = 0.3, brush=(43,140,190))
                    del_main = pg.BarGraphItem(x = delivery_X, height = delivery_Y, width = 0.3, brush=(166,189,219))
                    del_zoom = pg.BarGraphItem(x = delivery_X, height = delivery_Y, width = 0.3, brush=(166,189,219))
                    
                    main_plot.addItem(att_main)
                    main_plot.addItem(del_main)
                    zoom_plot.addItem(att_zoom)
                    zoom_plot.addItem(del_zoom)
                    
                    self.previousPlot = 'bar'
                    
                elif plotType == 'scatter':
                    att_main = pg.ScatterPlotItem(x=attempt_X, y=attempt_Y, symbol='o', pen=(255,255,255,200), brush=(43,140,190))
                    att_zoom = pg.ScatterPlotItem(x=attempt_X, y=attempt_Y, symbol='o', pen=(255,255,255,200), brush=(43,140,190))
                    del_main = pg.ScatterPlotItem(x=delivery_X, y=delivery_Y, symbol='o', pen=(255,255,255,200), brush=(166,189,219))
                    del_zoom = pg.ScatterPlotItem(x=delivery_X, y=delivery_Y, symbol='o', pen=(255,255,255,200), brush=(166,189,219))
                    
                    main_plot.addItem(att_main)
                    main_plot.addItem(del_main)
                    zoom_plot.addItem(att_zoom)
                    zoom_plot.addItem(del_zoom)
                    
                    self.previousPlot = 'scatter'
                    
                elif plotType == 'line':
                    main_plot.plot(attempt_X,attempt_Y,pen={'color':(43,140,190),'width':3})
                    zoom_plot.plot(attempt_X,attempt_Y,pen={'color':(43,140,190),'width':3})
                    main_plot.plot(delivery_X,delivery_Y,pen={'color':(166,189,219),'width':3})
                    zoom_plot.plot(delivery_X,delivery_Y,pen={'color':(166,189,219),'width':3})
                    
                    self.previousPlot = 'line'
                    
                else:
                    None
                    #Error

            elif cb_attempts.isChecked() and not cb_deliveries.isChecked():
                attempt_X = temp_df[temp_df['y'] <= CUTOFF]['x']
                attempt_Y = temp_df[temp_df['y'] <= CUTOFF]['y']
                
                if plotType == 'bar':
                    att_main = pg.BarGraphItem(x = attempt_X, height = attempt_Y, width = 0.3, brush=(43,140,190))
                    att_zoom = pg.BarGraphItem(x = attempt_X, height = attempt_Y, width = 0.3, brush=(43,140,190))
                    
                    main_plot.addItem(att_main)
                    zoom_plot.addItem(att_zoom)
                    
                    self.previousPlot = 'bar'
                    
                elif plotType == 'scatter':
                    att_main = pg.ScatterPlotItem(x=attempt_X, y=attempt_Y, symbol='o', pen=(255,255,255,200), brush=(43,140,190))
                    att_zoom = pg.ScatterPlotItem(x=attempt_X, y=attempt_Y, symbol='o', pen=(255,255,255,200), brush=(43,140,190))
                    
                    main_plot.addItem(att_main)
                    zoom_plot.addItem(att_zoom)
                    
                    self.previousPlot = 'scatter'
                    
                elif plotType == 'line':
                    main_plot.plot(attempt_X,attempt_Y,pen={'color':'r','width':3})
                    zoom_plot.plot(attempt_X,attempt_Y,pen={'color':'r','width':3})
                    
                    self.previousPlot = 'line'
                    
                else:
                    None
                    #Error

            elif not cb_attempts.isChecked() and cb_deliveries.isChecked():
                delivery_X = temp_df[temp_df['y'] > CUTOFF]['x']
                delivery_Y = temp_df[temp_df['y'] > CUTOFF]['y']
                
                if plotType == 'bar':
                    del_main = pg.BarGraphItem(x = delivery_X, height = delivery_Y, width = 0.3, brush=(166,189,219))
                    del_zoom = pg.BarGraphItem(x = delivery_X, height = delivery_Y, width = 0.3, brush=(166,189,219))
                    
                    main_plot.addItem(del_main)
                    zoom_plot.addItem(del_zoom)
                    
                    self.previousPlot = 'bar'
                    
                elif plotType == 'scatter':
                    del_main = pg.ScatterPlotItem(x=delivery_X, y=delivery_Y, symbol='o', pen=(255,255,255,200), brush=(166,189,219))
                    del_zoom = pg.ScatterPlotItem(x=delivery_X, y=delivery_Y, symbol='o', pen=(255,255,255,200), brush=(166,189,219))
                    
                    main_plot.addItem(del_main)
                    zoom_plot.addItem(del_zoom)
                    
                    self.previousPlot = 'scatter'
                    
                elif plotType == 'line':
                    main_plot.plot(delivery_X,delivery_Y,pen={'color':(166,189,219),'width':3})
                    zoom_plot.plot(delivery_X,delivery_Y,pen={'color':(166,189,219),'width':3})
                    
                    self.previousPlot = 'line'
                    
                else:
                    None
                    #Error
            else:
                None
                # Do not add anything to the plot.
        main_plot.show()
        self.updateZoomPlot()
        self.updateZoomRegion()
            
    
    #def formatData(self, list_files):
        #TODO
    
    
    # Remove selected item from the listbox
    def removeListItem(self, list_files):
        for item in list_files.selectedItems():
            del self.seriesData[item.text()]
            list_files.takeItem(list_files.row(item))
        list_files.show()
        
    
    # Calls the updateMainPlot function and passes the new plot type
    def barChanged(self, b):
        if b == True:
            self.updateMainPlot(self.list_files, self.main_plot, self.zoom_plot, self.rb_bar, self.rb_line, self.rb_scatter, self.cb_attempts, self.cb_deliveries, 'bar')
    
    def scatterChanged(self, b):
        if b == True:
            self.updateMainPlot(self.list_files, self.main_plot, self.zoom_plot, self.rb_bar, self.rb_line, self.rb_scatter, self.cb_attempts, self.cb_deliveries, 'scatter')
    
    def lineChanged(self, b):
        if b == True:
            self.updateMainPlot(self.list_files, self.main_plot, self.zoom_plot, self.rb_bar, self.rb_line, self.rb_scatter, self.cb_attempts, self.cb_deliveries, 'line')
    
    # Close event
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Exit Message', 'Are you sure you want to quit?',QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
    
    
    # File opening
    def openFileDialog(self, table, list_files, main_plot, zoom_plot):
        
        # Get file path
        path, _ = QtGui.QFileDialog.getOpenFileName(self, 'Open File', os.getcwd())
        self.setWindowTitle(path) # Remove once working!
        #f = open(path, 'r')
        
        # Read data into dataframe
        data = pd.read_csv(path)
        
        # Add IDs to listbox
        '''
        for each in data['InfusionID'].unique():
            item = QtGui.QListWidgetItem(str(each))
            list_files.addItem(item)
        '''
        
        for each in range(0,10):
            item = QtGui.QListWidgetItem(str(each))
            list_files.addItem(item)
        
        # Show the list
        list_files.show()
        
        # Resize table
        table.setRowCount(data.shape[0])
        table.setColumnCount(data.shape[1])
        table.setHorizontalHeaderLabels(['Statistic','Group Value', '1 Value', '2 Value', '3 Value', '4 Value', '5 Value', '6 Value', '7 Value'])
        #table.setVerticalHeaderLabels(['Mean Deliveries (deliveries/30 mins):','Standard Deviation Deliveries (deliveries/30 mins):','Mean Requests (deliveries/30 mins):','Standard Deviation Deliveries (deliveries/30 mins):','Mean Rest Time (mins):', 'Standard Deviation Rest Time (mins):'])
        
        # Populate table:
        '''
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                item = QtGui.QTableWidgetItem(str(data[i,j]))
                table.setItem(i,j,item)
        '''
        #table.show()
        
        
        # Plot initial data using default settings (Attempts & Deliveries, Line)

def main():
    app = QtGui.QApplication.instance()
    if app is None:
        app = QtGui.QApplication(sys.argv)
        
    ex = MainWindow()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()