# Introduction

## ClearVuAnalytics Optimizer

The ClearVuAnalytics Optimizer uses evolutionary optimization.

Evolutionary optimization
-------------------------

The general idea of evolutionary optimization is to mimic the cycle of generations in natural evolution.
In evolutionary optimization a candidate solution is called individual.
From an existing set of possible solutions, called parents, a larger set of individuals is created, using some
implementation dependent algorithm. From this set of offsprings the best solutions are selected to be the
parents for the next generation. This is repeated either for a number of generations or until a sufficient
quality has been reached.


    while i <= maxGeneration:
        # Create offsprings from parents.
        offsprings = self.next_offsprings(parents)
        # Adds fitness (quality) values to individuals.
        self.evaluate(offsprings)
        # Select parents for the next generation. 
        parents = self.select(offsprings)
        i += 1


