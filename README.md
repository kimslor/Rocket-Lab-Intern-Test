# RocketLabInternTest
Flight Analysis Intern Test

This program models the drop test of a dummy mass and plots two graphs: 
    descent rate vs time, altitude vs time.

The user is able to adjust three parameters: 
    Surface area of the parachute in its reefed state (reef area),
    Surface area of the parachute after full deployment (full area),
    Drag coefficient.

Installation Steps:
    1) Download miniconda3
    2) Create and activate development environment (conda create -n {py39} python=3.9)
    3) Install extra packages using pip (PyQt5, matplotlib) (refer to package list below)
    4) Download and install Visual Studio Code
    5) Select your Python interpreter by clicking on the status bar (Python 3.9 64-bit ('{py39}':conda))
    6) Open up the main.py file and then run

Features:
    - The program can plot multiple graphs on the same canvas by just clicking plot with different inputs
    - There is navigation tool bar which allows the user to edit the format of the canvas, zoom into selected parts of the plots, etc.
    - The user is also able to save a screenshot of the graphs using the 'Save the figure' button (furtherest to the right on the navigation toolbar)
    - Hovering your cursor on the plots will show the position of your cursor on the graph on the top right on the program

Thank you for reading and using my program.
-Kimsong Lor

Package List:
Package           Version
----------------- -------------------
certifi           2021.5.30
cycler            0.10.0
kiwisolver        1.3.1
matplotlib        3.4.3
numpy             1.21.1
Pillow            8.3.1
pip               21.2.3
pyparsing         2.4.7
PyQt5             5.15.4
PyQt5-Qt5         5.15.2
PyQt5-sip         12.9.0
python-dateutil   2.8.2
setuptools        52.0.0.post20210125
six               1.16.0
torch             1.9.0
torchvision       0.10.0
typing-extensions 3.10.0.0
wheel             0.37.0
wincertstore      0.2
