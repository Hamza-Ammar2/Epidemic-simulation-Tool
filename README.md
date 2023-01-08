# Epidemic-simulation-Tool

A python tool that uses molecular dynamics to simulate virus spread in an epidemic.
The simulation is updated via Verlet-velocity algorithm and paramters like social distancing are implemented 
via the lennard jones potential.

The simulation uses the SIR model (susciptible, infected, recovered). Users can dynamically alter variables like infection radius, social distancing index
travel rates recovery time and population size. Users can also experiment with adding central markets or quarantines. 

The tool was made using pygame and numpy.
