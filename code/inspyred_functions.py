'''
inspyred_functions.py
This module contains the utility functions for inspyred optimizer, such as the generator, the observer and the evaluators.
'''
from math import sqrt
import random
import matplotlib.pyplot as plt
import matplotlib
import rvo2
from math import isclose
import statistics
from tqdm import tqdm as tq
from datetime import datetime 

def distance(point1, point2):
	'''
	Function to calculate the distance between 2 tupleta (i.e. points coordinates).
	Returns the distance value.
	- point1 --> Tuplet with the coordinates of point1
	- point2 --> Tuplet with the coordinates of point2
	'''
	x1, y1 = point1
	x2, y2 = point2
	return sqrt((x1-x2)**2 + (y1-y2)**2)

def check_collisions(point1, point2, rad):
	'''
	Function to check if two agents are colliding.
	Returns a boolean value, True if the collision happens, False if it does not happen.
	- point1 --> Tuplet with the coordinates of point1
	- point2 --> Tuplet with the coordinates of point2
	- rad --> radius used to compare the distances and evaluate the possible collision. It should be the radius of the agents.
	'''
	if distance(point1, point2) < ((2*rad)+(1e-2)):
		return True
	else:
		return False


def generate_population(random, args):
	'''
	Function to generate the initial population of individuals. It makes use of the boundaries set in the "collision_avoidance_EC_scenario" file.
	'''
	chromosome = []
	bounder = args["_ec"].bounder

	for lo, hi in zip(bounder.lower_bound, bounder.upper_bound):
		chromosome.append(random.uniform(lo, hi))
	return chromosome


def custom_observer(population, num_generations, num_evaluations, args):
	'''
	Funtion to plot the main evolution statistics of the optimizer.
	'''
	best = max(population)
	print('Generations: {0}  Evaluations: {1}  Best: {2}'.format(num_generations, num_evaluations, str(best.fitness)))


def plot_agents(history, radius, ax):
	'''
	Function to plot the agents during their path in the simulation.
	It plots the four agents at each time step, which are represented by a point in their location and a circle of radius equal to the radius parameter of the simulator.
	- history --> history instance which contains all the n_iterations tuplets of the the four agents, grouped by time-step.
	'''
	for step in tq(range(history.__len__())):
			ag_nr = 0
			if step % 5 == 0:
				for x,y in history[step]:
					if ag_nr == 0:
						c0 = matplotlib.patches.Circle((x, y), radius=radius, facecolor='none', edgecolor='b', label='Agent 0')
						plt.scatter(x, y, s=1, marker='o', color='b')
						ax.add_artist(c0)
					elif ag_nr == 1:
						c1 = matplotlib.patches.Circle((x, y), radius=radius, facecolor='none', edgecolor='g', label='Agent 1')
						plt.scatter(x, y, s=1, marker='o', color='g')
						ax.add_artist(c1)
					elif ag_nr == 2:
						c2 = matplotlib.patches.Circle((x, y), radius=radius, facecolor='none', edgecolor='r', label='Agent 2')
						plt.scatter(x, y, s=1, marker='o', color='r')
						ax.add_artist(c2)
					elif ag_nr == 3:
						c3 = matplotlib.patches.Circle((x, y), radius=radius, facecolor='none', edgecolor='y', label='Agent 3')
						plt.scatter(x, y, s=1, marker='o', color='y')
						ax.add_artist(c3)
					ag_nr += 1
			plt.legend(handles=[c0, c1, c2, c3], loc='best')
			plt.draw()
			plt.pause(1e-30)


def plot_paths(history, radius, ax):
	'''
	Function to plot the agents path in the simulation.
	It plots the path of the four agents during the simulation. Each agent's path is a line that evolves at each time-step according to the "history" input parameter.
	- history --> history instance which contains all the n_iterations tuplets of the the four agents, grouped by time-step.
	'''
	for step in tq(range(history.__len__())):
			ag_nr = 0
			if step == 0:
				for x,y in history[step]:
					if ag_nr == 0:
						c0 = matplotlib.patches.Circle((x, y), radius=radius, facecolor='none', edgecolor='b', label='Agent 0')
						plt.scatter(x, y, s=1, marker='o', color='b')
						ax.add_artist(c0)
					elif ag_nr == 1:
						c1 = matplotlib.patches.Circle((x, y), radius=radius, facecolor='none', edgecolor='g', label='Agent 1')
						plt.scatter(x, y, s=1, marker='o', color='g')
						ax.add_artist(c1)
					elif ag_nr == 2:
						c2 = matplotlib.patches.Circle((x, y), radius=radius, facecolor='none', edgecolor='r', label='Agent 2')
						plt.scatter(x, y, s=1, marker='o', color='r')
						ax.add_artist(c2)
					elif ag_nr == 3:
						c3 = matplotlib.patches.Circle((x, y), radius=radius, facecolor='none', edgecolor='y', label='Agent 3')
						plt.scatter(x, y, s=1, marker='o', color='y')
						ax.add_artist(c3)
					ag_nr += 1
			else:
				for x,y in history[step]:
					ag0 = history[step-1][0]
					ag1 = history[step-1][1]
					ag2 = history[step-1][2]
					ag3 = history[step-1][3]
					if ag_nr == 0:
						plt.plot([ag0[0], x], [ag0[1], y], color='b', label='Agent0')
					elif ag_nr == 1:
						plt.plot([ag1[0], x], [ag1[1], y], color='g', label='Agent1')
					elif ag_nr == 2:
						plt.plot([ag2[0], x], [ag2[1], y], color='r', label='Agent2')
					elif ag_nr == 3:
						plt.plot([ag3[0], x], [ag3[1], y], color='y', label='Agent3')
					ag_nr += 1
			plt.legend(handles=[c0, c1, c2, c3], loc='best')
			plt.draw()
			plt.pause(1e-30)



