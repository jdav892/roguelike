from typing import Iterable, Any
from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov
from entity import Entity
from game_map import GameMap
from input_handlers import EventHandler


class Engine:
    #forced uniqueness using a set because adding an entity to the set twice doesn't make sense
    def __init__(self, event_handler: EventHandler, game_map: GameMap, player: Entity):
        self.event_handler = event_handler
        self.game_map = game_map
        self.player = player
        self.update_fov()
        
    def handle_enemy_turns(self) -> None:
        for entity in self.game_map.entities - {self.player}:
            #Fairly sure this is printing every npc that on the generated dungeon floor
            print(f"The {entity.name} wonders when it will gets a real turn")
        
    
    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)
            
            if action is None:
                continue
            
            action.perform(self, self.player)
            self.handle_enemy_turns()

            self.update_fov()
            
    def update_fov(self) -> None:
        """Recompute the visible area based on the players point of view."""
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8,
        )
        #If a tiles is "visible" it should be added to "explored".
        self.game_map.explored |= self.game_map.visible
        

    
    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)
            
        context.present(console)
        
        console.clear()