# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

ID_IMPORT_DATA = 1000
ID_AS_PNG = 1001
ID_LOWER_STAR = 1002
ID_RIPSER = 1003
ID_DISTANCE_MATRIX = 1004
ID_HOLES = 1005
ID_CLUSTER = 1006
ID_ABOUT = 1007

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"TDATuls", pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		self.m_menubar1 = wx.MenuBar( 0 )
		self.file = wx.Menu()
		self.importData = wx.MenuItem( self.file, ID_IMPORT_DATA, u"Import Data", wx.EmptyString, wx.ITEM_NORMAL )
		self.file.Append( self.importData )

		self.export = wx.Menu()
		self.asPng = wx.MenuItem( self.export, ID_AS_PNG, u"As .png", wx.EmptyString, wx.ITEM_NORMAL )
		self.export.Append( self.asPng )

		self.file.AppendSubMenu( self.export, u"Export" )

		self.m_menubar1.Append( self.file, u"File" )

		self.newOperation = wx.Menu()
		self.slidingWindow = wx.Menu()
		self.lowerStar = wx.MenuItem( self.slidingWindow, ID_LOWER_STAR, u"Lower Star", wx.EmptyString, wx.ITEM_NORMAL )
		self.slidingWindow.Append( self.lowerStar )

		self.ripser = wx.MenuItem( self.slidingWindow, ID_RIPSER, u"Ripser", wx.EmptyString, wx.ITEM_NORMAL )
		self.slidingWindow.Append( self.ripser )

		self.newOperation.AppendSubMenu( self.slidingWindow, u"Sliding Window" )

		self.correlationMatrix = wx.Menu()
		self.distanceMatrix = wx.MenuItem( self.correlationMatrix, ID_DISTANCE_MATRIX, u"Distance Matrix", wx.EmptyString, wx.ITEM_NORMAL )
		self.correlationMatrix.Append( self.distanceMatrix )

		self.holes = wx.MenuItem( self.correlationMatrix, ID_HOLES, u"Holes", wx.EmptyString, wx.ITEM_NORMAL )
		self.correlationMatrix.Append( self.holes )

		self.newOperation.AppendSubMenu( self.correlationMatrix, u"Correlation Matrix" )

		self.cluster = wx.MenuItem( self.newOperation, ID_CLUSTER, u"Cluster", wx.EmptyString, wx.ITEM_CHECK )
		self.newOperation.Append( self.cluster )

		self.m_menubar1.Append( self.newOperation, u"New Operation" )

		self.help = wx.Menu()
		self.about = wx.MenuItem( self.help, ID_ABOUT, u"About", wx.EmptyString, wx.ITEM_NORMAL )
		self.help.Append( self.about )

		self.m_menubar1.Append( self.help, u"Help" )

		self.SetMenuBar( self.m_menubar1 )

		self.panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )

		self.notebook = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )


		#self.SetSizer( notebookSizer )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_MENU, self.lowerStarOnMenuSelection, id = self.lowerStar.GetId() )
		self.Bind( wx.EVT_MENU, self.ripserOnMenuSelection, id = self.ripser.GetId() )
		self.Bind( wx.EVT_MENU, self.distanceMatrixOnMenuSelection, id = self.distanceMatrix.GetId() )
		self.Bind( wx.EVT_MENU, self.holesOnMenuSelection, id = self.holes.GetId() )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def lowerStarOnMenuSelection( self, event ):
		event.Skip()

	def ripserOnMenuSelection( self, event ):
		event.Skip()

	def distanceMatrixOnMenuSelection( self, event ):
		event.Skip()

	def holesOnMenuSelection( self, event ):
		event.Skip()


###########################################################################
## Class PanelLowerStar
###########################################################################

