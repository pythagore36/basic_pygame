def load_mine(mine_data):
    mine = {
        "type":"mine",
        "x":int(mine_data["x"]),
        "y":int(mine_data["y"]),                
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
        patrolling_data = {"target":0,
                           "velocity":int(mine_data["patrolling_speed"])}
        s = mine_data["patrolling_points"]
        points = parse_points(s)
        
        for i in range(len(points)):
            points[i] = (mine["x"] + points[i][0], mine["y"] + points[i][1])
        
        patrolling_data["points"] = points

        mine["patrolling_data"] = patrolling_data
        
    if "angle" in mine_data:
        mine["angle"] = int(mine_data["angle"])

    return mine

# format (x1,y1);(x2,y2);...;(xn,yn)
def parse_points(s):
    points = []
    for point_description in s.split(";"):
        coords = point_description.split(",")
        if len(coords) != 2 or coords[0][0]!='(' or coords[1][-1] != ')':
            continue
        points.append((int(coords[0][1:]), int(coords[1][0:-1])))
    return points