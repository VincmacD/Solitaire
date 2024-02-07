from enum import Enum
from collections import namedtuple

class PileType(Enum):
    #Represents the different types of piles in Solitaire.
    TABLEAU = 'tableau'
    FOUNDATION = 'foundation'
    WASTE = 'waste'
    STOCK = 'stock'

Order = namedtuple('Order', ['foundation', 'value', 'color_suit'])