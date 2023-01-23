# ABM-Assignment-1

The [agents.py](https://github.com/mdvadillo/ABM-Assignment-1/blob/main/agents.py) contains code for agents' behavior. We have 4 types of agents overall. Each agent gets assigned one of two groups in each dimension, in a model with two dimensions total. For explanation purposes, below we call the agents in the minority "In", and the agents not in the minority (in the majority) "Out". With this convention, agents can have the following types:

Dimension 1\2 | In | Out 
--- | --- | --- 
In | (1,1) | (0,1) 
Out | (1,0) | (0,0) 

[model.py](https://github.com/mdvadillo/ABM-Assignment-1/blob/main/model.py) constains the model, takes in model parameters and creates the agents. 

[server.py](https://github.com/mdvadillo/ABM-Assignment-1/blob/main/server.py)  creates the visualization

[run.py](https://github.com/mdvadillo/ABM-Assignment-1/blob/main/model.py)  runs the model
