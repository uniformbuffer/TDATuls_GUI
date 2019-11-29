# This is the file that will contain the actual implementation of the TDATuls interface
# All behaviour here depicted will be inherited from the noname.py file generated from the interface builder
import wx
import csv
import os
import logging
import numpy as np
from numpy import arange, sin, pi, genfromtxt, floor
import matplotlib
matplotlib.use('WXAgg')
from ripser import ripser

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx as NavigationToolbar
from matplotlib.figure import Figure

from TDATuls import *
from persim import plot_diagrams
from noname import MainFrame, PanelLowerStar, PanelRipser

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
	dialect = csv.Sniffer().sniff(file.readline())
	file.seek(0)

	#grab a sample and see if there is a header
	sample=file.readline()
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
		maxval = int(str(d["shape"]).split(',')[1].strip(')'))
		page.spn_window_size.SetRange(1,maxval)
		# Overlap can vary between no overlap (subsequent) or complete overlap (one window on top of the other)
		page.sl_overlap.SetRange(0,100)
		# Signal choice is equal to rows in data shape
		maxSignal = int(str(d["shape"]).split(',')[0].strip('('))
		page.ch_signal.SetItems([str(val) for val in range(maxSignal)])

		self.parent.Window.notebook.AddPage(page,'Lower Star on ' + d["path"])
		print("Lower Star tab created")

	def onMenuItemClickRipser(self,event):
		global Data
		d = None
		for dic in Data:
			if dic["path"] == self.Text: # corresponding data found
				d = dic
				break
		# create the notebook page corresponding to the chosen dataset
		page = AppPanelRipser(self.parent.Window.notebook,d['data'])

		# label display the shape of the dataset

		# Max window size is the max value of the columns of the dataset
		#maxval = int(str(d["shape"]).split(',')[1].strip(')'))
		#page.spn_window_size.SetRange(1,maxval)
		# Overlap can vary between no overlap (subsequent) or complete overlap (one window on top of the other)
		#page.sl_overlap.SetRange(0,100)

		self.parent.Window.notebook.AddPage(page,'Ripser on ' + d["path"])
		print("Ripser tab created")

	def onMenuItemClickCorrMat(self,event):
		global Data
		d = None
		for dic in Data:
			if dic["path"] == self.Text: # corresponding data found
				d = dic
				break
		# create the notebook page corresponding to the chosen dataset
		page = AppPanelRipser(self.parent.Window.notebook)
		page.dataDict = d
		# label display the shape of the dataset
		page.label_shape.SetLabel(d["shape"])
		# Max window size is the max value of the columns of the dataset
		maxval = int(str(d["shape"]).split(',')[1].strip(')'))
		page.spn_window_size.SetRange(1,maxval)
		# Overlap can vary between no overlap (subsequent) or complete overlap (one window on top of the other)
		page.sl_overlap.SetRange(0,100)


		self.parent.Window.notebook.AddPage(page,'Correlation Matrix on ' + d["path"])
		print("Correlation Matrix tab created")
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

		self.SetSizer(None)
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
					#entry.Check(True) # after dataset is imported, is automatically loaded
				
				self.updateOperationMenu()
				

			except IOError or csv.Error:
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
	def __init__(self, parent,data):
		PanelLowerStar.__init__(self, parent=parent)
		self.parent = parent # parent is notebook whose parent is frame
		self.data = data

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
		# Choice for selecting the signal
		self.ch_signal.Bind(wx.EVT_CHOICE,self.onSignalSelectionChange)

		# Create the canvas in the upper part of the sizer
		self.figure = Figure()
		self.axes = self.figure.add_subplot(111)
		self.canvas = FigureCanvas(self.scrolled_window, -1, self.figure)
		self.toolbar = NavigationToolbar(self.canvas)
		self.toolbar.Realize()

		scrolled_sizer = self.scrolled_window.GetSizer()
		# First child is canvasSizer, the second is settingsSizer
		canvasSizer = scrolled_sizer.GetChildren()[0].GetSizer()
		mainCanvasSizer = canvasSizer.GetChildren()[0].GetSizer()
		mainCanvasSizer.Add(self.canvas, 1, wx.ALL)
		mainCanvasSizer.Add(self.toolbar, 0, wx.LEFT | wx.EXPAND)


	def updateFigure(self,figure_index):
		self.figure = self.diagrams[list(self.diagrams)[0]]
		self.canvas = FigureCanvas(self.scrolled_window, -1, self.figure)
		self.toolbar = NavigationToolbar(self.canvas)
		self.figure_list = wx.Choice(self.toolbar, -1, (85, 18))
		self.figure_list.Bind(wx.EVT_CHOICE,self.onFigureChange)
		self.figure_list.SetItems(list(self.diagrams))
		self.figure_list.SetSelection(figure_index)
		self.toolbar.AddControl(self.figure_list,"figure_list")
		self.toolbar.Realize()
		scrolled_sizer = self.scrolled_window.GetSizer()
		# First child is canvasSizer, the second is settingsSizer
		canvasSizer = scrolled_sizer.GetChildren()[0].GetSizer()
		mainCanvasSizer = canvasSizer.GetChildren()[0].GetSizer()
		mainCanvasSizer.Clear()
		mainCanvasSizer.Add(self.canvas, 1, wx.ALL)
		mainCanvasSizer.Add(self.toolbar, 0, wx.LEFT | wx.EXPAND)
		self.Layout()

	def onExecuteButtonClick(self, event):
		self.Pers = []
		self.NormPers = []
		self.Diags = []
		windowSize = self.spn_window_size.GetValue()
		overlap_pct = self.sl_overlap.GetValue()/100 # between 0 and 1
		overlap = int(floor(windowSize * overlap_pct))
		# Devo scegliere su quale segnale fare la finestra tramite un controllo
		signal = self.ch_signal.GetSelection()
		#print(signal)(self.dataDict["data"]
		print(self.dataDict["data"][signal])
		print(overlap)
		if signal != wx.NOT_FOUND:
			W = signal_window(self.dataDict["data"][signal],windowSize,overlap)
			print(len(W))
			for w in W:
				lsf_dgm0 = doLowerStarFiltration(w)
				# Prepare the diagram for computing PE
				L = []
				L.append(lsf_dgm0)
				dmg = np.array(L)
				# Diagram ready
				ent = persentropy(lsf_dgm0)[0]
				pent = persentropy(dmg,normalize=True)[0]
				self.Diags.append(dmg)
				self.Pers.append(ent)
				self.Norm_Pers.append(pent)
		which_one = self.sl_which_window.GetValue()
		self.axes.plot(np.arange(windowSize-1),self.NormPers)
		self.canvas.draw()
	def onCloseButtonClick(self, event):
		index = self.parent.GetSelection()
		self.parent.DeletePage(index)
		self.parent.SendSizeEvent()
	def onEntropyCheck(self, event):
		mainSizer = self.GetSizer()
		# First child is canvasSizer, the second is settingsSizer
		canvasSizer = mainSizer.GetChildren()[0].GetSizer()
		optionalCanvasSizer = canvasSizer.GetChildren()[1].GetSizer()
		if self.chx_entropy.IsChecked(): # Box is checked and I need to add the pe plot
			self.pe_Figure = Figure()
			self.pe_axes = self.pe_Figure.add_subplot(111)
			self.pe_canvas = FigureCanvas(self, -1, self.pe_Figure)
			self.pe_toolbar = NavigationToolbar(self.pe_canvas)
			self.pe_toolbar.Realize()
			
			optionalCanvasSizer.Add(self.pe_canvas, 1, wx.ALL)
			optionalCanvasSizer.Add(self.pe_toolbar, 0, wx.LEFT | wx.EXPAND)
			self.SetSizer(mainSizer)
			self.Layout() # automatically reshape the page to fit the pe plot
		else: # Check is unchecked and I need to remove the pe plot
			# i remove them by simply destroying children of the sizer
			optionalCanvasSizer.Clear(True)
			optionalCanvasSizer.Layout()
	def onPctSliderChange(self,event):
		pass
	def onWindowSizeChange(self, event):
		pass
	def onSignalSelectionChange(self, event):
		pass
	def onFigureChange(self, event):
		figure = self.diagrams[self.figure_list.GetString(self.figure_list.GetCurrentSelection())]
		self.updateFigure(figure)

