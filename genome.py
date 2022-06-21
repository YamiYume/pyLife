from __future__ import annotations
from random import getrandbits, random
from more_itertools import sliced, pairwise



class Genome:
    '''
     Class in charge of generate and manipulate a hex string
     genome that codifies the brain structure of a Organism
    '''

    __slots__ = ('genome')

    def __init__(self, genome_size: int,
                 inheritance: Genome | None = None):
        '''
        __init__ Create a instance of the genome given how much
        genes it have or copy it if one is provide.

        Args:
            genome_size (int): Number of gene in the genome.
            inheritance (str, optional): Genome to inherit.
                                         Defaults to None.
        '''
        if inheritance is None:
            self.genome = ''.join(format(getrandbits(32), '0>8x') 
                                  for _ in range(genome_size))
        else:
            self.genome = inheritance.genome


    def mutate(self, probability: float):
        '''
        mutate Mutate a genome with a given probability

        Args:
            probability (float): How likely is to mutate
        '''
        if random() < probability:
            new_allele = format(int(random() * 16), 'x')
            position = int(random() * len(self.genome))
            self.genome = self.genome[:position] \
                          + new_allele \
                          + self.genome[position + 1:]

    @property
    def genome_decoded(self):
        decoded = []
        decode_div = (0, 1, 8, 9, 16, 32)
        for gene in sliced(self.genome, 8):
            gene = format(int(gene, 16), '0>32b')
            gene = tuple(gene[a:b] 
                         for a, b in pairwise(decode_div))
            gene = [int(value, 2) for value in gene]
            gene[-1] = (gene[-1] - 32767) / 3276.7
            decoded.append(tuple(gene)) 
        return *decoded,
        
if __name__ == '__main__':
    A = Genome(2)
    B = Genome(2, A)
    print(A.genome == B.genome)
    print(A.genome)
    print(B.genome)
    B.mutate(1)
    print(A.genome == B.genome)
    print(A.genome)
    print(B.genome)
    print(A.genome_decoded)
    print(B.genome_decoded)
