# Simulation
Simulations

## Week 0
First attempts with genetic algorithms. Doing random walks and
using evolution to minimize the distance to a goal, starting with
random walks. 
![UI](https://raw.githubusercontent.com/TylersDurden/Simulation/master/Goal_Based/wk0/brute_force.png)

[Animated Example](https://www.youtube.com/embed/fgHmwojZgBo)

## Week 1
Same thing as last week, but improving the search implementation
by doing more careful pruning and changing the way fitness is 
evaluated. 

![InitialPop](https://raw.githubusercontent.com/TylersDurden/Simulation/master/Goal_Based/wk1/Initial_Population.png)

One of the most challenging aspects of this is first pruning the population
and then evaluating them on fitness. The efficacy of pruning will make the
mutations more effective, and the quality of the fitness function will make
mutation and crossover more efficient. The paths that are pruned out are 
replaced with random seeds mutated with some fraction of survivors. 

![pruning](https://raw.githubusercontent.com/TylersDurden/Simulation/master/Goal_Based/wk1/pruning.png)
