# Parameters and Hyperparameters

There are two sets of parameters, one to define the optimization problem to be solved, the other to control the behaviour of the optimization algorithm.

## Parameters to define the optimization problem

* func_eval_worker_url: The URL of the function evaluation worker

* objectives: List of objectives

  An objective is defined by
  * name : The name of the objective
  * aim: The aim of the objective, one of
    * MINIMIZE: for minimizing
    * MAXIMIZE: for maximizing
    * VALUE: optimize for a specific target value
  * aim_value: the specific target value, it has only be provided for the aim VALUE

* variables: List of input variables (or design parameters)

  A variable consists of two entries
  * name: The name of the variable
  The second entry defines the lower and upper bound in case of real or integer variables and for class variables a list of possible class values has to be provided. Dependent on the varibale type these entries are:
  * info_real: A dictionary with two entries: lower_bound and upper_bound
  * info_int: A dictionary with two entries: lower_bound and upper_bound
  * info_class: A dictionary with entry values which is a list of possible class values as strings

## Parameters to control the algorithm
These parameters are optional and will be set to default values when they are not provided to the optimization algorithm.

The parameters for cva are:

* MaxGeneration 

The number of iterations after the optimization algorithms stops

* Mue

The number of parents in a iteration

* Lambda

The number of offsprings created in a iteration

