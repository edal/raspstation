
from math import ceil

from StationParameters import StationParameters


class Program:
    name = ""
    description = ""
    parameters: StationParameters

    def __init__(self, name, description, parameters: StationParameters):
        self.name = name
        self.description = description
        self.parameters = parameters

