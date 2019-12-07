# This is the file that will contain the actual implementation of the TDATuls interface
# All behaviour here depicted will be inherited from the noname.py file generated from the interface builder
import wx
import csv
import os
import logging
import pickle
import time

# Numpy
import numpy as np
from numpy import arange, sin, pi, genfromtxt, floor

# Matplot
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.widgets import Slider,Button
from matplotlib import pyplot as plt
from matplotlib import gridspec
from mpl_toolkits.mplot3d import Axes3D

# Ripser
from ripser import ripser

# Persim
from persim import PersImage, plot_diagrams, persistent_entropy

# Holes
import Holes as ho

# NetworkX
import networkx as nx

# Scipy
import scipy.stats as st

# Sklearn
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.decomposition import PCA

# Internals
from TDATuls import *
from noname import MainFrame, PanelLowerStar, PanelRipser, PanelCorrMatDist, PanelCorrMatHoles

#se la periodicità del segnale che vedo nella rappresentazione dopo le sliding windows si ripete per tutte le serie di punti piu o meno nelle stesse posizioni (correlazione verticale delle sliding window) significa che in quei punti qualcosa sta succedendo (si suppone proteine che vanno in folding)


ID_COUNTER = 2000
Data = []
Settings = {}

def inc_id_counter():
	global ID_COUNTER
	ID_COUNTER += 1
	return ID_COUNTER

def try_delimiter(line,delimiter):
    values = line.split(delimiter)
    if len(values) > 1:
        return True
    else:
        return False

def try_delimiters(line):
	delimiter = None
	if try_delimiter(line,';'):
		delimiter = ';'
	if try_delimiter(line,','):
		delimiter = ','
	return delimiter

def are_all_strings(values):
	if values == None:
		return False
	all_strings = True
	for value in values:
		try:
			float(value)
			all_strings = False
			break
		except ValueError:
			None
	return all_strings

def get_delimiter(line):
	delimiter = try_delimiters(line)
	if delimiter == None:
		die('Unable to detect dataset delimiter: supported delimiters are "," and ";"')
	return delimiter

def try_header(line,delimiter):
	values = line.split(delimiter)
	if are_all_strings(values):
		return True
	else:
		return False

'''
def try_header(line):
	values = try_all_split(line)
	if values != None:
		all_strings = True
		for value in values:
			try:
				float(value)
				all_strings = False
				break
			except ValueError:
				None
		if all_strings:
			return values
		else:
			return None
	return None
'''
def importCSVFile(file):
	first_line = file.readline()
	file.seek(0)

	delimiter = get_delimiter(first_line)

	data = None
	if try_header(first_line,delimiter):
		data = genfromtxt(file,delimiter=delimiter,skip_header=1)
	else:
		data = genfromtxt(file)

	dataDict = {}
	dataDict["path"] = os.path.realpath(file.name)
	for dic in Data:
		if dic["path"] == dataDict["path"]: # dataset alredy loaded, so no action takes place
			del dataDict
			print("dataset is already loaded in TDATuls")
			return False
	dataDict["id"] = inc_id_counter()
	dataDict["page_id"] = inc_id_counter()
	dataDict["shape"] = str(data.shape)
	dataDict["data"] = data
	Data.append(dataDict)
	'''
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
	data = genfromtxt(file,delimiter=',')#
	if csv.Sniffer().has_header(sample): #if there is a header
		data = data[1:,]
		dataDict["shape"] = str(data.shape)
	else:
		dataDict["shape"] = str(data.shape)
	dataDict["data"] = data
	Data.append(dataDict)
	'''
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
		page = AppPanelLowerStar(self.parent.Window.notebook,d['data'])
		'''page.dataDict = d
		# label display the shape of the dataset
		page.label_shape.SetLabel(d["shape"])
		# Max window size is the max value of the columns of the dataset
		maxval = int(str(d["shape"]).split(',')[1].strip(')'))
		page.spn_window_size.SetRange(1,maxval)
		# Overlap can vary between no overlap (subsequent) or complete overlap (one window on top of the other)
		page.sl_overlap.SetRange(0,100)
		# Signal choice is equal to rows in data shape
		maxSignal = int(str(d["shape"]).split(',')[0].strip('('))
		page.ch_signal.SetItems([str(val) for val in range(maxSignal)])'''

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
		page = AppPanelCorrMatDist(self.parent.Window.notebook,d['data'])
		#page.dataDict = d
		# label display the shape of the dataset
		#page.label_shape.SetLabel(d["shape"])
		# Max window size is the max value of the columns of the dataset
		#maxval = int(str(d["shape"]).split(',')[1].strip(')'))
		#page.spn_window_size.SetRange(1,maxval)
		# Overlap can vary between no overlap (subsequent) or complete overlap (one window on top of the other)
		#page.sl_overlap.SetRange(0,100)


		self.parent.Window.notebook.AddPage(page,'Correlation Matrix on ' + d["path"])
		print("Correlation Matrix tab created")
	def onMenuItemClickHoles(self,event):
		global Data
		d = None
		for dic in Data:
			if dic["path"] == self.Text: # corresponding data found
				d = dic
				break
		# create the notebook page corresponding to the chosen dataset
		page = AppPanelCorrMatHoles(self.parent.Window.notebook,d['data'])
		self.parent.Window.notebook.AddPage(page,'Holes on ' + d["path"])
		print("Holes tab created")


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
		for item in self.distanceMatrix.GetMenuItems():
			self.distanceMatrix.DestroyItem(item.Id)
		for item in self.holes.GetMenuItems():
			self.holes.DestroyItem(item.Id)
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

				id_distanceMatrix = inc_id_counter()
				data_distanceMatrix = AppPageMenuItem(self.distanceMatrix,id=id_distanceMatrix,text=str(dic["path"]))
				self.Bind(wx.EVT_MENU,data_distanceMatrix.onMenuItemClickCorrMat,id=id_distanceMatrix)
				self.distanceMatrix.Append(data_distanceMatrix)

				id_holes = inc_id_counter()
				data_holes = AppPageMenuItem(self.holes, id=id_holes,text=str(dic["path"]))
				self.Bind(wx.EVT_MENU,data_holes.onMenuItemClickHoles,id=id_holes)
				self.holes.Append(data_holes)




