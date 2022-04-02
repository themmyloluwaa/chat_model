from mesa.visualization.ModularVisualization import ModularServer
from .model import ChatrouletteModel

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import ChartModule, BarChartModule
from mesa.visualization.UserParam import UserSettableParameter


def agent_portrayal(agent):
    portrayal = {"Shape": "circle", "Filled": "true", "r": 0.5, "Layer":0}

    if agent.gender > 0:
        portrayal["Color"] = "red"
    else:
        portrayal["Color"] = "blue"

    return portrayal


grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

success_chart = ChartModule(
    [{"Label": "Total Success Matches", "Color": "purple"},
    {"Label": "Total Wealth", "Color": "orange"}]
)
rich_users = ChartModule(
    [{"Label": "Total Rich Users", "Color": "#0000FF"},
    {"Label": "Total Richer Users", "Color": "#0000FE"},
    {"Label": "Total Richest Users", "Color": "#0000EF"},
    ]
)
user_gender = ChartModule(
    [{"Label": "Total Male Users", "Color": "red"},
    {"Label": "Total Female Users", "Color": "blue"},
    ]
)
agent_chart_quid = BarChartModule(
    [{"Label": "Quid", "Color": "grey"},
    ],
    scope="agent",
    sort_by="Quid", canvas_width=2000
)
agent_chart_no_of_matches = BarChartModule(
    [{"Label": "Success Matches", "Color": "green"},
    ],
    scope="agent",
    sorting="ascending",
    sort_by="Quid", canvas_width=2000
)


model_params = {
    "N": UserSettableParameter(
        "slider", "Number of users", 100, 50, 200, description="Initial Number of users in CR"
    ),
    "run_time": UserSettableParameter(
        "slider",
        "Runtime",
        100,
        50,
        150,
        description="How many ticks should this run for",
    ),
}


server = ModularServer(ChatrouletteModel, [
                       grid, success_chart,rich_users,user_gender,agent_chart_no_of_matches, agent_chart_quid ], "Chatroulette Model", model_params)
server.port = 8521
