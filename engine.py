from typing import Set, Iterable, Any
from tcod.context import Context
from tcod.console import Console
from actions import EscapeAction, MovementAction
from entity import Entity
from input_handlers import EventHandler


class Engine:
    #forced uniqueness using a set because adding an entity to the set twice doesn't make sense
    def __init__(self, entities: Set[Entity], event_handler: EventHandler, game_map,  player: Entity):
        self.entities = entities
        self.event_handler = event_handler
        self.game_map = game_map
        self.player = player
        
    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)
            
            if action is None:
                continue
        
            if isinstance(action, MovementAction):
                self.player.move(dx=action.dx, dy=action.dy)
                
            elif isinstance(action, EscapeAction):
                raise SystemExit()
    
    def render(self, console: Console, context: Context) -> None:
        for entity in self.entities:
            console.print(entity.x, entity.y, entity.char, fg=entity.color)
            
        context.present(console)
        
        console.clear()