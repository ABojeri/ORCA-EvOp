from inspyred_functions import *
import csv
import sys
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

class Root(Tk):
	def __init__(self):
		super(Root, self).__init__()
		self.title("Browse Parameters File")
		self.minsize(200, 200)
		self.wm_iconbitmap('icon.ico')
		self.labelFrame = ttk.LabelFrame(self, text = "Select File")
		self.labelFrame.grid(column = 0, row = 1, padx = 20, pady = 20)
		self.button()

	def button(self):
		self.button = ttk.Button(self.labelFrame, text = "Browse A File",command = self.fileDialog)
		self.button.grid(column = 1, row = 1)

	def fileDialog(self):
		self.filename = filedialog.askopenfilename()
		self.label = ttk.Label(self.labelFrame, text = "")
		self.label.grid(column = 1, row = 2)
		self.label.configure(text = self.filename)

def main():
	root = Root()
	root.attributes("-topmost", True)
	root.mainloop()

	filename = root.filename
	with open(filename, mode='r') as best_individual_file:
		best_individual_reader = csv.reader(best_individual_file, delimiter=',')
		parameters = []
		i=0
		for param in best_individual_reader:
			while i<len(param):
				parameters.append(float(param[i]))
				i+=1

	print('STARTING SIMULATION OF BEST INDIVIDUAL...')
	collision_avoidance_scenario2(1/60., parameters[0], parameters[1], parameters[2], parameters[3], 0.1, parameters[4], gui_interface=True)



if __name__ == '__main__':
    main()


