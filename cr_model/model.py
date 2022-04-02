from mesa import  Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from .agents import CRUser
import random


RICH_THRESHOLD = 100
RICHER_THRESHOLD = 1000
RICHEST_THRESHOLD = 10000

MALE = 0
FEMALE = 1

def compute_total_success_matches(model):
    total_succes_matches = 0
    for agent in model.schedule.agents:
        total_succes_matches += agent.no_of_matches
    return total_succes_matches

def total_rich_agent(model):
    agents = [a for a in model.schedule.agents if a.quid >= RICH_THRESHOLD]
    return len(agents)

def total_richer_agent(model):
    agents = [a for a in model.schedule.agents if a.quid >= RICHER_THRESHOLD]
    return len(agents)

def total_richest_agent(model):
    agents = [a for a in model.schedule.agents if a.quid >= RICHEST_THRESHOLD]
    return len(agents)

def total_male(model):
    agents = [a for a in model.schedule.agents if a.gender == MALE]
    return len(agents)

def total_female(model):
    agents = [a for a in model.schedule.agents if a.gender == FEMALE]
    return len(agents)

def total_wealth(model):
    wealth = 0
    for agent in model.schedule.agents:
        wealth += agent.quid
    return wealth


class ChatrouletteModel(Model):
    def __init__(self, N,  run_time, width=10,height=10):
        self.num_of_users = N
        self.grid = MultiGrid(width, height, True)
        self.width = width
        self.height = height
        self.schedule = RandomActivation(self)
        self.run_time = run_time
        
        self.datacollector = DataCollector(
            model_reporters={"Total Success Matches": compute_total_success_matches,
            "Total Rich Users":total_rich_agent,
            "Total Richer Users":total_richer_agent,
            "Total Richest Users": total_richest_agent,
            "Total Male Users": total_male,
            "Total Female Users": total_female,
            "Total Wealth": total_wealth
            }, 
            agent_reporters={"Quid": lambda x: x.quid, "Success Matches":lambda x: x.no_of_matches}
        )

        for i in range(self.num_of_users):
            # set x, y coords randomly within the grid
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            gender = random.randint(0,1)
            gender_preference = random.randint(0,1)
            user = CRUser(i, self, (x,y), True, gender,gender_preference)

            self.grid.place_agent(user, (x,y))
            self.schedule.add(user)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        # tell all the agents in the model to run their step function
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

    def run_model(self):
        for i in range(self.run_time):
            self.step()

        