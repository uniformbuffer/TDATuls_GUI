import wx
from wx.adv import NotificationMessage
from functools import partial

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


	def __exit__(self, exc_type, exc_value, traceback):
		print('exited')

