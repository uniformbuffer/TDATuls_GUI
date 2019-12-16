# This is the file that will contain the actual implementation of the TDATuls interface
# All behaviour here depicted will be inherited from the noname.py file generated from the interface builder
import wx
from wx.adv import NotificationMessage
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
from noname import *

#se la periodicità del segnale che vedo nella rappresentazione dopo le sliding windows si ripete per tutte le serie di punti piu o meno nelle stesse posizioni (correlazione verticale delle sliding window) significa che in quei punti qualcosa sta succedendo (si suppone proteine che vanno in folding)
from functools import partial


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
		page = AppPanelLowerStar(self.parent.Window,d)

	def onMenuItemClickRipser(self,event):
		global Data
		d = None
		for dic in Data:
			if dic["path"] == self.Text: # corresponding data found
				d = dic
				break
		# create the notebook page corresponding to the chosen dataset
		page = AppPanelRipser(self.parent.Window,d)

	def onMenuItemClickCorrMat(self,event):
		global Data
		d = None
		for dic in Data:
			if dic["path"] == self.Text: # corresponding data found
				d = dic
				break
		# create the notebook page corresponding to the chosen dataset
		page = AppPanelCorrMatDist(self.parent.Window,d)

	def onMenuItemClickHoles(self,event):
		global Data
		d = None
		for dic in Data:
			if dic["path"] == self.Text: # corresponding data found
				d = dic
				break
		# create the notebook page corresponding to the chosen dataset
		page = AppPanelCorrMatHoles(self.parent.Window,d)

	def onMenuItemClickSpikes(self,event):
		global Data
		d = None
		for dic in Data:
			if dic["path"] == self.Text: # corresponding data found
				d = dic
				break
		# create the notebook page corresponding to the chosen dataset
		page = AppPanelSpikes(self.parent.Window,d)

	def onMenuItemClickMiniBatchKMeans(self,event):
		global Data
		d = None
		for dic in Data:
			if dic["path"] == self.Text: # corresponding data found
				d = dic
				break
		# create the notebook page corresponding to the chosen dataset
		page = AppPanelMiniBatchKMeans(self.parent.Window,d)

	def onMenuItemClickAffinityPropagation(self,event):
		global Data
		d = None
		for dic in Data:
			if dic["path"] == self.Text: # corresponding data found
				d = dic
				break
		# create the notebook page corresponding to the chosen dataset
		page = AppPanelAffinityPropagation(self.parent.Window,d)

	def onMenuItemClickMeanShift(self,event):
		global Data
		d = None
		for dic in Data:
			if dic["path"] == self.Text: # corresponding data found
				d = dic
				break
		# create the notebook page corresponding to the chosen dataset
		page = AppPanelMeanShift(self.parent.Window,d)

	def onMenuItemClickSpectralClustering(self,event):
		global Data
		d = None
		for dic in Data:
			if dic["path"] == self.Text: # corresponding data found
				d = dic
				break
		# create the notebook page corresponding to the chosen dataset
		page = AppPanelSpectralClustering(self.parent.Window,d)

	def onMenuItemClickWard(self,event):
		global Data
		d = None
		for dic in Data:
			if dic["path"] == self.Text: # corresponding data found
				d = dic
				break
		# create the notebook page corresponding to the chosen dataset
		page = AppPanelWard(self.parent.Window,d)

	def onMenuItemClickAgglomerativeClustering(self,event):
		global Data
		d = None
		for dic in Data:
			if dic["path"] == self.Text: # corresponding data found
				d = dic
				break
		# create the notebook page corresponding to the chosen dataset
		page = AppPanelAgglomerativeClustering(self.parent.Window,d)

	def onMenuItemClickDBSCAN(self,event):
		global Data
		d = None
		for dic in Data:
			if dic["path"] == self.Text: # corresponding data found
				d = dic
				break
		# create the notebook page corresponding to the chosen dataset
		page = AppPanelDBSCAN(self.parent.Window,d)

	def onMenuItemClickOPTICS(self,event):
		global Data
		d = None
		for dic in Data:
			if dic["path"] == self.Text: # corresponding data found
				d = dic
				break
		# create the notebook page corresponding to the chosen dataset
		page = AppPanelOPTICS(self.parent.Window,d)

	def onMenuItemClickBirch(self,event):
		global Data
		d = None
		for dic in Data:
			if dic["path"] == self.Text: # corresponding data found
				d = dic
				break
		# create the notebook page corresponding to the chosen dataset
		page = AppPanelBirch(self.parent.Window,d)

	def onMenuItemClickGaussianMixture(self,event):
		global Data
		d = None
		for dic in Data:
			if dic["path"] == self.Text: # corresponding data found
				d = dic
				break
		# create the notebook page corresponding to the chosen dataset
		page = AppPanelGaussianMixture(self.parent.Window,d)

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
		for item in self.spikes.GetMenuItems():
			self.spikes.DestroyItem(item.Id)
		for item in self.distanceMatrix.GetMenuItems():
			self.distanceMatrix.DestroyItem(item.Id)
		for item in self.holes.GetMenuItems():
			self.holes.DestroyItem(item.Id)
		for item in self.MiniBatchKMeans.GetMenuItems():
			self.MiniBatchKMeans.DestroyItem(item.Id)
		for item in self.AffinityPropagation.GetMenuItems():
			self.AffinityPropagation.DestroyItem(item.Id)
		for item in self.MeanShift.GetMenuItems():
			self.MeanShift.DestroyItem(item.Id)
		for item in self.SpectralClustering.GetMenuItems():
			self.SpectralClustering.DestroyItem(item.Id)
		for item in self.Ward.GetMenuItems():
			self.Ward.DestroyItem(item.Id)
		for item in self.AgglomerativeClustering.GetMenuItems():
			self.AgglomerativeClustering.DestroyItem(item.Id)
		for item in self.DBSCAN.GetMenuItems():
			self.DBSCAN.DestroyItem(item.Id)
		for item in self.OPTICS.GetMenuItems():
			self.OPTICS.DestroyItem(item.Id)
		for item in self.Birch.GetMenuItems():
			self.Birch.DestroyItem(item.Id)
		for item in self.GaussianMixture.GetMenuItems():
			self.GaussianMixture.DestroyItem(item.Id)

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

				id_Spikes = inc_id_counter()
				dataEntrySpikes = AppPageMenuItem(self.spikes, id=id_Spikes,text=str(dic["path"]))
				self.Bind(wx.EVT_MENU,dataEntrySpikes.onMenuItemClickSpikes,id=id_Spikes)
				self.spikes.Append(dataEntrySpikes)


				id_distanceMatrix = inc_id_counter()
				data_distanceMatrix = AppPageMenuItem(self.distanceMatrix,id=id_distanceMatrix,text=str(dic["path"]))
				self.Bind(wx.EVT_MENU,data_distanceMatrix.onMenuItemClickCorrMat,id=id_distanceMatrix)
				self.distanceMatrix.Append(data_distanceMatrix)

				id_holes = inc_id_counter()
				data_holes = AppPageMenuItem(self.holes, id=id_holes,text=str(dic["path"]))
				self.Bind(wx.EVT_MENU,data_holes.onMenuItemClickHoles,id=id_holes)
				self.holes.Append(data_holes)

				id_MiniBatchKMeans = inc_id_counter()
				data_MiniBatchKMeans = AppPageMenuItem(self.MiniBatchKMeans, id=id_MiniBatchKMeans,text=str(dic["path"]))
				self.Bind(wx.EVT_MENU,data_MiniBatchKMeans.onMenuItemClickMiniBatchKMeans,id=id_MiniBatchKMeans)
				self.MiniBatchKMeans.Append(data_MiniBatchKMeans)

				id_AffinityPropagation = inc_id_counter()
				data_AffinityPropagation = AppPageMenuItem(self.AffinityPropagation, id=id_AffinityPropagation,text=str(dic["path"]))
				self.Bind(wx.EVT_MENU,data_AffinityPropagation.onMenuItemClickAffinityPropagation,id=id_AffinityPropagation)
				self.AffinityPropagation.Append(data_AffinityPropagation)

				id_MeanShift = inc_id_counter()
				data_MeanShift = AppPageMenuItem(self.MeanShift, id=id_MeanShift,text=str(dic["path"]))
				self.Bind(wx.EVT_MENU,data_MeanShift.onMenuItemClickMeanShift,id=id_MeanShift)
				self.MeanShift.Append(data_MeanShift)

				id_SpectralClustering = inc_id_counter()
				data_SpectralClustering = AppPageMenuItem(self.SpectralClustering, id=id_SpectralClustering,text=str(dic["path"]))
				self.Bind(wx.EVT_MENU,data_SpectralClustering.onMenuItemClickSpectralClustering,id=id_SpectralClustering)
				self.SpectralClustering.Append(data_SpectralClustering)

				id_Ward = inc_id_counter()
				data_Ward = AppPageMenuItem(self.Ward, id=id_Ward,text=str(dic["path"]))
				self.Bind(wx.EVT_MENU,data_Ward.onMenuItemClickWard,id=id_Ward)
				self.Ward.Append(data_Ward)

				id_AgglomerativeClustering = inc_id_counter()
				data_AgglomerativeClustering = AppPageMenuItem(self.AgglomerativeClustering, id=id_AgglomerativeClustering,text=str(dic["path"]))
				self.Bind(wx.EVT_MENU,data_AgglomerativeClustering.onMenuItemClickAgglomerativeClustering,id=id_AgglomerativeClustering)
				self.AgglomerativeClustering.Append(data_AgglomerativeClustering)

				id_DBSCAN = inc_id_counter()
				data_DBSCAN = AppPageMenuItem(self.DBSCAN, id=id_DBSCAN,text=str(dic["path"]))
				self.Bind(wx.EVT_MENU,data_DBSCAN.onMenuItemClickDBSCAN,id=id_DBSCAN)
				self.DBSCAN.Append(data_DBSCAN)

				id_OPTICS = inc_id_counter()
				data_OPTICS = AppPageMenuItem(self.OPTICS, id=id_OPTICS,text=str(dic["path"]))
				self.Bind(wx.EVT_MENU,data_OPTICS.onMenuItemClickOPTICS,id=id_OPTICS)
				self.OPTICS.Append(data_OPTICS)

				id_Birch = inc_id_counter()
				data_Birch = AppPageMenuItem(self.Birch, id=id_Birch,text=str(dic["path"]))
				self.Bind(wx.EVT_MENU,data_Birch.onMenuItemClickBirch,id=id_Birch)
				self.Birch.Append(data_Birch)

				id_GaussianMixture = inc_id_counter()
				data_GaussianMixture = AppPageMenuItem(self.GaussianMixture, id=id_GaussianMixture,text=str(dic["path"]))
				self.Bind(wx.EVT_MENU,data_GaussianMixture.onMenuItemClickGaussianMixture,id=id_GaussianMixture)
				self.GaussianMixture.Append(data_GaussianMixture)


