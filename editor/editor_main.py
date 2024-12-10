import tkinter as tk
import pygame
import canvas_renderer
import json
import math
import entity_stuff

pygame.init()
pygame.font.init()
pygame.display.set_mode((600, 600),pygame.HIDDEN)
entity_stuff.init()
canvas_renderer.init()


data = {"mode":"tilemap", "submode":""}
selection_page = 0

backgroundColor='gray75'

window = tk.Tk()
window.title("editor")
window.geometry("600x600")

window.columnconfigure((0,1,2), weight = 1, uniform='a')
window.rowconfigure(0,weight=1)

leftPanel = tk.Frame(master=window, bg=backgroundColor)
leftPanel.grid(row=0,column=0,columnspan=2, sticky="WENS")

leftPanel.columnconfigure(0, weight=1)
leftPanel.rowconfigure(0, weight=3)
leftPanel.rowconfigure(1, weight=1)

canvas = tk.Canvas(leftPanel, background=backgroundColor)
canvas.grid(row=0, column=0, sticky="WENS")

bottomLeftPanel = tk.Frame(master=leftPanel, bg=backgroundColor)
bottomLeftPanel.grid(row=1,column=0,sticky="WENS")

bottomLeftPanel.rowconfigure(0,weight=1)
bottomLeftPanel.columnconfigure((0,1),weight=1, uniform='a')

saveButton = tk.Button(bottomLeftPanel, text="SAVE")
saveButton.grid(row=0,column=0)

canvasControlPanel = tk.Frame(master=bottomLeftPanel, bg=backgroundColor)
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

rightPanel = tk.Frame(master=window, bg=backgroundColor)
rightPanel.grid(row=0,column=2, columnspan=1, sticky="WENS")

rightPanel.rowconfigure((0,1,2), weight=1, uniform='a')
rightPanel.columnconfigure(0, weight=1)

commandPanel = tk.Frame(master=rightPanel, bg=backgroundColor)
commandPanel.grid(row=0, column=0, sticky='WENS')
commandPanel.columnconfigure(0,weight=1)
commandPanel.rowconfigure((0,1,2), weight = 1, uniform='a')
modePanel = tk.Frame(master=commandPanel, bg = backgroundColor)
modePanel.grid(column=0,row=0,sticky='WENS')

modePanel.rowconfigure(0,weight=1)
modePanel.columnconfigure((0,1), weight= 1)

var_mode = tk.IntVar()

def select_mode():
   global selection_page
   if var_mode.get() == 1:
      data["mode"] = "tilemap"
   if var_mode.get() == 2:
      data["mode"] = "entities"
      data["submode"] = "add_entities"   
   selection_page = 0
   updateSubmodePanel()
   redrawSelectionCanvas()
   updateEntityFieldPanel()

R1 = tk.Radiobutton(modePanel, text="Tile map", variable=var_mode, value=1, command=select_mode)
R1.select()
R2 = tk.Radiobutton(modePanel, text="Entities", variable=var_mode, value=2, command=select_mode)
R1.grid(row=0, column=0)
R2.grid(row=0, column=1)

submodePanel = tk.Frame(master=commandPanel, bg = backgroundColor)
submodePanel.grid(column=0,row=1, rowspan=2, sticky='WENS')

var_submode = tk.IntVar()

def updateSubmodePanel():
   submodePanel.grid_forget()
   for child in submodePanel.winfo_children():
      child.destroy()
   
   if data["mode"] == "entities":
      submodePanel.grid(column=0,row=1, rowspan=2, sticky='WENS')
      submodePanel.rowconfigure((0,1,2), weight= 1)
      submodePanel.columnconfigure(0, weight= 1)
      SR1 = tk.Radiobutton(submodePanel, text="Add entities", variable=var_submode, value=1, command=select_submode)
      SR1.select()
      SR2 = tk.Radiobutton(submodePanel, text="Select entity", variable=var_submode, value=2, command=select_submode)
      SR3 = tk.Radiobutton(submodePanel, text="Remove entity", variable=var_submode, value=3, command=select_submode)
      SR1.grid(row=0, column=0, sticky='WENS')
      SR2.grid(row=1, column=0, sticky='WENS')      
      SR3.grid(row=2, column=0, sticky='WENS')


def select_submode():
   global selection_page
   if var_submode.get() == 1:
      data["submode"] = "add_entities"
   if var_submode.get() == 2:
      data["submode"] = "select_entity"
   if var_submode.get() == 3:
      data["submode"] = "remove_entity"
   selection_page = 0
   redrawSelectionCanvas()

updateSubmodePanel()

selectionPanel = tk.Frame(master=rightPanel, bg=backgroundColor)
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

entityFieldPanel = tk.Frame(master=rightPanel, bg=backgroundColor)

entityFieldEntries = []

f = open("level_data_edited.txt", "r")
level_data = json.load(f)

tiles = []

number_of_tiles = 23