def collision_avoidance_scenario1(time_step, param0, param1, param2, param3, rad, param4, gui_interface=False):
	'''
	Function to run a simulation with RVO2 simulator in scenario I environment. It is used to evaluate the fitness function value of a set of parameters that represent a candidate solution.
	Returns the fitness function value for the input parameters set.
	- time_step --> simulation time-step
	- param0 --> First parameter to be optimized, which correspond to neigh_dist
	- param1 --> Second parameter to be optimized, which correspond to max_neigh
	- param2 --> Third parameter to be optimized, which correspond to t_horiz
	- param3 --> Fourth parameter to be optimized, which correspond to t_horiz_obst
	- rad --> agents radius
	- param4 --> Fifth parameter to be optimized, which correspond to max_speed
	- gui_interface --> boolean value use to activate (True) or deactivate (False) the plot of the simulation at the end of the agents path computation.
	'''
	gui = gui_interface

	now = datetime.now()
	timestamp = now.strftime('%Y_%m_%d_%H_%M_%S')

	fitness = 0.0

	plt.close('all')

	t_step = time_step
	neigh_dist = param0
	max_neigh = param1
	t_horiz = param2
	t_horiz_obst = param3
	radius = rad
	max_speed = param4

	sim = rvo2.PyRVOSimulator(t_step, neigh_dist, max_neigh, t_horiz, t_horiz_obst, radius, max_speed)

	n_iterations = int(t_step*100000)
	r_buffer = 1e-1


	boundary1 = [(-1, -1), (-1, 11), (-1.5, 11.5), (-1.5, -1.5)]
	boundary2 = [(-1, 11), (11, 11), (11.5, 11.5), (-1.5, 11.5)]
	boundary3 = [(11, 11), (11, -1), (11.5, -1.5), (11.5, 11.5)]
	boundary4 = [(11, -1), (-1, -1), (-1.5, -1.5), (11.5, -1.5)]

	vertices = [(6, 4), (6, 6), (4, 6), (4, 4)]


	a0 = sim.addAgent((0, 0))
	a1 = sim.addAgent((10, 0))
	a2 = sim.addAgent((10, 10))
	a3 = sim.addAgent((0, 10))

	b1 = sim.addObstacle(boundary1)
	b2 = sim.addObstacle(boundary2)
	b3 = sim.addObstacle(boundary3)
	b4 = sim.addObstacle(boundary4)

	o1 = sim.addObstacle(vertices)
	sim.processObstacles()

	sim.setAgentPrefVelocity(a0, (1, 1))
	sim.setAgentPrefVelocity(a1, (-1, 1))
	sim.setAgentPrefVelocity(a2, (-1, -1))
	sim.setAgentPrefVelocity(a3, (1, -1))

	history = []
	history.append([(0,0), (10,0), (10,10), (0,10)])
	positions = [(0,0), (10,0), (10,10), (0,10)]

	ag0_results = {'agent_nr': 0, 'found': False, 'timestep': n_iterations, 'position': []}
	ag1_results = {'agent_nr': 1, 'found': False, 'timestep': n_iterations, 'position': []}
	ag2_results = {'agent_nr': 2, 'found': False, 'timestep': n_iterations, 'position': []}
	ag3_results = {'agent_nr': 3, 'found': False, 'timestep': n_iterations, 'position': []}

	collisions = 0

	for step in range(n_iterations):
		if ag0_results['found'] == True and ag1_results['found'] == True and ag2_results['found'] == True and ag3_results['found'] == True:
			if gui:
				print('ALL AGENTS REACHED THEIR TARGETS! SIMULATION COMPLETED...')
			break

		sim.doStep()
		positions = []
		for agent_no in (a0, a1, a2, a3):
			pos = '(%5.3f, %5.3f)' % sim.getAgentPosition(agent_no)
			pos_tuple = eval(pos)
			positions.append(pos_tuple)

		history.append(positions)

		if check_collisions(positions[0], positions[1], radius):
			collisions += 1
		if check_collisions(positions[0], positions[2], radius):
			collisions += 1
		if check_collisions(positions[0], positions[3], radius):
			collisions += 1
		if check_collisions(positions[1], positions[2], radius):
			collisions += 1
		if check_collisions(positions[1], positions[3], radius):
			collisions += 1
		if check_collisions(positions[2], positions[3], radius):
			collisions += 1

		sim.setAgentPrefVelocity(a0, (10 - positions[0][0], 10 - positions[0][1]))
		sim.setAgentPrefVelocity(a1, (0 - positions[1][0], 10 - positions[1][1]))
		sim.setAgentPrefVelocity(a2, (0 - positions[2][0], 0 - positions[2][1]))
		sim.setAgentPrefVelocity(a3, (10 - positions[3][0], 0 - positions[3][1]))

		if isclose(history[-1][0][0], 10, abs_tol=r_buffer) == True and isclose(history[-1][0][1], 10, abs_tol=r_buffer) == True and ag0_results['found'] == False:
			ag0_results['found'] = True
			ag0_results['timestep'] = step
			ag0_results['position'] = positions[0]
			if gui == True:
				print('AGENT 0 TARGET REACHED: %s' % str(positions[0]))
		
		if isclose(history[-1][1][0], 0, abs_tol=r_buffer) == True and isclose(history[-1][1][1], 10, abs_tol=r_buffer) == True and ag1_results['found'] == False:
			ag1_results['found'] = True
			ag1_results['timestep'] = step
			ag1_results['position'] = positions[1]
			if gui == True:
				print('AGENT 1 TARGET REACHED: %s' % str(positions[1]))
		
		if isclose(history[-1][2][0], 0, abs_tol=r_buffer) == True and isclose(history[-1][2][1], 0, abs_tol=r_buffer) == True and ag2_results['found'] == False:
			ag2_results['found'] = True
			ag2_results['timestep'] = step
			ag2_results['position'] = positions[2]
			if gui==True:
				print('AGENT 2 TARGET REACHED: %s' % str(positions[2]))
		
		if isclose(history[-1][3][0], 10, abs_tol=r_buffer) == True and isclose(history[-1][3][1], 0, abs_tol=r_buffer) == True and ag3_results['found'] == False:
			ag3_results['found'] = True
			ag3_results['timestep'] = step
			ag3_results['position'] = positions[3]
			if gui==True:
				print('AGENT 3 TARGET REACHED: %s' % str(positions[3]))
		
	if gui==True:
		print('Number of collisions: %d'% collisions)

	errors = []
	errors.append(distance(history[-1][0], (10.0, 10.0)))
	errors.append(distance(history[-1][1], (0.0, 10.0)))
	errors.append(distance(history[-1][2], (0.0, 0.0)))
	errors.append(distance(history[-1][3], (10.0, 0.0)))

	mean_error = statistics.mean(errors)
	mean_error_norm = mean_error / distance((0,0), (10,10))
	collisions_norm = collisions / (6*n_iterations)
	mean_duration = (ag0_results['timestep'] + ag1_results['timestep'] + ag2_results['timestep'] + ag3_results['timestep']) / 4
	mean_duration_norm = mean_duration / n_iterations


	fitness = mean_error + mean_duration_norm + collisions

	if gui == True:
		print('Fitness: {0} for set of parameters: [{1}, {2}, {3}, {4}, {5}]'.format(fitness, param0, param1, param2, param3, param4))
		plt.show()
		fig, ax = plt.subplots()
		plt.fill([boundary1[0][0], boundary1[1][0], boundary1[2][0], boundary1[3][0]], [boundary1[0][1], boundary1[1][1], boundary1[2][1], boundary1[3][1]], 'gray')
		plt.fill([boundary2[0][0], boundary2[1][0], boundary2[2][0], boundary2[3][0]], [boundary2[0][1], boundary2[1][1], boundary2[2][1], boundary2[3][1]], 'gray')
		plt.fill([boundary3[0][0], boundary3[1][0], boundary3[2][0], boundary3[3][0]], [boundary3[0][1], boundary3[1][1], boundary3[2][1], boundary3[3][1]], 'gray')
		plt.fill([boundary4[0][0], boundary4[1][0], boundary4[2][0], boundary4[3][0]], [boundary4[0][1], boundary4[1][1], boundary4[2][1], boundary4[3][1]], 'gray')
		plt.fill([vertices[0][0], vertices[1][0], vertices[2][0], vertices[3][0]], [vertices[0][1], vertices[1][1], vertices[2][1], vertices[3][1]], 'gray')

		plot_agents(history, radius, ax)
		#plot_paths(history, radius, ax) #DECOMMENT IF ONLY AGENTS PATH LINES ARE NEEDED

		plt.show()



	return fitness


