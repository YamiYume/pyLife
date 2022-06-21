from functools import partial

from neurons import Actuator, Neuron, Receptor

class Brain:
    
    __slots__ = ('brain', 'actuator',
                 'outputs')
    
    def __init__(self, organism,
                 enviroment):
        inputs = [partial(enviroment.__getattribute__(function_name), organism)
                  for function_name in enviroment.configuration.inputs]
        outputs = tuple(partial(organism.__getattribute__(function_name), enviroment)
                        for function_name in enviroment.configuration.outputs)
        brain = [
            [Receptor(input_function) for input_function in inputs],
            [Neuron() for _ in range(enviroment.configuration.middle)],
            [Neuron() for _ in range(len(outputs))]
            ]
        self.actuator = Actuator()
        for neuron in brain[2]:
            self.actuator.set_synapse(neuron)
        for type_1, number_1, type_2, number_2, weight \
        in organism.genetics.genome_decoded:
            parent = brain[type_1][number_1 % len(brain[type_1])]
            child = brain[type_2 + 1][number_2 % len(brain[type_2])]
            child.set_synapse(parent, weight)
        self.actuator.check_wiring_cascade()

        removal = []
        for level in range(len(brain)):
            for neuron in list(brain[level]):
                if not neuron.check_wiring():
                    brain[level].remove(neuron)

        self.brain = tuple(tuple(level) for level in brain)
        self.outputs = outputs
    
    def actuate(self):
        vector = self.actuator.calculate()
        for x, function in zip(vector, self.outputs):
            function(x)