for row_data in level_data["tilemap"]["tiles"]:
   row = []
   for tile_data in row_data.split(","):
      row.append(int(tile_data))
   tiles.append(row)

data["tiles"] = tiles
data["entities"] = level_data["entities"]
data["text_coordinates"] = "(0,0)"
data["pov"] = {"x":0, "y":0}
data["tile_width"] = 32
data["tile_height"] = 32
data["mouse_inside_canvas"] = False

canvas_image = canvas_renderer.render_canvas(data)

canvas.create_image(0, 0, image=canvas_image, anchor=tk.NW)

selectionCanvas_image = None

def entityFieldEvent(event):
   if not "current_selected_entity" in data:      
      return
   
   entity = data["current_selected_entity"]
   
   widget = event.widget
   fieldEntry = None
   for entityFieldEntry in entityFieldEntries:
      if widget == entityFieldEntry["entry"]:
         fieldEntry = entityFieldEntry
   
   if fieldEntry != None:
      entity[fieldEntry["field_name"]] = widget.get()
      redrawCanvas()


def updateEntityFieldPanel():

   global entityFieldEntries

   entityFieldPanel.grid_forget()
   for child in entityFieldPanel.winfo_children():
      child.destroy()

   if data["mode"] != "entities":
      return

   if not "current_selected_entity" in data:      
      return

   entity = data["current_selected_entity"]

   entityFieldEntries = [{
      "field_name":"x",
      "label": tk.Label(entityFieldPanel, text = "x"),
      "entry": tk.Entry(entityFieldPanel)
   },{
      "field_name":"y",
      "label": tk.Label(entityFieldPanel, text = "y"),
      "entry": tk.Entry(entityFieldPanel)
   },{
      "field_name":"angle",
      "label": tk.Label(entityFieldPanel, text = "angle"),
      "entry": tk.Entry(entityFieldPanel)
   }]

   fields = entity_stuff.get_fields_by_entity_name(entity["type"])

   for field in fields:
      field_name = field["key"]
      entry = tk.Entry(entityFieldPanel)
      entityFieldEntries.append({"field_name":field_name,
                                 "label": tk.Label(entityFieldPanel, text = field_name),
                                 "entry":entry})

   entityFieldPanel.grid(row=2, column=0, sticky='WENS')
   entityFieldPanel.columnconfigure((0,1), weight=1)
   entityFieldPanel.rowconfigure([0,1,2,3,4,5,6,7,8,9,10,11], weight=1, uniform='a')   

   for i in range(len(entityFieldEntries)):
      field_name = entityFieldEntries[i]["field_name"]
      label = entityFieldEntries[i]["label"]
      entry = entityFieldEntries[i]["entry"]

      if field_name in entity:
         field_value = entity[field_name]
         entry.insert(0,str(field_value))

      label.grid(column=0,row=i,sticky='WENS')
      entry.grid(column=1,row=i,sticky='WENS')

      entry.bind('<FocusOut>',entityFieldEvent)
      entry.bind('<Return>',entityFieldEvent)

   return

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

   element_width = 0
   if data["mode"] == "tilemap":
      element_width = data["tile_width"]
   elif data["mode"] == "entities":      
      element_width = entity_stuff.get_entity_data()["image_width"]

   number_of_elements = 0
   if data["mode"] == "tilemap":
      number_of_elements = number_of_tiles
   elif data["mode"] == "entities":
      number_of_elements = len(entity_stuff.get_entity_data()["entities"])

   page_size = int(w / element_width)
   first_element = page_size * selection_page
   last_element = min(first_element + page_size - 1, number_of_elements)

   data["selection_first_element"] = first_element
   data["selection_last_element"] = last_element

   selectionCanvas.create_rectangle(0,0,w,h, fill=backgroundColor)  

   selectionCanvas_image = canvas_renderer.render_selection_canvas(data)
   selectionCanvas.create_image(0, 0, image=selectionCanvas_image, anchor=tk.NW)

def motion(event):
  global text_coordinates, data
  tile_x = int(event.x/data["tile_width"]) + data["pov"]["x"]
  tile_y = int(event.y/data["tile_height"]) + data["pov"]["y"]
  coord_x = int(event.x) + data["pov"]["x"] * data["tile_width"]
  coord_y = int(event.y) + data["pov"]["y"] * data["tile_height"]
  data["text_coordinates"] = "(" + str(tile_x) + "," + str(tile_y) + ") / (" + str(coord_x) + "," + str(coord_y) + ")"
  data["mouse_tile_x"] = tile_x
  data["mouse_tile_y"] = tile_y
  data["mouse_x"] = event.x
  data["mouse_y"] = event.y

  if data["mode"] == "entities" and (data["submode"] == "select_entity" or data["submode"] == "remove_entity"):     
     mouse_on_entity = None
     shortest_distance = 1000
     for entity in data["entities"]:
        entity_x = int(entity["x"])
        entity_y = int(entity["y"])
        distance = math.sqrt(math.pow(coord_x - entity_x, 2) + math.pow(coord_y - entity_y, 2))
        if distance < shortest_distance and distance < 300:
           shortest_distance = distance
           mouse_on_entity = entity
     if mouse_on_entity != None:
        data["mouse_on_entity"] = mouse_on_entity   

  redrawCanvas()


