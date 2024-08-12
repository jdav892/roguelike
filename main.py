import tcod

from engine import Engine
from entity import Entity
from input_handlers import EventHandler


def main():
    #Screen size variables
   screen_width = 80
   screen_height = 50 
   
   #title of screen
   tileset = tcod.tileset.load_tilesheet(
       "roguelike/pyimg.png", 32, 8, tcod.tileset.CHARMAP_TCOD
   )
   
   event_handler = EventHandler()
   
   #Using Entity to initialize player and npc
   player = Entity(int(screen_width / 2), int(screen_height / 2), "@", (255, 255, 255))
   npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), "@", (255, 255, 0))
   entities = {npc, player}
   
   engine = Engine(entities=entities, event_handler=event_handler, player=player)
   
   with tcod.context.new_terminal(
       screen_width,
       screen_height,
       tileset=tileset,
       title="RogueLike",
       vsync=True,
   )as context:
       #Numpy accesses 2D arrays in [y, x] order which is pretty unintuitive but should be noted
       root_console = tcod.console.Console(screen_width, screen_height, order="F")
       #Game loop
       while True:
           #to be printed to screen at player(x,y)
           engine.render(console=root_console, context=context)
           events = tcod.event.wait()
           #using engine object to handle screen behavior
           engine.handle_events(events)
    
if __name__ == "__main__":
    main()
    