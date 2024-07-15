from enum import Enum

class Status(Enum):
    OK = 'Action accepted'
    SOLVED = 'Optimal'
    NO_SOLUTION = 'Infeasible'

class Variants(Enum):
    SQUARES = 'squares'
    DIAGONAL = 'diagonal'
    NON_CONSECUTIVE_NEIGHBOR = 'non_consecutive_neighbor'


variants_default = {Variants.SQUARES:True,
                    Variants.DIAGONAL:False,
                    Variants.NON_CONSECUTIVE_NEIGHBOR:False}