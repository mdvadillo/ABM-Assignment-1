# can choose to just import mesa or to do these and streamline code a little
from mesa import Model
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector

from agents import SegAgent
import numpy as np


# set up the model and initialize the world
class SegModel(Model):
    height = 16
    width = height

    # adding agents to the world
    def __init__(self, width, height, num_agents, minority_pc_1, minority_pc_2, intolerance_1, intolerance_2, stopping_level):
        self.num_agents = num_agents  # we're allowing these values to be set at each run
        self.minority_pc_1 = minority_pc_1
        self.minority_pc_2 = minority_pc_2
        self.intolerance_1 = intolerance_1
        self.intolerance_2 = intolerance_2
        self.width = width
        self.height = height
        self.grid = SingleGrid(width, height, torus=True)
        self.schedule = RandomActivation(self)
        self.stopping_level = stopping_level

        # global measures for how agents are doing overall
        self.happy = 0
        self.happy0 = 0
        self.happy1 = 0
        self.similar_g = 0
        self.similar_g0 = 0
        self.similar_g1 = 0
        self.num_agents0 = 0
        self.num_agents1 = 0
        self.neighbors_g = 0
        self.neighbors_g0 = 0
        self.neighbors_g1 = 0
        self.pct_neighbors = 0
        self.pct_neighbors0 = 0
        self.pct_neighbors1 = 0
        self.pct_neighbors_e = 0
        self.pct_neighbors_e0 = 0
        self.pct_neighbors_e1 = 0

        # placing agents at random in the world
        # setting finite number of each agent type
        self.num_agents1 = round(self.num_agents * self.minority_pc_1)
        self.num_agents0 = self.num_agents - self.num_agents1

        for i in range(self.num_agents):

            if i < self.num_agents1:
                self.agent_type_1 = 1
            else:
                self.agent_type_1 = 0
            
            # selecting the type for our new parameter

            self.agent_type_2 = np.random.binomial(n = 1, p = self.minority_pc_2)

            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)

            agent = SegAgent(i, self, self.agent_type_1, self.agent_type_2)
            self.schedule.add(agent)
            self.grid.position_agent(agent, (x, y))

        self.running = True  # need this for batch runner

        # somewhat extensive data collection
        self.datacollector = DataCollector(
            model_reporters={"Pct Happy": lambda m: round(100 * m.happy / m.num_agents, 1),
                             "Pct Happy Group A": lambda m: round(100 * m.happy0 / m.num_agents0, 1),
                             "Pct Happy Group B": lambda m: round(100 * m.happy1 / m.num_agents1, 1),
                             "Avg pct similar neighbors": lambda m: m.pct_neighbors,
                             "Avg pct similar neighbors (A)": lambda m: m.pct_neighbors0,
                             "Avg pct similar neighbors (B)": lambda m: m.pct_neighbors1,
                             "Avg pct similar neighbors (count empty)": lambda m: m.pct_neighbors_e,
                             "Avg pct similar neighbors (A) (count empty)": lambda m: m.pct_neighbors_e0,
                             "Avg pct similar neighbors (B) (count empty)": lambda m: m.pct_neighbors_e1,
                             "Num Agents": lambda m: m.num_agents,
                             "Num Agents (A)": lambda m: m.num_agents0,
                             "Num Agents (B)": lambda m: m.num_agents1,
                             "Pct group B": lambda m: m.minority_pc_1,
                             "Intolerance_1": lambda m: m.intolerance_1},
            
            # Model-level count of happy agents  + subgroup counts
            agent_reporters={"Similar_empty": lambda a: round(100 * a.similar / 8, 1),
                             "Similar_no_empty": lambda a: a.a_pct_similar,
                             "Agent type on first category": lambda a: a.type_1,
                             "Agent type on second category": lambda a: a.type_2}
            # Agent-level reporters can allow for individual measures
        )
        

    # define what happens in one step of the model
    # model stopped when all agents are happy
    def step(self):
        self.happy = 0  # Reset counter of happy agents
        self.happy0 = 0  # Reset counter of happy agents
        self.happy1 = 0  # Reset counter of happy agents
        self.similar_g = 0  # Reset counter of similar agents
        self.similar_g0 = 0  # Reset counter of similar agents
        self.similar_g1 = 0  # Reset counter of similar agents
        self.neighbors_g = 0
        self.neighbors_g0 = 0
        self.neighbors_g1 = 0

        for agent in self.schedule.agents:
            self.neighbors_g += agent.neighbors_a
            self.similar_g += agent.similar

            if agent.type_1 == 0:
                self.neighbors_g0 += agent.neighbors_a
                self.similar_g0 += agent.similar0
            else:
                self.neighbors_g1 += agent.neighbors_a
                self.similar_g1 += agent.similar1

        self.schedule.step()
        self.datacollector.collect(self)
        
        # calculate % neighbors and include empty cells
        self.pct_neighbors_e = round(100 * self.similar_g / (8 * self.num_agents), 1)
        self.pct_neighbors_e0 = round(100 * self.similar_g0 / (8 * self.num_agents0), 1)
        self.pct_neighbors_e1 = round(100 * self.similar_g1 / (8 * self.num_agents1), 1)

        # solves division by zero issue
        if self.neighbors_g == 0:
            self.pct_neighbors = 0
        else:
            self.pct_neighbors = round(100 * self.similar_g / self.neighbors_g, 1)
            self.pct_neighbors0 = round(100 * self.similar_g0 / self.neighbors_g0, 1)
            self.pct_neighbors1 = round(100 * self.similar_g1 / self.neighbors_g1, 1)

        # stops the model when everyone is happy
        if self.happy >= self.stopping_level * self.schedule.get_agent_count():
            self.running = False