class BasePanel():
	def __init__(self, parent,data):
		self.parent = parent # parent is notebook whose parent is frame
		self.data = data
		self.diagrams = {}
		self.figure = None
		self.canvas = None
		self.toolbar = None
		self.figure_list = None
		self.updateFigure(0)

	def updateFigure(self,figure_index):
		if len(self.diagrams) == 0:
			figure = Figure()
			figure.add_subplot(111)
			self.diagrams['empty'] = figure

		if figure_index < 0 or figure_index >= len(self.diagrams):
			print('Error during figure update: index '+str(figure_index)+' out of range')
			return
		self.figure = self.diagrams[list(self.diagrams)[figure_index]]
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

	# Now we override the behaviour of the lowerStar menu selection
	# The change here requires to select on which data to perform the filtration
# Now we override the behaviour of the Panel page for lower star filtration
class AppPanelLowerStar(PanelLowerStar,BasePanel):
	def __init__(self, parent,data):
		PanelLowerStar.__init__(self, parent=parent)
		BasePanel.__init__(self, parent=parent, data=data)
		print('Loading lower star panel')

		# Set Label
		self.label_shape.SetLabel(str(self.data.shape))

		# Entropy check
		self.persistent_entropy = False
		self.chx_entropy.Bind(wx.EVT_CHECKBOX,self.onEntropyCheck)

		# Execute button
		self.btn_execute.Bind(wx.EVT_BUTTON,self.onExecuteButtonClick)

		# Close button
		self.btn_close.Bind(wx.EVT_BUTTON,self.onCloseButtonClick)

		# Overlap slider
		# SpinCtrl window size
		self.window_size_slider.Bind(wx.EVT_SCROLL,self.onWindowSizeSliderChange)
		self.window_size_slider.SetMax(self.data.shape[0])
		self.window_size = self.window_size_slider.GetValue()

		# Choice for selecting the signal
		if self.data.dtype.names == None:
			list = []
			for i in range(0,self.data.shape[1]):
				list.append(str(i))
			self.ch_signal.SetItems(list)
		else:
			self.ch_signal.SetItems(self.data.dtype.names)
		self.ch_signal.SetSelection(0)

	def onExecuteButtonClick(self, event):
		window_size = self.window_size_slider.GetValue()
		overlap = self.overlap_slider.GetValue()
		signal_index = self.ch_signal.GetCurrentSelection()
		windows = calculate_windows(window_size,overlap,self.data.shape[0])
		diagrams = {}

		norm_pers = []
		i = 0
		for window in windows:
			#Lower Star Filtration
			figure = plt.figure()
			plt.figure(figure.number)
			lsf_dgm0 = doLowerStarFiltration(self.data[window,signal_index])
			plt.plot(lsf_dgm0)
			diagrams['window'+str(i)+': lower star filtration'] = figure

			if self.chx_entropy.IsChecked():
				# Persistent Entropy
				L = []
				L.append(lsf_dgm0)
				dmg = np.array(L)
				ent = persentropy(dmg)[0]

				# Normalized Persistent Entropy
				pent = persentropy(dmg,normalize=True)[0]
				norm_pers.append(pent)
			i += 1

		if self.chx_entropy.IsChecked():
			figure = plt.figure()
			plt.figure(figure.number)
			plt.plot(np.arange(len(windows)),norm_pers)
			diagrams['normalized persistent entropy'] = figure

		self.diagrams = diagrams
		self.updateFigure(0)
	def onCloseButtonClick(self, event):
		index = self.parent.GetSelection()
		self.parent.DeletePage(index)
		self.parent.SendSizeEvent()
	def onEntropyCheck(self, event):
		self.persistent_entropy = self.chx_entropy.IsChecked()

	def onWindowSizeSliderChange(self, event):
		self.overlap_slider.SetMax(self.window_size_slider.GetValue())

	def onFigureChange(self, event):
		self.updateFigure(self.figure_list.GetCurrentSelection())

