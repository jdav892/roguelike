from __future__ import annotations
from typing import Optional, TYPE_CHECKING

import tcod.event

from actions import Action, BumpAction, EscapeAction, WaitAction

if TYPE_CHECKING:
    from engine import Engine
    
MOVEMENT_KEYS = {
    #Arrow keys.
    tcod.event.KeySym.UP: (0, -1),
    tcod.event.KeySym.DOWN: (0, 1),
    tcod.event.KeySym.LEFT: (-1, 0),
    tcod.event.KeySym.RIGHT: (1, 0),
    tcod.event.KeySym.HOME: (-1, -1),
    tcod.event.KeySym.END: (1, -1),
    tcod.event.KeySym.PAGEUP: (1, -1),
    tcod.event.KeySym.PAGEDOWN: (1, 1),
    #Numpad keys.
    tcod.event.KeySym.KP_1: (-1, 1),
    tcod.event.KeySym.KP_2: (0, 1),
    tcod.event.KeySym.KP_3: (1, 1),
    tcod.event.KeySym.KP_4: (-1, 0),
    tcod.event.KeySym.KP_6: (1, 0),
    tcod.event.KeySym.KP_7: (-1, -1),
    tcod.event.KeySym.KP_8: (0, -1),
    tcod.event.KeySym.KP_9: (1, -1)
}

WAIT_KEYS = {
    tcod.event.KeySym.KP_PERIOD,
    tcod.event.KeySym.KP_5,
    tcod.event.KeySym.KP_CLEAR,
}


class EventHandler(tcod.event.EventDispatch[Action]):
    def __init__(self, engine: Engine):
        self.engine = engine
        
    def handle_events(self) -> None:
        for event in tcod.event.wait():
            action = self.dispatch(event)
            
            if action is None:
                continue
            
            action.perform()
            
            self.engine.handle_enemy_turns()
            self.engine.update_fov() # Updates the FOV before next player action
    
    
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        #Quit event when we click "X" window of the program
        raise SystemExit()
    
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        #Set to None if no key valid key is pressed.
        action: Optional[Action] = None
        
        key = event.sym
        
        player = self.engine.player
        
        #Movement keys based on Up, Down, Left, Right movements.
        #if key == tcod.event.KeySym.UP:
        #    action = BumpAction(player, dx = 0, dy = -1)
        #elif key == tcod.event.KeySym.DOWN:
        #    action = BumpAction(player, dx = 0, dy = 1)
        #elif key == tcod.event.KeySym.LEFT:
        #    action = BumpAction(player, dx = -1, dy = 0)
        #elif key == tcod.event.KeySym.RIGHT:
        #    action = BumpAction(player, dx = 1, dy = 0)
        
        if key in MOVEMENT_KEYS:
            dx, dy = MOVEMENT_KEYS[key]
            action = BumpAction(player, dx, dy)
        elif key in WAIT_KEYS:
            action = WaitAction(player) 
        elif key == tcod.event.KeySym.ESCAPE:
            #Escape key press exits the game through returning the EscapeAction
            action = EscapeAction(player)
            
        return action
        