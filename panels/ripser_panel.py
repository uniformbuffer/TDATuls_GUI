from export import *
from panels.base_panel import *
from noname import PanelRipser

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
		self.window_size_slider.SetMax(self.data.shape[1])

		#self.add_category('Windows')

	def onExecuteButtonClick(self, event):
		self.clear_exports()

		overlap = self.overlap_slider.GetValue()
		window_size = self.window_size_slider.GetValue()
		distance_matrix = self.chx_distance_matrix.IsChecked()
		max_hom_dim = self.spn_max_hom_dim.GetValue()
		metric = self.ch_metric.GetString(self.ch_metric.GetCurrentSelection())
		windows = calculate_windows(window_size,overlap,self.data.shape[1])
		diagrams = {}
		i = 0
		for window in windows:
			dgms = doRipsFiltration(self.data[:,window],max_hom_dim,distance_matrix,metric)#['dgms']
			figure = plt.figure()
			plt.figure(figure.number)
			plot_diagrams(dgms)
			diagrams['window'+str(i)] = figure
			for k in range(0,len(dgms)):
				self.add_export('Windows','Window'+str(i)+" - Homology:"+str(k),dgms[k])
			i+=1

		wx.adv.NotificationMessage('Done', message="Done")
		self.diagrams = diagrams
		self.updateFigure(0)

	def onWindowSizeSliderChange(self, event):
		self.overlap_slider.SetMax(self.window_size_slider.GetValue())

	def onFigureChange(self, event):
		self.updateFigure(self.figure_list.GetCurrentSelection())


