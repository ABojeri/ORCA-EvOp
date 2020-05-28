'''
collision_avoidance_EC_scenario_4.py
This module allows to run the optimization process of RVO2 simulator on scenario IV.
The parameters to set are:
- popul_size (int) --> population size of the evolutionary strategy
- max_eval (int) --> maximum number of evaluation to terminate the evolution strategy
- constraints (int or float) --> set the constraints boundaries for the candidate's chromosomes.
	It should be compiled as follows: [(l_1, l_2, ..., l_n), (u_1, u_2, ..., u_n)],
	where "l_i" is the lower-bound of parameter i-th and "u_i" is the upper-bound of parameter i-th
- tournament_size --> tournament size of the EC selector
- num_elites --> number of elites for the generational replacement
- mutation_rate/crossover_rate --> respectively, the mutation and crossover rates of the EC variators
'''

import inspyred
from random import Random
import csv
from time import time
from inspyred_functions import *
from datetime import datetime



def main():

	popul_size = 100
	max_eval = 100000
	timeStep = 1/60.

	now = datetime.now()
	timestamp = now.strftime('%Y_%m_%d_%H_%M_%S')

	rand = Random()
	rand.seed(int(time()))
# 				neigh_dist	maxNeigh	    t_horiz  	     t_horiz_obst      max_speed
	constraints=((0.1,		1,    		0.1,   				0.1,				0.5),
             	(5,    		3, 			10,   				10,				5))

	algorithm = inspyred.ec.EvolutionaryComputation(rand)
	algorithm.terminator = [inspyred.ec.terminators.evaluation_termination]
	algorithm.observer = [inspyred.ec.observers.file_observer, custom_observer]
	algorithm.selector = inspyred.ec.selectors.tournament_selection
	algorithm.replacer = inspyred.ec.replacers.generational_replacement
	algorithm.variator = [inspyred.ec.variators.heuristic_crossover, inspyred.ec.variators.gaussian_mutation]

	ind_file_name = 'drones_ec_individuals_scenario4_'+timestamp+'.csv'
	ind_file = open(ind_file_name, 'w+')
	stats_file_name = 'drones_ec_statistics_scenario4_'+timestamp+'.csv'
	stats_file = open(stats_file_name, 'w+')


	final_pop = algorithm.evolve(generator=generate_population,
                             	evaluator=simulation_evaluator_scenario4,
                             	pop_size=popul_size,
                             	maximize=False,
                             	bounder=inspyred.ec.Bounder(constraints[0], constraints[1]),
                             	num_selected=popul_size,
                             	tournament_size=4,
                             	num_elites=1,
                             	mutation_rate=0.4,
                             	crossover_rate=0.6,
                             	max_evaluations=max_eval,
                             	individuals_file=ind_file,
                             	statistics_file=stats_file)

	ind_file.close()

	final_pop.sort(reverse=True)
	best = final_pop[0]
	components = best.candidate
	print('\nFittest individual:\n')
	print(best)

	with open('best_individual_parameters_scenario2_'+timestamp+'.csv', mode='w') as best_individual_file:
		best_individual_writer = csv.writer(best_individual_file, delimiter=",", quoting=csv.QUOTE_MINIMAL)
		best_individual_writer.writerow(best.candidate)


	return algorithm



if __name__ == '__main__':
    main()

