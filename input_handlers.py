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
        
    def handle_events(self, context: tcod.context.Context) -> None:
        for event in tcod.event.wait():
            context.convert_event(event)
            self.dispatch(event)
            
    def ev_mousemotion(self, event: tcod.event.MouseMotion) -> None:
        if self.engine.game_map.in_bounds(event.tile.x, event.tile.y):
            self.engine.mouse_location = event.tile.x, event.tile.y
    
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        #Quit event when we click "X" window of the program
        raise SystemExit()
    
    def on_render(self, console: tcod.Console) -> None:
        self.engine.render(console)
    
class MainGameEventHandler(EventHandler): 
    def handle_events(self, context: tcod.context.Context) -> None:
        for event in tcod.event.wait():
            context.convert_event(event)
            
            action = self.dispatch(event)
            
            if action is None:
                continue
            
            action.perform()
            
            self.engine.handle_enemy_turns()
            self.engine.update_fov() # Updates the FOV before next player action
    
    
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
        elif key == tcod.event.KeySym.K_v:
            self.engine.event_handler = HistoryViewer(self.engine)
            
        return action

class GameOverEventHandler(EventHandler):
    def handle_events(self, context: tcod.context.Context) -> None:
        for event in tcod.event.wait():
            action = self.dispatch(event)
            
            if action is None:
                continue
                
            action.perform()
            
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None
        
        key = event.sym
        
        if key == tcod.event.KeySym.ESCAPE:
            action = EscapeAction(self.engine.player)
            
        #No valid key was pressed
        
        return action
    

CURSOR_Y_KEYS = {
    tcod.event.KeySym.K_UP: -1,
    tcod.event.KeySym.K_DOWN: 1,
    tcod.event.KeySym.K_PAGEUP: -10,
    tcod.event.KeySym.K_PAGEDOWN: 10,
}

class HistoryViewer(EventHandler):
    """Print the history on a larger window that can be navigated by the user."""
    
    def __init__(self, engine: Engine):
        super().__init__(engine)
        self.log_length = len(engine.message_log.messages)
        self.cursor = self.log_length - 1
        
    def on_render(self, console: tcod.Console) -> None:
        super().on_render(console) #Draw the main state as background
        
        log_console = tcod.Console(console.width - 6, console.height - 6)
        
        #Draw a frame with a custom banner title.
        log_console.draw_frame(0, 0, log_console.width, log_console.height)
        log_console.print_box(
            0, 0, log_console.width, 1, "|Message history|", alignment=tcod.CENTER
        )
        
        #Render the message log using the cursor parameter
        self.engine.message_log.render_messages(
            log_console,
            1,
            1,
            log_console.width - 2,
            log_console.height - 2,
            self.engine.message_log.messages[: self.cursor + 1],
        )
        log_console.blit(console, 3, 3)
        
    def ev_keydown(self, event: tcod.event.KeyDown) -> None:
        #Conditional movement
        if event.sym in CURSOR_Y_KEYS:
            adjust = CURSOR_Y_KEYS[event.sym]
            if adjust < 0 and self.cursor == 0:
                #Only move from the top to the bottom if at edge
                self.cursor = self.log_length - 1
            elif adjust > 0 and self.cursor == self.log_length - 1:
                #Same with bottom to top movement
                self.cursor = 0
            else:
                #Otherwise move while staying clamped to the bounds of log
                self.cursor = max(0, min(self.cursor + adjust, self.log_length - 1))
        elif event.sym == tcod.event.KeySym.K_HOME:
            self.cursor = 0 #Move to top message
        elif event.sym == tcod.event.KeySym.K_END:
            self.cursor = self.log_length - 1 #Move directly to last message
        else:       #Any other key moves back to main game state
            self.engine.event_handler = MainGameEventHandler(self.engine)
            
    
    
        