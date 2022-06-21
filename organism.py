from typing import Dict
from genome import Genome
from brain import Brain
from random import random

class Organism:

    def __init__(self, enviroment,
                 inheritance: Genome = None, mutate: bool = False):
        if inheritance is not None:
            self.genetics = inheritance
        else:
            self.genetics = Genome(enviroment.configuration.genome_size)
        if mutate:
            self.genetics.mutate(enviroment.configuration.mutation)
        self.brain = Brain(self, enviroment)
        span = False
        while not span:
            position = (int(random() * enviroment.configuration.enviroment_size[0]),
                        int(random() * enviroment.configuration.enviroment_size[1]))
            span = (enviroment.check_span(position))
        self.position = position

    def graph_data(self) -> Dict:
        color = self.genetics.genome[:-2]
        return {'color': tuple(int(color[i:i+2], 16) for i in (0, 2, 4)),
                'position': self.position}

    def simulate(self):
        self.brain.actuate()

    def vertical_movement(self, enviroment, value: float):
        if random() < abs(value):
            new_position = (self.position[0],
                            self.position[1] + int(value / abs(value)))
            if enviroment.check_actual(new_position):
                self.position = new_position

    def horizontal_movement(self, enviroment, value: float):
        if random() < abs(value):
            new_position = (self.position[0] + int(value / abs(value)),
                            self.position[1])
            if enviroment.check_actual(new_position):
                self.position = new_position