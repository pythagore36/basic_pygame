import collision_manager
import renderer


def init(door_object):
    global hitbox_closed, hitbox_open, opening_counter, closing_counter
    if "model" in door_object:
        hitbox_closed = door_object["model"]["hitbox_closed"]
        hitbox_open = door_object["model"]["hitbox_open"]
        door_object["hitboxes"] = [hitbox_closed]
        opening_counter = door_object["model"]["opening_number_frames"]
        closing_counter = door_object["model"]["closing_number_frames"]



def open(door_object):
    if door_object["state"] == "closed":
        door_object["state"] = "opening"
        door_object["counter"] = opening_counter
        door_object["frame"] = 0

def close(door_object, level_data):
    if door_object["state"] == "open":
        door_object["hitboxes"] = [hitbox_closed]

        # door cannot close if something is under it
        collisions = collision_manager.search_collisions(door_object, hitbox_closed, level_data)
        for collision in collisions:
            if collision["collision_type"] == "entity" and collision["hitbox"]["role"] == "solid":
                door_object["hitboxes"] = [hitbox_open]
                return

        door_object["state"] = "closing"
        door_object["counter"] = closing_counter
        door_object["frame"] = 0

def get_entity_field(id, field_name, level_data):
    for entity in level_data["entities"]:
        if "id" in entity and entity["id"] == id and field_name in entity:
            return entity[field_name]
    return None
    
def check_condition(condition, level_data):
    if condition["type"] == "state":
        id = condition["id"]
        state = condition["state"]
        return get_entity_field(id, "state", level_data) == state
    if condition["type"] == "and":
        children = condition["children"]
        for child in children:
            if not check_condition(child, level_data):
                return False
        return True
    if condition["type"] == "or":
        children = condition["children"]
        for child in children:
            if check_condition(child, level_data):
                return True
        return False
    if condition["type"] == "false":
        return False
    if condition["type"] == "true":
        return True
    return False

def update(door_object, level_data):    
    
    if "hitboxes" not in door_object:
        if door_object["state"] == "open":
            door_object["hitboxes"] = [hitbox_open]
        else :
            door_object["hitboxes"] = [hitbox_closed]

    if door_object["state"] == "opening":
        door_object["counter"] -= 1
        if door_object["counter"] <= 0:                    
            door_object["state"] = "open"
            door_object["hitboxes"] = [hitbox_open]
    
    if door_object["state"] == "closing":
        door_object["counter"] -= 1
        if door_object["counter"] <= 0:        
            door_object["state"] = "closed"
            
    if check_condition(door_object["open_condition"], level_data):
        open(door_object)
    else:
        close(door_object, level_data)

    return

def render(door_object, level_data):
    state = str(door_object["state"])
    if "model" in door_object and "state_sprites" in door_object["model"] and state in door_object["model"]["state_sprites"]:
        door_object["current_sprite"] = door_object["model"]["state_sprites"][state]
        renderer.render_sprite(door_object, level_data["camera"])    