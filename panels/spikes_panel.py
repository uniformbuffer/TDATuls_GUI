from export import *
from panels.base_panel import *
from noname import PanelSpikes

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
		self.add_export('','Spikes',spikes_list)
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

