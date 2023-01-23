# ABM-Assignment-1

The [agents.py](https://github.com/mdvadillo/ABM-Assignment-1/blob/main/agents.py) contains code for agents' behavior. We have 4 types of agents overall. Each agent gets assigned one of two groups in each dimension, in a model with two dimensions total. Agents can be have 

```math
\begin{align*}
type_1 = 0, & type_2 = 0, \\  
type_1 = 1, & type_2 = 0,\\
type_1 = 0, & type_2 = 1,\\
type_1 = 1, & type_2 = 1
\end{align*}
```

[model.py](https://github.com/mdvadillo/ABM-Assignment-1/blob/main/model.py) constains the model, takes in model parameters and creates the agents. 

[server.py](https://github.com/mdvadillo/ABM-Assignment-1/blob/main/server.py)  creates the visualization

[run.py](https://github.com/mdvadillo/ABM-Assignment-1/blob/main/model.py)  runs the model
