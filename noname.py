# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.9.0 Dec  2 2019)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

ID_IMPORT_DATA = 1000
ID_AS_PNG = 1001
ID_ALL_DIAGRAMS = 1002
ID_ALL_PERSISTENT_ENTROPIES = 1003
ID_ALL_NORMALIZED_ENTROPIES = 1004
ID_ALL_CORRELATION_MATRICES = 1005
ID_ALL_CORRELATION_MATRICES_AS_EDGELIST = 1006
ID_IMPORT_DATA_BEFORE_USE = 1007
ID_ABOUT = 1008

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"TDATuls", pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		self.main_menu = wx.MenuBar( 0 )
		self.file = wx.Menu()
		self.importData = wx.MenuItem( self.file, ID_IMPORT_DATA, u"Import Data", wx.EmptyString, wx.ITEM_NORMAL )
		self.file.Append( self.importData )

		self.export = wx.Menu()
		self.asPng = wx.MenuItem( self.export, ID_AS_PNG, u"As png", wx.EmptyString, wx.ITEM_NORMAL )
		self.export.Append( self.asPng )

		self.allDiagrams = wx.MenuItem( self.export, ID_ALL_DIAGRAMS, u"All Diagrams", wx.EmptyString, wx.ITEM_NORMAL )
		self.export.Append( self.allDiagrams )

		self.allPersistentEntropies = wx.MenuItem( self.export, ID_ALL_PERSISTENT_ENTROPIES, u"All Persistent Entropies", wx.EmptyString, wx.ITEM_NORMAL )
		self.export.Append( self.allPersistentEntropies )

		self.allNormalizedEntropies = wx.MenuItem( self.export, ID_ALL_NORMALIZED_ENTROPIES, u"All Normalized Entropies", wx.EmptyString, wx.ITEM_NORMAL )
		self.export.Append( self.allNormalizedEntropies )

		self.allCorrelationMatrices = wx.MenuItem( self.export, ID_ALL_CORRELATION_MATRICES, u"All Correlation Matrices", wx.EmptyString, wx.ITEM_NORMAL )
		self.export.Append( self.allCorrelationMatrices )

		self.allCorrelationMatricesAsEdgelist = wx.MenuItem( self.export, ID_ALL_CORRELATION_MATRICES_AS_EDGELIST, u"All Correlation Matrices as Edgelist", wx.EmptyString, wx.ITEM_NORMAL )
		self.export.Append( self.allCorrelationMatricesAsEdgelist )

		self.file.AppendSubMenu( self.export, u"Export" )

		self.file.AppendSeparator()

		self.main_menu.Append( self.file, u"File" )

		self.newOperation = wx.Menu()
		self.slidingWindow = wx.Menu()
		self.lowerStar = wx.Menu()
		self.importDataBeforeUse = wx.MenuItem( self.lowerStar, ID_IMPORT_DATA_BEFORE_USE, u"IMPORT DATA BEFORE USE", wx.EmptyString, wx.ITEM_NORMAL )
		self.lowerStar.Append( self.importDataBeforeUse )

		self.slidingWindow.AppendSubMenu( self.lowerStar, u"Lower Star" )

		self.ripser = wx.Menu()
		self.importDataBeforeUse = wx.MenuItem( self.ripser, ID_IMPORT_DATA_BEFORE_USE, u"IMPORT DATA BEFORE USE", wx.EmptyString, wx.ITEM_NORMAL )
		self.ripser.Append( self.importDataBeforeUse )

		self.slidingWindow.AppendSubMenu( self.ripser, u"Ripser" )

		self.spikes = wx.Menu()
		self.importDataBeforeUse1 = wx.MenuItem( self.spikes, ID_IMPORT_DATA_BEFORE_USE, u"IMPORT DATA BEFORE USE", wx.EmptyString, wx.ITEM_NORMAL )
		self.spikes.Append( self.importDataBeforeUse1 )

		self.slidingWindow.AppendSubMenu( self.spikes, u"Spikes" )

		self.newOperation.AppendSubMenu( self.slidingWindow, u"Sliding Window" )

		self.correlationMatrix = wx.Menu()
		self.distanceMatrix = wx.Menu()
		self.importDataBeforeUse = wx.MenuItem( self.distanceMatrix, ID_IMPORT_DATA_BEFORE_USE, u"IMPORT DATA BEFORE USE", wx.EmptyString, wx.ITEM_NORMAL )
		self.distanceMatrix.Append( self.importDataBeforeUse )

		self.correlationMatrix.AppendSubMenu( self.distanceMatrix, u"Distance Matrix" )

		self.holes = wx.Menu()
		self.importDataBeforeUse = wx.MenuItem( self.holes, ID_IMPORT_DATA_BEFORE_USE, u"IMPORT DATA BEFORE USE", wx.EmptyString, wx.ITEM_NORMAL )
		self.holes.Append( self.importDataBeforeUse )

		self.correlationMatrix.AppendSubMenu( self.holes, u"Holes" )

		self.newOperation.AppendSubMenu( self.correlationMatrix, u"Correlation Matrix" )

		self.cluster = wx.Menu()
		self.MiniBatchKMeans = wx.Menu()
		self.importDataBeforeUse2 = wx.MenuItem( self.MiniBatchKMeans, ID_IMPORT_DATA_BEFORE_USE, u"IMPORT DATA BEFORE USE", wx.EmptyString, wx.ITEM_NORMAL )
		self.MiniBatchKMeans.Append( self.importDataBeforeUse2 )

		self.cluster.AppendSubMenu( self.MiniBatchKMeans, u"MiniBatchKMeans" )

		self.AffinityPropagation = wx.Menu()
		self.importDataBeforeUse21 = wx.MenuItem( self.AffinityPropagation, ID_IMPORT_DATA_BEFORE_USE, u"IMPORT DATA BEFORE USE", wx.EmptyString, wx.ITEM_NORMAL )
		self.AffinityPropagation.Append( self.importDataBeforeUse21 )

		self.cluster.AppendSubMenu( self.AffinityPropagation, u"AffinityPropagation" )

		self.MeanShift = wx.Menu()
		self.importDataBeforeUse22 = wx.MenuItem( self.MeanShift, ID_IMPORT_DATA_BEFORE_USE, u"IMPORT DATA BEFORE USE", wx.EmptyString, wx.ITEM_NORMAL )
		self.MeanShift.Append( self.importDataBeforeUse22 )

		self.cluster.AppendSubMenu( self.MeanShift, u"MeanShift" )

		self.SpectralClustering = wx.Menu()
		self.importDataBeforeUse221 = wx.MenuItem( self.SpectralClustering, ID_IMPORT_DATA_BEFORE_USE, u"IMPORT DATA BEFORE USE", wx.EmptyString, wx.ITEM_NORMAL )
		self.SpectralClustering.Append( self.importDataBeforeUse221 )

		self.cluster.AppendSubMenu( self.SpectralClustering, u"SpectralClustering" )

		self.Ward = wx.Menu()
		self.importDataBeforeUse222 = wx.MenuItem( self.Ward, ID_IMPORT_DATA_BEFORE_USE, u"IMPORT DATA BEFORE USE", wx.EmptyString, wx.ITEM_NORMAL )
		self.Ward.Append( self.importDataBeforeUse222 )

		self.cluster.AppendSubMenu( self.Ward, u"Ward" )

		self.AgglomerativeClustering = wx.Menu()
		self.importDataBeforeUse223 = wx.MenuItem( self.AgglomerativeClustering, ID_IMPORT_DATA_BEFORE_USE, u"IMPORT DATA BEFORE USE", wx.EmptyString, wx.ITEM_NORMAL )
		self.AgglomerativeClustering.Append( self.importDataBeforeUse223 )

		self.cluster.AppendSubMenu( self.AgglomerativeClustering, u"AgglomerativeClustering" )

		self.DBSCAN = wx.Menu()
		self.importDataBeforeUse224 = wx.MenuItem( self.DBSCAN, ID_IMPORT_DATA_BEFORE_USE, u"IMPORT DATA BEFORE USE", wx.EmptyString, wx.ITEM_NORMAL )
		self.DBSCAN.Append( self.importDataBeforeUse224 )

		self.cluster.AppendSubMenu( self.DBSCAN, u"DBSCAN" )

		self.OPTICS = wx.Menu()
		self.importDataBeforeUse225 = wx.MenuItem( self.OPTICS, ID_IMPORT_DATA_BEFORE_USE, u"IMPORT DATA BEFORE USE", wx.EmptyString, wx.ITEM_NORMAL )
		self.OPTICS.Append( self.importDataBeforeUse225 )

		self.cluster.AppendSubMenu( self.OPTICS, u"OPTICS" )

		self.Birch = wx.Menu()
		self.importDataBeforeUse2251 = wx.MenuItem( self.Birch, ID_IMPORT_DATA_BEFORE_USE, u"IMPORT DATA BEFORE USE", wx.EmptyString, wx.ITEM_NORMAL )
		self.Birch.Append( self.importDataBeforeUse2251 )

		self.cluster.AppendSubMenu( self.Birch, u"Birch" )

		self.GaussianMixture = wx.Menu()
		self.importDataBeforeUse2252 = wx.MenuItem( self.GaussianMixture, ID_IMPORT_DATA_BEFORE_USE, u"IMPORT DATA BEFORE USE", wx.EmptyString, wx.ITEM_NORMAL )
		self.GaussianMixture.Append( self.importDataBeforeUse2252 )

		self.cluster.AppendSubMenu( self.GaussianMixture, u"GaussianMixture" )

		self.newOperation.AppendSubMenu( self.cluster, u"Cluster" )

		self.main_menu.Append( self.newOperation, u"New Operation" )

		self.export = wx.Menu()
		self.main_menu.Append( self.export, u"Export" )

		self.help = wx.Menu()
		self.about = wx.MenuItem( self.help, ID_ABOUT, u"About", wx.EmptyString, wx.ITEM_NORMAL )
		self.help.Append( self.about )

		self.main_menu.Append( self.help, u"Help" )

		self.SetMenuBar( self.main_menu )

		notebookSizerDELETEMEAFTER = wx.BoxSizer( wx.VERTICAL )

		self.panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		notebookSizerDELETEMEAFTER.Add( self.panel, 1, wx.EXPAND|wx.ALL, 5 )


		self.SetSizer( notebookSizerDELETEMEAFTER )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_MENU, self.importDataOnMenuSelection, id = self.importData.GetId() )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def importDataOnMenuSelection( self, event ):
		event.Skip()