class AppPanelRipser(PanelRipser):
	def __init__(self, parent,data):
		PanelRipser.__init__(self, parent=parent)
		self.parent = parent # parent is notebook whose parent is frame
		self.data = data
		self.diagrams = {}
		self.canvas = None
		self.toolbar = None
		self.figure_list = None
		self.metric = self.ch_metric.GetString(self.ch_metric.GetCurrentSelection())
		self.distance_matrix = self.chx_distance_matrix.IsChecked()
		self.max_hom_dim = self.spn_max_hom_dim.GetValue()
		self.window_size_slider.SetMax(self.data.shape[0])
		self.window_size = self.window_size_slider.GetValue()
		self.overlap = self.overlap_slider.GetValue()


		self.label_shape.SetLabel(str(self.data.shape))
		# Execute button
		self.btn_execute.Bind(wx.EVT_BUTTON,self.onExecuteButtonClick)
		# Close button
		self.btn_close.Bind(wx.EVT_BUTTON,self.onCloseButtonClick)
		# Entropy box
		self.chx_entropy.Bind(wx.EVT_CHECKBOX,self.onEntropyCheck)
		# Overlap slider
		self.overlap_slider.Bind(wx.EVT_SCROLL,self.onOverlapSliderChange)
		# SpinCtrl window size
		self.window_size_slider.Bind(wx.EVT_SCROLL,self.onWindowSizeSliderChange)
		# Choice for selecting the signal
		self.ch_metric.Bind(wx.EVT_CHOICE,self.onMetricSelectionChange)
		self.chx_distance_matrix.Bind(wx.EVT_CHECKBOX,self.onDistanceMatrixCheck)
		self.spn_max_hom_dim.Bind(wx.EVT_SPINCTRL,self.onMaxHomDimChange)


		figure = Figure()
		figure.add_subplot(111)
		self.diagrams['default'] = figure
		self.updateFigure(0)


	def updateFigure(self,figure_index):
		self.figure = self.diagrams[list(self.diagrams)[0]]
		if self.canvas != None:
			self.canvas.Destroy()
		self.canvas = FigureCanvas(self.scrolled_window, -1, self.figure)
		if self.toolbar != None:
			self.toolbar.Destroy()
		self.toolbar = NavigationToolbar(self.canvas)
		self.figure_list = wx.Choice(self.toolbar, -1, (85, 18))
		self.figure_list.Bind(wx.EVT_CHOICE,self.onFigureChange)
		self.figure_list.SetItems(list(self.diagrams))
		self.figure_list.SetSelection(figure_index)
		self.toolbar.AddControl(self.figure_list,"figure_list")
		self.toolbar.Realize()
		scrolled_sizer = self.scrolled_window.GetSizer()
		# First child is canvasSizer, the second is settingsSizer
		canvasSizer = scrolled_sizer.GetChildren()[0].GetSizer()
		mainCanvasSizer = canvasSizer.GetChildren()[0].GetSizer()
		mainCanvasSizer.Clear()
		mainCanvasSizer.Add(self.canvas, 1, wx.ALL)
		mainCanvasSizer.Add(self.toolbar, 0, wx.LEFT | wx.EXPAND)
		self.Layout()

	def onExecuteButtonClick(self, event):
		windows = calculate_windows(self.window_size,self.overlap,self.data.shape[0])
		diagrams = {}
		i = 0
		for window in windows:
			dgms = ripser(self.data[window])['dgms']#,self.max_hom_dim,self.distance_matrix,self.metric
			figure = plt.figure()
			plt.figure(figure.number)
			plot_diagrams(dgms)
			diagrams['window'+str(i)] = figure
			i+=1

		self.diagrams = diagrams
		self.updateFigure(0)

	def onCloseButtonClick(self, event):
		index = self.parent.GetSelection()
		self.parent.DeletePage(index)
		self.parent.SendSizeEvent()
	def onEntropyCheck(self, event):
		mainSizer = self.GetSizer()
		# First child is canvasSizer, the second is settingsSizer
		canvasSizer = mainSizer.GetChildren()[0].GetSizer()
		optionalCanvasSizer = canvasSizer.GetChildren()[1].GetSizer()
		if self.chx_entropy.IsChecked(): # Box is checked and I need to add the pe plot
			self.pe_Figure = Figure()
			self.pe_axes = self.pe_Figure.add_subplot(111)
			self.pe_canvas = FigureCanvas(self, -1, self.pe_Figure)
			self.pe_toolbar = NavigationToolbar(self.pe_canvas)
			self.pe_toolbar.Realize()

			optionalCanvasSizer.Add(self.pe_canvas, 1, wx.ALL)
			optionalCanvasSizer.Add(self.pe_toolbar, 0, wx.LEFT | wx.EXPAND)
			self.SetSizer(mainSizer)
			self.Layout() # automatically reshape the page to fit the pe plot
		else: # Check is unchecked and I need to remove the pe plot
			# i remove them by simply destroying children of the sizer
			optionalCanvasSizer.Clear(True)
			optionalCanvasSizer.Layout()
	def onDistanceMatrixCheck(self, event):
		self.distance_matrix = self.chx_distance_matrix.IsChecked()
	def onMaxHomDimChange(self,event):
		self.max_hom_dim = self.spn_max_hom_dim.GetValue()
	def onOverlapSliderChange(self,event):
		self.overlap = self.overlap_slider.GetValue()

	def onWindowSizeSliderChange(self, event):
		self.window_size = self.window_size_slider.GetValue()
		self.overlap_slider.SetMax(self.window_size)

	def onMetricSelectionChange(self, event):
		self.metric = self.ch_metric.GetString(self.ch_metric.GetCurrentSelection())
		pass

	def onFigureChange(self, event):
		figure = self.diagrams[self.figure_list.GetString(self.figure_list.GetCurrentSelection())]
		self.updateFigure(figure)
		