class AppPanelRipser(PanelRipser,BasePanel):
	def __init__(self, parent,data):
		PanelRipser.__init__(self, parent=parent)
		BasePanel.__init__(self, parent=parent, data=data)

		# Set Label
		self.label_shape.SetLabel(str(self.data.shape))

		# Execute button
		self.btn_execute.Bind(wx.EVT_BUTTON,self.onExecuteButtonClick)
		# Close button
		self.btn_close.Bind(wx.EVT_BUTTON,self.onCloseButtonClick)

		# Slider window size
		self.window_size_slider.Bind(wx.EVT_SCROLL,self.onWindowSizeSliderChange)
		self.window_size_slider.SetMax(self.data.shape[0])

	def onExecuteButtonClick(self, event):
		overlap = self.overlap_slider.GetValue()
		window_size = self.window_size_slider.GetValue()
		distance_matrix = self.chx_distance_matrix.IsChecked()
		max_hom_dim = self.spn_max_hom_dim.GetValue()
		metric = self.ch_metric.GetString(self.ch_metric.GetCurrentSelection())
		windows = calculate_windows(window_size,overlap,self.data.shape[0])
		diagrams = {}
		i = 0
		for window in windows:
			dgms = doRipsFiltration(self.data[window],max_hom_dim,distance_matrix,metric)#['dgms']
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

	def onWindowSizeSliderChange(self, event):
		self.overlap_slider.SetMax(self.window_size_slider.GetValue())

	def onFigureChange(self, event):
		self.updateFigure(self.figure_list.GetCurrentSelection())



class AppPanelCorrMatDist(PanelCorrMatDist,BasePanel):
	def __init__(self, parent,data):
		PanelRipser.__init__(self, parent=parent)
		BasePanel.__init__(self, parent=parent, data=data)

		# Set Label
		self.label_shape.SetLabel(str(self.data.shape))

		# Execute button
		self.btn_execute.Bind(wx.EVT_BUTTON,self.onExecuteButtonClick)
		# Close button
		self.btn_close.Bind(wx.EVT_BUTTON,self.onCloseButtonClick)

		# Slider window size
		self.window_size_slider.Bind(wx.EVT_SCROLL,self.onWindowSizeSliderChange)
		self.window_size_slider.SetMax(self.data.shape[0])

	def onExecuteButtonClick(self, event):
		overlap = self.overlap_slider.GetValue()
		window_size = self.window_size_slider.GetValue()
		distance_matrix = self.chx_distance_matrix.IsChecked()
		max_hom_dim = self.spn_max_hom_dim.GetValue()
		metric = self.ch_metric.GetString(self.ch_metric.GetCurrentSelection())


		#transpose the data before applying sliding window 10001 x 15 -> 15 x 10001
		#data = data.transpose()

		#remove the timecorrelationMatrix column from data
		#data = data[1:,] # for dim 0 pick from one to end, for dim 1 leave it as it is

		#restore data in its original shape
		#data = data.transpose()

		#### CORRELATION MATRICES AND Persistent Entropy ####
		#X = data.transpose()

		windows = calculate_windows(window_size,overlap,self.data.shape[0])
		diagrams = {}
		WCorr = []
		shapes = (self.data.shape[1],self.data.shape[1])
		for window in windows:
			#w is 14x100
			print(window)
			wcorr = np.zeros((self.data.shape[1],self.data.shape[1])) #14x14
			print(wcorr.shape)
			for i in range(self.data.shape[1]):
				for j in range(self.data.shape[1]):
					coeff,pvalue = st.pearsonr(self.data[i,:],self.data[j,:])
					if coeff > 0 and pvalue < 0.05:
						wcorr[i,j] = coeff
			WCorr.append(wcorr)

		corrmatdist = np.zeros(shapes) #14x14
		for i,wc1 in enumerate(WCorr):
			if i < 14:
				for j,wc2 in enumerate(WCorr):
					if j < 14:
					    corrmatdist[i,j] = abs_distance(wc1,wc2)

		figure = plt.figure()
		plt.figure(figure.number)
		D = pairwise_distances(corrmatdist)
		hoDgms = doRipsFiltration(D,maxHomDim=2,distance_matrix=True)
		Pers = persentropy(hoDgms)
		plot_diagrams(hoDgms)
		diagrams['correlation__matrix'] = figure

		#distance1 sembra dare un risultato concreto
		#l'entropia in H1 è 0 e c'è un solo barcode
		self.diagrams = diagrams
		self.updateFigure(0)

	def onCloseButtonClick(self, event):
		index = self.parent.GetSelection()
		self.parent.DeletePage(index)
		self.parent.SendSizeEvent()
	def onWindowSizeSliderChange(self, event):
		self.overlap_slider.SetMax(self.window_size_slider.GetValue())

	def onFigureChange(self, event):
		self.updateFigure(self.figure_list.GetCurrentSelection())
		

