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
from export import *

#Panels
from panels.affinity_propagation_panel import AppPanelAffinityPropagation
from panels.agglomerative_clustering_panel import AppPanelAgglomerativeClustering
from panels.birch_panel import AppPanelBirch
from panels.corr_mat_dist_panel import AppPanelCorrMatDist
from panels.corr_mat_holes_panel import AppPanelCorrMatHoles
from panels.dbscan_panel import AppPanelDBSCAN
from panels.gaussian_mixture_panel import AppPanelGaussianMixture
from panels.lower_star_panel import AppPanelLowerStar
from panels.mean_shift_panel import AppPanelMeanShift
from panels.mini_batch_kmeans_panel import AppPanelMiniBatchKMeans
from panels.optics_panel import AppPanelOPTICS
from panels.ripser_panel import AppPanelRipser
from panels.spectral_clustering_panel import AppPanelSpectralClustering
from panels.spikes_panel import AppPanelSpikes
from panels.ward_panel import AppPanelWard

#se la periodicità del segnale che vedo nella rappresentazione dopo le sliding windows si ripete per tutte le serie di punti piu o meno nelle stesse posizioni (correlazione verticale delle sliding window) significa che in quei punti qualcosa sta succedendo (si suppone proteine che vanno in folding)
from functools import partial


#from ripser import PanelRipser




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