class ExportCategory():
	def __init__(self,parent_menu, name):
		self.name = name
		self.parent_menu = parent_menu
		self.menu = wx.Menu()
		self.menu_item = parent_menu.AppendSubMenu(self.menu,self.name)
		self.menu.Append(wx.MenuItem(self.menu, id=0,text="EXECUTE BEFORE EXPORT DATA"))
		self.exports = {}


	def add_export(self,name,data):
		id = len(self.exports)
		if id == 0:
			self.clear_exports()
		self.exports[name] = data
		menu = wx.MenuItem(self.menu, id=id,text=name)
		self.menu.Bind(wx.EVT_MENU,partial(self.export_file_dialog,name),menu)
		self.menu.Append(menu)


	def clear_exports(self):
		for item in self.menu.GetMenuItems():
			self.menu.DestroyItem(item.Id)
			self.menu.Unbind(wx.EVT_MENU)
		name = "Export All"
		item = wx.MenuItem(self.menu, id=-1,text=name)
		self.menu.Bind(wx.EVT_MENU,self.export_folder_dialog,item)
		self.menu.Append(item)

	def export_folder_dialog(self,event):
		dialog = wx.DirDialog (None, "Choose output directory", "", wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
		if dialog.ShowModal() == wx.ID_CANCEL:
			return

		self.export_folder(dialog.GetPath())


	def export_folder(self,path):
		for name in self.exports:
			np.savetxt(os.path.join(path,name),self.exports[name])

		wx.adv.NotificationMessage('Saved successfully', message="Saved successfully")

	def export_file_dialog(self,name,event):
		dialog = wx.FileDialog(None, "Save file", wildcard="Csv files (*.csv)|*.csv",style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
		if dialog.ShowModal() == wx.ID_CANCEL:
			return
		self.export_file(dialog.GetPath(),name)


	def export_file(self,path,name):
		np.savetxt(path,self.exports[name])
		wx.adv.NotificationMessage('Saved successfully', message="Saved successfully")




	'''
	def save_data(self,name,event):
		dialog = wx.DirDialog (None, "Choose output directory", "", wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
		if dialog.ShowModal() == wx.ID_CANCEL:
			return

		path = dialog.GetPath()
		np.savetxt(os.path.join(path,name),self.exports[name])
		wx.adv.NotificationMessage('Saved successfully', message="Saved successfully")
	'''

	def __exit__(self, exc_type, exc_value, traceback):
		print('exited')


class BasePanel():
	def __init__(self, name, parent,data):
		self.parent = parent
		self.id = inc_id_counter()
		self.data = data['data']
		self.path = data['path']
		self.diagrams = {}
		self.categories = {}
		self.name = name
		self.tab_name = str(self.id) + ": " + self.name
		#name: data
		#
		#

		self.parent.notebook.AddPage(self, self.tab_name + ' on ' + self.path)

		self.menu = wx.Menu()
		self.menu_item = self.parent.export.AppendSubMenu(self.menu,self.tab_name)
		self.menu.Append(wx.MenuItem(self.menu, id=0,text="NO EXPORT AVAILABLE"))

		self.figure = None
		self.canvas = None
		self.toolbar = None
		self.figure_list = None
		self.updateFigure(0)

		print(self.name + " tab created")

	def add_category(self,name):
		if len(self.categories) == 0:
			self.clear_categories()
		category = ExportCategory(self.menu,name)
		self.categories[name] = category

	def add_export(self,category_name,name,data):
		category = self.categories[category_name]
		category.add_export(name,data)

	def clear_categories(self):
		for item in self.menu.GetMenuItems():
			self.menu.DestroyItem(item.Id)

	def clear_exports(self,category_name):
		category = self.categories[category_name]
		category.clear_exports()

	def onCloseButtonClick(self, event):
		self.parent.export.DestroyItem(self.menu_item)
		index = self.parent.notebook.GetSelection()
		self.parent.notebook.DeletePage(index)
		self.parent.notebook.SendSizeEvent()

	def clearOldFigures(self):
		if len(self.diagrams) > 0:
			self.toolbar.Destroy()
			self.canvas.Destroy()
			for name in self.diagrams:
				plt.close(self.diagrams[name])

	def updateFigure(self,figure_index):
		self.clearOldFigures()
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
		PanelLowerStar.__init__(self, parent=parent.notebook)
		BasePanel.__init__(self, name='LowerStar', parent=parent, data=data)

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

		wx.adv.NotificationMessage('Done', message="Done")
		self.diagrams = diagrams
		self.updateFigure(0)

	def onEntropyCheck(self, event):
		self.persistent_entropy = self.chx_entropy.IsChecked()

	def onWindowSizeSliderChange(self, event):
		self.overlap_slider.SetMax(self.window_size_slider.GetValue())

	def onFigureChange(self, event):
		self.updateFigure(self.figure_list.GetCurrentSelection())

class AppPanelRipser(PanelRipser,BasePanel):
	def __init__(self, parent,data):
		PanelRipser.__init__(self, parent=parent.notebook)
		BasePanel.__init__(self, name='Ripser', parent=parent, data=data)

		# Set Label
		self.label_shape.SetLabel(str(self.data.shape))

		# Execute button
		self.btn_execute.Bind(wx.EVT_BUTTON,self.onExecuteButtonClick)
		# Close button
		self.btn_close.Bind(wx.EVT_BUTTON,self.onCloseButtonClick)

		# Slider window size
		self.window_size_slider.Bind(wx.EVT_SCROLL,self.onWindowSizeSliderChange)
		self.window_size_slider.SetMax(self.data.shape[0])

		self.add_category('Windows')

	def onExecuteButtonClick(self, event):
		self.clear_exports('Windows')

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
			self.add_export('Windows','window'+str(i),dgms)
			i+=1

		wx.adv.NotificationMessage('Done', message="Done")
		self.diagrams = diagrams
		self.updateFigure(0)

	def onWindowSizeSliderChange(self, event):
		self.overlap_slider.SetMax(self.window_size_slider.GetValue())

	def onFigureChange(self, event):
		self.updateFigure(self.figure_list.GetCurrentSelection())



class AppPanelCorrMatDist(PanelCorrMatDist,BasePanel):
	def __init__(self, parent,data):
		PanelCorrMatDist.__init__(self, parent=parent.notebook)
		BasePanel.__init__(self, name='CorrMatDist', parent=parent, data=data)

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
			#print(window)
			wcorr = np.zeros((self.data.shape[1],self.data.shape[1])) #14x14
			#print(wcorr.shape)
			for i in range(self.data.shape[1]):
				for j in range(self.data.shape[1]):
					#print(self.data[window].shape,self.data[window][:,i].shape)
					coeff,pvalue = st.pearsonr(self.data[window][:,i],self.data[window][:,j])
					if coeff > 0 and pvalue < 0.05:
						#print('Written ('+str(i)+','+str(j)+') = '+str(coeff))
						wcorr[i,j] = coeff
			#print('wcorr',wcorr)
			WCorr.append(wcorr)
		#print('WCorr',len(WCorr))
		corrmatdist = np.zeros(shapes) #14x14
		#print(corrmatdist.shape)
		#for i,wc1 in enumerate(WCorr):
		#	if i < 14:
		#		for j,wc2 in enumerate(WCorr):
		#			if j < 14:
		#			    corrmatdist[i,j] = abs_distance(wc1,wc2)

		for i in range(0,len(WCorr)):
			for j in range(0,len(WCorr)):
				corrmatdist[i,j] = abs_distance(WCorr[i],WCorr[j])
				#print(corrmatdist[i,j])

		#print(corrmatdist)
		'''
		#### CORRELATION MATRICES AND Persistent Entropy ####
		print(self.data)
		W = matrix_window(self.data,window_size,window_size-overlap)
		WCorr = []
		print(W)
		shapes = (W.shape[0],W.shape[0])
		print(shapes)
		for w in W:
			#w is 14x100
			wcorr = np.zeros(shapes) #14x14
			for i in range(w.shape[0]):
				for j in range(w.shape[0]):
					coeff,pvalue = st.pearsonr(w[i,:],w[j,:])
					if coeff > 0 and pvalue < 0.05:
						wcorr[i,j] = coeff
			WCorr.append(wcorr)

		# for wc in WCorr:
		# 	G = nx.Graph()
		# 	G = nx.read_edgelist(to_edgelist(wc))
		# 	pos = nx.spring_layout(G)
		# 	nx.draw_networkx(G, pos)
		# 	nx.draw_networkx_edges(G, pos)
		# 	nx.draw_networkx_edge_labels(G,pos,edge_labels=nx.get_edge_attributes(G,'weight'))
		# 	plt.show()

		corrmatdist = np.zeros(shapes) #14x14
		for i,wc1 in enumerate(WCorr):
			if i < 14:
				for j,wc2 in enumerate(WCorr):
				    if j < 14:
				        corrmatdist[i,j]=abs_distance(wc1,wc2)
		'''

		#print('corrmatdist',corrmatdist)
		figure = plt.figure()
		plt.figure(figure.number)
		D = pairwise_distances(corrmatdist)
		#print('D',D)
		hoDgms = doRipsFiltration(D,maxHomDim=2,distance_matrix=True)
		#print('Ripser',hoDgms)
		Pers = persentropy(hoDgms)
		#print('Persentropy',Pers)
		plot_diagrams(hoDgms)
		diagrams['correlation_matrix'] = figure

		#distance1 sembra dare un risultato concreto
		#l'entropia in H1 è 0 e c'è un solo barcode
		wx.adv.NotificationMessage('Done', message="Done")
		self.diagrams = diagrams
		self.updateFigure(0)

	def onWindowSizeSliderChange(self, event):
		self.overlap_slider.SetMax(self.window_size_slider.GetValue())

	def onFigureChange(self, event):
		self.updateFigure(self.figure_list.GetCurrentSelection())
		

class AppPanelCorrMatHoles(PanelCorrMatHoles,BasePanel):
	def __init__(self, parent,data):
		PanelCorrMatHoles.__init__(self, parent=parent.notebook)
		BasePanel.__init__(self, name='CorrMatHoles', parent=parent, data=data)

		# Set Label
		self.label_shape.SetLabel(str(self.data.shape))

		self.btn_open_folder.Bind(wx.EVT_BUTTON,self.onSelectFolder)

		# Execute button
		self.btn_execute.Bind(wx.EVT_BUTTON,self.onExecuteButtonClick)
		# Close button
		self.btn_close.Bind(wx.EVT_BUTTON,self.onCloseButtonClick)


		# Slider window size
		self.window_size_slider.Bind(wx.EVT_SCROLL,self.onWindowSizeSliderChange)
		self.window_size_slider.SetMax(self.data.shape[0])

		self.updateFigure(0)

	def onExportPikle(self,event):
		dialog = wx.DirDialog (None, "Choose output directory", "", wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
		if dialog.ShowModal() == wx.ID_CANCEL:
			return
		self.txt_open_folder.SetValue(dialog.GetPath())

	def onSelectFolder(self,event):
		dialog = wx.DirDialog (None, "Choose output directory", "", wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
		if dialog.ShowModal() == wx.ID_CANCEL:
			return
		self.txt_open_folder.SetValue(dialog.GetPath())

	def onExecuteButtonClick(self, event):
		overlap = self.overlap_slider.GetValue()
		window_size = self.window_size_slider.GetValue()
		windows = calculate_windows(window_size,overlap,self.data.shape[0])
		output_path = self.txt_open_folder.GetValue()
		if not os.path.isdir(output_path):
			wx.adv.NotificationMessage('Error', message="Output directory does not exist")
			print('Output directory does not exist')
			return
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
				ho.persistent_homology_calculation(os.path.join(output_path,"clique-%d.pkl"%(i)), 1, "matrices", ".")
				Fil.append(cliqueDict)
				#diagrams['window'+str(i)] = figure


		wx.adv.NotificationMessage('Done', message="Done")
		self.diagrams = diagrams
		self.updateFigure(0)

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


class AppPanelSpikes(PanelSpikes,BasePanel):
	def __init__(self, parent,data):
		PanelSpikes.__init__(self, parent=parent.notebook)
		BasePanel.__init__(self, name='Spikes', parent=parent, data=data)

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
		threshold = self.threshold_slider.GetValue()
		windows = calculate_windows(window_size,overlap,self.data.shape[0])
		diagrams = {}

		spikes_list = spikes(self.data,window=(window_size,overlap),threshold=threshold)

		print('Plotting results...')
		cols = np.ceil(np.sqrt(spikes_list.shape[1]))
		rows = np.ceil(spikes_list.shape[1]/cols)
		for i in range(0,spikes_list.shape[1]):
			figure = plt.figure()
			plt.figure(figure.number)
			plt.ylim(-1,1)
			plt.xlabel('Time')
			plt.ylabel('Direction')
			plt.plot(spikes_list[:,i])
			diagrams['Spikes on signal '+str(i)] = figure
		print('Results plotted')

		wx.adv.NotificationMessage('Done', message="Done")
		self.diagrams = diagrams
		self.updateFigure(0)

	def onWindowSizeSliderChange(self, event):
		self.overlap_slider.SetMax(self.window_size_slider.GetValue())

	def onFigureChange(self, event):
		self.updateFigure(self.figure_list.GetCurrentSelection())

class AppPanelMiniBatchKMeans(PanelMiniBatchKMeans,BasePanel):
	def __init__(self, parent,data):
		PanelMiniBatchKMeans.__init__(self, parent=parent.notebook)
		BasePanel.__init__(self, name='MiniBatchKMeans', parent=parent, data=data)

		# Set Label
		self.label_shape.SetLabel(str(self.data.shape))

		# Execute button
		self.btn_execute.Bind(wx.EVT_BUTTON,self.onExecuteButtonClick)
		# Close button
		self.btn_close.Bind(wx.EVT_BUTTON,self.onCloseButtonClick)

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
		nclusters = int(self.ncluster_textctrl.GetValue())
		if nclusters < 2:
			print("Error: Number of clusters must be greater then 2")
			return
		signal_index = self.ch_signal.GetCurrentSelection()

		diagrams = {}
		name = 'MiniBatchKMeans'
		data = self.data[:,signal_index]
		time_line = np.arange(len(data))
		timed_data = np.vstack((time_line,data)).transpose()

		algorithm = cluster.MiniBatchKMeans(n_clusters=nclusters)
		figure = plt.figure()
		plt.figure(figure.number)

		plot_cluster(name,algorithm,timed_data)

		diagrams[name] = figure

		wx.adv.NotificationMessage('Done', message="Done")
		self.diagrams = diagrams
		self.updateFigure(0)

	def onWindowSizeSliderChange(self, event):
		self.overlap_slider.SetMax(self.window_size_slider.GetValue())

	def onFigureChange(self, event):
		self.updateFigure(self.figure_list.GetCurrentSelection())

class AppPanelAffinityPropagation(PanelAffinityPropagation,BasePanel):
	def __init__(self, parent,data):
		PanelAffinityPropagation.__init__(self, parent=parent.notebook)
		BasePanel.__init__(self, name='AffinityPropagation', parent=parent, data=data)

		# Set Label
		self.label_shape.SetLabel(str(self.data.shape))

		# Execute button
		self.btn_execute.Bind(wx.EVT_BUTTON,self.onExecuteButtonClick)
		# Close button
		self.btn_close.Bind(wx.EVT_BUTTON,self.onCloseButtonClick)

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
		damping = float(self.damping_textctrl.GetValue())
		preference = int(self.preference_textctrl.GetValue())
		signal_index = self.ch_signal.GetCurrentSelection()

		diagrams = {}
		name = 'AffinityPropagation'
		data = self.data[:,signal_index]
		time_line = np.arange(len(data))
		timed_data = np.vstack((time_line,data)).transpose()

		algorithm = cluster.AffinityPropagation(damping=damping, preference=preference)
		figure = plt.figure()
		plt.figure(figure.number)

		plot_cluster(name,algorithm,timed_data)

		diagrams[name] = figure

		wx.adv.NotificationMessage('Done', message="Done")
		self.diagrams = diagrams
		self.updateFigure(0)

	def onWindowSizeSliderChange(self, event):
		self.overlap_slider.SetMax(self.window_size_slider.GetValue())

	def onFigureChange(self, event):
		self.updateFigure(self.figure_list.GetCurrentSelection())



class AppPanelMeanShift(PanelMeanShift,BasePanel):
	def __init__(self, parent,data):
		PanelMeanShift.__init__(self, parent=parent.notebook)
		BasePanel.__init__(self, name='MeanShift', parent=parent, data=data)

		# Set Label
		self.label_shape.SetLabel(str(self.data.shape))

		# Execute button
		self.btn_execute.Bind(wx.EVT_BUTTON,self.onExecuteButtonClick)
		# Close button
		self.btn_close.Bind(wx.EVT_BUTTON,self.onCloseButtonClick)

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
		quantile = float(self.quantile_textctrl.GetValue())
		signal_index = self.ch_signal.GetCurrentSelection()

		diagrams = {}
		name = 'MeanShift'
		data = self.data[:,signal_index]
		time_line = np.arange(len(data))
		timed_data = np.vstack((time_line,data)).transpose()

		bandwidth = cluster.estimate_bandwidth(timed_data, quantile=quantile)
		algorithm = cluster.MeanShift(bandwidth=bandwidth, bin_seeding=True)
		figure = plt.figure()
		plt.figure(figure.number)

		plot_cluster(name,algorithm,timed_data)

		diagrams[name] = figure

		wx.adv.NotificationMessage('Done', message="Done")
		self.diagrams = diagrams
		self.updateFigure(0)

	def onWindowSizeSliderChange(self, event):
		self.overlap_slider.SetMax(self.window_size_slider.GetValue())

	def onFigureChange(self, event):
		self.updateFigure(self.figure_list.GetCurrentSelection())



class AppPanelSpectralClustering(PanelSpectralClustering,BasePanel):
	def __init__(self, parent,data):
		PanelSpectralClustering.__init__(self, parent=parent.notebook)
		BasePanel.__init__(self, name='SpectralClustering', parent=parent, data=data)

		# Set Label
		self.label_shape.SetLabel(str(self.data.shape))

		# Execute button
		self.btn_execute.Bind(wx.EVT_BUTTON,self.onExecuteButtonClick)
		# Close button
		self.btn_close.Bind(wx.EVT_BUTTON,self.onCloseButtonClick)

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
		nclusters = int(self.ncluster_textctrl.GetValue())
		if nclusters < 2:
			print("Error: Number of clusters must be greater then 2")
			return
		signal_index = self.ch_signal.GetCurrentSelection()
		diagrams = {}
		name = 'SpectralClustering'
		data = self.data[:,signal_index]
		time_line = np.arange(len(data))
		timed_data = np.vstack((time_line,data)).transpose()

		algorithm = cluster.SpectralClustering(n_clusters=nclusters, eigen_solver='arpack',affinity="nearest_neighbors")
		figure = plt.figure()
		plt.figure(figure.number)

		plot_cluster(name,algorithm,timed_data)

		diagrams[name] = figure

		wx.adv.NotificationMessage('Done', message="Done")
		self.diagrams = diagrams
		self.updateFigure(0)

	def onWindowSizeSliderChange(self, event):
		self.overlap_slider.SetMax(self.window_size_slider.GetValue())

	def onFigureChange(self, event):
		self.updateFigure(self.figure_list.GetCurrentSelection())



class AppPanelWard(PanelWard,BasePanel):
	def __init__(self, parent,data):
		PanelWard.__init__(self, parent=parent.notebook)
		BasePanel.__init__(self, name='Ward', parent=parent, data=data)

		# Set Label
		self.label_shape.SetLabel(str(self.data.shape))

		# Execute button
		self.btn_execute.Bind(wx.EVT_BUTTON,self.onExecuteButtonClick)
		# Close button
		self.btn_close.Bind(wx.EVT_BUTTON,self.onCloseButtonClick)

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
		nclusters = int(self.ncluster_textctrl.GetValue())
		if nclusters < 2:
			print("Error: Number of clusters must be greater then 2")
			return
		neighbors = int(self.neighbors_textctrl.GetValue())
		signal_index = self.ch_signal.GetCurrentSelection()
		diagrams = {}
		name = 'Ward'
		data = self.data[:,signal_index]
		time_line = np.arange(len(data))
		timed_data = np.vstack((time_line,data)).transpose()

		connectivity = kneighbors_graph(timed_data, n_neighbors=neighbors, include_self=False)
		algorithm = cluster.AgglomerativeClustering(n_clusters=nclusters, linkage='ward',connectivity=connectivity)
		figure = plt.figure()
		plt.figure(figure.number)

		plot_cluster(name,algorithm,timed_data)

		diagrams[name] = figure

		wx.adv.NotificationMessage('Done', message="Done")
		self.diagrams = diagrams
		self.updateFigure(0)

	def onWindowSizeSliderChange(self, event):
		self.overlap_slider.SetMax(self.window_size_slider.GetValue())

	def onFigureChange(self, event):
		self.updateFigure(self.figure_list.GetCurrentSelection())



class AppPanelAgglomerativeClustering(PanelAgglomerativeClustering,BasePanel):
	def __init__(self, parent,data):
		PanelAgglomerativeClustering.__init__(self, parent=parent.notebook)
		BasePanel.__init__(self, name='AgglomerativeClustering', parent=parent, data=data)

		# Set Label
		self.label_shape.SetLabel(str(self.data.shape))

		# Execute button
		self.btn_execute.Bind(wx.EVT_BUTTON,self.onExecuteButtonClick)
		# Close button
		self.btn_close.Bind(wx.EVT_BUTTON,self.onCloseButtonClick)

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
		nclusters = int(self.ncluster_textctrl.GetValue())
		if nclusters < 2:
			print("Error: Number of clusters must be greater then 2")
			return
		neighbors = int(self.neighbors_textctrl.GetValue())
		signal_index = self.ch_signal.GetCurrentSelection()
		diagrams = {}
		name = 'AgglomerativeClustering'
		data = self.data[:,signal_index]
		time_line = np.arange(len(data))
		timed_data = np.vstack((time_line,data)).transpose()

		connectivity = kneighbors_graph(timed_data, n_neighbors=neighbors, include_self=False)
		algorithm = cluster.AgglomerativeClustering(linkage="average", affinity="cityblock",n_clusters=nclusters, connectivity=connectivity)
		figure = plt.figure()
		plt.figure(figure.number)

		plot_cluster(name,algorithm,timed_data)

		diagrams[name] = figure

		wx.adv.NotificationMessage('Done', message="Done")
		self.diagrams = diagrams
		self.updateFigure(0)

	def onWindowSizeSliderChange(self, event):
		self.overlap_slider.SetMax(self.window_size_slider.GetValue())

	def onFigureChange(self, event):
		self.updateFigure(self.figure_list.GetCurrentSelection())



class AppPanelDBSCAN(PanelDBSCAN,BasePanel):
	def __init__(self, parent,data):
		PanelDBSCAN.__init__(self, parent=parent.notebook)
		BasePanel.__init__(self, name='DBSCAN', parent=parent, data=data)

		# Set Label
		self.label_shape.SetLabel(str(self.data.shape))

		# Execute button
		self.btn_execute.Bind(wx.EVT_BUTTON,self.onExecuteButtonClick)
		# Close button
		self.btn_close.Bind(wx.EVT_BUTTON,self.onCloseButtonClick)

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
		eps = float(self.eps_textctrl.GetValue())
		signal_index = self.ch_signal.GetCurrentSelection()
		diagrams = {}
		name = 'DBSCAN'
		data = self.data[:,signal_index]
		time_line = np.arange(len(data))
		timed_data = np.vstack((time_line,data)).transpose()

		algorithm = cluster.DBSCAN(eps=eps)
		figure = plt.figure()
		plt.figure(figure.number)

		plot_cluster(name,algorithm,timed_data)

		diagrams[name] = figure

		wx.adv.NotificationMessage('Done', message="Done")
		self.diagrams = diagrams
		self.updateFigure(0)

	def onWindowSizeSliderChange(self, event):
		self.overlap_slider.SetMax(self.window_size_slider.GetValue())

	def onFigureChange(self, event):
		self.updateFigure(self.figure_list.GetCurrentSelection())



class AppPanelOPTICS(PanelOPTICS,BasePanel):
	def __init__(self, parent,data):
		PanelOPTICS.__init__(self, parent=parent.notebook)
		BasePanel.__init__(self, name='OPTICS', parent=parent, data=data)

		# Set Label
		self.label_shape.SetLabel(str(self.data.shape))

		# Execute button
		self.btn_execute.Bind(wx.EVT_BUTTON,self.onExecuteButtonClick)
		# Close button
		self.btn_close.Bind(wx.EVT_BUTTON,self.onCloseButtonClick)

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
		min_samples = int(self.min_samples_textctrl.GetValue())
		xi = float(self.xi_textctrl.GetValue())
		min_cluster_size = float(self.min_cluster_size_textctrl.GetValue())
		signal_index = self.ch_signal.GetCurrentSelection()
		diagrams = {}
		name = 'OPTICS'
		data = self.data[:,signal_index]
		time_line = np.arange(len(data))
		timed_data = np.vstack((time_line,data)).transpose()

		algorithm = cluster.OPTICS(min_samples=min_samples,xi=xi,min_cluster_size=min_cluster_size)
		figure = plt.figure()
		plt.figure(figure.number)

		plot_cluster(name,algorithm,timed_data)

		diagrams[name] = figure

		wx.adv.NotificationMessage('Done', message="Done")
		self.diagrams = diagrams
		self.updateFigure(0)

	def onWindowSizeSliderChange(self, event):
		self.overlap_slider.SetMax(self.window_size_slider.GetValue())

	def onFigureChange(self, event):
		self.updateFigure(self.figure_list.GetCurrentSelection())



class AppPanelBirch(PanelBirch,BasePanel):
	def __init__(self, parent,data):
		PanelBirch.__init__(self, parent=parent.notebook)
		BasePanel.__init__(self, name='Birch', parent=parent, data=data)

		# Set Label
		self.label_shape.SetLabel(str(self.data.shape))

		# Execute button
		self.btn_execute.Bind(wx.EVT_BUTTON,self.onExecuteButtonClick)
		# Close button
		self.btn_close.Bind(wx.EVT_BUTTON,self.onCloseButtonClick)

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
		nclusters = int(self.ncluster_textctrl.GetValue())
		if nclusters < 2:
			print("Error: Number of clusters must be greater then 2")
			return
		signal_index = self.ch_signal.GetCurrentSelection()
		diagrams = {}
		name = 'Birch'
		data = self.data[:,signal_index]
		time_line = np.arange(len(data))
		timed_data = np.vstack((time_line,data)).transpose()

		algorithm = cluster.Birch(n_clusters=nclusters)
		figure = plt.figure()
		plt.figure(figure.number)

		plot_cluster(name,algorithm,timed_data)

		diagrams[name] = figure

		wx.adv.NotificationMessage('Done', message="Done")
		self.diagrams = diagrams
		self.updateFigure(0)

	def onWindowSizeSliderChange(self, event):
		self.overlap_slider.SetMax(self.window_size_slider.GetValue())

	def onFigureChange(self, event):
		self.updateFigure(self.figure_list.GetCurrentSelection())



class AppPanelGaussianMixture(PanelGaussianMixture,BasePanel):
	def __init__(self, parent,data):
		PanelGaussianMixture.__init__(self, parent=parent.notebook)
		BasePanel.__init__(self, name='GaussianMixture', parent=parent, data=data)

		# Set Label
		self.label_shape.SetLabel(str(self.data.shape))

		# Execute button
		self.btn_execute.Bind(wx.EVT_BUTTON,self.onExecuteButtonClick)
		# Close button
		self.btn_close.Bind(wx.EVT_BUTTON,self.onCloseButtonClick)

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
		nclusters = int(self.ncluster_textctrl.GetValue())
		if nclusters < 2:
			print("Error: Number of clusters must be greater then 2")
			return
		signal_index = self.ch_signal.GetCurrentSelection()
		diagrams = {}
		name = 'GaussianMixture'
		data = self.data[:,signal_index]
		time_line = np.arange(len(data))
		timed_data = np.vstack((time_line,data)).transpose()

		algorithm = mixture.GaussianMixture(n_components=nclusters, covariance_type='full')
		figure = plt.figure()
		plt.figure(figure.number)

		plot_cluster(name,algorithm,timed_data)

		diagrams[name] = figure

		wx.adv.NotificationMessage('Done', message="Done")
		self.diagrams = diagrams
		self.updateFigure(0)

	def onWindowSizeSliderChange(self, event):
		self.overlap_slider.SetMax(self.window_size_slider.GetValue())

	def onFigureChange(self, event):
		self.updateFigure(self.figure_list.GetCurrentSelection())
		
