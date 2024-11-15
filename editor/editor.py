import tkinter as tk
import pygame
import canvas_renderer
import json

pygame.init()
pygame.font.init()
pygame.display.set_mode((600, 600),pygame.HIDDEN)
canvas_renderer.init()

backgroundColor='gray75'

window = tk.Tk()
window.title("editor")
window.geometry("600x600")

window.columnconfigure((0,1,2), weight = 1, uniform='a')
window.rowconfigure(0,weight=1)

leftPanel = tk.Frame(master=window, bg="red")
leftPanel.grid(row=0,column=0,columnspan=2, sticky="WENS")

leftPanel.columnconfigure(0, weight=1)
leftPanel.rowconfigure(0, weight=3)
leftPanel.rowconfigure(1, weight=1)

canvas = tk.Canvas(leftPanel, background=backgroundColor)
canvas.grid(row=0, column=0, sticky="WENS")

bottomLeftPanel = tk.Frame(master=leftPanel, bg="gray75")
bottomLeftPanel.grid(row=1,column=0,sticky="WENS")

bottomLeftPanel.rowconfigure(0,weight=1)
bottomLeftPanel.columnconfigure((0,1),weight=1, uniform='a')

saveButton = tk.Button(bottomLeftPanel, text="SAVE")
saveButton.grid(row=0,column=0)

canvasControlPanel = tk.Frame(master=bottomLeftPanel, bg="yellow")
canvasControlPanel.grid(row=0,column=1,sticky="WENS")

canvasControlPanel.columnconfigure((0,1,2,3,4), weight=1)
canvasControlPanel.rowconfigure((0,1,2), weight=1)

upButton = tk.Button(canvasControlPanel, text='UP')
downButton = tk.Button(canvasControlPanel, text='DOWN')
leftButton = tk.Button(canvasControlPanel, text='LEFT')
rightButton = tk.Button(canvasControlPanel, text='RIGHT')
zoomInButton = tk.Button(canvasControlPanel, text='+')
zoomOutButton = tk.Button(canvasControlPanel, text='-')

upButton.grid(row=0, column=2)
downButton.grid(row=3, column=2)
leftButton.grid(row=1,column=0)
rightButton.grid(row=1, column = 4)
zoomOutButton.grid(row=1,column=1, sticky='WE')
zoomInButton.grid(row=1,column=3, sticky='WE')

rightPanel = tk.Frame(master=window, bg="blue")
rightPanel.grid(row=0,column=2, columnspan=1, sticky="WENS")

rightPanel.rowconfigure((0,1,2), weight=1, uniform='a')
rightPanel.columnconfigure(0, weight=1)


selectionPanel = tk.Frame(master=rightPanel, bg="yellow")
selectionPanel.grid(row=1, column=0, sticky='WENS')
selectionPanel.columnconfigure((0,1), weight=1)
selectionPanel.rowconfigure(0, weight=2, uniform='a')
selectionPanel.rowconfigure(1, weight=1, uniform='a')

selectionCanvas = tk.Canvas(selectionPanel, background=backgroundColor)
selectionCanvas.grid(row=0, column=0, columnspan=2, sticky='WENS')
previousSelectionButton = tk.Button(selectionPanel, text='<=')
nextSelectionButton = tk.Button(selectionPanel, text='=>')
previousSelectionButton.grid(row=1, column=0)
nextSelectionButton.grid(row=1, column=1)

f = open("level_data.txt", "r")
level_data = json.load(f)

data = {}

tiles = []

number_of_tiles = 23

for row_data in level_data["tilemap"]["tiles"]:
   row = []
   for tile_data in row_data.split(","):
      row.append(int(tile_data))
   tiles.append(row)

data["tiles"] = tiles
data["text_coordinates"] = "(0,0)"
data["pov"] = {"x":0, "y":0}
data["tile_width"] = 32
data["tile_height"] = 32
data["mouse_inside_canvas"] = False

selection_page = 0

canvas_image = canvas_renderer.render_canvas(data)

canvas.create_image(0, 0, image=canvas_image, anchor=tk.NW)

selectionCanvas_image = None


