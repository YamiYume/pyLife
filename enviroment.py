from typing import Tuple

from configuration import Configuration
from organism import Organism

class Enviroment:

    __slots__ = ('configuration', 'generation', 'time_counter',
                 'span_space', 'actual_space', 'proposal_space',
                 'population')

    def __init__(self, configuration: Configuration) -> None:
        self.configuration = configuration
        self.generation = 0
        self.time_counter = 0
        self.span_space = []
        self.actual_space = []
        self.proposal_space = []
        self.population = []

    def check_span(self, position: Tuple[int, int]) -> bool:
        if position in self.span_space:
            return False
        self.span_space.append(position)
        return True

    def check_actual(self, position: Tuple[int, int]) -> bool:
        if position in self.actual_space or position in self.proposal_space \
        or position[0] >= self.configuration.enviroment_size[0] or position[0] < 0\
        or position[1] >= self.configuration.enviroment_size[1] or position[1] < 0:
            return False
        self.proposal_space.append(position)
        return True

    def generate(self):
        self.actual_space = []
        self.proposal_space = []
        self.span_space = []
        if self.population:
            new_population = [Organism(self,
                                       self.population[x % len(self.population)].genetics,
                                       True)
                              for x in range(self.configuration.population_size)]
        else:
            new_population = [Organism(self) 
                              for _ in range(self.configuration.population_size)]
        self.population = new_population
        self.actual_space = self.span_space
        self.generation += 1

    def simulate(self):
        for organism in self.population:
            organism.simulate()
        self.time_counter += 1
        self.actual_space = self.proposal_space
        self.proposal_space = []
        return tuple(organism.graph_data() for organism in self.population)
    
    def eliminate(self):
        self.__getattribute__(self.configuration.elimination_function)()
        return len(self.population) / self.configuration.population_size * 100

    @property
    def alive(self):
        condition = self.time_counter < self.configuration.enviroment_lifespan
        if not condition:
            self.time_counter = 0
        return condition

    def elimination_sides(self):
        border = int(0.15 * self.configuration.enviroment_size[0])
        survivors = []
        for organism in self.population:
            if (organism.position[0] < border or
                organism.position[0] > self.configuration.enviroment_size[0] - border):
                survivors.append(organism)
        self.population = survivors

    def input_distance_left(self, organism: Organism):
        return ((self.configuration.enviroment_size[0] - organism.position[0])
                / self.configuration.enviroment_size[0])

    def input_distance_right(self, organism: Organism):
        return ((organism.position[0])
                / self.configuration.enviroment_size[0])