def on_window_resize(event):
   global selection_page
   redrawCanvas()
   selection_page = 0
   redrawSelectionCanvas()
   return

def pov_up(event):
   data["pov"]["y"]-=5
   redrawCanvas()

def pov_down(event):
   data["pov"]["y"]+=5
   redrawCanvas()

def pov_left(event):
   data["pov"]["x"]-=5
   redrawCanvas()

def pov_right(event):
   data["pov"]["x"]+=5
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

def select_element(event):
   w = selectionCanvas.winfo_width()   

   element_width = 0
   if data["mode"] == "tilemap":
      element_width = data["tile_width"]
   elif data["mode"] == "entities":
      element_width = entity_stuff.get_entity_data()["image_width"]

   number_of_elements = 0
   if data["mode"] == "tilemap":
      number_of_elements = number_of_tiles
   elif data["mode"] == "entities":
      number_of_elements = len(entity_stuff.get_entity_data()["entities"])

   page_size = int(w / element_width)
   
   first_element = page_size * selection_page

   element = first_element + int(event.x / element_width)
   if data["mode"] == "tilemap":
      if element <= number_of_tiles:
         data["selected_tile"] = element
         redrawSelectionCanvas()
   elif data["mode"] == "entities":
      if element < number_of_elements:
         data["selected_entity"] = element
         redrawSelectionCanvas()

def mouse_entered_canvas(event):   
   data["mouse_inside_canvas"] = True

def mouse_exited_canvas(event):   
   data["mouse_inside_canvas"] = False
   redrawCanvas()

def click_on_canvas(event):
   if data["mode"] == "tilemap":
      setup_tile(event)
   elif data["mode"] == "entities" and data["submode"] == "add_entities":
      setup_entity(event)
   elif data["mode"] == "entities" and data["submode"] == "select_entity":
      select_entity(event)
   elif data["mode"] == "entities" and data["submode"] == "remove_entity":
      remove_entity(event)

def select_entity(event):
   global data
   if "mouse_on_entity" in data:
      data["current_selected_entity"] = data["mouse_on_entity"]
      redrawCanvas()
      updateEntityFieldPanel()

def remove_entity(event):
   global data
   if "mouse_on_entity" in data:
      entity = data["mouse_on_entity"]
      del data["mouse_on_entity"]
      if "current_selected_entity" in data and data["current_selected_entity"] == "entity":
         del data["current_selected_entity"]
      data["entities"].remove(entity)
      redrawCanvas()
      updateEntityFieldPanel()

def setup_entity(event):
   global data
   if not "selected_entity" in data:
      return
   selected_entity = entity_stuff.get_entity_data()["entities"][data["selected_entity"]]
   x = event.x + data["pov"]["x"] * data["tile_width"]
   y = event.y + data["pov"]["y"] * data["tile_height"]
   angle = 0
   entity = {
      "type":selected_entity["name"],
      "x":x,
      "y":y,
      "angle":angle
   }
   data["entities"].append(entity)

   data["current_selected_entity"] = entity
   updateEntityFieldPanel()

   redrawCanvas()


def setup_tile(event):
   global data, tiles
   if not "selected_tile" in data:
      return   
   tile_x = data["mouse_tile_x"]
   tile_y = data["mouse_tile_y"] 
   
   if tile_x < 0:
      return
   if tile_y < 0:
      return

   cols = len(tiles[0])
   rows = len(tiles)

   if tile_x >= cols:
      right_add_colums(tile_x - cols + 1)
   if tile_y >= rows:
      bottom_add_rows(tile_y - rows + 1)

   tiles = data["tiles"]

   if tile_y < len(tiles):
      if tile_x < len(tiles[tile_y]):
         tiles[tile_y][tile_x] = data["selected_tile"]
         redrawCanvas()

def right_add_colums(number_of_columns):
   global tiles
   for row in tiles:
      for i in range(number_of_columns):
         row.append(0)

def bottom_add_rows(number_of_rows):
   global tiles
   cols = len(tiles[0])
   for i in range(number_of_rows):
      row = []
      for col in range(cols):
         row.append(0)
      tiles.append(row)


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
canvas.bind('<Button-1>', click_on_canvas)
selectionCanvas.bind('<Button-1>', select_element)
window.bind("<Configure>", on_window_resize)
upButton.bind('<Button-1>', pov_up)
downButton.bind('<Button-1>', pov_down)
leftButton.bind('<Button-1>', pov_left)
rightButton.bind('<Button-1>', pov_right)
previousSelectionButton.bind('<Button-1>', previous_selection_page)
nextSelectionButton.bind('<Button-1>', next_selection_page)
saveButton.bind('<Button-1>', save)

window.mainloop()


