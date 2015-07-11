# pip install enum34
from enum import Enum
    
class BusinessDayConvention (Enum):
    none = 0
    nerarest = 1
    preceding = 2
    following = 3
    modified_preceding = 4
    modified_following = 5