def redrawCanvas():
    global canvas_image
    w = canvas.winfo_width()
    h = canvas.winfo_height()

    data["canvas_width"] = w
    data["canvas_height"] = h

    canvas.create_rectangle(0,0,w,h, fill=backgroundColor)  

    canvas_image = canvas_renderer.render_canvas(data)
    canvas.create_image(0, 0, image=canvas_image, anchor=tk.NW)

def redrawSelectionCanvas():
   global selectionCanvas_image
   w = selectionCanvas.winfo_width()
   h = selectionCanvas.winfo_height()

   page_size = int(w / data["tile_width"])
   first_tile = page_size * selection_page
   last_tile = min(first_tile + page_size - 1, number_of_tiles)

   data["selection_first_tile"] = first_tile
   data["selection_last_tile"] = last_tile

   selectionCanvas.create_rectangle(0,0,w,h, fill=backgroundColor)  

   selectionCanvas_image = canvas_renderer.render_selection_canvas(data)
   selectionCanvas.create_image(0, 0, image=selectionCanvas_image, anchor=tk.NW)

def motion(event):
  global text_coordinates, data
  tile_x = int(event.x/data["tile_width"]) + data["pov"]["x"]
  tile_y = int(event.y/data["tile_height"]) + data["pov"]["y"]
  data["text_coordinates"] = "(" + str(tile_x) + "," + str(tile_y) + ")"
  data["mouse_tile_x"] = tile_x
  data["mouse_tile_y"] = tile_y
  redrawCanvas()


def on_window_resize(event):
   global selection_page
   redrawCanvas()
   selection_page = 0
   redrawSelectionCanvas()
   return

def pov_up(event):
   data["pov"]["y"]-=1
   redrawCanvas()

def pov_down(event):
   data["pov"]["y"]+=1
   redrawCanvas()

def pov_left(event):
   data["pov"]["x"]-=1
   redrawCanvas()

def pov_right(event):
   data["pov"]["x"]+=1
   redrawCanvas()

def previous_selection_page(event):
   global selection_page
   if selection_page > 0:
      selection_page -= 1
      redrawSelectionCanvas()

def next_selection_page(event):
   global selection_page
   w = selectionCanvas.winfo_width()   
   number_of_pages = int((number_of_tiles + 1) * data["tile_width"] / w) + 1   
   if selection_page + 1 < number_of_pages:
      selection_page += 1      
      redrawSelectionCanvas()

def select_tile(event):
   w = selectionCanvas.winfo_width()   

   page_size = int(w / data["tile_width"])
   first_tile = page_size * selection_page

   tile = first_tile + int(event.x / data["tile_width"])
   if tile <= number_of_tiles:
      data["selected_tile"] = tile
      redrawSelectionCanvas()

def mouse_entered_canvas(event):   
   data["mouse_inside_canvas"] = True

def mouse_exited_canvas(event):   
   data["mouse_inside_canvas"] = False
   redrawCanvas()

def setup_tile(event):
   global data, tiles
   if not "selected_tile" in data:
      return   
   tile_x = data["mouse_tile_x"]
   tile_y = data["mouse_tile_y"] 
   
   tiles = data["tiles"]

   if tile_y < len(tiles):
      if tile_x < len(tiles[tile_y]):
         tiles[tile_y][tile_x] = data["selected_tile"]
         redrawCanvas()


def save(event):
   global level_data
   tiles_to_save = []
   for row in tiles:
      row_str = []
      for tile in row:
         row_str.append(str(tile))
      tiles_to_save.append(",".join(row_str))
   level_data["tilemap"]["tiles"] = tiles_to_save

   out_file = open("level_data_edited.txt", "w")
   json.dump(level_data, out_file, indent=4)
   

canvas.bind('<Motion>',motion)
canvas.bind('<Enter>',mouse_entered_canvas)
canvas.bind('<Leave>',mouse_exited_canvas)
canvas.bind('<Button-1>', setup_tile)
selectionCanvas.bind('<Button-1>', select_tile)
window.bind("<Configure>", on_window_resize)
upButton.bind('<Button-1>', pov_up)
downButton.bind('<Button-1>', pov_down)
leftButton.bind('<Button-1>', pov_left)
rightButton.bind('<Button-1>', pov_right)
previousSelectionButton.bind('<Button-1>', previous_selection_page)
nextSelectionButton.bind('<Button-1>', next_selection_page)
saveButton.bind('<Button-1>', save)

window.mainloop()


