import tcod

from actions import EscapeAction, MovementAction
from input_handlers import EventHandler


def main():
    #Screen size variables
   screen_width = 80
   screen_height = 50
   
   player_x = int(screen_width / 2)
   player_y = int(screen_height / 2)
   
   #title of screen
   tileset = tcod.tileset.load_tilesheet(
       "roguelike/pyimg.png", 32, 8, tcod.tileset.CHARMAP_TCOD
   )
   
   event_handler = EventHandler()
   
   with tcod.context.new_terminal(
       screen_width,
       screen_height,
       tileset=tileset,
       title="RogueLike",
       vsync=True,
   )as context:
       #Numpy accesses 2D arrays in [y, x] order which is pretty unintuitive but should be noted
       root_console = tcod.Console(screen_width, screen_height, order="F")
       #Game loop
       while True:
           #to be printed to screen at player(x,y)
           root_console.print(x=player_x, y=player_y, string="@")
           context.present(root_console)
           #root_console.clear() is used to clear old positions of player
           root_console.clear()
           for event in tcod.event.wait():
               if event.type == "QUIT":
                   raise SystemExit()
               action = event_handler.dispatch(event)
               
               if action is None:
                   continue
               if isinstance(action, MovementAction):
                   #updating player position based on key press through action
                   player_x += action.dx
                   player_y += action.dy
               elif isinstance(action, EscapeAction):
                   raise SystemExit()    
    
    
if __name__ == "__main__":
    main()
    