class PanelLowerStar ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		mainSizer = wx.FlexGridSizer( 2, 1, 30, 30 )
		mainSizer.SetFlexibleDirection( wx.BOTH )
		mainSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		canvasSizer = wx.FlexGridSizer( 1, 1, 0, 10 )
		canvasSizer.SetFlexibleDirection( wx.BOTH )
		canvasSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )


		mainSizer.Add( canvasSizer, 1, wx.EXPAND, 5 )

		settingsSizer = wx.FlexGridSizer( 0, 2, 0, 0 )
		settingsSizer.SetFlexibleDirection( wx.BOTH )
		settingsSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText10 = wx.StaticText( self, wx.ID_ANY, u"Dataset shape:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )

		settingsSizer.Add( self.m_staticText10, 0, wx.ALL, 5 )

		self.label_shape = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_shape.Wrap( -1 )

		settingsSizer.Add( self.label_shape, 0, wx.ALL, 5 )

		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Window Size:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )

		settingsSizer.Add( self.m_staticText1, 0, wx.ALL, 5 )

		self.spn_window_size = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10, 2 )
		settingsSizer.Add( self.spn_window_size, 0, wx.ALL, 5 )

		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Overlap Pct:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )

		settingsSizer.Add( self.m_staticText2, 0, wx.ALL, 5 )

		self.sl_overlap = wx.Slider( self, wx.ID_ANY, 50, 0, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
		settingsSizer.Add( self.sl_overlap, 0, wx.ALL, 5 )

		self.chx_entropy = wx.CheckBox( self, wx.ID_ANY, u"Pers. Entropy", wx.DefaultPosition, wx.DefaultSize, 0 )
		settingsSizer.Add( self.chx_entropy, 0, wx.ALL, 5 )

		self.btn_execute = wx.Button( self, wx.ID_ANY, u"Execute", wx.DefaultPosition, wx.DefaultSize, 0 )
		settingsSizer.Add( self.btn_execute, 0, wx.ALL, 5 )

		self.btn_close = wx.Button( self, wx.ID_ANY, u"Close Tab", wx.DefaultPosition, wx.DefaultSize, 0 )
		settingsSizer.Add( self.btn_close, 0, wx.ALL, 5 )


		mainSizer.Add( settingsSizer, 1, wx.EXPAND, 5 )


		self.SetSizer( mainSizer )
		self.Layout()

	def __del__( self ):
		pass


###########################################################################
## Class PanelRipser
###########################################################################

class PanelRipser ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		mainSizer = wx.FlexGridSizer( 0, 2, 0, 0 )
		mainSizer.SetFlexibleDirection( wx.BOTH )
		mainSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		canvasSizer = wx.FlexGridSizer( 1, 1, 0, 10 )
		canvasSizer.SetFlexibleDirection( wx.BOTH )
		canvasSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )


		mainSizer.Add( canvasSizer, 1, wx.EXPAND, 5 )

		settingsSizer = wx.FlexGridSizer( 0, 2, 0, 0 )
		settingsSizer.SetFlexibleDirection( wx.BOTH )
		settingsSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText12 = wx.StaticText( self, wx.ID_ANY, u"Dataset shape:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )

		settingsSizer.Add( self.m_staticText12, 0, wx.ALL, 5 )

		self.label_shape = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_shape.Wrap( -1 )

		settingsSizer.Add( self.label_shape, 0, wx.ALL, 5 )

		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"Window Size:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )

		settingsSizer.Add( self.m_staticText3, 0, wx.ALL, 5 )

		self.spn_window_size = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10, 0 )
		settingsSizer.Add( self.spn_window_size, 0, wx.ALL, 5 )

		self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"Overalp Pct", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )

		settingsSizer.Add( self.m_staticText4, 0, wx.ALL, 5 )

		self.sl_overlap = wx.Slider( self, wx.ID_ANY, 50, 0, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
		settingsSizer.Add( self.sl_overlap, 0, wx.ALL, 5 )

		self.chx_entropy = wx.CheckBox( self, wx.ID_ANY, u"Pers. Entropy", wx.DefaultPosition, wx.DefaultSize, 0 )
		settingsSizer.Add( self.chx_entropy, 0, wx.ALL, 5 )

		self.btn_execute = wx.Button( self, wx.ID_ANY, u"Execute", wx.DefaultPosition, wx.DefaultSize, 0 )
		settingsSizer.Add( self.btn_execute, 0, wx.ALL, 5 )

		self.btn_close = wx.Button( self, wx.ID_ANY, u"Close Tab", wx.DefaultPosition, wx.DefaultSize, 0 )
		settingsSizer.Add( self.btn_close, 0, wx.ALL, 5 )


		mainSizer.Add( settingsSizer, 1, wx.EXPAND, 5 )


		self.SetSizer( mainSizer )
		self.Layout()

	def __del__( self ):
		pass


###########################################################################
## Class PanelCorrMatDist
###########################################################################

class PanelCorrMatDist ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		mainSizer = wx.FlexGridSizer( 0, 2, 0, 0 )
		mainSizer.SetFlexibleDirection( wx.BOTH )
		mainSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		canvasSizer = wx.FlexGridSizer( 1, 1, 0, 10 )
		canvasSizer.SetFlexibleDirection( wx.BOTH )
		canvasSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )


		mainSizer.Add( canvasSizer, 1, wx.EXPAND, 5 )

		settingsSizer = wx.FlexGridSizer( 0, 2, 0, 0 )
		settingsSizer.SetFlexibleDirection( wx.BOTH )
		settingsSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText14 = wx.StaticText( self, wx.ID_ANY, u"Dataset shape:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText14.Wrap( -1 )

		settingsSizer.Add( self.m_staticText14, 0, wx.ALL, 5 )

		self.label_shape = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_shape.Wrap( -1 )

		settingsSizer.Add( self.label_shape, 0, wx.ALL, 5 )

		self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, u"Window Size:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )

		settingsSizer.Add( self.m_staticText5, 0, wx.ALL, 5 )

		self.spn_window_size = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10, 0 )
		settingsSizer.Add( self.spn_window_size, 0, wx.ALL, 5 )

		self.m_staticText6 = wx.StaticText( self, wx.ID_ANY, u"Overlap Pct", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )

		settingsSizer.Add( self.m_staticText6, 0, wx.ALL, 5 )

		self.sl_overlap = wx.Slider( self, wx.ID_ANY, 50, 0, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
		settingsSizer.Add( self.sl_overlap, 0, wx.ALL, 5 )

		self.m_staticText9 = wx.StaticText( self, wx.ID_ANY, u"Distance Metric", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9.Wrap( -1 )

		settingsSizer.Add( self.m_staticText9, 0, wx.ALL, 5 )

		ch_metricChoices = []
		self.ch_metric = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, ch_metricChoices, 0 )
		self.ch_metric.SetSelection( 0 )
		settingsSizer.Add( self.ch_metric, 0, wx.ALL, 5 )

		self.chx_entropy = wx.CheckBox( self, wx.ID_ANY, u"Pers. Entropy", wx.DefaultPosition, wx.DefaultSize, 0 )
		settingsSizer.Add( self.chx_entropy, 0, wx.ALL, 5 )

		self.btn_execute = wx.Button( self, wx.ID_ANY, u"Execute", wx.DefaultPosition, wx.DefaultSize, 0 )
		settingsSizer.Add( self.btn_execute, 0, wx.ALL, 5 )

		self.btn_close = wx.Button( self, wx.ID_ANY, u"Close Tab", wx.DefaultPosition, wx.DefaultSize, 0 )
		settingsSizer.Add( self.btn_close, 0, wx.ALL, 5 )


		mainSizer.Add( settingsSizer, 1, wx.EXPAND, 5 )


		self.SetSizer( mainSizer )
		self.Layout()

	def __del__( self ):
		pass


###########################################################################
## Class PanelCorrMatHoles
###########################################################################

class PanelCorrMatHoles ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		mainSizer = wx.FlexGridSizer( 0, 2, 0, 0 )
		mainSizer.SetFlexibleDirection( wx.BOTH )
		mainSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		canvasSizer = wx.FlexGridSizer( 0, 2, 0, 0 )
		canvasSizer.SetFlexibleDirection( wx.BOTH )
		canvasSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )


		mainSizer.Add( canvasSizer, 1, wx.EXPAND, 5 )

		settingsSizer = wx.FlexGridSizer( 0, 2, 0, 0 )
		settingsSizer.SetFlexibleDirection( wx.BOTH )
		settingsSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText16 = wx.StaticText( self, wx.ID_ANY, u"Dataset shape:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText16.Wrap( -1 )

		settingsSizer.Add( self.m_staticText16, 0, wx.ALL, 5 )

		self.label_shape = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_shape.Wrap( -1 )

		settingsSizer.Add( self.label_shape, 0, wx.ALL, 5 )

		self.m_staticText10 = wx.StaticText( self, wx.ID_ANY, u"Windows size:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )

		settingsSizer.Add( self.m_staticText10, 0, wx.ALL, 5 )

		self.spn_window_size = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10, 0 )
		settingsSizer.Add( self.spn_window_size, 0, wx.ALL, 5 )

		self.m_staticText12 = wx.StaticText( self, wx.ID_ANY, u"Overlap Pct", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )

		settingsSizer.Add( self.m_staticText12, 0, wx.ALL, 5 )

		self.sl_overlap = wx.Slider( self, wx.ID_ANY, 50, 0, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
		settingsSizer.Add( self.sl_overlap, 0, wx.ALL, 5 )

		self.m_staticText18 = wx.StaticText( self, wx.ID_ANY, u"Distance metric", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText18.Wrap( -1 )

		settingsSizer.Add( self.m_staticText18, 0, wx.ALL, 5 )

		ch_metricChoices = []
		self.ch_metric = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, ch_metricChoices, 0 )
		self.ch_metric.SetSelection( 0 )
		settingsSizer.Add( self.ch_metric, 0, wx.ALL, 5 )

		self.chx_entropy = wx.CheckBox( self, wx.ID_ANY, u"Pers. Entropy", wx.DefaultPosition, wx.DefaultSize, 0 )
		settingsSizer.Add( self.chx_entropy, 0, wx.ALL, 5 )

		self.btn_execute = wx.Button( self, wx.ID_ANY, u"Execute", wx.DefaultPosition, wx.DefaultSize, 0 )
		settingsSizer.Add( self.btn_execute, 0, wx.ALL, 5 )

		self.btn_close = wx.Button( self, wx.ID_ANY, u"Close Tab", wx.DefaultPosition, wx.DefaultSize, 0 )
		settingsSizer.Add( self.btn_close, 0, wx.ALL, 5 )


		mainSizer.Add( settingsSizer, 1, wx.EXPAND, 5 )


		self.SetSizer( mainSizer )
		self.Layout()

	def __del__( self ):
		pass


###########################################################################
## Class GenericCanvasPanel
###########################################################################

class GenericCanvasPanel ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		genericSizer = wx.BoxSizer( wx.VERTICAL )

		self.genericNotebook = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

		genericSizer.Add( self.genericNotebook, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizer( genericSizer )
		self.Layout()

	def __del__( self ):
		pass


