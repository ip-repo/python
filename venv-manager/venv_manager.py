import os
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview

class VenvManager(ttk.Frame):
	"""venvmanager class build the app widgets and functionality."""
	def __init__(self, master):
		super().__init__(master,padding=(10,20))
		self.venvs_list_file = "venv_list.txt"
		self.i = 0
		self.pack(fill=BOTH, expand=NO)
		self.init_widgets()

	def init_widgets(self):
		"""this method build the widgets."""
		self.instruction = ttk.Label(self,text="Welcome to venv manager.", width=50)
		self.instruction.pack(fill=X)

		self.version = ttk.StringVar(value="")
		self.path = ttk.StringVar(value="")
		self.name = ttk.StringVar(value="")
		
		self.build_form_entry("Python Version:", self.version )
		self.build_form_entry("Venv Path:", self.path)
		self.build_form_entry("Venv Name:", self.name)
		self.parse_data()
		self.table = self.build_table()
		
		self.buttons = self.build_form_buttons()
		
	def build_form_buttons(self):
		"""this method build the buttons."""
		button_container = ttk.Frame(self)
		button_container.pack(fill=X, expand=NO, pady=(15,10))
		
		launch_venv = ttk.Button(
		master=button_container,
		text="Launch",
		command=self.launch_clicked,
		bootstyle=DANGER,
		width=20
		)
		launch_venv.pack(side=RIGHT, padx=5)

		save_venv = ttk.Button(
		master=button_container,
		text="Save",
		command=self.add_row,
		bootstyle=SUCCESS,
		width=20
		)
		save_venv.pack(side=RIGHT, padx=5)

		delete_venv = ttk.Button(
		master=button_container,
		text="Delete",
		command=self.delete_row,
		bootstyle=SUCCESS,
		width=20
		)
		delete_venv.pack(side=RIGHT, padx=5)


		clear_venv = ttk.Button(
		master=button_container,
		text="Clear",
		command=self.clear,
		bootstyle=SUCCESS,
		width=20
		)
		clear_venv.pack(side=RIGHT, padx=5)
		return button_container

	def build_form_entry(self, label, variable):
		"""
		this method build a form entry
		"""
		container = ttk.Frame(self)
		container.pack(fill=X,expand=YES, pady=10)

		form_field_label = ttk.Label(master=container, text=label, width=15)
		form_field_label.pack(side=LEFT, padx=3)

		form_input = ttk.Entry(master=container, textvariable=variable)
		form_input.pack(side=LEFT,pady=5, fill=X, expand=YES)
		return form_input
	
	def parse_data(self):
		"""
		this method parse the venv list text file.
		"""
		self.venvs = []
		with open(self.venvs_list_file,"r") as venvs_file:
			for venv in venvs_file:
				to_add = venv.rstrip().split(",")
				if to_add in self.venvs:
					continue
				else:
					self.venvs.append(to_add)
					
	def build_table(self):
		"""
		this method build the table view widget.
		"""
		coldata = [
			{"text": "Name","width":80 },
			{"text" : "Path", "width": 776},
			{"text": "Version","width":80 },
		]
		table = Tableview(
			master=self,
			coldata=coldata,
			rowdata=self.venvs,
			paginated=True,
			autoalign=True,
			bootstyle=PRIMARY,
			#stripecolor=(self.colors.light,None)
		)
		table.pack(fill=X, expand=NO)
		table.view.bind("<<TreeviewSelect>>", self.item_selected)
		return table

	def item_selected(self, *args):
		"""this method is used when user click on a tableview row and update the form."""
		if self.i == 0:
			self.i +=1
		else:

			table_item_selected_values = self.table.get_rows(selected=True)[0].values
			self.name.set(table_item_selected_values[0])
			self.path.set(table_item_selected_values[1])
			self.version.set(table_item_selected_values[2])
			
	def clear(self):
		"""this method clear the form inputs when Clear button is clicked."""
		self.name.set("")
		self.path.set("")
		self.version.set("")
		self.instruction.configure(text="Welcom to venv manager.")
	
	def delete_row(self):
		"""this method is called when user click to delete a table row."""
		if self.venvs:
			venvs = []
			to_delete = self.table.get_rows(selected=True)[0].values
			for venv in self.venvs:
				if venv[0] == to_delete[0] and  venv[1] == to_delete[1] and  venv[2] == to_delete[2]:
					continue
				else:
					venvs.append(venv)
			self.venvs = venvs

			if self.venvs:
				output = ""
				with open(self.venvs_list_file,"w")as venvs_list_file:
					for venv in self.venvs:
						output+= ",".join(venv)+"\n"
					venvs_list_file.write(output)
					...
			else:
				with open(self.venvs_list_file,"w")as venvs_list_file:
					venvs_list_file.write("")
			self.table.destroy()
			self.buttons.destroy()
			self.parse_data()
			self.table = self.build_table()
			self.buttons = self.build_form_buttons()
			self.clear()
			self.instruction.configure(text=self.name.get() + " Deleted!")
		
	def add_row(self):
		"""this method add a table row according to user input."""
		venvs = []
		if os.path.exists(self.path.get()):
			for venv in self.venvs:
				if self.path.get() in venv:
					self.instruction.configure(text="Venv already enlisted.")
					return
			with open(self.venvs_list_file, "r") as venvs_file:
				for venv in venvs_file:
					venvs.append(venv)
			venvs.append("{},{},{}\n".format(self.name.get(), self.path.get(), self.version.get()))
			with open(self.venvs_list_file, "w") as venvs_file:
				venvs_file.write("".join(venvs))
			self.table.destroy()
			self.buttons.destroy()
			self.parse_data()
			self.table = self.build_table()
			self.buttons = self.build_form_buttons()
		
			self.instruction.configure(text=self.name.get() + " Saved!")
			self.clear()
		else:
			self.instruction.configure(text="Path not found!")

	def launch_clicked(self):
		"""this method activate the venv selected in a new cmd window."""
		
		os.system("start cmd.exe /k {}".format(r'{}'.format(self.table.get_rows(selected=True)[0].values[1])))
		
		self.instruction.configure(text="Launching cmd and if path is correct the venv will be activated.")
		
			
		
if __name__ == "__main__":
	app = ttk.Window(title="Venv Manager", themename="darkly", resizable=(False, False))
	VenvManager(app)
	app.mainloop()