###########################################################################
## Class PanelLowerStar
###########################################################################

class PanelLowerStar ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		mainSizer = wx.BoxSizer( wx.VERTICAL )

		self.scrolled_window = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.VSCROLL )
		self.scrolled_window.SetScrollRate( 5, 5 )
		scrolled_sizer = wx.FlexGridSizer( 2, 1, 30, 30 )
		scrolled_sizer.SetFlexibleDirection( wx.BOTH )
		scrolled_sizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		canvasSizer = wx.FlexGridSizer( 0, 2, 0, 10 )
		canvasSizer.SetFlexibleDirection( wx.BOTH )
		canvasSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		mainCanvasSizer = wx.BoxSizer( wx.VERTICAL )


		canvasSizer.Add( mainCanvasSizer, 1, wx.EXPAND, 5 )

		optionalCanvasSizer = wx.BoxSizer( wx.VERTICAL )


		canvasSizer.Add( optionalCanvasSizer, 1, wx.EXPAND, 5 )


		scrolled_sizer.Add( canvasSizer, 1, wx.EXPAND, 5 )

		settingsSizer = wx.FlexGridSizer( 0, 2, 0, 0 )
		settingsSizer.SetFlexibleDirection( wx.BOTH )
		settingsSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText10 = wx.StaticText( self.scrolled_window, wx.ID_ANY, u"Dataset shape:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )

		settingsSizer.Add( self.m_staticText10, 0, wx.ALL, 5 )

		self.label_shape = wx.StaticText( self.scrolled_window, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_shape.Wrap( -1 )

		settingsSizer.Add( self.label_shape, 0, wx.ALL, 5 )

		self.m_staticText19 = wx.StaticText( self.scrolled_window, wx.ID_ANY, u"Select signal:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText19.Wrap( -1 )

		settingsSizer.Add( self.m_staticText19, 0, wx.ALL, 5 )

		ch_signalChoices = []
		self.ch_signal = wx.Choice( self.scrolled_window, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, ch_signalChoices, 0 )
		self.ch_signal.SetSelection( 0 )
		settingsSizer.Add( self.ch_signal, 0, wx.ALL, 5 )

		self.m_staticText1 = wx.StaticText( self.scrolled_window, wx.ID_ANY, u"Window Size:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )

		settingsSizer.Add( self.m_staticText1, 0, wx.ALL, 5 )

		self.window_size_slider = wx.Slider( self.scrolled_window, wx.ID_ANY, 50, 1, 100, wx.DefaultPosition, wx.Size( 200,-1 ), wx.SL_HORIZONTAL|wx.SL_VALUE_LABEL )
		settingsSizer.Add( self.window_size_slider, 0, wx.ALL, 5 )

		self.m_staticText2 = wx.StaticText( self.scrolled_window, wx.ID_ANY, u"Overlap:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )

		settingsSizer.Add( self.m_staticText2, 0, wx.ALL, 5 )

		self.overlap_slider = wx.Slider( self.scrolled_window, wx.ID_ANY, 0, 0, 100, wx.DefaultPosition, wx.Size( 200,-1 ), wx.SL_HORIZONTAL|wx.SL_VALUE_LABEL )
		settingsSizer.Add( self.overlap_slider, 0, wx.ALL, 5 )

		self.chx_entropy = wx.CheckBox( self.scrolled_window, wx.ID_ANY, u"Pers. Entropy", wx.DefaultPosition, wx.DefaultSize, 0 )
		settingsSizer.Add( self.chx_entropy, 0, wx.ALL, 5 )

		ch_pe_signalChoices = []
		self.ch_pe_signal = wx.Choice( self.scrolled_window, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, ch_pe_signalChoices, 0 )
		self.ch_pe_signal.SetSelection( 0 )
		self.ch_pe_signal.Hide()

		settingsSizer.Add( self.ch_pe_signal, 0, wx.ALL, 5 )

		self.btn_execute = wx.Button( self.scrolled_window, wx.ID_ANY, u"Execute", wx.DefaultPosition, wx.DefaultSize, 0 )
		settingsSizer.Add( self.btn_execute, 0, wx.ALL, 5 )

		self.btn_close = wx.Button( self.scrolled_window, wx.ID_ANY, u"Close Tab", wx.DefaultPosition, wx.DefaultSize, 0 )
		settingsSizer.Add( self.btn_close, 0, wx.ALL, 5 )


		scrolled_sizer.Add( settingsSizer, 1, wx.EXPAND, 5 )


		self.scrolled_window.SetSizer( scrolled_sizer )
		self.scrolled_window.Layout()
		scrolled_sizer.Fit( self.scrolled_window )
		mainSizer.Add( self.scrolled_window, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizer( mainSizer )
		self.Layout()

	def __del__( self ):
		pass


###########################################################################
## Class PanelRipser
###########################################################################

class PanelRipser ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,340 ), style = wx.TAB_TRAVERSAL|wx.VSCROLL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		mainSizer = wx.BoxSizer( wx.VERTICAL )

		self.scrolled_window = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.VSCROLL )
		self.scrolled_window.SetScrollRate( 5, 5 )
		scrolled_sizer = wx.FlexGridSizer( 2, 1, 0, 0 )
		scrolled_sizer.SetFlexibleDirection( wx.BOTH )
		scrolled_sizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		canvasSizer = wx.FlexGridSizer( 1, 2, 0, 10 )
		canvasSizer.SetFlexibleDirection( wx.BOTH )
		canvasSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		mainCanvasSizer = wx.BoxSizer( wx.VERTICAL )


		canvasSizer.Add( mainCanvasSizer, 1, wx.EXPAND, 5 )

		optionalCanvasSizer = wx.BoxSizer( wx.VERTICAL )


		canvasSizer.Add( optionalCanvasSizer, 1, wx.EXPAND, 5 )


		scrolled_sizer.Add( canvasSizer, 1, wx.EXPAND, 5 )

		settingsSizer = wx.FlexGridSizer( 0, 2, 0, 0 )
		settingsSizer.SetFlexibleDirection( wx.BOTH )
		settingsSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText12 = wx.StaticText( self.scrolled_window, wx.ID_ANY, u"Dataset shape:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )

		settingsSizer.Add( self.m_staticText12, 0, wx.ALL, 5 )

		self.label_shape = wx.StaticText( self.scrolled_window, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_shape.Wrap( -1 )

		settingsSizer.Add( self.label_shape, 0, wx.ALL, 5 )

		self.m_staticText33 = wx.StaticText( self.scrolled_window, wx.ID_ANY, u"Window Size:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText33.Wrap( -1 )

		settingsSizer.Add( self.m_staticText33, 0, wx.ALL, 5 )

		self.window_size_slider = wx.Slider( self.scrolled_window, wx.ID_ANY, 50, 1, 100, wx.DefaultPosition, wx.Size( 200,-1 ), wx.SL_HORIZONTAL|wx.SL_VALUE_LABEL )
		settingsSizer.Add( self.window_size_slider, 0, wx.ALL, 5 )

		self.m_staticText35 = wx.StaticText( self.scrolled_window, wx.ID_ANY, u"Overlap:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText35.Wrap( -1 )

		settingsSizer.Add( self.m_staticText35, 0, wx.ALL, 5 )

		self.overlap_slider = wx.Slider( self.scrolled_window, wx.ID_ANY, 0, 0, 100, wx.DefaultPosition, wx.Size( 200,-1 ), wx.SL_HORIZONTAL|wx.SL_VALUE_LABEL )
		settingsSizer.Add( self.overlap_slider, 0, wx.ALL, 5 )

		self.m_staticText31 = wx.StaticText( self.scrolled_window, wx.ID_ANY, u"Metric:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText31.Wrap( -1 )

		settingsSizer.Add( self.m_staticText31, 0, wx.ALL, 5 )

		ch_metricChoices = [ u"euclidean", u"minkowski", u"chebyshev" ]
		self.ch_metric = wx.Choice( self.scrolled_window, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, ch_metricChoices, 0 )
		self.ch_metric.SetSelection( 0 )
		settingsSizer.Add( self.ch_metric, 0, wx.ALL, 5 )

		self.m_staticText32 = wx.StaticText( self.scrolled_window, wx.ID_ANY, u"Max Homology\nDimension:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText32.Wrap( -1 )

		settingsSizer.Add( self.m_staticText32, 0, wx.ALL, 5 )

		self.spn_max_hom_dim = wx.SpinCtrl( self.scrolled_window, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 3, 0 )
		settingsSizer.Add( self.spn_max_hom_dim, 0, wx.ALL, 5 )

		self.chx_distance_matrix = wx.CheckBox( self.scrolled_window, wx.ID_ANY, u"Distance Matrix", wx.DefaultPosition, wx.DefaultSize, 0 )
		settingsSizer.Add( self.chx_distance_matrix, 0, wx.ALL, 5 )

		self.label_shape11 = wx.StaticText( self.scrolled_window, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_shape11.Wrap( -1 )

		settingsSizer.Add( self.label_shape11, 0, wx.ALL, 5 )

		self.btn_execute = wx.Button( self.scrolled_window, wx.ID_ANY, u"Execute", wx.DefaultPosition, wx.DefaultSize, 0 )
		settingsSizer.Add( self.btn_execute, 0, wx.ALL, 5 )

		self.btn_close = wx.Button( self.scrolled_window, wx.ID_ANY, u"Close Tab", wx.DefaultPosition, wx.DefaultSize, 0 )
		settingsSizer.Add( self.btn_close, 0, wx.ALL, 5 )


		scrolled_sizer.Add( settingsSizer, 1, wx.EXPAND, 5 )


		self.scrolled_window.SetSizer( scrolled_sizer )
		self.scrolled_window.Layout()
		scrolled_sizer.Fit( self.scrolled_window )
		mainSizer.Add( self.scrolled_window, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizer( mainSizer )
		self.Layout()

	def __del__( self ):
		pass


###########################################################################
## Class PanelCorrMatHoles
###########################################################################

class PanelCorrMatHoles ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,340 ), style = wx.TAB_TRAVERSAL|wx.VSCROLL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		mainSizer = wx.BoxSizer( wx.VERTICAL )

		self.scrolled_window = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.VSCROLL )
		self.scrolled_window.SetScrollRate( 5, 5 )
		scrolled_sizer = wx.FlexGridSizer( 2, 1, 0, 0 )
		scrolled_sizer.SetFlexibleDirection( wx.BOTH )
		scrolled_sizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		canvasSizer = wx.FlexGridSizer( 1, 2, 0, 10 )
		canvasSizer.SetFlexibleDirection( wx.BOTH )
		canvasSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		mainCanvasSizer = wx.BoxSizer( wx.VERTICAL )


		canvasSizer.Add( mainCanvasSizer, 1, wx.EXPAND, 5 )

		optionalCanvasSizer = wx.BoxSizer( wx.VERTICAL )


		canvasSizer.Add( optionalCanvasSizer, 1, wx.EXPAND, 5 )


		scrolled_sizer.Add( canvasSizer, 1, wx.EXPAND, 5 )

		settingsSizer = wx.FlexGridSizer( 0, 2, 0, 0 )
		settingsSizer.SetFlexibleDirection( wx.BOTH )
		settingsSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText12 = wx.StaticText( self.scrolled_window, wx.ID_ANY, u"Dataset shape:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )

		settingsSizer.Add( self.m_staticText12, 0, wx.ALL, 5 )

		self.label_shape = wx.StaticText( self.scrolled_window, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_shape.Wrap( -1 )

		settingsSizer.Add( self.label_shape, 0, wx.ALL, 5 )

		self.m_staticText33 = wx.StaticText( self.scrolled_window, wx.ID_ANY, u"Window Size:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText33.Wrap( -1 )

		settingsSizer.Add( self.m_staticText33, 0, wx.ALL, 5 )

		self.window_size_slider = wx.Slider( self.scrolled_window, wx.ID_ANY, 50, 1, 100, wx.DefaultPosition, wx.Size( 200,-1 ), wx.SL_HORIZONTAL|wx.SL_VALUE_LABEL )
		settingsSizer.Add( self.window_size_slider, 0, wx.ALL, 5 )

		self.m_staticText35 = wx.StaticText( self.scrolled_window, wx.ID_ANY, u"Overlap:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText35.Wrap( -1 )

		settingsSizer.Add( self.m_staticText35, 0, wx.ALL, 5 )

		self.overlap_slider = wx.Slider( self.scrolled_window, wx.ID_ANY, 0, 0, 100, wx.DefaultPosition, wx.Size( 200,-1 ), wx.SL_HORIZONTAL|wx.SL_VALUE_LABEL )
		settingsSizer.Add( self.overlap_slider, 0, wx.ALL, 5 )

		self.btn_open_folder = wx.Button( self.scrolled_window, wx.ID_ANY, u"Output Folder", wx.DefaultPosition, wx.DefaultSize, 0 )
		settingsSizer.Add( self.btn_open_folder, 0, wx.ALL, 5 )

		self.txt_open_folder = wx.TextCtrl( self.scrolled_window, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		settingsSizer.Add( self.txt_open_folder, 0, wx.ALL, 5 )

		self.btn_execute = wx.Button( self.scrolled_window, wx.ID_ANY, u"Execute", wx.DefaultPosition, wx.DefaultSize, 0 )
		settingsSizer.Add( self.btn_execute, 0, wx.ALL, 5 )

		self.btn_close = wx.Button( self.scrolled_window, wx.ID_ANY, u"Close Tab", wx.DefaultPosition, wx.DefaultSize, 0 )
		settingsSizer.Add( self.btn_close, 0, wx.ALL, 5 )


		scrolled_sizer.Add( settingsSizer, 1, wx.EXPAND, 5 )


		self.scrolled_window.SetSizer( scrolled_sizer )
		self.scrolled_window.Layout()
		scrolled_sizer.Fit( self.scrolled_window )
		mainSizer.Add( self.scrolled_window, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizer( mainSizer )
		self.Layout()

	def __del__( self ):
		pass


###########################################################################
## Class PanelCorrMatDist
###########################################################################

class PanelCorrMatDist ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,340 ), style = wx.TAB_TRAVERSAL|wx.VSCROLL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		mainSizer = wx.BoxSizer( wx.VERTICAL )

		self.scrolled_window = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.VSCROLL )
		self.scrolled_window.SetScrollRate( 5, 5 )
		scrolled_sizer = wx.FlexGridSizer( 2, 1, 0, 0 )
		scrolled_sizer.SetFlexibleDirection( wx.BOTH )
		scrolled_sizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		canvasSizer = wx.FlexGridSizer( 1, 2, 0, 10 )
		canvasSizer.SetFlexibleDirection( wx.BOTH )
		canvasSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		mainCanvasSizer = wx.BoxSizer( wx.VERTICAL )


		canvasSizer.Add( mainCanvasSizer, 1, wx.EXPAND, 5 )

		optionalCanvasSizer = wx.BoxSizer( wx.VERTICAL )


		canvasSizer.Add( optionalCanvasSizer, 1, wx.EXPAND, 5 )


		scrolled_sizer.Add( canvasSizer, 1, wx.EXPAND, 5 )

		settingsSizer = wx.FlexGridSizer( 0, 2, 0, 0 )
		settingsSizer.SetFlexibleDirection( wx.BOTH )
		settingsSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText12 = wx.StaticText( self.scrolled_window, wx.ID_ANY, u"Dataset shape:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )

		settingsSizer.Add( self.m_staticText12, 0, wx.ALL, 5 )

		self.label_shape = wx.StaticText( self.scrolled_window, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_shape.Wrap( -1 )

		settingsSizer.Add( self.label_shape, 0, wx.ALL, 5 )

		self.m_staticText33 = wx.StaticText( self.scrolled_window, wx.ID_ANY, u"Window Size:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText33.Wrap( -1 )

		settingsSizer.Add( self.m_staticText33, 0, wx.ALL, 5 )

		self.window_size_slider = wx.Slider( self.scrolled_window, wx.ID_ANY, 50, 1, 100, wx.DefaultPosition, wx.Size( 200,-1 ), wx.SL_HORIZONTAL|wx.SL_VALUE_LABEL )
		settingsSizer.Add( self.window_size_slider, 0, wx.ALL, 5 )

		self.m_staticText35 = wx.StaticText( self.scrolled_window, wx.ID_ANY, u"Overlap:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText35.Wrap( -1 )

		settingsSizer.Add( self.m_staticText35, 0, wx.ALL, 5 )

		self.overlap_slider = wx.Slider( self.scrolled_window, wx.ID_ANY, 0, 0, 100, wx.DefaultPosition, wx.Size( 200,-1 ), wx.SL_HORIZONTAL|wx.SL_VALUE_LABEL )
		settingsSizer.Add( self.overlap_slider, 0, wx.ALL, 5 )

		self.btn_execute = wx.Button( self.scrolled_window, wx.ID_ANY, u"Execute", wx.DefaultPosition, wx.DefaultSize, 0 )
		settingsSizer.Add( self.btn_execute, 0, wx.ALL, 5 )

		self.btn_close = wx.Button( self.scrolled_window, wx.ID_ANY, u"Close Tab", wx.DefaultPosition, wx.DefaultSize, 0 )
		settingsSizer.Add( self.btn_close, 0, wx.ALL, 5 )


		scrolled_sizer.Add( settingsSizer, 1, wx.EXPAND, 5 )


		self.scrolled_window.SetSizer( scrolled_sizer )
		self.scrolled_window.Layout()
		scrolled_sizer.Fit( self.scrolled_window )
		mainSizer.Add( self.scrolled_window, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizer( mainSizer )
		self.Layout()

	def __del__( self ):
		pass


###########################################################################
## Class PanelSpikes
###########################################################################

class PanelSpikes ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,340 ), style = wx.TAB_TRAVERSAL|wx.VSCROLL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		mainSizer = wx.BoxSizer( wx.VERTICAL )

		self.scrolled_window = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.VSCROLL )
		self.scrolled_window.SetScrollRate( 5, 5 )
		scrolled_sizer = wx.FlexGridSizer( 2, 1, 0, 0 )
		scrolled_sizer.SetFlexibleDirection( wx.BOTH )
		scrolled_sizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		canvasSizer = wx.FlexGridSizer( 1, 2, 0, 10 )
		canvasSizer.SetFlexibleDirection( wx.BOTH )
		canvasSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		mainCanvasSizer = wx.BoxSizer( wx.VERTICAL )


		canvasSizer.Add( mainCanvasSizer, 1, wx.EXPAND, 5 )

		optionalCanvasSizer = wx.BoxSizer( wx.VERTICAL )


		canvasSizer.Add( optionalCanvasSizer, 1, wx.EXPAND, 5 )


		scrolled_sizer.Add( canvasSizer, 1, wx.EXPAND, 5 )

		settingsSizer = wx.FlexGridSizer( 0, 2, 0, 0 )
		settingsSizer.SetFlexibleDirection( wx.BOTH )
		settingsSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText12 = wx.StaticText( self.scrolled_window, wx.ID_ANY, u"Dataset shape:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )

		settingsSizer.Add( self.m_staticText12, 0, wx.ALL, 5 )

		self.label_shape = wx.StaticText( self.scrolled_window, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_shape.Wrap( -1 )

		settingsSizer.Add( self.label_shape, 0, wx.ALL, 5 )

		self.m_staticText33 = wx.StaticText( self.scrolled_window, wx.ID_ANY, u"Window Size:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText33.Wrap( -1 )

		settingsSizer.Add( self.m_staticText33, 0, wx.ALL, 5 )

		self.window_size_slider = wx.Slider( self.scrolled_window, wx.ID_ANY, 50, 1, 100, wx.DefaultPosition, wx.Size( 200,-1 ), wx.SL_HORIZONTAL|wx.SL_VALUE_LABEL )
		settingsSizer.Add( self.window_size_slider, 0, wx.ALL, 5 )

		self.m_staticText35 = wx.StaticText( self.scrolled_window, wx.ID_ANY, u"Overlap:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText35.Wrap( -1 )

		settingsSizer.Add( self.m_staticText35, 0, wx.ALL, 5 )

		self.overlap_slider = wx.Slider( self.scrolled_window, wx.ID_ANY, 0, 0, 100, wx.DefaultPosition, wx.Size( 200,-1 ), wx.SL_HORIZONTAL|wx.SL_VALUE_LABEL )
		settingsSizer.Add( self.overlap_slider, 0, wx.ALL, 5 )

		self.m_staticText351 = wx.StaticText( self.scrolled_window, wx.ID_ANY, u"Threshold %:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText351.Wrap( -1 )

		settingsSizer.Add( self.m_staticText351, 0, wx.ALL, 5 )

		self.threshold_slider = wx.Slider( self.scrolled_window, wx.ID_ANY, 30, 0, 100, wx.DefaultPosition, wx.Size( 200,-1 ), wx.SL_HORIZONTAL|wx.SL_VALUE_LABEL )
		settingsSizer.Add( self.threshold_slider, 0, wx.ALL, 5 )

		self.btn_execute = wx.Button( self.scrolled_window, wx.ID_ANY, u"Execute", wx.DefaultPosition, wx.DefaultSize, 0 )
		settingsSizer.Add( self.btn_execute, 0, wx.ALL, 5 )

		self.btn_close = wx.Button( self.scrolled_window, wx.ID_ANY, u"Close Tab", wx.DefaultPosition, wx.DefaultSize, 0 )
		settingsSizer.Add( self.btn_close, 0, wx.ALL, 5 )


		scrolled_sizer.Add( settingsSizer, 1, wx.EXPAND, 5 )


		self.scrolled_window.SetSizer( scrolled_sizer )
		self.scrolled_window.Layout()
		scrolled_sizer.Fit( self.scrolled_window )
		mainSizer.Add( self.scrolled_window, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizer( mainSizer )
		self.Layout()

	def __del__( self ):
		pass


###########################################################################
## Class PanelMiniBatchKMeans
###########################################################################

class PanelMiniBatchKMeans ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,340 ), style = wx.TAB_TRAVERSAL|wx.VSCROLL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		mainSizer = wx.BoxSizer( wx.VERTICAL )

		self.scrolled_window = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.VSCROLL )
		self.scrolled_window.SetScrollRate( 5, 5 )
		scrolled_sizer = wx.FlexGridSizer( 2, 1, 0, 0 )
		scrolled_sizer.SetFlexibleDirection( wx.BOTH )
		scrolled_sizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		canvasSizer = wx.FlexGridSizer( 1, 2, 0, 10 )
		canvasSizer.SetFlexibleDirection( wx.BOTH )
		canvasSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		mainCanvasSizer = wx.BoxSizer( wx.VERTICAL )


		canvasSizer.Add( mainCanvasSizer, 1, wx.EXPAND, 5 )

		optionalCanvasSizer = wx.BoxSizer( wx.VERTICAL )


		canvasSizer.Add( optionalCanvasSizer, 1, wx.EXPAND, 5 )


		scrolled_sizer.Add( canvasSizer, 1, wx.EXPAND, 5 )

		settingsSizer = wx.FlexGridSizer( 0, 2, 0, 0 )
		settingsSizer.SetFlexibleDirection( wx.BOTH )
		settingsSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText12 = wx.StaticText( self.scrolled_window, wx.ID_ANY, u"Dataset shape:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )

		settingsSizer.Add( self.m_staticText12, 0, wx.ALL, 5 )

		self.label_shape = wx.StaticText( self.scrolled_window, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_shape.Wrap( -1 )

		settingsSizer.Add( self.label_shape, 0, wx.ALL, 5 )

		self.m_staticText33 = wx.StaticText( self.scrolled_window, wx.ID_ANY, u"Cluster Number:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText33.Wrap( -1 )

		settingsSizer.Add( self.m_staticText33, 0, wx.ALL, 5 )

		self.ncluster_textctrl = wx.TextCtrl( self.scrolled_window, wx.ID_ANY, u"1", wx.DefaultPosition, wx.DefaultSize, 0 )
		settingsSizer.Add( self.ncluster_textctrl, 0, wx.ALL, 5 )

		self.btn_execute = wx.Button( self.scrolled_window, wx.ID_ANY, u"Execute", wx.DefaultPosition, wx.DefaultSize, 0 )
		settingsSizer.Add( self.btn_execute, 0, wx.ALL, 5 )

		self.btn_close = wx.Button( self.scrolled_window, wx.ID_ANY, u"Close Tab", wx.DefaultPosition, wx.DefaultSize, 0 )
		settingsSizer.Add( self.btn_close, 0, wx.ALL, 5 )


		scrolled_sizer.Add( settingsSizer, 1, wx.EXPAND, 5 )


		self.scrolled_window.SetSizer( scrolled_sizer )
		self.scrolled_window.Layout()
		scrolled_sizer.Fit( self.scrolled_window )
		mainSizer.Add( self.scrolled_window, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizer( mainSizer )
		self.Layout()

	def __del__( self ):
		pass


###########################################################################
## Class PanelAffinityPropagation
###########################################################################

class PanelAffinityPropagation ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,340 ), style = wx.TAB_TRAVERSAL|wx.VSCROLL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		mainSizer = wx.BoxSizer( wx.VERTICAL )

		self.scrolled_window = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.VSCROLL )
		self.scrolled_window.SetScrollRate( 5, 5 )
		scrolled_sizer = wx.FlexGridSizer( 2, 1, 0, 0 )
		scrolled_sizer.SetFlexibleDirection( wx.BOTH )
		scrolled_sizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		canvasSizer = wx.FlexGridSizer( 1, 2, 0, 10 )
		canvasSizer.SetFlexibleDirection( wx.BOTH )
		canvasSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		mainCanvasSizer = wx.BoxSizer( wx.VERTICAL )


		canvasSizer.Add( mainCanvasSizer, 1, wx.EXPAND, 5 )

		optionalCanvasSizer = wx.BoxSizer( wx.VERTICAL )


		canvasSizer.Add( optionalCanvasSizer, 1, wx.EXPAND, 5 )


		scrolled_sizer.Add( canvasSizer, 1, wx.EXPAND, 5 )

		settingsSizer = wx.FlexGridSizer( 0, 2, 0, 0 )
		settingsSizer.SetFlexibleDirection( wx.BOTH )
		settingsSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText12 = wx.StaticText( self.scrolled_window, wx.ID_ANY, u"Dataset shape:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )

		settingsSizer.Add( self.m_staticText12, 0, wx.ALL, 5 )

		self.label_shape = wx.StaticText( self.scrolled_window, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_shape.Wrap( -1 )

		settingsSizer.Add( self.label_shape, 0, wx.ALL, 5 )

		self.m_staticText33 = wx.StaticText( self.scrolled_window, wx.ID_ANY, u"Window Size:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText33.Wrap( -1 )

		settingsSizer.Add( self.m_staticText33, 0, wx.ALL, 5 )

		self.window_size_slider = wx.Slider( self.scrolled_window, wx.ID_ANY, 50, 1, 100, wx.DefaultPosition, wx.Size( 200,-1 ), wx.SL_HORIZONTAL|wx.SL_VALUE_LABEL )
		settingsSizer.Add( self.window_size_slider, 0, wx.ALL, 5 )

		self.m_staticText35 = wx.StaticText( self.scrolled_window, wx.ID_ANY, u"Overlap:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText35.Wrap( -1 )

		settingsSizer.Add( self.m_staticText35, 0, wx.ALL, 5 )

		self.overlap_slider = wx.Slider( self.scrolled_window, wx.ID_ANY, 0, 0, 100, wx.DefaultPosition, wx.Size( 200,-1 ), wx.SL_HORIZONTAL|wx.SL_VALUE_LABEL )
		settingsSizer.Add( self.overlap_slider, 0, wx.ALL, 5 )

		self.btn_execute = wx.Button( self.scrolled_window, wx.ID_ANY, u"Execute", wx.DefaultPosition, wx.DefaultSize, 0 )
		settingsSizer.Add( self.btn_execute, 0, wx.ALL, 5 )

		self.btn_close = wx.Button( self.scrolled_window, wx.ID_ANY, u"Close Tab", wx.DefaultPosition, wx.DefaultSize, 0 )
		settingsSizer.Add( self.btn_close, 0, wx.ALL, 5 )


		scrolled_sizer.Add( settingsSizer, 1, wx.EXPAND, 5 )


		self.scrolled_window.SetSizer( scrolled_sizer )
		self.scrolled_window.Layout()
		scrolled_sizer.Fit( self.scrolled_window )
		mainSizer.Add( self.scrolled_window, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizer( mainSizer )
		self.Layout()

	def __del__( self ):
		pass


###########################################################################
## Class PanelMeanShift
###########################################################################

class PanelMeanShift ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,340 ), style = wx.TAB_TRAVERSAL|wx.VSCROLL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		mainSizer = wx.BoxSizer( wx.VERTICAL )

		self.scrolled_window = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.VSCROLL )
		self.scrolled_window.SetScrollRate( 5, 5 )
		scrolled_sizer = wx.FlexGridSizer( 2, 1, 0, 0 )
		scrolled_sizer.SetFlexibleDirection( wx.BOTH )
		scrolled_sizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		canvasSizer = wx.FlexGridSizer( 1, 2, 0, 10 )
		canvasSizer.SetFlexibleDirection( wx.BOTH )
		canvasSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		mainCanvasSizer = wx.BoxSizer( wx.VERTICAL )


		canvasSizer.Add( mainCanvasSizer, 1, wx.EXPAND, 5 )

		optionalCanvasSizer = wx.BoxSizer( wx.VERTICAL )


		canvasSizer.Add( optionalCanvasSizer, 1, wx.EXPAND, 5 )


		scrolled_sizer.Add( canvasSizer, 1, wx.EXPAND, 5 )

		settingsSizer = wx.FlexGridSizer( 0, 2, 0, 0 )
		settingsSizer.SetFlexibleDirection( wx.BOTH )
		settingsSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText12 = wx.StaticText( self.scrolled_window, wx.ID_ANY, u"Dataset shape:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )

		settingsSizer.Add( self.m_staticText12, 0, wx.ALL, 5 )

		self.label_shape = wx.StaticText( self.scrolled_window, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_shape.Wrap( -1 )

		settingsSizer.Add( self.label_shape, 0, wx.ALL, 5 )

		self.m_staticText33 = wx.StaticText( self.scrolled_window, wx.ID_ANY, u"Window Size:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText33.Wrap( -1 )

		settingsSizer.Add( self.m_staticText33, 0, wx.ALL, 5 )

		self.window_size_slider = wx.Slider( self.scrolled_window, wx.ID_ANY, 50, 1, 100, wx.DefaultPosition, wx.Size( 200,-1 ), wx.SL_HORIZONTAL|wx.SL_VALUE_LABEL )
		settingsSizer.Add( self.window_size_slider, 0, wx.ALL, 5 )

		self.m_staticText35 = wx.StaticText( self.scrolled_window, wx.ID_ANY, u"Overlap:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText35.Wrap( -1 )

		settingsSizer.Add( self.m_staticText35, 0, wx.ALL, 5 )

		self.overlap_slider = wx.Slider( self.scrolled_window, wx.ID_ANY, 0, 0, 100, wx.DefaultPosition, wx.Size( 200,-1 ), wx.SL_HORIZONTAL|wx.SL_VALUE_LABEL )
		settingsSizer.Add( self.overlap_slider, 0, wx.ALL, 5 )

		self.btn_execute = wx.Button( self.scrolled_window, wx.ID_ANY, u"Execute", wx.DefaultPosition, wx.DefaultSize, 0 )
		settingsSizer.Add( self.btn_execute, 0, wx.ALL, 5 )

		self.btn_close = wx.Button( self.scrolled_window, wx.ID_ANY, u"Close Tab", wx.DefaultPosition, wx.DefaultSize, 0 )
		settingsSizer.Add( self.btn_close, 0, wx.ALL, 5 )


		scrolled_sizer.Add( settingsSizer, 1, wx.EXPAND, 5 )


		self.scrolled_window.SetSizer( scrolled_sizer )
		self.scrolled_window.Layout()
		scrolled_sizer.Fit( self.scrolled_window )
		mainSizer.Add( self.scrolled_window, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizer( mainSizer )
		self.Layout()

	def __del__( self ):
		pass


###########################################################################
## Class PanelSpectralClustering
###########################################################################

class PanelSpectralClustering ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,340 ), style = wx.TAB_TRAVERSAL|wx.VSCROLL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		mainSizer = wx.BoxSizer( wx.VERTICAL )

		self.scrolled_window = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.VSCROLL )
		self.scrolled_window.SetScrollRate( 5, 5 )
		scrolled_sizer = wx.FlexGridSizer( 2, 1, 0, 0 )
		scrolled_sizer.SetFlexibleDirection( wx.BOTH )
		scrolled_sizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		canvasSizer = wx.FlexGridSizer( 1, 2, 0, 10 )
		canvasSizer.SetFlexibleDirection( wx.BOTH )
		canvasSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		mainCanvasSizer = wx.BoxSizer( wx.VERTICAL )


		canvasSizer.Add( mainCanvasSizer, 1, wx.EXPAND, 5 )

		optionalCanvasSizer = wx.BoxSizer( wx.VERTICAL )


		canvasSizer.Add( optionalCanvasSizer, 1, wx.EXPAND, 5 )


		scrolled_sizer.Add( canvasSizer, 1, wx.EXPAND, 5 )

		settingsSizer = wx.FlexGridSizer( 0, 2, 0, 0 )
		settingsSizer.SetFlexibleDirection( wx.BOTH )
		settingsSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText12 = wx.StaticText( self.scrolled_window, wx.ID_ANY, u"Dataset shape:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )

		settingsSizer.Add( self.m_staticText12, 0, wx.ALL, 5 )

		self.label_shape = wx.StaticText( self.scrolled_window, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_shape.Wrap( -1 )

		settingsSizer.Add( self.label_shape, 0, wx.ALL, 5 )

		self.m_staticText33 = wx.StaticText( self.scrolled_window, wx.ID_ANY, u"Window Size:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText33.Wrap( -1 )

		settingsSizer.Add( self.m_staticText33, 0, wx.ALL, 5 )

		self.window_size_slider = wx.Slider( self.scrolled_window, wx.ID_ANY, 50, 1, 100, wx.DefaultPosition, wx.Size( 200,-1 ), wx.SL_HORIZONTAL|wx.SL_VALUE_LABEL )
		settingsSizer.Add( self.window_size_slider, 0, wx.ALL, 5 )

		self.m_staticText35 = wx.StaticText( self.scrolled_window, wx.ID_ANY, u"Overlap:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText35.Wrap( -1 )

		settingsSizer.Add( self.m_staticText35, 0, wx.ALL, 5 )

		self.overlap_slider = wx.Slider( self.scrolled_window, wx.ID_ANY, 0, 0, 100, wx.DefaultPosition, wx.Size( 200,-1 ), wx.SL_HORIZONTAL|wx.SL_VALUE_LABEL )
		settingsSizer.Add( self.overlap_slider, 0, wx.ALL, 5 )

		self.btn_execute = wx.Button( self.scrolled_window, wx.ID_ANY, u"Execute", wx.DefaultPosition, wx.DefaultSize, 0 )
		settingsSizer.Add( self.btn_execute, 0, wx.ALL, 5 )

		self.btn_close = wx.Button( self.scrolled_window, wx.ID_ANY, u"Close Tab", wx.DefaultPosition, wx.DefaultSize, 0 )
		settingsSizer.Add( self.btn_close, 0, wx.ALL, 5 )


		scrolled_sizer.Add( settingsSizer, 1, wx.EXPAND, 5 )


		self.scrolled_window.SetSizer( scrolled_sizer )
		self.scrolled_window.Layout()
		scrolled_sizer.Fit( self.scrolled_window )
		mainSizer.Add( self.scrolled_window, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizer( mainSizer )
		self.Layout()

	def __del__( self ):
		pass


###########################################################################
## Class PanelWard
###########################################################################

class PanelWard ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,340 ), style = wx.TAB_TRAVERSAL|wx.VSCROLL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		mainSizer = wx.BoxSizer( wx.VERTICAL )

		self.scrolled_window = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.VSCROLL )
		self.scrolled_window.SetScrollRate( 5, 5 )
		scrolled_sizer = wx.FlexGridSizer( 2, 1, 0, 0 )
		scrolled_sizer.SetFlexibleDirection( wx.BOTH )
		scrolled_sizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		canvasSizer = wx.FlexGridSizer( 1, 2, 0, 10 )
		canvasSizer.SetFlexibleDirection( wx.BOTH )
		canvasSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		mainCanvasSizer = wx.BoxSizer( wx.VERTICAL )


		canvasSizer.Add( mainCanvasSizer, 1, wx.EXPAND, 5 )

		optionalCanvasSizer = wx.BoxSizer( wx.VERTICAL )


		canvasSizer.Add( optionalCanvasSizer, 1, wx.EXPAND, 5 )


		scrolled_sizer.Add( canvasSizer, 1, wx.EXPAND, 5 )

		settingsSizer = wx.FlexGridSizer( 0, 2, 0, 0 )
		settingsSizer.SetFlexibleDirection( wx.BOTH )
		settingsSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText12 = wx.StaticText( self.scrolled_window, wx.ID_ANY, u"Dataset shape:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )

		settingsSizer.Add( self.m_staticText12, 0, wx.ALL, 5 )

		self.label_shape = wx.StaticText( self.scrolled_window, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_shape.Wrap( -1 )

		settingsSizer.Add( self.label_shape, 0, wx.ALL, 5 )

		self.m_staticText33 = wx.StaticText( self.scrolled_window, wx.ID_ANY, u"Window Size:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText33.Wrap( -1 )

		settingsSizer.Add( self.m_staticText33, 0, wx.ALL, 5 )

		self.window_size_slider = wx.Slider( self.scrolled_window, wx.ID_ANY, 50, 1, 100, wx.DefaultPosition, wx.Size( 200,-1 ), wx.SL_HORIZONTAL|wx.SL_VALUE_LABEL )
		settingsSizer.Add( self.window_size_slider, 0, wx.ALL, 5 )

		self.m_staticText35 = wx.StaticText( self.scrolled_window, wx.ID_ANY, u"Overlap:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText35.Wrap( -1 )

		settingsSizer.Add( self.m_staticText35, 0, wx.ALL, 5 )

		self.overlap_slider = wx.Slider( self.scrolled_window, wx.ID_ANY, 0, 0, 100, wx.DefaultPosition, wx.Size( 200,-1 ), wx.SL_HORIZONTAL|wx.SL_VALUE_LABEL )
		settingsSizer.Add( self.overlap_slider, 0, wx.ALL, 5 )

		self.btn_execute = wx.Button( self.scrolled_window, wx.ID_ANY, u"Execute", wx.DefaultPosition, wx.DefaultSize, 0 )
		settingsSizer.Add( self.btn_execute, 0, wx.ALL, 5 )

		self.btn_close = wx.Button( self.scrolled_window, wx.ID_ANY, u"Close Tab", wx.DefaultPosition, wx.DefaultSize, 0 )
		settingsSizer.Add( self.btn_close, 0, wx.ALL, 5 )


		scrolled_sizer.Add( settingsSizer, 1, wx.EXPAND, 5 )


		self.scrolled_window.SetSizer( scrolled_sizer )
		self.scrolled_window.Layout()
		scrolled_sizer.Fit( self.scrolled_window )
		mainSizer.Add( self.scrolled_window, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizer( mainSizer )
		self.Layout()

	def __del__( self ):
		pass


###########################################################################
## Class PanelAgglomerativeClustering
###########################################################################

class PanelAgglomerativeClustering ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,340 ), style = wx.TAB_TRAVERSAL|wx.VSCROLL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		mainSizer = wx.BoxSizer( wx.VERTICAL )

		self.scrolled_window = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.VSCROLL )
		self.scrolled_window.SetScrollRate( 5, 5 )
		scrolled_sizer = wx.FlexGridSizer( 2, 1, 0, 0 )
		scrolled_sizer.SetFlexibleDirection( wx.BOTH )
		scrolled_sizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		canvasSizer = wx.FlexGridSizer( 1, 2, 0, 10 )
		canvasSizer.SetFlexibleDirection( wx.BOTH )
		canvasSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		mainCanvasSizer = wx.BoxSizer( wx.VERTICAL )


		canvasSizer.Add( mainCanvasSizer, 1, wx.EXPAND, 5 )

		optionalCanvasSizer = wx.BoxSizer( wx.VERTICAL )


		canvasSizer.Add( optionalCanvasSizer, 1, wx.EXPAND, 5 )


		scrolled_sizer.Add( canvasSizer, 1, wx.EXPAND, 5 )

		settingsSizer = wx.FlexGridSizer( 0, 2, 0, 0 )
		settingsSizer.SetFlexibleDirection( wx.BOTH )
		settingsSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText12 = wx.StaticText( self.scrolled_window, wx.ID_ANY, u"Dataset shape:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )

		settingsSizer.Add( self.m_staticText12, 0, wx.ALL, 5 )

		self.label_shape = wx.StaticText( self.scrolled_window, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_shape.Wrap( -1 )

		settingsSizer.Add( self.label_shape, 0, wx.ALL, 5 )

		self.m_staticText33 = wx.StaticText( self.scrolled_window, wx.ID_ANY, u"Window Size:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText33.Wrap( -1 )

		settingsSizer.Add( self.m_staticText33, 0, wx.ALL, 5 )

		self.window_size_slider = wx.Slider( self.scrolled_window, wx.ID_ANY, 50, 1, 100, wx.DefaultPosition, wx.Size( 200,-1 ), wx.SL_HORIZONTAL|wx.SL_VALUE_LABEL )
		settingsSizer.Add( self.window_size_slider, 0, wx.ALL, 5 )

		self.m_staticText35 = wx.StaticText( self.scrolled_window, wx.ID_ANY, u"Overlap:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText35.Wrap( -1 )

		settingsSizer.Add( self.m_staticText35, 0, wx.ALL, 5 )

		self.overlap_slider = wx.Slider( self.scrolled_window, wx.ID_ANY, 0, 0, 100, wx.DefaultPosition, wx.Size( 200,-1 ), wx.SL_HORIZONTAL|wx.SL_VALUE_LABEL )
		settingsSizer.Add( self.overlap_slider, 0, wx.ALL, 5 )

		self.btn_execute = wx.Button( self.scrolled_window, wx.ID_ANY, u"Execute", wx.DefaultPosition, wx.DefaultSize, 0 )
		settingsSizer.Add( self.btn_execute, 0, wx.ALL, 5 )

		self.btn_close = wx.Button( self.scrolled_window, wx.ID_ANY, u"Close Tab", wx.DefaultPosition, wx.DefaultSize, 0 )
		settingsSizer.Add( self.btn_close, 0, wx.ALL, 5 )


		scrolled_sizer.Add( settingsSizer, 1, wx.EXPAND, 5 )


		self.scrolled_window.SetSizer( scrolled_sizer )
		self.scrolled_window.Layout()
		scrolled_sizer.Fit( self.scrolled_window )
		mainSizer.Add( self.scrolled_window, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizer( mainSizer )
		self.Layout()

	def __del__( self ):
		pass


###########################################################################
## Class PanelDBSCAN
###########################################################################

class PanelDBSCAN ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,340 ), style = wx.TAB_TRAVERSAL|wx.VSCROLL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		mainSizer = wx.BoxSizer( wx.VERTICAL )

		self.scrolled_window = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.VSCROLL )
		self.scrolled_window.SetScrollRate( 5, 5 )
		scrolled_sizer = wx.FlexGridSizer( 2, 1, 0, 0 )
		scrolled_sizer.SetFlexibleDirection( wx.BOTH )
		scrolled_sizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		canvasSizer = wx.FlexGridSizer( 1, 2, 0, 10 )
		canvasSizer.SetFlexibleDirection( wx.BOTH )
		canvasSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		mainCanvasSizer = wx.BoxSizer( wx.VERTICAL )


		canvasSizer.Add( mainCanvasSizer, 1, wx.EXPAND, 5 )

		optionalCanvasSizer = wx.BoxSizer( wx.VERTICAL )


		canvasSizer.Add( optionalCanvasSizer, 1, wx.EXPAND, 5 )


		scrolled_sizer.Add( canvasSizer, 1, wx.EXPAND, 5 )

		settingsSizer = wx.FlexGridSizer( 0, 2, 0, 0 )
		settingsSizer.SetFlexibleDirection( wx.BOTH )
		settingsSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText12 = wx.StaticText( self.scrolled_window, wx.ID_ANY, u"Dataset shape:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )

		settingsSizer.Add( self.m_staticText12, 0, wx.ALL, 5 )

		self.label_shape = wx.StaticText( self.scrolled_window, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_shape.Wrap( -1 )

		settingsSizer.Add( self.label_shape, 0, wx.ALL, 5 )

		self.m_staticText33 = wx.StaticText( self.scrolled_window, wx.ID_ANY, u"Window Size:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText33.Wrap( -1 )

		settingsSizer.Add( self.m_staticText33, 0, wx.ALL, 5 )

		self.window_size_slider = wx.Slider( self.scrolled_window, wx.ID_ANY, 50, 1, 100, wx.DefaultPosition, wx.Size( 200,-1 ), wx.SL_HORIZONTAL|wx.SL_VALUE_LABEL )
		settingsSizer.Add( self.window_size_slider, 0, wx.ALL, 5 )

		self.m_staticText35 = wx.StaticText( self.scrolled_window, wx.ID_ANY, u"Overlap:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText35.Wrap( -1 )

		settingsSizer.Add( self.m_staticText35, 0, wx.ALL, 5 )

		self.overlap_slider = wx.Slider( self.scrolled_window, wx.ID_ANY, 0, 0, 100, wx.DefaultPosition, wx.Size( 200,-1 ), wx.SL_HORIZONTAL|wx.SL_VALUE_LABEL )
		settingsSizer.Add( self.overlap_slider, 0, wx.ALL, 5 )

		self.btn_execute = wx.Button( self.scrolled_window, wx.ID_ANY, u"Execute", wx.DefaultPosition, wx.DefaultSize, 0 )
		settingsSizer.Add( self.btn_execute, 0, wx.ALL, 5 )

		self.btn_close = wx.Button( self.scrolled_window, wx.ID_ANY, u"Close Tab", wx.DefaultPosition, wx.DefaultSize, 0 )
		settingsSizer.Add( self.btn_close, 0, wx.ALL, 5 )


		scrolled_sizer.Add( settingsSizer, 1, wx.EXPAND, 5 )


		self.scrolled_window.SetSizer( scrolled_sizer )
		self.scrolled_window.Layout()
		scrolled_sizer.Fit( self.scrolled_window )
		mainSizer.Add( self.scrolled_window, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizer( mainSizer )
		self.Layout()

	def __del__( self ):
		pass


###########################################################################
## Class PanelOPTICS
###########################################################################

class PanelOPTICS ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,340 ), style = wx.TAB_TRAVERSAL|wx.VSCROLL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		mainSizer = wx.BoxSizer( wx.VERTICAL )

		self.scrolled_window = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.VSCROLL )
		self.scrolled_window.SetScrollRate( 5, 5 )
		scrolled_sizer = wx.FlexGridSizer( 2, 1, 0, 0 )
		scrolled_sizer.SetFlexibleDirection( wx.BOTH )
		scrolled_sizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		canvasSizer = wx.FlexGridSizer( 1, 2, 0, 10 )
		canvasSizer.SetFlexibleDirection( wx.BOTH )
		canvasSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		mainCanvasSizer = wx.BoxSizer( wx.VERTICAL )


		canvasSizer.Add( mainCanvasSizer, 1, wx.EXPAND, 5 )

		optionalCanvasSizer = wx.BoxSizer( wx.VERTICAL )


		canvasSizer.Add( optionalCanvasSizer, 1, wx.EXPAND, 5 )


		scrolled_sizer.Add( canvasSizer, 1, wx.EXPAND, 5 )

		settingsSizer = wx.FlexGridSizer( 0, 2, 0, 0 )
		settingsSizer.SetFlexibleDirection( wx.BOTH )
		settingsSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText12 = wx.StaticText( self.scrolled_window, wx.ID_ANY, u"Dataset shape:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )

		settingsSizer.Add( self.m_staticText12, 0, wx.ALL, 5 )

		self.label_shape = wx.StaticText( self.scrolled_window, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_shape.Wrap( -1 )

		settingsSizer.Add( self.label_shape, 0, wx.ALL, 5 )

		self.m_staticText33 = wx.StaticText( self.scrolled_window, wx.ID_ANY, u"Window Size:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText33.Wrap( -1 )

		settingsSizer.Add( self.m_staticText33, 0, wx.ALL, 5 )

		self.window_size_slider = wx.Slider( self.scrolled_window, wx.ID_ANY, 50, 1, 100, wx.DefaultPosition, wx.Size( 200,-1 ), wx.SL_HORIZONTAL|wx.SL_VALUE_LABEL )
		settingsSizer.Add( self.window_size_slider, 0, wx.ALL, 5 )

		self.m_staticText35 = wx.StaticText( self.scrolled_window, wx.ID_ANY, u"Overlap:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText35.Wrap( -1 )

		settingsSizer.Add( self.m_staticText35, 0, wx.ALL, 5 )

		self.overlap_slider = wx.Slider( self.scrolled_window, wx.ID_ANY, 0, 0, 100, wx.DefaultPosition, wx.Size( 200,-1 ), wx.SL_HORIZONTAL|wx.SL_VALUE_LABEL )
		settingsSizer.Add( self.overlap_slider, 0, wx.ALL, 5 )

		self.btn_execute = wx.Button( self.scrolled_window, wx.ID_ANY, u"Execute", wx.DefaultPosition, wx.DefaultSize, 0 )
		settingsSizer.Add( self.btn_execute, 0, wx.ALL, 5 )

		self.btn_close = wx.Button( self.scrolled_window, wx.ID_ANY, u"Close Tab", wx.DefaultPosition, wx.DefaultSize, 0 )
		settingsSizer.Add( self.btn_close, 0, wx.ALL, 5 )


		scrolled_sizer.Add( settingsSizer, 1, wx.EXPAND, 5 )


		self.scrolled_window.SetSizer( scrolled_sizer )
		self.scrolled_window.Layout()
		scrolled_sizer.Fit( self.scrolled_window )
		mainSizer.Add( self.scrolled_window, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizer( mainSizer )
		self.Layout()

	def __del__( self ):
		pass


###########################################################################
## Class PanelBirch
###########################################################################

class PanelBirch ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,340 ), style = wx.TAB_TRAVERSAL|wx.VSCROLL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		mainSizer = wx.BoxSizer( wx.VERTICAL )

		self.scrolled_window = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.VSCROLL )
		self.scrolled_window.SetScrollRate( 5, 5 )
		scrolled_sizer = wx.FlexGridSizer( 2, 1, 0, 0 )
		scrolled_sizer.SetFlexibleDirection( wx.BOTH )
		scrolled_sizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		canvasSizer = wx.FlexGridSizer( 1, 2, 0, 10 )
		canvasSizer.SetFlexibleDirection( wx.BOTH )
		canvasSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		mainCanvasSizer = wx.BoxSizer( wx.VERTICAL )


		canvasSizer.Add( mainCanvasSizer, 1, wx.EXPAND, 5 )

		optionalCanvasSizer = wx.BoxSizer( wx.VERTICAL )


		canvasSizer.Add( optionalCanvasSizer, 1, wx.EXPAND, 5 )


		scrolled_sizer.Add( canvasSizer, 1, wx.EXPAND, 5 )

		settingsSizer = wx.FlexGridSizer( 0, 2, 0, 0 )
		settingsSizer.SetFlexibleDirection( wx.BOTH )
		settingsSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText12 = wx.StaticText( self.scrolled_window, wx.ID_ANY, u"Dataset shape:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )

		settingsSizer.Add( self.m_staticText12, 0, wx.ALL, 5 )

		self.label_shape = wx.StaticText( self.scrolled_window, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_shape.Wrap( -1 )

		settingsSizer.Add( self.label_shape, 0, wx.ALL, 5 )

		self.m_staticText33 = wx.StaticText( self.scrolled_window, wx.ID_ANY, u"Window Size:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText33.Wrap( -1 )

		settingsSizer.Add( self.m_staticText33, 0, wx.ALL, 5 )

		self.window_size_slider = wx.Slider( self.scrolled_window, wx.ID_ANY, 50, 1, 100, wx.DefaultPosition, wx.Size( 200,-1 ), wx.SL_HORIZONTAL|wx.SL_VALUE_LABEL )
		settingsSizer.Add( self.window_size_slider, 0, wx.ALL, 5 )

		self.m_staticText35 = wx.StaticText( self.scrolled_window, wx.ID_ANY, u"Overlap:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText35.Wrap( -1 )

		settingsSizer.Add( self.m_staticText35, 0, wx.ALL, 5 )

		self.overlap_slider = wx.Slider( self.scrolled_window, wx.ID_ANY, 0, 0, 100, wx.DefaultPosition, wx.Size( 200,-1 ), wx.SL_HORIZONTAL|wx.SL_VALUE_LABEL )
		settingsSizer.Add( self.overlap_slider, 0, wx.ALL, 5 )

		self.btn_execute = wx.Button( self.scrolled_window, wx.ID_ANY, u"Execute", wx.DefaultPosition, wx.DefaultSize, 0 )
		settingsSizer.Add( self.btn_execute, 0, wx.ALL, 5 )

		self.btn_close = wx.Button( self.scrolled_window, wx.ID_ANY, u"Close Tab", wx.DefaultPosition, wx.DefaultSize, 0 )
		settingsSizer.Add( self.btn_close, 0, wx.ALL, 5 )


		scrolled_sizer.Add( settingsSizer, 1, wx.EXPAND, 5 )


		self.scrolled_window.SetSizer( scrolled_sizer )
		self.scrolled_window.Layout()
		scrolled_sizer.Fit( self.scrolled_window )
		mainSizer.Add( self.scrolled_window, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizer( mainSizer )
		self.Layout()

	def __del__( self ):
		pass


###########################################################################
## Class PanelGaussianMixture
###########################################################################

class PanelGaussianMixture ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,340 ), style = wx.TAB_TRAVERSAL|wx.VSCROLL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		mainSizer = wx.BoxSizer( wx.VERTICAL )

		self.scrolled_window = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.VSCROLL )
		self.scrolled_window.SetScrollRate( 5, 5 )
		scrolled_sizer = wx.FlexGridSizer( 2, 1, 0, 0 )
		scrolled_sizer.SetFlexibleDirection( wx.BOTH )
		scrolled_sizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		canvasSizer = wx.FlexGridSizer( 1, 2, 0, 10 )
		canvasSizer.SetFlexibleDirection( wx.BOTH )
		canvasSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		mainCanvasSizer = wx.BoxSizer( wx.VERTICAL )


		canvasSizer.Add( mainCanvasSizer, 1, wx.EXPAND, 5 )

		optionalCanvasSizer = wx.BoxSizer( wx.VERTICAL )


		canvasSizer.Add( optionalCanvasSizer, 1, wx.EXPAND, 5 )


		scrolled_sizer.Add( canvasSizer, 1, wx.EXPAND, 5 )

		settingsSizer = wx.FlexGridSizer( 0, 2, 0, 0 )
		settingsSizer.SetFlexibleDirection( wx.BOTH )
		settingsSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText12 = wx.StaticText( self.scrolled_window, wx.ID_ANY, u"Dataset shape:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )

		settingsSizer.Add( self.m_staticText12, 0, wx.ALL, 5 )

		self.label_shape = wx.StaticText( self.scrolled_window, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_shape.Wrap( -1 )

		settingsSizer.Add( self.label_shape, 0, wx.ALL, 5 )

		self.m_staticText33 = wx.StaticText( self.scrolled_window, wx.ID_ANY, u"Window Size:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText33.Wrap( -1 )

		settingsSizer.Add( self.m_staticText33, 0, wx.ALL, 5 )

		self.window_size_slider = wx.Slider( self.scrolled_window, wx.ID_ANY, 50, 1, 100, wx.DefaultPosition, wx.Size( 200,-1 ), wx.SL_HORIZONTAL|wx.SL_VALUE_LABEL )
		settingsSizer.Add( self.window_size_slider, 0, wx.ALL, 5 )

		self.m_staticText35 = wx.StaticText( self.scrolled_window, wx.ID_ANY, u"Overlap:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText35.Wrap( -1 )

		settingsSizer.Add( self.m_staticText35, 0, wx.ALL, 5 )

		self.overlap_slider = wx.Slider( self.scrolled_window, wx.ID_ANY, 0, 0, 100, wx.DefaultPosition, wx.Size( 200,-1 ), wx.SL_HORIZONTAL|wx.SL_VALUE_LABEL )
		settingsSizer.Add( self.overlap_slider, 0, wx.ALL, 5 )

		self.btn_execute = wx.Button( self.scrolled_window, wx.ID_ANY, u"Execute", wx.DefaultPosition, wx.DefaultSize, 0 )
		settingsSizer.Add( self.btn_execute, 0, wx.ALL, 5 )

		self.btn_close = wx.Button( self.scrolled_window, wx.ID_ANY, u"Close Tab", wx.DefaultPosition, wx.DefaultSize, 0 )
		settingsSizer.Add( self.btn_close, 0, wx.ALL, 5 )


		scrolled_sizer.Add( settingsSizer, 1, wx.EXPAND, 5 )


		self.scrolled_window.SetSizer( scrolled_sizer )
		self.scrolled_window.Layout()
		scrolled_sizer.Fit( self.scrolled_window )
		mainSizer.Add( self.scrolled_window, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizer( mainSizer )
		self.Layout()

	def __del__( self ):
		pass


###########################################################################
## Class GenericCanvasPanel
###########################################################################

class GenericCanvasPanel ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL|wx.VSCROLL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		genericSizer = wx.BoxSizer( wx.VERTICAL )

		self.genericNotebook = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

		genericSizer.Add( self.genericNotebook, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizer( genericSizer )
		self.Layout()

	def __del__( self ):
		pass


