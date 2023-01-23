# can choose to just import mesa or to do these and streamline code a little
from mesa import Agent
from mesa import Model
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector


# set up and initialize the agents
class SegAgent(Agent):
    def __init__(self, pos, model, agent_type_1, agent_type_2):  # agents and their characteristics
        super().__init__(pos, model)
        self.pos = pos
        self.type_1 = agent_type_1
        self.type_2 = agent_type_2
        self.similar = 0  # agent-specific measures of neighbor similarity
        self.similar0 = 0
        self.similar1 = 0
        self.neighbors_a = 0  # count of neighbors for each agent (ignore empty squares)
        self.a_pct_similar = 0  # calculate neighbor percents

    # describe what happens in each step for the agents
    # agents check surroundings and count neighbors of the same type
    def step(self):
        self.similar = 0  # reset these counters each time step
        self.similar0 = 0
        self.similar1 = 0
        self.neighbors_a = 0
        self.a_pct_similar = 0

        # get neighbors and determine if your intolerance threshold is met
        for neighbor in self.model.grid.iter_neighbors(self.pos, True):
            self.neighbors_a += 1

            if neighbor.type_1 == self.type_1:
                self.similar += 1/2      # since we can be similar in two ways, weight both markers (equal weights). 

                if self.type_1 == 0:
                    self.similar0 += 1

                elif self.type_1 == 1:
                    self.similar1 += 1
                
            if neighbor.type_2 == self.type_2: # look at second dimension of similarity, 50% weight of total similarity
                self.similar += 1/2            # adding assitional if statemnt to not mess group tracking of first dimension

        # If unhappy, move:
        # this permits different types to have different group thresholds
        radius = 8-self.similar
        if self.type_1 == 0:
            if self.similar < 8 * 1/2 * (self.model.intolerance_1 + self.model.intolerance_2):
                self.model.grid.move_to_empty(self)
                #self.move(radius)
            else:
                self.model.happy += 1
                self.model.happy0 += 1
        else:
            if self.similar < 8 * 1/2 * (self.model.intolerance_1 + self.model.intolerance_2):
                #self.move(radius)
                self.model.grid.move_to_empty(self) 
            else:
                self.model.happy += 1
                self.model.happy1 += 1


        if self.neighbors_a > 0:
            self.a_pct_similar = round(100 * self.similar / self.neighbors_a, 1)
        else:
            self.a_pct_similar = 0



    # set up the actions available to agents
    def move(self, radius): #note, this isn't called and doesn't quite work yet -- non-empty cell issue
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=False,
            include_center=True,
            radius = radius
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)


