# This is the file that will contain the actual implementation of the TDATuls interface
# All behaviour here depicted will be inherited from the noname.py file generated from the interface builder
import wx
import csv
import os
import logging
import numpy as np
from numpy import arange, sin, pi, genfromtxt
import matplotlib
matplotlib.use('WXAgg')

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure

#from TDATuls import doLowerStarFiltration
from noname import MainFrame, PanelLowerStar

ID_COUNTER = 2000
Data = []
Settings = {}

def inc_id_counter():
	global ID_COUNTER
	ID_COUNTER += 1
	return ID_COUNTER

def importCSVFile(file):
	global Data
	#check for file format with sniffer
	dialect = csv.Sniffer().sniff(file.read(1024))
	file.seek(0)

	#grab a sample and see if there is a header
	sample=file.read(2048)
	file.seek(0)

	dataDict = {}
	dataDict["path"] = os.path.realpath(file.name)
	for dic in Data:
		if dic["path"] == dataDict["path"]: # dataset alredy loaded, so no action takes place
			del dataDict
			print("dataset is already loaded in TDATuls")
			return False
	dataDict["id"] = inc_id_counter()
	dataDict["page_id"] = inc_id_counter()
	data = genfromtxt(file,delimiter=dialect.delimiter)
	if csv.Sniffer().has_header(sample): #if there is a header
		data = data[1:,]
		dataDict["shape"] = str(data.shape)
	else:
		dataDict["shape"] = str(data.shape)
	dataDict["data"] = data
	Data.append(dataDict)

def openCSVFile(file,dic):
	global Data
	#check for file format with sniffer
	dialect = csv.Sniffer().sniff(file.read(1024))
	file.seek(0)

	#grab a sample and see if there is a header
	sample=file.read(2048)
	file.seek(0)

	data = genfromtxt(file,delimiter=dialect.delimiter)
	if csv.Sniffer().has_header(sample): #if there is a header
		data = data[1:,]
		dic["shape"] = str(data.shape)
	else:
		dic["shape"] = str(data.shape)
	dic["data"] = data

	# Update the item inside the Data list
	for idx, item in enumerate(Data):
   		if item["id"] == dic["id"]:
			   Data[idx] = dic

class AppCheckMenuItem(wx.MenuItem):
	def __init__( self, parent, idx, text ):
		wx.MenuItem.__init__(self, parentMenu=parent, id=idx, text=text, kind=wx.ITEM_CHECK)
		self.parent = parent

	def onMenuItemCheck( self, event ):
		global Data
		if not self.IsChecked():
			self.Check(check=True)
		else:
			self.Check(check=False)
		if self.IsChecked(): # item has just been checked thus data will be loaded from path and put into memory
			for dic in Data:
				if dic["id"] == self.Id and dic["data"] is None : # if entry is checked and data is not loaded
					if dic["path"] != "":
						with open(dic["path"],'r') as file:
							openCSVFile(file,dic)
							file.close()
						print("data reloaded successfully")
		else: # item has just been unchecked thus data will be unloaded from memory and its value set to None
			for dic in Data:
				if dic["id"] == self.Id and dic["data"] is not None:
					dic["data"] = None
			print("data unloaded successfully")
		self.parent.Window.updateOperationMenu()

class AppPageMenuItem(wx.MenuItem):
	def __init__(self, parent, id, text):
		wx.MenuItem.__init__(self, parent, id=id, text=text)
		self.parent = parent

	def onMenuItemClickLowerStar(self, event):
		global Data
		d = None
		for dic in Data:
			if dic["path"] == self.Text: # corresponding data found
				d = dic
				break
		# create the notebook page corresponding to the chosen dataset
		page = AppPanelLowerStar(self.parent.Window.notebook)
		page.dataDict = d
		# label display the shape of the dataset
		page.label_shape.SetLabel(d["shape"])
		# Max window size is the max value of the columns of the dataset
		page.spn_window_size.SetRange(1,tuple(d["shape"][3]))
		# Overlap can vary between no overlap (subsequent) or complete overlap (one window on top of the other)
		page.sl_overlap.SetRange(0,1)
		self.parent.Window.notebook.AddPage(page,'Lower Star')
		print("Lower Star tab created")

	def onMenuItemClickRipser(self,event):
		pass

	def onMenuItemClickCorrMat(self,event):
		pass
	def onMenuItemClickHoles(self,event):
		pass


