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

## Week 2 

The predator prey relationship is a classic evolutionary topic of study. 
Starting with a simple object, the script chase.py start by creating a prey
object with an arbitrary number of random steps. Unfortunately for this 
unwitting prey, it's exposed to a predator that's started at an arbitrary point
in the same NxN space. Given the same number of steps as it's prey's random walk
the predator attempts to close in and capture the prey over the course of it's own
highly targeted walk. 

![chase](https://raw.githubusercontent.com/TylersDurden/Simulation/master/Videos/basic_chase.mp4)  
```
______________________________
|       ~ SIMULATION ~       |     
|----------------------------|
├── Emergent
│   ├── imutil.py
│   ├── imutil.pyc
│   └── test.py
├── Goal_Based
│   ├── wk0
│   │   ├── best.mp4
│   │   ├── brute_force.png
│   │   ├── experiment.py
│   │   ├── genetic_maze_builder.py
│   │   ├── genetic_maze_builder.pyc
│   │   ├── genetic_maze_solving.py
│   │   ├── highlights.mp4
│   │   ├── rockets.py
│   │   ├── utility.py
│   │   └── utility.pyc
│   ├── wk1
│   │   ├── evolutionary1.py
│   │   ├── evoutils.py
│   │   ├── evoutils.pyc
│   │   ├── Initial_Population.png
│   │   └── pruning.png
│   └── wk2
│       ├── chase.py
│       ├── chase.pyc
│       ├── dynamic_chase.py
│       ├── prey_evolution.py
│       ├── utility.py
│       └── utility.pyc
├── Nature
│   ├── bloom.py
│   ├── dla2.py
│   ├── genetic_walks.py
│   ├── GOL.py
│   ├── particles.py
│   ├── space
│   │   ├── galactic.py
│   │   ├── imutil.py
│   │   └── imutil.pyc
│   ├── utility.py
│   └── utility.pyc
├── README.md
└── Videos
    ├── basic_chase.mp4
    ├── burst.mp4
    ├── common_origin_fireflies.mp4
    ├── common_origin.mp4
    └── randomly.mp4
```
8 directories, 40 files
