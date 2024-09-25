import copy
import tcod
import color
import traceback
from engine import Engine
import entity_factories
import exceptions
import input_handlers
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
   max_monsters_per_room = 2
   max_items_per_room = 2
   
   #title of screen
   tileset = tcod.tileset.load_tilesheet(
       "roguelike/pyimg.png", 32, 8, tcod.tileset.CHARMAP_TCOD
   )
         
   #Using Entity to initialize player and npc
   player = copy.deepcopy(entity_factories.player)
   
   engine = Engine(player = player)
   
    
   engine.game_map = generate_dungeon(
       max_rooms=max_rooms,
       room_min_size=room_min_size,
       room_max_size=room_max_size,
       map_width=map_width,
       map_height=map_height,
       max_monsters_per_room=max_monsters_per_room,
       max_items_per_room=max_items_per_room,
       engine = engine
   )
   engine.update_fov()
   
   engine.message_log.add_message(
       "Welcome to another dungeon, good luck!", color.welcome_text
   )
   
   handler: input_handlers.BaseEventHandler = input_handlers.MainGameEventHandler(engine)
   
   with tcod.context.new_terminal(
       screen_width,
       screen_height,
       tileset=tileset,
       title="Dungeon Runner",
       vsync=True,
   )as context:
       #Numpy accesses 2D arrays in [y, x] order which is pretty unintuitive but should be noted
       root_console = tcod.console.Console(screen_width, screen_height, order="F")
       #Game loop
       #Using engine object to handle screen behavior
       try:
           while True:
               root_console.clear()
               handler.on_render(console=root_console)
               context.present(root_console)
               
               try:
                   for event in tcod.event.wait():
                       context.convert_event(event)
                       handler = handler.handle_events(event)
               except Exception: #Handle exceptions in game
                   traceback.print_exc() #Print error to stderr
                   #Then print the error to the message log
                   if isinstance(handler, input_handlers.EventHandler):
                       handler.engine.message_log.add_message(
                           traceback.format_exc(), color.error
                       )
       except exceptions.QuitWithoutSaving:
            raise
       except SystemExit: #Save and Quit
           #TODO add the save function here
           raise
       except BaseException: #Save on ay other unexpected exception
           #TODO add the save function here
           raise
                   
               
    
if __name__ == "__main__":
    main()
    