# Start by overriding the behaviour of the MainFrame
class AppFrame(MainFrame):
	def __init__( self, parent ):
		MainFrame.__init__( self,parent=parent )

		# Here we change the display of elements and their behaviour
		# The most important change is to make the panel a child of the frame
		# outside any sizer and then create a notebook and a sizer which the notebook is a child of
		# then this sizer is added as the sizer of the panel

		# This list will contain the reference of each dataset loaded
		# The format of each object is
		'''
			file:	{
						path : "......",
						shape : "(14x14)"
						id : ID_ITEM
						page_id : ID_ITEM
						data : None
					}
		'''

		# Recreate the panel in order to set the frame as the parent
		#self.panel = wx.Panel(self)
		# Recreate the notebook in order to set the panel as the parent
		self.notebook = wx.Notebook(self.panel)
		notebookSizer = wx.BoxSizer()
		notebookSizer.Add(self.notebook, 1, wx.EXPAND)

		self.panel.SetSizer( notebookSizer )

		self.Layout()
		
		self.Centre(wx.BOTH)

	# Now we override the behaviour of the ImportData menu button
	def importDataOnMenuSelection( self, event ):
		global Data
		with wx.FileDialog(self, "Open data file", wildcard="CSV files (*.csv)|*.csv",style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
			
			if fileDialog.ShowModal() == wx.ID_CANCEL:
				return     # the user changed their mind

			# Proceed loading the file chosen by the user
			pathname = fileDialog.GetPath()
			try:
				with open(pathname, 'r') as file:
					importCSVFile(file)
					print("data loaded successfully")
					file.close()
				
				
				# Now for every data we have inside the Data array we create the entry in the file menu to (un)check
				for dic in Data:
					exist,_ = self.file.FindChildItem(dic["id"])
					if exist != None: # The entry for the dataset is already present
						continue
					p = dic["path"]
					# We add each entry to the file menu
					entry = AppCheckMenuItem(self.file,dic["id"],p)
					#print(entry.parent.Window.updateOperationMenu)
					self.Bind(wx.EVT_MENU,entry.onMenuItemCheck,id=dic["id"])
					self.file.AppendCheckItem(dic["id"],dic["path"])
					entry.Check(True) # after dataset is imported, is automatically loaded
				
				self.updateOperationMenu()
				

			except IOError and csv.Error:
				print("Unable to import file")

	def updateOperationMenu(self):
		global Data
		# Now for every item we have in file menu that is checked, create the operation entry for the 4 filtrations
		# If the item is checked, data must be loaded inside the data label of the dictionary
		# if the item is unchecked, data must be None and when it is checked, data must be loaded from path
		for item in self.lowerStar.GetMenuItems():
			self.lowerStar.DestroyItem(item.Id)
		for item in self.ripser.GetMenuItems():
			self.ripser.DestroyItem(item.Id)
		for dic in Data:
			if dic["data"] is not None: # dataset is loaded
				id_lowerStar = inc_id_counter()
				dataEntryLowerStar = AppPageMenuItem(self.lowerStar,id=id_lowerStar,text=str(dic["path"]))
				self.Bind(wx.EVT_MENU,dataEntryLowerStar.onMenuItemClickLowerStar,id=id_lowerStar)
				self.lowerStar.Append(dataEntryLowerStar)
				id_Ripser = inc_id_counter()
				dataEntryRipser = AppPageMenuItem(self.ripser, id=id_Ripser,text=str(dic["path"]))
				self.Bind(wx.EVT_MENU,dataEntryRipser.onMenuItemClickRipser,id=id_Ripser)
				self.ripser.Append(dataEntryRipser)

	# Now we override the behaviour of the lowerStar menu selection
	# The change here requires to select on which data to perform the filtration
# Now we override the behaviour of the Panel page for lower star filtration
class AppPanelLowerStar(PanelLowerStar):
	def __init__(self, parent):
		PanelLowerStar.__init__(self, parent=parent)
		
		self.dataDict = None

		# Execute button
		self.btn_execute.Bind(wx.EVT_BUTTON,self.onExecuteButtonClick)
		# Close button
		self.btn_close.Bind(wx.EVT_BUTTON,self.onCloseButtonClick)
		# Entropy box
		self.chx_entropy.Bind(wx.EVT_CHECKBOX,self.onEntropyCheck)
		# Overlap slider
		self.sl_overlap.Bind(wx.EVT_SCROLL,self.onPctSliderChange)
		# SpinCtrl window size
		self.spn_window_size.Bind(wx.EVT_SPINCTRL,self.onWindowSizeChange)

		# Create the canvas in the upper part of the sizer
		self.figure = Figure()
		self.axes = self.figure.add_subplot(111)
		self.canvas = FigureCanvas(self, -1, self.figure)

		mainSizer = self.GetSizer()
		# First child is canvasSizer, the second is settingsSizer
		canvasSizer = mainSizer.GetChildren()[0].GetSizer()
		canvasSizer.Add(self.canvas, 1, wx.ALL)
		self.SetSizer(mainSizer)

	def onExecuteButtonClick(self, event):
		pass
	def onCloseButtonClick(self, event):
		pass
	def onEntropyCheck(self, event):
		pass
	def onPctSliderChange(self,event):
		pass
	def onWindowSizeChange(self, event):
		pass

