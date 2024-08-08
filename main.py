import tcod

def main():
    #Screen size variables
   screen_width = 80
   screen_height = 50
   
   #title of screen
   tileset = tcod.tileset.load_tilesheet(
       "roguelike/pyimg.png", 32, 8, tcod.tileset.CHARMAP_TCOD
   )
   with tcod.context.new_terminal(
       screen_width,
       screen_height,
       tileset=tileset,
       title="RogueLike",
       vsync=True,
   )as context:
       root_console = tcod.Console(screen_width, screen_height, order="F")
       while True:
           #to be printed to screen
           root_console.print(x=1, y=1, string="@")
           context.present(root_console)
           for event in tcod.event.wait():
               if event.type == "QUIT":
                   raise SystemExit()
    
    
    
    
if __name__ == "__main__":
    main()
    