class AppPanelCorrMatHoles(PanelCorrMatHoles,BasePanel):
	def __init__(self, parent,data):
		PanelRipser.__init__(self, parent=parent)
		BasePanel.__init__(self, parent=parent, data=data)

		# Set Label
		self.label_shape.SetLabel(str(self.data.shape))

		# Execute button
		self.btn_execute.Bind(wx.EVT_BUTTON,self.onExecuteButtonClick)
		# Close button
		self.btn_close.Bind(wx.EVT_BUTTON,self.onCloseButtonClick)

		# Slider window size
		self.window_size_slider.Bind(wx.EVT_SCROLL,self.onWindowSizeSliderChange)
		self.window_size_slider.SetMax(self.data.shape[0])

		self.updateFigure(0)

	def onExecuteButtonClick(self, event):
		overlap = self.overlap_slider.GetValue()
		window_size = self.window_size_slider.GetValue()
		distance_matrix = self.chx_distance_matrix.IsChecked()
		max_hom_dim = self.spn_max_hom_dim.GetValue()
		metric = self.ch_metric.GetString(self.ch_metric.GetCurrentSelection())
		windows = calculate_windows(window_size,overlap,self.data.shape[0])
		diagrams = {}

		#### CORRELATION MATRICES AND HOLES #####
		X = self.data.transpose()
		n_signal = X.shape[0]
		W = matrix_window(X,window_size,window_size-overlap)
		WCORR = []
		Fil = []
		for w in W:
			Wcorr = np.full((n_signal,n_signal),24.0)
			for i in range(n_signal): # 14x14 correlation of signals
				for j in range(n_signal):
					coeff,pvalue = st.pearsonr(X[i,:],X[j,:])
					if coeff > 0 and pvalue < 0.05:
						Wcorr[i,j] = coeff
					else:
						Wcorr[i,j] = 0
			WCORR.append(Wcorr)
		for i,wc in enumerate(WCORR):
			if i < len(WCORR):
				#figure = plt.figure()
				#plt.figure(figure.number)

				G = nx.Graph(wc)

				#TODO creare a mano il grafo a partire dalla matrice
				# for i in range(len(wc)):
				# 	for j in range(len(wc[i])):
				# 		G.add_edge(i,j,weight=wc[i][j])
				cliqueDict = ho.standard_weight_clique_rank_filtration(G)
				with open('clique-%d.pkl'%(i), 'wb') as f:
					pickle.dump(cliqueDict, f, protocol=2)
				ho.persistent_homology_calculation("clique-%d.pkl"%(i), 1, "matrices", ".")
				Fil.append(cliqueDict)
				#diagrams['window'+str(i)] = figure


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

	def onWindowSizeSliderChange(self, event):
		self.overlap_slider.SetMax(self.window_size_slider.GetValue())

	def onFigureChange(self, event):
		self.updateFigure(self.figure_list.GetCurrentSelection())

