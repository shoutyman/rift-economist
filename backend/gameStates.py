#standard library imports
from enum import Enum, auto

#This file contains enums for describing the current state of the game.
class GameStates(Enum):
    UNKNOWN = auto()
    NO_GAME_DETECTED = auto()
    LOADING = auto()
    RUNNING = auto()
