from enum import IntEnum

class Stage(IntEnum):
    START = 0
    WHAITING_NAME = 1
    WHAITING_CHOSE_HERO = 2
    TEXT_IS_READY = 3
    WHAITING_PHOTO = 4
    POST_IS_READY = 5