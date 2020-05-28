'''
PLOT BEST FITNESS OF RUN:
Single statistics file in input.
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
		self.title("Browse Statistics File")
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
	fitness = []
	with open(filename, mode='r') as file:
		reader = csv.reader(file, delimiter=',')
		for row in reader:
			fitness.append(float(row[3]))

	stdev_fitness = statistics.stdev(fitness)
	x = np.arange(np.size(fitness))

	fig, ax = pyplot.subplots()
	#error = ax.errorbar(x, fitness, yerr = stdev_fitness)
	#pyplot.title('Fitness over epochs')
	pyplot.xlabel('Generation')
	pyplot.ylabel('Fitness')
	#pyplot.ylim((0, max(fitness)))
	pyplot.grid()
	pyplot.plot(fitness, color='g')
	#pyplot.errorbar(x, fitness, yerr=stdev_fitness, ecolor='red', errorevery=100)
	pyplot.show()



if __name__ == '__main__':
	main()


