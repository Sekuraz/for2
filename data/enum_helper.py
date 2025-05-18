import enum

from operator import or_ as _or_
from functools import reduce

def with_limits(enumeration: enum.Enum):
    "add NONE and ALL psuedo-members to enumeration"
    none_mbr = enumeration(0)
    all_mbr = enumeration(reduce(_or_, enumeration))
    enumeration.NONE = none_mbr
    enumeration.ALL = all_mbr
    enumeration._member_map_['NONE'] = none_mbr
    enumeration._member_map_['ALL'] = all_mbr
    return enumeration