def simulation_evaluator_scenario1(candidates, args):
	'''
	Funtion to evaluate the parameters set generated by the EC algorithm for scenario I.
	- candidates --> candidates chromosomes used to feed the collision-avoidance simulator
	'''
	t_step = 1/60.
	radius = 0.1
	fitness=[]
	for chromosome in candidates:
		neigh_dist = chromosome[0]
		max_neigh = chromosome[1]
		t_horiz = chromosome[2]
		t_horiz_obst = chromosome[3]
		max_speed = chromosome[4]
		fitness.append(collision_avoidance_scenario1(t_step, neigh_dist, max_neigh, t_horiz, t_horiz_obst, radius, max_speed))
	return fitness



def collision_avoidance_scenario2(time_step, param0, param1, param2, param3, rad, param4, gui_interface=False):
	'''
	Function to run a simulation with RVO2 simulator in scenario II environment. It is used to evaluate the fitness function value of a set of parameters that represent a candidate solution.
	Returns the fitness function value for the input parameters set.
	- time_step --> simulation time-step
	- param0 --> First parameter to be optimized, which correspond to neigh_dist
	- param1 --> Second parameter to be optimized, which correspond to max_neigh
	- param2 --> Third parameter to be optimized, which correspond to t_horiz
	- param3 --> Fourth parameter to be optimized, which correspond to t_horiz_obst
	- rad --> agents radius
	- param4 --> Fifth parameter to be optimized, which correspond to max_speed
	- gui_interface --> boolean value use to activate (True) or deactivate (False) the plot of the simulation at the end of the agents path computation.
	'''
	gui = gui_interface

	now = datetime.now()
	timestamp = now.strftime('%Y_%m_%d_%H_%M_%S')

	fitness = 0.0

	plt.close('all')

	t_step = time_step
	neigh_dist = param0
	max_neigh = param1
	t_horiz = param2
	t_horiz_obst = param3
	radius = rad
	max_speed = param4

	sim = rvo2.PyRVOSimulator(t_step, neigh_dist, max_neigh, t_horiz, t_horiz_obst, radius, max_speed)

	n_iterations = int(t_step*100000)
	r_buffer = 1e-1

	boundary1 = [(-1, -1), (-1, 11), (-1.5, 11.5), (-1.5, -1.5)]
	boundary2 = [(-1, 11), (11, 11), (11.5, 11.5), (-1.5, 11.5)]
	boundary3 = [(11, 11), (11, -1), (11.5, -1.5), (11.5, 11.5)]
	boundary4 = [(11, -1), (-1, -1), (-1.5, -1.5), (11.5, -1.5)]
	

	vertices1 = [(2, 2), (4, 2), (4, 4), (2, 4)]
	vertices2 = [(6, 2), (8, 2), (8, 4), (6, 4)]
	vertices3 = [(6, 6), (8, 6), (8, 8), (6, 8)]
	vertices4 = [(2, 6), (4, 6), (4, 8), (2, 8)]

	a0 = sim.addAgent((0, 0))
	a1 = sim.addAgent((10, 0))
	a2 = sim.addAgent((10, 10))
	a3 = sim.addAgent((0, 10))


	b1 = sim.addObstacle(boundary1)
	b2 = sim.addObstacle(boundary2)
	b3 = sim.addObstacle(boundary3)
	b4 = sim.addObstacle(boundary4)

	o1 = sim.addObstacle(vertices1)
	o2 = sim.addObstacle(vertices2)
	o3 = sim.addObstacle(vertices3)
	o4 = sim.addObstacle(vertices4)
	sim.processObstacles()

	sim.setAgentPrefVelocity(a0, (1, 1))
	sim.setAgentPrefVelocity(a1, (-1, 1))
	sim.setAgentPrefVelocity(a2, (-1, -1))
	sim.setAgentPrefVelocity(a3, (1, -1))

	history = []
	history.append([(0,0), (10,0), (10,10), (0,10)])
	positions = [(0,0), (10,0), (10,10), (0,10)]

	ag0_results = {'agent_nr': 0, 'found': False, 'timestep': n_iterations, 'position': []}
	ag1_results = {'agent_nr': 1, 'found': False, 'timestep': n_iterations, 'position': []}
	ag2_results = {'agent_nr': 2, 'found': False, 'timestep': n_iterations, 'position': []}
	ag3_results = {'agent_nr': 3, 'found': False, 'timestep': n_iterations, 'position': []}

	collisions = 0

	for step in range(n_iterations):
		if ag0_results['found'] == True and ag1_results['found'] == True and ag2_results['found'] == True and ag3_results['found'] == True:
			if gui:
				print('ALL AGENTS REACHED THEIR TARGETS! SIMULATION COMPLETED...')
			break

		sim.doStep()
		positions = []
		for agent_no in (a0, a1, a2, a3):
			pos = '(%5.3f, %5.3f)' % sim.getAgentPosition(agent_no)
			pos_tuple = eval(pos)
			positions.append(pos_tuple)

		history.append(positions)

		if check_collisions(positions[0], positions[1], radius):
			collisions += 1
		if check_collisions(positions[0], positions[2], radius):
			collisions += 1
		if check_collisions(positions[0], positions[3], radius):
			collisions += 1
		if check_collisions(positions[1], positions[2], radius):
			collisions += 1
		if check_collisions(positions[1], positions[3], radius):
			collisions += 1
		if check_collisions(positions[2], positions[3], radius):
			collisions += 1

		sim.setAgentPrefVelocity(a0, (10 - positions[0][0], 10 - positions[0][1]))
		sim.setAgentPrefVelocity(a1, (0 - positions[1][0], 10 - positions[1][1]))
		sim.setAgentPrefVelocity(a2, (0 - positions[2][0], 0 - positions[2][1]))
		sim.setAgentPrefVelocity(a3, (10 - positions[3][0], 0 - positions[3][1]))

		if isclose(history[-1][0][0], 10, abs_tol=r_buffer) == True and isclose(history[-1][0][1], 10, abs_tol=r_buffer) == True and ag0_results['found'] == False:
			ag0_results['found'] = True
			ag0_results['timestep'] = step
			ag0_results['position'] = positions[0]
			if gui == True:
				print('AGENT 0 TARGET REACHED: %s' % str(positions[0]))
		
		if isclose(history[-1][1][0], 0, abs_tol=r_buffer) == True and isclose(history[-1][1][1], 10, abs_tol=r_buffer) == True and ag1_results['found'] == False:
			ag1_results['found'] = True
			ag1_results['timestep'] = step
			ag1_results['position'] = positions[1]
			if gui == True:
				print('AGENT 1 TARGET REACHED: %s' % str(positions[1]))
		
		if isclose(history[-1][2][0], 0, abs_tol=r_buffer) == True and isclose(history[-1][2][1], 0, abs_tol=r_buffer) == True and ag2_results['found'] == False:
			ag2_results['found'] = True
			ag2_results['timestep'] = step
			ag2_results['position'] = positions[2]
			if gui==True:
				print('AGENT 2 TARGET REACHED: %s' % str(positions[2]))
		
		if isclose(history[-1][3][0], 10, abs_tol=r_buffer) == True and isclose(history[-1][3][1], 0, abs_tol=r_buffer) == True and ag3_results['found'] == False:
			ag3_results['found'] = True
			ag3_results['timestep'] = step
			ag3_results['position'] = positions[3]
			if gui==True:
				print('AGENT 3 TARGET REACHED: %s' % str(positions[3]))
		
	if gui==True:
		print('Number of collisions: %d'% collisions)

	errors = []
	errors.append(distance(history[-1][0], (10.0, 10.0)))
	errors.append(distance(history[-1][1], (0.0, 10.0)))
	errors.append(distance(history[-1][2], (0.0, 0.0)))
	errors.append(distance(history[-1][3], (10.0, 0.0)))

	mean_error = statistics.mean(errors)
	mean_error_norm = mean_error / distance((0,0), (10,10))
	collisions_norm = collisions / (6*n_iterations)
	mean_duration = (ag0_results['timestep'] + ag1_results['timestep'] + ag2_results['timestep'] + ag3_results['timestep']) / 4
	mean_duration_norm = mean_duration / n_iterations

	fitness = mean_error + mean_duration_norm + collisions

	if gui == True:
		print('Fitness: {0} for set of parameters: [{1}, {2}, {3}, {4}, {5}]'.format(fitness, param0, param1, param2, param3, param4))
		plt.show()
		fig, ax = plt.subplots()
		plt.fill([boundary1[0][0], boundary1[1][0], boundary1[2][0], boundary1[3][0]], [boundary1[0][1], boundary1[1][1], boundary1[2][1], boundary1[3][1]], 'gray')
		plt.fill([boundary2[0][0], boundary2[1][0], boundary2[2][0], boundary2[3][0]], [boundary2[0][1], boundary2[1][1], boundary2[2][1], boundary2[3][1]], 'gray')
		plt.fill([boundary3[0][0], boundary3[1][0], boundary3[2][0], boundary3[3][0]], [boundary3[0][1], boundary3[1][1], boundary3[2][1], boundary3[3][1]], 'gray')
		plt.fill([boundary4[0][0], boundary4[1][0], boundary4[2][0], boundary4[3][0]], [boundary4[0][1], boundary4[1][1], boundary4[2][1], boundary4[3][1]], 'gray')
		plt.fill([vertices1[0][0], vertices1[1][0], vertices1[2][0], vertices1[3][0]], [vertices1[0][1], vertices1[1][1], vertices1[2][1], vertices1[3][1]], 'gray')
		plt.fill([vertices2[0][0], vertices2[1][0], vertices2[2][0], vertices2[3][0]], [vertices2[0][1], vertices2[1][1], vertices2[2][1], vertices2[3][1]], 'gray')
		plt.fill([vertices3[0][0], vertices3[1][0], vertices3[2][0], vertices3[3][0]], [vertices3[0][1], vertices3[1][1], vertices3[2][1], vertices3[3][1]], 'gray')
		plt.fill([vertices4[0][0], vertices4[1][0], vertices4[2][0], vertices4[3][0]], [vertices4[0][1], vertices4[1][1], vertices4[2][1], vertices4[3][1]], 'gray')

		plot_agents(history, radius, ax)
		#plot_paths(history, radius, ax) #DECOMMENT IF ONLY AGENTS PATH LINES ARE NEEDED

		plt.show()

	return fitness


