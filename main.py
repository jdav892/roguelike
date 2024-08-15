import tcod

from engine import Engine
from entity import Entity
from input_handlers import EventHandler
from procgen import generate_dungeon

def main():
    #Screen size variables
   screen_width = 80
   screen_height = 50 
   
   map_width = 80
   map_height = 45
   
   room_max_size = 10
   room_min_size = 6
   max_rooms = 30
   
   #title of screen
   tileset = tcod.tileset.load_tilesheet(
       "roguelike/pyimg.png", 32, 8, tcod.tileset.CHARMAP_TCOD
   )
   
   event_handler = EventHandler()
   
   #Using Entity to initialize player and npc
   player = Entity(int(screen_width / 2), int(screen_height / 2), "@", (255, 255, 255))
   
   game_map = generate_dungeon(
       max_rooms=max_rooms,
       room_min_size=room_min_size,
       room_max_size=room_max_size,
       map_width=map_width,
       map_height=map_height,
       player=player
   )
   engine = Engine(event_handler=event_handler, game_map=game_map, player=player)
   
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
    