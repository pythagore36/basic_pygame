def load_mine(mine_data):
    mine = {
        "type":"mine",
        "x":mine_data["x"],
        "y":mine_data["y"],        
        "explosion_animation_delay":3,
        "vx":0,
        "vy":0,
        "hitbox": {"x":-15,
        "y":-15,
        "width":30,
        "height":30},
        "state":mine_data["state"]
    }

    if mine_data["state"] == "patrolling":
        patrolling_data = mine_data["patrolling_data"]
        points = patrolling_data["points"]
        for i in range(len(points)):
            points[i] = (mine_data["x"] + points[i][0], mine_data["y"] + points[i][1])
        mine["patrolling_data"] = patrolling_data
        
    return mine