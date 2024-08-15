from typing import Optional

import tcod.event

from actions import Action, BumpAction, EscapeAction 

class EventHandler(tcod.event.EventDispatch[Action]):
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        #Quit event when we click "X" window of the program
        raise SystemExit()
    
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        #Set to None if no key valid key is pressed.
        action: Optional[Action] = None
        
        key = event.sym
        #Movement keys based on Up, Down, Left, Right movements.
        if key == tcod.event.KeySym.UP:
            action = BumpAction(dx = 0, dy = -1)
        elif key == tcod.event.KeySym.DOWN:
            action = BumpAction(dx = 0, dy = 1)
        elif key == tcod.event.KeySym.LEFT:
            action = BumpAction(dx = -1, dy = 0)
        elif key == tcod.event.KeySym.RIGHT:
            action = BumpAction(dx = 1, dy = 0)

        elif key == tcod.event.K_ESCAPE:
            #Escape key press exits the game through returning the EscapeAction
            action = EscapeAction
            
        return action
        