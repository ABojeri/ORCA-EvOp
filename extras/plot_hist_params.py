'''
PLOT HISTOGRAM DISTRIBUTION OF PARAMETERS:
Multiple parameters files in input.
'''


import csv
import sys
from matplotlib import pyplot
import statistics
import numpy as np
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

class Root(Tk):
	def __init__(self):
		super(Root, self).__init__()
		self.title("Browse Files")
		self.minsize(200, 200)
		self.wm_iconbitmap('icon.ico')
		self.labelFrame = ttk.LabelFrame(self, text = "Select Statistics Files")
		self.labelFrame.grid(column = 0, row = 1, padx = 20, pady = 20)
		self.button()

	def button(self):
		self.button = ttk.Button(self.labelFrame, text = "Browse Files",command = self.fileDialog)
		self.button.grid(column = 1, row = 1)

	def fileDialog(self):
		self.filename = filedialog.askopenfilenames()
		self.label = ttk.Label(self.labelFrame, text = "")
		self.label.grid(column = 1, row = 2)
		self.label.configure(text = self.filename)

def main():
	root = Root()
	root.attributes("-topmost", True)
	root.mainloop()

	filenames = root.filename

	neigh_dist = []
	maxNeigh = []
	t_horiz = []
	t_horiz_obst = []
	radius = []
	max_speed = []

	for index, f in enumerate(filenames):
		with open(f, mode='r') as file:
			reader = csv.reader(file, delimiter=',')
			for row in reader:
				neigh_dist.append(float(row[0]))
				maxNeigh.append(float(row[1]))
				t_horiz.append(float(row[2]))
				t_horiz_obst.append(float(row[3]))
				max_speed.append(float(row[4]))

	fig, ax = pyplot.subplots(5, 1)
	range = np.arange(0, 11, 2)


	ax[0].hist(neigh_dist, bins=np.arange(0.1, 5.2, 0.1), density=False, align='left', edgecolor='black', linewidth=1)
	ax[0].set_title('neighborDist')
	ax[0].grid(axis='y')
	ax[0].set_yticks(ticks=range)

	ax[1].hist(maxNeigh, bins=np.arange(1, 5, 1), density=False, align='left', edgecolor='black', linewidth=1)
	ax[1].set_title('maxNeighbors')
	ax[1].grid(axis='y')
	ax[1].set_yticks(ticks=range)
	ax[1].set_xticks([1, 2, 3])

	ax[2].hist(t_horiz, bins=np.arange(0.1, 11, 0.5), density=False, align='left', edgecolor='black', linewidth=1)
	ax[2].set_title('timeHorizon')
	ax[2].grid(axis='y')
	ax[2].set_yticks(ticks=range)

	ax[3].hist(t_horiz_obst, bins=np.arange(0.1, 11, 0.5), density=False, align='left', edgecolor='black', linewidth=1)
	ax[3].set_title('timeHorizonObst')
	ax[3].grid(axis='y')
	ax[3].set_yticks(ticks=range)

	ax[4].hist(max_speed, bins=np.arange(0.5, 6, 0.5), density=False, align='left', edgecolor='black', linewidth=1)
	ax[4].set_title('maxSpeed')
	ax[4].grid(axis='y')
	ax[4].set_yticks(ticks=range)
	
	pyplot.subplots_adjust(hspace = 0.5)
	pyplot.show()





if __name__ == '__main__':
	main()

