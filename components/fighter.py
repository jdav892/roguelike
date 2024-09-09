from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity
    
class BaseComponent:
    entity: Entity #Owns instance of entity
    
    @property
    def engine(self) -> Engine:
        return self.entity.gamemap.engine