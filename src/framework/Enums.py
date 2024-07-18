from enum import Enum

class Status(Enum):
    OK = 'Action accepted'
    SOLVED = 'Optimal'
    NO_SOLUTION = 'Infeasible'

class Variants(Enum):
    SQUARES = 'squares'
    DIAGONAL = 'diagonal'
    NON_CONSECUTIVE_NEIGHBOR = 'non_consecutive_neighbor'
    CHESS_KING = 'chess_king'
    CHESS_KNIGHT = 'chess_knight'


variants_default = {Variants.SQUARES:True,
                    Variants.DIAGONAL:False,
                    Variants.NON_CONSECUTIVE_NEIGHBOR:False,
                    Variants.CHESS_KING:False,
                    Variants.CHESS_KNIGHT:False}