from __future__ import annotations
from typing import TYPE_CHECKING
from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov
from entity import Actor
from game_map import GameMap
from input_handlers import MainGameEventHandler
from message_log import MessageLog
from render_functions import render_bar

if TYPE_CHECKING:
    from entity import Entity
    from game_map import GameMap
    from input_handlers import EventHandler


class Engine:
    game_map: GameMap
    #forced uniqueness using a set because adding an entity to the set twice doesn't make sense
    def __init__(self, player: Actor):
        self.event_handler: EventHandler = MainGameEventHandler(self)
        self.message_log = MessageLog()
        self.player = player
     
    def handle_enemy_turns(self) -> None:
        for entity in self.game_map.entities - {self.player}:
            #Fairly sure this is printing every npc that on the generated dungeon floor
            #Changed this from printing presence of enemy to using ai for movement
            if entity.ai:
                entity.ai.perform() 
               
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
        
        self.message_log.render(console=console, x=21, y=45, height=5)
        
        render_bar(
            console=console,
            current_value=self.player.fighter.hp,
            maximum_value=self.player.fighter.max_hp,
            total_width=20,
            
        )
            
        context.present(console)
        
        console.clear()