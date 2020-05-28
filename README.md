# ORCA-EvOp
A framework for evolutionary collision-avoidance optimization for drones trajectories based on ORCA.


# Introduction
ORCA-EvOp is a general framework developed for the optimization of Optimal Reciprocal Collision Avoidance algorithm through the use of Evolutionary Strategies. The project was developed for the [Third International Workshop On Advances In Innovative Drone Enhanced Application](https://www.fruct.org/idea20).

# How to 
## Run the optimizer
To run the code, once the repository is downloaded and installed, it is necessary to install all the dependecies through [pip](https://pip.pypa.io/en/stable/).
Once the dependecies are installed and the parameters are set accordingly to the needs, navigate with the command line to the folder where the [code](https://github.com/ABojeri/ORCA-EvOp/tree/master/code) is contained and run the following:
```shell
python collision_avoidance_EC_scenario*x*.py
```
where instead of \*x\* there will be the number of the scenario you want to optimize.

## Visualize the simulation

Once the optimization is completed, to see the simulation GUI, run the following script:
'''shell
python visualize_simulation_scenario*x*.py
'''
where, as previously, instead of \*x\* indicate the number of the scenario to simulate. A window opens to select the parameters set, which is generated by the optimizer at the end of the execution by saving the global best solution to a .csv file which has a different syntax depending on the start time stampt. In general it will have the following template: "best_individual_parameters_scenario*x*_*year*_*month*_*day*_*hour*_*minutes*_*seconds*.csv".  
To plot only the agents paths, comment row 302 and decomment row 303 for scenario I in file "[inspyred_functions.py](https://github.com/ABojeri/ORCA-EvOp/blob/master/code/inspyred_functions.py)". To do the same for scenario II, comment row 501 and decomment row 502. For scenario III comment row 715 and decomment row 716. For scenario IV comment row 943 and decomment row 944. Once the modifications are saved, run the following command:
'''shell
python visualize_simulation_scenario*x*.py
'''
by subsituting \*x\* with the scenario number to visualize.

## Plot the results 
To plot the results, it is possible to use the modules in [extras](https://github.com/ABojeri/ORCA-EvOp/tree/master/extras), where some scripts to plot the best fitness trend, the average fitness trend between multiple runs and the parameters distribution among different runs can be shown.
For example, to plot the fitness trend of the best individuals of a single run, copy and paste in command line the following command in the [extras](https://github.com/ABojeri/ORCA-EvOp/tree/master/extras) folder:
'''shell
python plot_best_fitness.py
'''
A window will open to select the desired statistics file generated by the optimizer, which has the following syntax: "drones_ec_statistics_scenario*x*_*year*_*month*_*day*_*hour*_*minutes*_*seconds*.csv".
