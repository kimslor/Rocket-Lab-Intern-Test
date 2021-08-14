# RocketLab Flight Analysis Intern Test
# Author: Kimsong Lor  
# Date: 14/08/2021

import sys
import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLabel, QSpinBox, QDoubleSpinBox, QPushButton, QVBoxLayout, QHBoxLayout

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=8, height=12, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.descentRate = fig.add_subplot(2, 1, 1)
        self.altitude = fig.add_subplot(2, 1, 2)
        fig.tight_layout(pad=4, w_pad=1, h_pad=8)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Flight Analysis Intern Test")

        self.cs = MplCanvas(self, width=8, height=12, dpi=100)
        self.cs.descentRate.set(xlabel='Time (ms)', ylabel='Descent Rate (m/s)', title='Descent Rate vs Time')
        self.cs.altitude.set(xlabel='Time (ms)', ylabel='Alitude (m)', title='Altitude vs Time')

        #create label and spinbox for reefedArea
        self.reefedAreaLabel = QLabel()
        self.reefedAreaLabel.setText('Reefed Area:')
        self.reefedAreaSpinbox = QSpinBox()
        self.reefedAreaSpinbox.setRange(5, 20)

        #create label and spinbox for fullArea
        self.fullAreaLabel = QLabel()
        self.fullAreaLabel.setText('Full Area:')
        self.fullAreaSpinbox = QSpinBox()
        self.fullAreaSpinbox.setRange(50, 200)

        #create label and spinbox for dragCoef
        self.dragCoefLabel = QLabel()
        self.dragCoefLabel.setText('Drag Coefficient:')
        self.dragCoefSpinbox = QDoubleSpinBox()
        self.dragCoefSpinbox.setSingleStep(0.1)
        self.dragCoefSpinbox.setRange(0.0, 2.0)

        #create button for plotting
        self.plotButton = QPushButton()
        self.plotButton.setText('Plot')
        self.plotButton.setMaximumSize(137, 30)
        self.plotButton.clicked.connect(self.plotData)      #connecting plot button plot function

        #create button for clearing canvas
        self.clearButton = QPushButton()
        self.clearButton.setText('Clear')
        self.clearButton.setMaximumSize(137, 30)
        self.clearButton.clicked.connect(self.clearCanvas)      #connecting plot button plot function

        #create layouts and insert widgets
            #reefedArea selection vboxlayout
        self.reefedAreaSelection = QVBoxLayout(self)
        self.reefedAreaSelection.addWidget(self.reefedAreaLabel)
        self.reefedAreaSelection.addWidget(self.reefedAreaSpinbox)

            #fullArea selection vboxlayout
        self.fullAreaSelection = QVBoxLayout(self)
        self.fullAreaSelection.addWidget(self.fullAreaLabel)
        self.fullAreaSelection.addWidget(self.fullAreaSpinbox)

            #dragCoef selection vboxlayout
        self.dragCoefSelection = QVBoxLayout(self)
        self.dragCoefSelection.addWidget(self.dragCoefLabel)
        self.dragCoefSelection.addWidget(self.dragCoefSpinbox)

            #model, dataset, iterations hboxlayout
        self.UserSelection = QHBoxLayout(self)
        self.UserSelection.addLayout(self.reefedAreaSelection)
        self.UserSelection.addLayout(self.fullAreaSelection)
        self.UserSelection.addLayout(self.dragCoefSelection)
        self.UserSelection.addWidget(self.plotButton)
        self.UserSelection.addWidget(self.clearButton)

        #create navigation toolbar
        toolbar = NavigationToolbar(self.cs, self)

        #create layout and add in the toolbar, user inputs, and canvas
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(toolbar)
        self.layout.addLayout(self.UserSelection)
        self.layout.addWidget(self.cs)

        #create a placeholder widget to hold our toolbar and canvas
        widget = QtWidgets.QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

        self.show()

    def plotData(self):
        #parameters for this test system
        m_initPosi = 600        #meters
        m_dummyMass = 500       #kgs
        m_fluidDens = 1.2       #kg/m^3
        m_accelGrav = 9.81     #m/s^2
        m_timeStep = 0.0001     #s

        #user inputs
        m_reefedArea = self.reefedAreaSpinbox.value()     #m^2 
        m_fullArea = self.fullAreaSpinbox.value()         #m^2
        m_dragCoef = self.dragCoefSpinbox.value()         #drag coefficient

        #generate data based on given parameters
        #returns a list of lists [[time],[descentRate],[altitude]]
        data = generateData(m_initPosi, m_dummyMass, m_reefedArea, m_fullArea, m_dragCoef, m_fluidDens, m_accelGrav, m_timeStep)

        #descent rate vs time graph
        self.cs.descentRate.set(xlabel='Time (ms)', ylabel='Descent Rate (m/s)', title='Descent Rate vs Time')
        self.cs.descentRate.plot(data[0], data[1])

        #altitude vs time graph
        self.cs.altitude.set(xlabel='Time (ms)', ylabel='Alitude (m)', title='Altitude vs Time')
        self.cs.altitude.plot(data[0], data[2])

        self.cs.draw()

    def clearCanvas(self):
        self.cs.descentRate.cla()
        self.cs.altitude.cla()
        self.cs.descentRate.set(xlabel='Time (ms)', ylabel='Descent Rate (m/s)', title='Descent Rate vs Time')
        self.cs.altitude.set(xlabel='Time (ms)', ylabel='Alitude (m)', title='Altitude vs Time')

        self.cs.draw()


def generateData(initPosi, dummyMass, reefedArea, fullArea, dragCoef, fluidDens, accelGrav, timeStep):
    
    #data to be returned and plotted
    time = []
    descentRate = []
    altitude = []
    
    x = initPosi    #positon
    vf = 0          #final velocity
    vi = 0          #inital velocity
    currentTime = 0

    fullDeployTime = 5     #time taken for parachute to inflate into reefed state just before full deployment
    
    while(x > 0):
        #append updated data for timeStep
        time.append(currentTime)
        descentRate.append(vf)
        altitude.append(x)

        #if it is time for inflation to full deployment
        if (currentTime > fullDeployTime):
            currentTime += timeStep     #time increment
            a2 = calculateNetAcceleration(fluidDens, vf, dragCoef, fullArea, dummyMass, accelGrav)
            vf = vi + a2*timeStep    #calculate new velocity and displacement using kinematic equations
            x -= ((vf + vi)/2)*timeStep 
            vi = vf             #save for init velocity for next timestep

        #else inflating into reefed state
        else:
            currentTime += timeStep         #time increment
            area1 = (currentTime/fullDeployTime)*reefedArea      #area increases linearly based on fullDeployTime
            a1 = calculateNetAcceleration(fluidDens, vf, dragCoef, area1, dummyMass, accelGrav)
            vf = vi + a1*timeStep    #calculate new velocity and displacement using kinematic equations
            x -= ((vf + vi)/2)*timeStep 
            vi = vf             #save for init velocity for next timestep

    #collect data into one list to return
    data = [time, descentRate, altitude]

    return data

def calculateNetAcceleration(fluidDens, v, dragCoef, area, dummyMass, accelGrav):
    #calculate the net force acting on the body, in this case there is only two: drag and gravitional
    dragForce = 0.5*(fluidDens)*(v**2)*(dragCoef)*(area)
    gravForce = dummyMass*accelGrav
    netForce = gravForce - dragForce

    #returns the net acceleration on the body
    return netForce/dummyMass


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()