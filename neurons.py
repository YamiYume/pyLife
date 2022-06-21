from __future__ import annotations

from typing import TYPE_CHECKING, Callable, List

import numpy as np

if TYPE_CHECKING:
    pass


class Receptor:
    
    __slots__ = ('calculation', 'calculation_function',
                 'wired')

    def __init__(self, calculation_function: Callable):
        self.calculation = None
        self.calculation_function = calculation_function
        self.wired = None

    def calculate(self, visited: List[Neuron | Receptor | Actuator] = []):
        if self.calculation is None:
            self.calculation = self.calculation_function()
        return self.calculation

    def clean_calculation(self, visited: List[Neuron | Receptor | Actuator] = []):
        self.calculation = None

    def check_wiring(self, visited: List[Neuron | Receptor | Actuator] = []):
        if self.wired is None:
            self.wired = any(neuron.__class__ == Actuator for neuron in visited)
        return self.wired

class Neuron:

    __slots__ = ('parents', 'weights',
                 'calculation', 'last_calculation',
                 'wired')

    def __init__(self):
        self.weights = np.array(tuple())
        self.parents = []
        self.calculation = None
        self.last_calculation = 0
        self.wired = None

    def set_synapse(self, neuron: Neuron | Receptor,
                    weight: float):
        if neuron not in self.parents:
            self.parents.append(neuron)
            self.weights = np.append(self.weights, (weight,))

    def calculate(self, visited: List[Neuron | Receptor | Actuator] = []):
        if self.calculation is None:
            visited.append(self)
            synapses = [0] * len(self.weights)
            if self in self.parents:
                synapses[self.parents.index(self)] = self.last_calculation
            for parent in set(self.parents) - set(visited):
                synapses[self.parents.index(parent)] = parent.calculate(visited)
            self.calculation = np.tanh(np.dot(np.array(synapses),
                                              self.weights))
        return self.calculation

    def clean_calculation(self, visited: List[Neuron | Receptor | Actuator] = []):
        visited.append(self)
        if self.calculation is not None:
            self.last_calculation = self.calculation
        self.calculation = None
        for parent in set(self.parents) - set(visited):
            parent.clean_calculation(visited)

    def check_wiring(self, visited: List[Neuron | Receptor | Actuator] = []):

        if not self.parents:
            self.wired = False

        if self.wired is None:
            visited.append(self)
            wired = False
            if any(neuron.__class__ == Actuator for neuron in visited):
                to_delete = []
                for parent in set(self.parents) - set(visited):
                    parent_check = parent.check_wiring(visited)
                    if not parent_check:
                        to_delete.append(self.parents.index(parent))
                    wired = wired or parent_check

                for index in sorted(to_delete, reverse=True):
                    del self.parents[index]
                    np.delete(self.weights, index)

            self.wired = wired

        return self.wired

class Actuator:

    __slots__ = ('parents')

    def __init__(self):
        self.parents = [] 

    def set_synapse(self, neuron: Neuron):
        self.parents.append(neuron)

    def calculate(self, visited: List[Neuron | Receptor | Actuator] = []):
        visited.append(self)
        synapses = [parent.calculate(visited)
                    for parent in self.parents]
        self.clean_calculation()
        return *synapses,

    def clean_calculation(self, visited: List[Neuron | Receptor | Actuator] = []):
        visited.append(self)
        for parent in self.parents:
            parent.clean_calculation(visited)

    def check_wiring_cascade(self, visited: List[Neuron | Receptor | Actuator] = []):
        visited.append(self)
        for index, parent in enumerate(self.parents):
            if not parent.check_wiring(visited):
                self.parents[index] = DumbNeuron

class DumbNeuron():

    @staticmethod
    def calculate(visited):
        return 0

    @staticmethod
    def clean_calculation(visited):
        pass



if __name__ == '__main__':
    r1 = Receptor(lambda : 0.2)
    r2 = Receptor(lambda : 0)
    r3 = Receptor(lambda : 0.5)

    n1 = Neuron()
    n2 = Neuron()
    n3 = Neuron()
    n4 = Neuron()

    n5 = Neuron()
    n6 = Neuron()
    n7 = Neuron()

    a = Actuator()

    a.set_synapse(n5)
    a.set_synapse(n6)
    a.set_synapse(n7)

    n5.set_synapse(n5, 2)
    n7.set_synapse(n7, 3)
    n7.set_synapse(n4, 4)
    
    n1.set_synapse(r1, 1)
    n6.set_synapse(n2, -2)
    n6.set_synapse(n3, -3)
    n6.set_synapse(r2, -6)
    n2.set_synapse(r3, -1)
    n3.set_synapse(r3, 2)
    n4.set_synapse(r2, 3)
    n4.set_synapse(r3, 2)

    a.check_wiring_cascade()

    print(f'wired r1: {r1.check_wiring()}')
    print(f'wired r2: {r2.check_wiring()}')
    print(f'wired r3: {r3.check_wiring()}')

    print(f'wired n1: {n1.check_wiring()}')
    print(f'wired n2: {n2.check_wiring()}')
    print(f'wired n3: {n3.check_wiring()}')
    print(f'wired n4: {n4.check_wiring()}')
    print(f'wired n5: {n5.check_wiring()}')
    print(f'wired n6: {n6.check_wiring()}')
    print(f'wired n7: {n7.check_wiring()}')