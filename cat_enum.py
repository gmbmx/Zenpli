# Enums for high performance and data quality assurance
# They should be modified when new values arrive
from enum import Enum


class ValuesCat7(Enum):
    frequent = 1,
    never = 2,
    infrequent = 3,
    always = 4


class ValuesCat8(Enum):
    happy = 1,
    surprised = 2,
    sad = 3,
    scared = 4


class Missing(Enum):
    na = 1,
    null = 2,
    NA = 3,
    NULL = 4,
    nan = 5,
    missing = 6,
    miss = 7
