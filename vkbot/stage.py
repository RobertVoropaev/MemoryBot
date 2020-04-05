from enum import IntEnum

class Stage(IntEnum):
    START = 0
    WHAITING_NAME = 1
    WHAITING_CHOSE_HERO = 2
    HERO_NOT_FOUND = 3
    TEXT_IS_READY = 4
    WHAITING_PHOTO = 5
    POST_IS_READY = 6