def simulation_evaluator_scenario2(candidates, args):
	'''
	Funtion to evaluate the parameters set generated by the EC algorithm for scenario II.
	- candidates --> candidates chromosomes used to feed the collision-avoidance simulator
	'''
	t_step = 1/60.
	radius = 0.1
	fitness=[]
	for chromosome in candidates:
		neigh_dist = chromosome[0]
		max_neigh = chromosome[1]
		t_horiz = chromosome[2]
		t_horiz_obst = chromosome[3]
		max_speed = chromosome[4]
		fitness.append(collision_avoidance_scenario2(t_step, neigh_dist, max_neigh, t_horiz, t_horiz_obst, radius, max_speed))
	return fitness





def collision_avoidance_scenario3(time_step, param0, param1, param2, param3, rad, param4, gui_interface=False):
	'''
	Function to run a simulation with RVO2 simulator in scenario III environment. It is used to evaluate the fitness function value of a set of parameters that represent a candidate solution.
	Returns the fitness function value for the input parameters set.
	- time_step --> simulation time-step
	- param0 --> First parameter to be optimized, which correspond to neigh_dist
	- param1 --> Second parameter to be optimized, which correspond to max_neigh
	- param2 --> Third parameter to be optimized, which correspond to t_horiz
	- param3 --> Fourth parameter to be optimized, which correspond to t_horiz_obst
	- rad --> agents radius
	- param4 --> Fifth parameter to be optimized, which correspond to max_speed
	- gui_interface --> boolean value use to activate (True) or deactivate (False) the plot of the simulation at the end of the agents path computation.
	'''
	gui = gui_interface

	now = datetime.now()
	timestamp = now.strftime('%Y_%m_%d_%H_%M_%S')

	fitness = 0.0

	plt.close('all')

	t_step = time_step
	neigh_dist = param0
	max_neigh = param1
	t_horiz = param2
	t_horiz_obst = param3
	radius = rad
	max_speed = param4

	sim = rvo2.PyRVOSimulator(t_step, neigh_dist, max_neigh, t_horiz, t_horiz_obst, radius, max_speed)

	n_iterations = int(t_step*100000)
	r_buffer = 1e-1

	boundary1 = [(-1, -1), (-1, 11), (-1.5, 11.5), (-1.5, -1.5)]
	boundary2 = [(-1, 11), (11, 11), (11.5, 11.5), (-1.5, 11.5)]
	boundary3 = [(11, 11), (11, -1), (11.5, -1.5), (11.5, 11.5)]
	boundary4 = [(11, -1), (-1, -1), (-1.5, -1.5), (11.5, -1.5)]
	

	vertices1 = [(2, 2), (4, 2), (4, 4), (2, 4)]
	vertices2 = [(6, 2), (8, 2), (8, 4), (6, 4)]
	vertices3 = [(6, 6), (8, 6), (8, 8), (6, 8)]
	vertices4 = [(2, 6), (4, 6), (4, 8), (2, 8)]
	vertices5 = [(4.5, 0.5), (5.5, 0.5), (5.5, 1.5), (4.5, 1.5)]
	vertices6 = [(8.5, 4.5), (9.5, 4.5), (9.5, 5.5), (8.5, 5.5)]
	vertices7 = [(4.5, 8.5), (5.5, 8.5), (5.5, 9.5), (4.5, 9.5)]
	vertices8 = [(0.5, 4.5), (1.5, 4.5), (1.5, 5.5), (0.5, 5.5)]
	vertices9 = [(4.5, 4.5), (5.5, 4.5), (5.5, 5.5), (4.5, 5.5)]


	a0 = sim.addAgent((0, 0))
	a1 = sim.addAgent((10, 0))
	a2 = sim.addAgent((10, 10))
	a3 = sim.addAgent((0, 10))

	b1 = sim.addObstacle(boundary1)
	b2 = sim.addObstacle(boundary2)
	b3 = sim.addObstacle(boundary3)
	b4 = sim.addObstacle(boundary4)

	o1 = sim.addObstacle(vertices1)
	o2 = sim.addObstacle(vertices2)
	o3 = sim.addObstacle(vertices3)
	o4 = sim.addObstacle(vertices4)
	o5 = sim.addObstacle(vertices5)
	o6 = sim.addObstacle(vertices6)
	o7 = sim.addObstacle(vertices7)
	o8 = sim.addObstacle(vertices8)
	o9 = sim.addObstacle(vertices9)
	sim.processObstacles()

	sim.setAgentPrefVelocity(a0, (1, 1))
	sim.setAgentPrefVelocity(a1, (-1, 1))
	sim.setAgentPrefVelocity(a2, (-1, -1))
	sim.setAgentPrefVelocity(a3, (1, -1))

	history = []
	history.append([(0,0), (10,0), (10,10), (0,10)])
	positions = [(0,0), (10,0), (10,10), (0,10)]

	ag0_results = {'agent_nr': 0, 'found': False, 'timestep': n_iterations, 'position': []}
	ag1_results = {'agent_nr': 1, 'found': False, 'timestep': n_iterations, 'position': []}
	ag2_results = {'agent_nr': 2, 'found': False, 'timestep': n_iterations, 'position': []}
	ag3_results = {'agent_nr': 3, 'found': False, 'timestep': n_iterations, 'position': []}

	collisions = 0

	for step in range(n_iterations):
		if ag0_results['found'] == True and ag1_results['found'] == True and ag2_results['found'] == True and ag3_results['found'] == True:
			if gui:
				print('ALL AGENTS REACHED THEIR TARGETS! SIMULATION COMPLETED...')
			break

		sim.doStep()
		positions = []
		for agent_no in (a0, a1, a2, a3):
			pos = '(%5.3f, %5.3f)' % sim.getAgentPosition(agent_no)
			pos_tuple = eval(pos)
			positions.append(pos_tuple)

		history.append(positions)

		if check_collisions(positions[0], positions[1], radius):
			collisions += 1
		if check_collisions(positions[0], positions[2], radius):
			collisions += 1
		if check_collisions(positions[0], positions[3], radius):
			collisions += 1
		if check_collisions(positions[1], positions[2], radius):
			collisions += 1
		if check_collisions(positions[1], positions[3], radius):
			collisions += 1
		if check_collisions(positions[2], positions[3], radius):
			collisions += 1

		sim.setAgentPrefVelocity(a0, (10 - positions[0][0], 10 - positions[0][1]))
		sim.setAgentPrefVelocity(a1, (0 - positions[1][0], 10 - positions[1][1]))
		sim.setAgentPrefVelocity(a2, (0 - positions[2][0], 0 - positions[2][1]))
		sim.setAgentPrefVelocity(a3, (10 - positions[3][0], 0 - positions[3][1]))

		if isclose(history[-1][0][0], 10, abs_tol=r_buffer) == True and isclose(history[-1][0][1], 10, abs_tol=r_buffer) == True and ag0_results['found'] == False:
			ag0_results['found'] = True
			ag0_results['timestep'] = step
			ag0_results['position'] = positions[0]
			if gui == True:
				print('AGENT 0 TARGET REACHED: %s' % str(positions[0]))
		
		if isclose(history[-1][1][0], 0, abs_tol=r_buffer) == True and isclose(history[-1][1][1], 10, abs_tol=r_buffer) == True and ag1_results['found'] == False:
			ag1_results['found'] = True
			ag1_results['timestep'] = step
			ag1_results['position'] = positions[1]
			if gui == True:
				print('AGENT 1 TARGET REACHED: %s' % str(positions[1]))
		
		if isclose(history[-1][2][0], 0, abs_tol=r_buffer) == True and isclose(history[-1][2][1], 0, abs_tol=r_buffer) == True and ag2_results['found'] == False:
			ag2_results['found'] = True
			ag2_results['timestep'] = step
			ag2_results['position'] = positions[2]
			if gui==True:
				print('AGENT 2 TARGET REACHED: %s' % str(positions[2]))
		
		if isclose(history[-1][3][0], 10, abs_tol=r_buffer) == True and isclose(history[-1][3][1], 0, abs_tol=r_buffer) == True and ag3_results['found'] == False:
			ag3_results['found'] = True
			ag3_results['timestep'] = step
			ag3_results['position'] = positions[3]
			if gui==True:
				print('AGENT 3 TARGET REACHED: %s' % str(positions[3]))
		
	if gui==True:
		print('Number of collisions: %d'% collisions)

	errors = []
	errors.append(distance(history[-1][0], (10.0, 10.0)))
	errors.append(distance(history[-1][1], (0.0, 10.0)))
	errors.append(distance(history[-1][2], (0.0, 0.0)))
	errors.append(distance(history[-1][3], (10.0, 0.0)))

	mean_error = statistics.mean(errors)
	mean_error_norm = mean_error / distance((0,0), (10,10))
	collisions_norm = collisions / (6*n_iterations)
	mean_duration = (ag0_results['timestep'] + ag1_results['timestep'] + ag2_results['timestep'] + ag3_results['timestep']) / 4
	mean_duration_norm = mean_duration / n_iterations

	fitness = mean_error + mean_duration_norm + collisions

	if gui == True:
		print('Fitness: {0} for set of parameters: [{1}, {2}, {3}, {4}, {5}]'.format(fitness, param0, param1, param2, param3, param4))
		plt.show()
		fig, ax = plt.subplots()
		plt.fill([boundary1[0][0], boundary1[1][0], boundary1[2][0], boundary1[3][0]], [boundary1[0][1], boundary1[1][1], boundary1[2][1], boundary1[3][1]], 'gray')
		plt.fill([boundary2[0][0], boundary2[1][0], boundary2[2][0], boundary2[3][0]], [boundary2[0][1], boundary2[1][1], boundary2[2][1], boundary2[3][1]], 'gray')
		plt.fill([boundary3[0][0], boundary3[1][0], boundary3[2][0], boundary3[3][0]], [boundary3[0][1], boundary3[1][1], boundary3[2][1], boundary3[3][1]], 'gray')
		plt.fill([boundary4[0][0], boundary4[1][0], boundary4[2][0], boundary4[3][0]], [boundary4[0][1], boundary4[1][1], boundary4[2][1], boundary4[3][1]], 'gray')
		plt.fill([vertices1[0][0], vertices1[1][0], vertices1[2][0], vertices1[3][0]], [vertices1[0][1], vertices1[1][1], vertices1[2][1], vertices1[3][1]], 'gray')
		plt.fill([vertices2[0][0], vertices2[1][0], vertices2[2][0], vertices2[3][0]], [vertices2[0][1], vertices2[1][1], vertices2[2][1], vertices2[3][1]], 'gray')
		plt.fill([vertices3[0][0], vertices3[1][0], vertices3[2][0], vertices3[3][0]], [vertices3[0][1], vertices3[1][1], vertices3[2][1], vertices3[3][1]], 'gray')
		plt.fill([vertices4[0][0], vertices4[1][0], vertices4[2][0], vertices4[3][0]], [vertices4[0][1], vertices4[1][1], vertices4[2][1], vertices4[3][1]], 'gray')
		plt.fill([vertices5[0][0], vertices5[1][0], vertices5[2][0], vertices5[3][0]], [vertices5[0][1], vertices5[1][1], vertices5[2][1], vertices5[3][1]], 'gray')
		plt.fill([vertices6[0][0], vertices6[1][0], vertices6[2][0], vertices6[3][0]], [vertices6[0][1], vertices6[1][1], vertices6[2][1], vertices6[3][1]], 'gray')
		plt.fill([vertices7[0][0], vertices7[1][0], vertices7[2][0], vertices7[3][0]], [vertices7[0][1], vertices7[1][1], vertices7[2][1], vertices7[3][1]], 'gray')
		plt.fill([vertices8[0][0], vertices8[1][0], vertices8[2][0], vertices8[3][0]], [vertices8[0][1], vertices8[1][1], vertices8[2][1], vertices8[3][1]], 'gray')
		plt.fill([vertices9[0][0], vertices9[1][0], vertices9[2][0], vertices9[3][0]], [vertices9[0][1], vertices9[1][1], vertices9[2][1], vertices9[3][1]], 'gray')

		plot_agents(history, radius, ax)
		#plot_paths(history, radius, ax) #DECOMMENT IF ONLY AGENTS PATH LINES ARE NEEDED

		plt.show()


	return fitness


