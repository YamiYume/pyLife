from typing import List, Tuple

class Configuration:
    
    __slots__ = ('_input_functions', '_output_functions',
                 '_middle_layer', '_genome_size',
                 '_mutation_probability', '_enviroment_size',
                 '_enviroment_lifespan', '_population_size',
                 '_elimination_function')
    
    def __init__(self):
        self._input_functions = []
        self._output_functions = []
        self._middle_layer = 0
        self._genome_size = 0
        self._mutation_probability = 0
        self._enviroment_size = (0, 0)
        self._enviroment_lifespan = 0
        self._population_size = 0
        self._elimination_function = None

    def _get_inputs(self):
        return self._input_functions

    def _set_inputs(self, input_functions: List[str]):
        self._input_functions = input_functions

    inputs = property(fget=_get_inputs, fset=_set_inputs)
    
    def _get_outputs(self):
        return self._output_functions

    def _set_outputs(self, output_functions: List[str]):
        self._output_functions = output_functions

    outputs = property(fget=_get_outputs, fset=_set_outputs)

    def _get_middle(self):
        return self._middle_layer

    def _set_middle(self, middle_layer: int):
        self._middle_layer = middle_layer

    middle = property(fget = _get_middle, fset=_set_middle)

    def _get_genome_size(self):
        return self._genome_size
    
    def _set_genome_size(self, genome_size: int):
        self._genome_size = genome_size

    genome_size = property(fget=_get_genome_size, fset=_set_genome_size)

    def _get_mutation_probability(self):
        return self._mutation_probability
    
    def _set_mutation_probability(self, mutation_probability: float):
        self._mutation_probability = mutation_probability

    mutation = property(fget=_get_mutation_probability, fset=_set_mutation_probability)

    def _get_enviroment_size(self):
        return self._enviroment_size
    
    def _set_enviroment_size(self, enviroment_size: Tuple[int, int]):
        self._enviroment_size = enviroment_size

    enviroment_size = property(fget=_get_enviroment_size, fset=_set_enviroment_size)
    
    def _get_enviroment_lifespan(self):
        return self._enviroment_lifespan
    
    def _set_enviroment_lifespan(self, enviroment_lifespan: int):
        self._enviroment_lifespan = enviroment_lifespan

    enviroment_lifespan = property(fget=_get_enviroment_lifespan,
                                   fset=_set_enviroment_lifespan)

    def _get_population_size(self):
        return self._population_size
    
    def _set_population_size(self, population_size: int):
        self._population_size = population_size

    population_size = property(fget=_get_population_size, fset=_set_population_size)
    
    def _get_elimination_function(self):
        return self._elimination_function
    
    def _set_elimination_function(self, elimination_function: str):
        self._elimination_function = elimination_function

    elimination_function = property(fget=_get_elimination_function,
                                    fset=_set_elimination_function)