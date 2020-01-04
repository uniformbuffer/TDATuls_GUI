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

#se la periodicità del segnale che vedo nella rappresentazione dopo le sliding windows si ripete per tutte le serie di punti piu o meno nelle stesse posizioni (correlazione verticale delle sliding window) significa che in quei punti qualcosa sta succedendo (si suppone proteine che vanno in folding)
from functools import partial


ID = 0
def get_id():
	global ID
	ID += 1
	return ID

class BasePanel():
	def __init__(self, name, parent,data):
		self.parent = parent
		self.id = get_id()
		self.data = data['data']

	#	if len(self.data.shape) < 2:
	#		self.data = self.data.reshape((self.data.shape[0],1)).transpose()

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
		self.menu.Append(wx.MenuItem(self.menu, id=1,text="EXECUTE BEFORE EXPORT"))

		self.figure = None
		self.canvas = None
		self.toolbar = None
		self.figure_list = None
		self.updateFigure(0)

		print(self.name + " tab created")

	def add_export(self,category_name,name,data):
		if not (category_name in self.categories):
			if len(self.categories) == 0:
				self.clear_categories()
			category = ExportCategory(self.menu,category_name)
			self.categories[category_name] = category
		category = self.categories[category_name]
		category.add_export(name,data)

	def clear_categories(self):
		for item in self.menu.GetMenuItems():
			self.menu.DestroyItem(item.Id)

	def clear_exports(self):
		self.categories = {}
		for item in self.menu.GetMenuItems():
			self.menu.DestroyItem(item.Id)
		#if category_name in self.categories:
		#	category = self.categories[category_name]
		#	category.clear_exports()

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


