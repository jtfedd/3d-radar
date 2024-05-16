from enum import Enum


class UILayer(Enum):
    # 3D Layers
    MAP_ROADS = 0
    MAP_COUNTIES = 1
    MAP_STATES = 2

    MAP_SVW = 3
    MAP_TOW = 4

    # 2D Layers
    MARKER_BACKGROUND = 0
    MARKER = 1

    LABEL_BACKGROUND = 2
    LABEL_CONTENT = 3

    BACKGROUND = 10
    BACKGROUND_DECORATION = 11

    CONTENT_BACKGROUND = 12
    CONTENT = 13
    CONTENT_BADGE_BACKGROUND = 14
    CONTENT_BADGE_FOREGROUND = 15
    CONTENT_INTERACTION = 16

    MODAL_SHADOW = 20
    MODAL_BACKGROUND = 21

    MODAL_CONTENT_BACKGROUND = 22
    MODAL_CONTENT = 23
    MODAL_CONTENT_INTERACTION = 24
