# This is the file that will contain the actual implementation of the TDATuls interface
# All behaviour here depicted will be inherited from the noname.py file generated from the interface builder
import wx
import csv
from numpy import arange, sin, pi, genfromtxt
import matplotlib
matplotlib.use('WXAgg')

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure

from TDATuls import doLowerStarFiltration
from noname import MainFrame

# Start by overriding the behaviour of the MainFrame
class AppFrame(MainFrame):
    def __init__( self, parent ):
        super.__init__( self, parent )

        # Here we change the display of elements and their behaviour
        # The most important change is to make the panel a child of the frame
        # outside any sizer and then create a notebook and a sizer which the notebook is a child of
        # then this sizer is added as the sizer of the panel

        # Recreate the panel in order to set the frame as the parent
        self.panel = wx.Panel(self)
        # Recreate the notebook in order to set the panel as the parent
        self.notebook = wx.Notebook(self.panel)
        self.notebookSizer = wx.BoxSizer()
        self.notebookSizer.Add(self.notebook, 1, wx.EXPAND)

        self.panel.SetSizer( self.notebookSizer )
        
        self.Layout()
        
        self.Centre(wx.BOTH)
        
