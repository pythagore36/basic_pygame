import collision_manager
import renderer
import patrolling

def init(mine_object):
    global state_sprites, explosion_counter
    mine_object["vx"] = 0
    mine_object["vy"] = 0
    if "model" in mine_object:
        model = mine_object["model"]
        mine_object["hitboxes"] = model["hitboxes"]
        state_sprites = model["state_sprites"]
        explosion_counter = model["explosion_counter"]

def remove_mine(mine_object, level_data):    
    level_data["messages"].append({
        "type":"remove_entity",
        "object":mine_object
    })

def damage_player(level_data, health_points):
    player_object = level_data["entities"][0]
    level_data["messages"].append({
        "type":"entity",
        "to": player_object,
        "object": {
            "title":"damage",
            "health_points": health_points
        }
    })

def update(mine_object, level_data):    
    if mine_object["state"] in ["standing", "patrolling"]:             
        collisions = collision_manager.search_collisions(mine_object, mine_object["hitboxes"][0], level_data)
        
        for collision in collisions:
            if collision["collision_type"] == "entity" and collision["entity"]["type"] == "player":
                mine_object["state"] = "exploding"
                mine_object["explosion_timer"] = explosion_counter
                damage_player(level_data,1)

    if mine_object["state"] == "patrolling":
        mine_object["vx"] = 0
        mine_object["vy"] = 0

        patrolling.apply_patrolling(mine_object)

        mine_object["x"] += mine_object["vx"]
        mine_object["y"] += mine_object["vy"]
    
    if mine_object["state"] == 'exploding':
        mine_object["explosion_timer"] -= 1
        # si on est arrivé à la fin de l'animation d'explosion, on supprime le projectile
        if mine_object["explosion_timer"] <= 0:
            remove_mine(mine_object, level_data)

def render(mine_object, level_data):
    state = str(mine_object["state"])
    if state in state_sprites:
        mine_object["current_sprite"] = state_sprites[state]
        renderer.render_sprite(mine_object, level_data["camera"]) 