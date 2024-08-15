from __future__ import annotations
import copy
from typing import Tuple, TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from game_map import GameMap
    
T = TypeVar("T", bound="Entity")

class Entity:
    """A generic object to represent things in game such as Players, Enemies, Items, etc."""
    
    def __init__(self, x: int, y: int, char: str, color: Tuple[int, int, int]):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        
    def move(self, dx: int, dy: int) -> None:
        #Move entity by amount given
        self.x += dx
        self.y += dy