def simulation_evaluator_scenario3(candidates, args):
	'''
	Funtion to evaluate the parameters set generated by the EC algorithm for scenario III.
	- candidates --> candidates chromosomes used to feed the collision-avoidance simulator
	'''
	t_step = 1/60.
	radius = 0.1
	fitness=[]
	for chromosome in candidates:
		neigh_dist = chromosome[0]
		max_neigh = chromosome[1]
		t_horiz = chromosome[2]
		t_horiz_obst = chromosome[3]
		max_speed = chromosome[4]
		fitness.append(collision_avoidance_scenario3(t_step, neigh_dist, max_neigh, t_horiz, t_horiz_obst, radius, max_speed))
	return fitness



def collision_avoidance_scenario4(time_step, param0, param1, param2, param3, rad, param4, gui_interface=False):
	'''
	Function to run a simulation with RVO2 simulator in scenario IV environment. It is used to evaluate the fitness function value of a set of parameters that represent a candidate solution.
	Returns the fitness function value for the input parameters set.
	- time_step --> simulation time-step
	- param0 --> First parameter to be optimized, which correspond to neigh_dist
	- param1 --> Second parameter to be optimized, which correspond to max_neigh
	- param2 --> Third parameter to be optimized, which correspond to t_horiz
	- param3 --> Fourth parameter to be optimized, which correspond to t_horiz_obst
	- rad --> agents radius
	- param4 --> Fifth parameter to be optimized, which correspond to max_speed
	- gui_interface --> boolean value use to activate (True) or deactivate (False) the plot of the simulation at the end of the agents path computation.
	'''
	gui = gui_interface

	now = datetime.now()
	timestamp = now.strftime('%Y_%m_%d_%H_%M_%S')

	fitness = 0.0

	plt.close('all')

	t_step = time_step
	neigh_dist = param0
	max_neigh = param1
	t_horiz = param2
	t_horiz_obst = param3
	radius = rad
	max_speed = param4

	sim = rvo2.PyRVOSimulator(t_step, neigh_dist, max_neigh, t_horiz, t_horiz_obst, radius, max_speed)

	n_iterations = int(t_step*100000)
	r_buffer = 1e-1



	boundary1 = [(-1, -1), (-1, 11), (-1.5, 11.5), (-1.5, -1.5)]
	boundary2 = [(-1, 11), (11, 11), (11.5, 11.5), (-1.5, 11.5)]
	boundary3 = [(11, 11), (11, -1), (11.5, -1.5), (11.5, 11.5)]
	boundary4 = [(11, -1), (-1, -1), (-1.5, -1.5), (11.5, -1.5)]
	

	vertices1 = [(1.5, 2.5), (2.5, 2.5), (2.5, 3.5), (1.5, 3.5)]
	vertices2 = [(7.5, 2.5), (8.5, 2.5), (8.5, 3.5), (7.5, 3.5)]
	vertices3 = [(7.5, 6.5), (8.5, 6.5), (8.5, 7.5), (7.5, 7.5)]
	vertices4 = [(1.5, 6.5), (2.5, 6.5), (2.5, 7.5), (1.5, 7.5)]
	vertices5 = [(4.5, -0.5), (5.5, -0.5), (5.5, 1.5), (4.5, 1.5)]
	vertices6 = [(8.5, 4.5), (10.5, 4.5), (10.5, 5.5), (8.5, 5.5)]
	vertices7 = [(4.5, 8.5), (5.5, 8.5), (5.5, 10.5), (4.5, 10.5)]
	vertices8 = [(-0.5, 4.5), (1.5, 4.5), (1.5, 5.5), (-0.5, 5.5)]
	vertices9 = [(4.5, 4.5), (5.5, 4.5), (5.5, 5.5), (4.5, 5.5)]
	vertices22 = [(4.5, 2.5), (5.5, 2.5), (5.5, 3.5), (4.5, 3.5)]
	vertices23 = [(6.5, 4.5), (7.5, 4.5), (7.5, 5.5), (6.5, 5.5)]
	vertices24 = [(4.5, 6.5), (5.5, 6.5), (5.5, 7.5), (4.5, 7.5)]
	vertices25 = [(2.5, 4.5), (3.5, 4.5), (3.5, 5.5), (2.5, 5.5)]

	a0 = sim.addAgent((0, 0))
	a1 = sim.addAgent((10, 0))
	a2 = sim.addAgent((10, 10))
	a3 = sim.addAgent((0, 10))


	b1 = sim.addObstacle(boundary1)
	b2 = sim.addObstacle(boundary2)
	b3 = sim.addObstacle(boundary3)
	b4 = sim.addObstacle(boundary4)

	o1 = sim.addObstacle(vertices1)
	o2 = sim.addObstacle(vertices2)
	o3 = sim.addObstacle(vertices3)
	o4 = sim.addObstacle(vertices4)
	o5 = sim.addObstacle(vertices5)
	o6 = sim.addObstacle(vertices6)
	o7 = sim.addObstacle(vertices7)
	o8 = sim.addObstacle(vertices8)
	o9 = sim.addObstacle(vertices9)
	o22 = sim.addObstacle(vertices22)
	o23 = sim.addObstacle(vertices23)
	o24 = sim.addObstacle(vertices24)
	o25 = sim.addObstacle(vertices25)
	sim.processObstacles()

	sim.setAgentPrefVelocity(a0, (1, 1))
	sim.setAgentPrefVelocity(a1, (-1, 1))
	sim.setAgentPrefVelocity(a2, (-1, -1))
	sim.setAgentPrefVelocity(a3, (1, -1))

	history = []
	history.append([(0,0), (10,0), (10,10), (0,10)])
	positions = [(0,0), (10,0), (10,10), (0,10)]


	ag0_results = {'agent_nr': 0, 'found': False, 'timestep': n_iterations, 'position': []}
	ag1_results = {'agent_nr': 1, 'found': False, 'timestep': n_iterations, 'position': []}
	ag2_results = {'agent_nr': 2, 'found': False, 'timestep': n_iterations, 'position': []}
	ag3_results = {'agent_nr': 3, 'found': False, 'timestep': n_iterations, 'position': []}

	collisions = 0

	for step in range(n_iterations):
		if ag0_results['found'] == True and ag1_results['found'] == True and ag2_results['found'] == True and ag3_results['found'] == True:
			if gui:
				print('ALL AGENTS REACHED THEIR TARGETS!')
			break

		sim.doStep()
		positions = []
		for agent_no in (a0, a1, a2, a3):
			pos = '(%5.3f, %5.3f)' % sim.getAgentPosition(agent_no)
			pos_tuple = eval(pos)
			positions.append(pos_tuple)

		history.append(positions)

		if check_collisions(positions[0], positions[1], radius):
			collisions += 1
		if check_collisions(positions[0], positions[2], radius):
			collisions += 1
		if check_collisions(positions[0], positions[3], radius):
			collisions += 1
		if check_collisions(positions[1], positions[2], radius):
			collisions += 1
		if check_collisions(positions[1], positions[3], radius):
			collisions += 1
		if check_collisions(positions[2], positions[3], radius):
			collisions += 1

		sim.setAgentPrefVelocity(a0, (10 - positions[0][0], 10 - positions[0][1]))
		sim.setAgentPrefVelocity(a1, (0 - positions[1][0], 10 - positions[1][1]))
		sim.setAgentPrefVelocity(a2, (0 - positions[2][0], 0 - positions[2][1]))
		sim.setAgentPrefVelocity(a3, (10 - positions[3][0], 0 - positions[3][1]))

		if isclose(history[-1][0][0], 10, abs_tol=r_buffer) == True and isclose(history[-1][0][1], 10, abs_tol=r_buffer) == True and ag0_results['found'] == False:
			ag0_results['found'] = True
			ag0_results['timestep'] = step
			ag0_results['position'] = positions[0]
			if gui == True:
				print('AGENT 0 TARGET REACHED: %s' % str(positions[0]))
		
		if isclose(history[-1][1][0], 0, abs_tol=r_buffer) == True and isclose(history[-1][1][1], 10, abs_tol=r_buffer) == True and ag1_results['found'] == False:
			ag1_results['found'] = True
			ag1_results['timestep'] = step
			ag1_results['position'] = positions[1]
			if gui == True:
				print('AGENT 1 TARGET REACHED: %s' % str(positions[1]))
		
		if isclose(history[-1][2][0], 0, abs_tol=r_buffer) == True and isclose(history[-1][2][1], 0, abs_tol=r_buffer) == True and ag2_results['found'] == False:
			ag2_results['found'] = True
			ag2_results['timestep'] = step
			ag2_results['position'] = positions[2]
			if gui==True:
				print('AGENT 2 TARGET REACHED: %s' % str(positions[2]))
		
		if isclose(history[-1][3][0], 10, abs_tol=r_buffer) == True and isclose(history[-1][3][1], 0, abs_tol=r_buffer) == True and ag3_results['found'] == False:
			ag3_results['found'] = True
			ag3_results['timestep'] = step
			ag3_results['position'] = positions[3]
			if gui==True:
				print('AGENT 3 TARGET REACHED: %s' % str(positions[3]))
		
	if gui==True:
		print('Number of collisions: %d'% collisions)

	errors = []
	errors.append(distance(history[-1][0], (10.0, 10.0)))
	errors.append(distance(history[-1][1], (0.0, 10.0)))
	errors.append(distance(history[-1][2], (0.0, 0.0)))
	errors.append(distance(history[-1][3], (10.0, 0.0)))

	mean_error = statistics.mean(errors)
	mean_error_norm = mean_error / distance((0,0), (10,10))
	collisions_norm = collisions / (6*n_iterations)
	mean_duration = (ag0_results['timestep'] + ag1_results['timestep'] + ag2_results['timestep'] + ag3_results['timestep']) / 4
	mean_duration_norm = mean_duration / n_iterations

	fitness = mean_error + mean_duration_norm + collisions

	if gui == True:
		print('Fitness: {0} for set of parameters: [{1}, {2}, {3}, {4}, {5}]'.format(fitness, param0, param1, param2, param3, param4))
		plt.show()
		fig, ax = plt.subplots()
		plt.fill([boundary1[0][0], boundary1[1][0], boundary1[2][0], boundary1[3][0]], [boundary1[0][1], boundary1[1][1], boundary1[2][1], boundary1[3][1]], 'gray')
		plt.fill([boundary2[0][0], boundary2[1][0], boundary2[2][0], boundary2[3][0]], [boundary2[0][1], boundary2[1][1], boundary2[2][1], boundary2[3][1]], 'gray')
		plt.fill([boundary3[0][0], boundary3[1][0], boundary3[2][0], boundary3[3][0]], [boundary3[0][1], boundary3[1][1], boundary3[2][1], boundary3[3][1]], 'gray')
		plt.fill([boundary4[0][0], boundary4[1][0], boundary4[2][0], boundary4[3][0]], [boundary4[0][1], boundary4[1][1], boundary4[2][1], boundary4[3][1]], 'gray')
		plt.fill([vertices1[0][0], vertices1[1][0], vertices1[2][0], vertices1[3][0]], [vertices1[0][1], vertices1[1][1], vertices1[2][1], vertices1[3][1]], 'gray')
		plt.fill([vertices2[0][0], vertices2[1][0], vertices2[2][0], vertices2[3][0]], [vertices2[0][1], vertices2[1][1], vertices2[2][1], vertices2[3][1]], 'gray')
		plt.fill([vertices3[0][0], vertices3[1][0], vertices3[2][0], vertices3[3][0]], [vertices3[0][1], vertices3[1][1], vertices3[2][1], vertices3[3][1]], 'gray')
		plt.fill([vertices4[0][0], vertices4[1][0], vertices4[2][0], vertices4[3][0]], [vertices4[0][1], vertices4[1][1], vertices4[2][1], vertices4[3][1]], 'gray')
		plt.fill([vertices5[0][0], vertices5[1][0], vertices5[2][0], vertices5[3][0]], [vertices5[0][1], vertices5[1][1], vertices5[2][1], vertices5[3][1]], 'gray')
		plt.fill([vertices6[0][0], vertices6[1][0], vertices6[2][0], vertices6[3][0]], [vertices6[0][1], vertices6[1][1], vertices6[2][1], vertices6[3][1]], 'gray')
		plt.fill([vertices7[0][0], vertices7[1][0], vertices7[2][0], vertices7[3][0]], [vertices7[0][1], vertices7[1][1], vertices7[2][1], vertices7[3][1]], 'gray')
		plt.fill([vertices8[0][0], vertices8[1][0], vertices8[2][0], vertices8[3][0]], [vertices8[0][1], vertices8[1][1], vertices8[2][1], vertices8[3][1]], 'gray')
		plt.fill([vertices9[0][0], vertices9[1][0], vertices9[2][0], vertices9[3][0]], [vertices9[0][1], vertices9[1][1], vertices9[2][1], vertices9[3][1]], 'gray')
		plt.fill([vertices22[0][0], vertices22[1][0], vertices22[2][0], vertices22[3][0]], [vertices22[0][1], vertices22[1][1], vertices22[2][1], vertices22[3][1]], 'gray')
		plt.fill([vertices23[0][0], vertices23[1][0], vertices23[2][0], vertices23[3][0]], [vertices23[0][1], vertices23[1][1], vertices23[2][1], vertices23[3][1]], 'gray')
		plt.fill([vertices24[0][0], vertices24[1][0], vertices24[2][0], vertices24[3][0]], [vertices24[0][1], vertices24[1][1], vertices24[2][1], vertices24[3][1]], 'gray')
		plt.fill([vertices25[0][0], vertices25[1][0], vertices25[2][0], vertices25[3][0]], [vertices25[0][1], vertices25[1][1], vertices25[2][1], vertices25[3][1]], 'gray')
		
		plot_agents(history, radius, ax)
		#plot_paths(history, radius, ax) #DECOMMENT IF ONLY AGENTS PATH LINES ARE NEEDED

		plt.show()


	return fitness


def simulation_evaluator_scenario4(candidates, args):
	'''
	Funtion to evaluate the parameters set generated by the EC algorithm for scenario IV.
	- candidates --> candidates chromosomes used to feed the collision-avoidance simulator
	'''
	t_step = 1/60.
	radius = 0.1
	fitness=[]
	for chromosome in candidates:
		neigh_dist = chromosome[0]
		max_neigh = chromosome[1]
		t_horiz = chromosome[2]
		t_horiz_obst = chromosome[3]
		max_speed = chromosome[4]
		fitness.append(collision_avoidance_scenario4(t_step, neigh_dist, max_neigh, t_horiz, t_horiz_obst, radius, max_speed))
	return fitness



