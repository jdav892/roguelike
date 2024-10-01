import tcod
import color
import traceback
import exceptions
import input_handlers
import setup_game

def save_game(handler: input_handlers.BaseEventHandler, filename: str) -> None:
    #If the current event handler has an active Engine then save it
    if isinstance(handler, input_handlers.EventHandler):
        handler.engine.save_as(filename)
        print("Game saved")

def main():
    #Screen size variables
   screen_width = 80
   screen_height = 50 
   
   #title of screen
   tileset = tcod.tileset.load_tilesheet(
       "C:/Users/jay-5/Documents/code/pythonProj/roguelike/pyimg.png", 32, 8, tcod.tileset.CHARMAP_TCOD
   )
   
   handler: input_handlers.BaseEventHandler = setup_game.MainMenu()
   
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
           save_game(handler, "savegame.sav")
           raise
       except BaseException: #Save on ay other unexpected exception
           save_game(handler, "savegame.sav")
           raise
                   
               
    
if __name__ == "__main__":
    main()
    