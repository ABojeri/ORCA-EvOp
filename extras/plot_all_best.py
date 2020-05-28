'''
PLOT ALL THE FITNESS BEST VALUES:
Multiple statistics files in input.
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

	fig, ax = pyplot.subplots()

	pyplot.grid()
	h = []
	names = np.arange(10)
	minimum = []

	for index, f in enumerate(filenames):
		fitness = []
		with open(f, mode='r') as file:
			reader = csv.reader(file, delimiter=',')
			for row in reader:
				fitness.append(float(row[3]))

		x = np.arange(np.size(fitness))
		pyplot.plot(fitness, label=("Evolution {0}: {1}".format(index+1, min(fitness))))
		minimum.append(min(fitness))

	abs_minimum = min(minimum)
	best_run = minimum.index(min(minimum))

	ax.legend(loc='best')
	pyplot.title('Fitness over generations\n Minimum Value at Evolution {0}: {1}'.format(best_run+1, abs_minimum))
	pyplot.xlabel('Generation')
	pyplot.ylabel('Fitness')


	pyplot.show()



if __name__ == '__main__':
	main()


