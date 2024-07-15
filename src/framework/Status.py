from enum import Enum

class Status(Enum):
    OK = 'Action accepted'
    SOLVED = 'Optimal'
    NO_SOLUTION = 'Infeasible'