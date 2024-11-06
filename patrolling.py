import math

# une entity à laquelle on peut appliquer un patrolling est tout objet contenant des champs x,y,vx,vy et un champ patrolling_data contenant 
# une liste de points, la vitesse de patrolling et la cible courante.

def apply_patrolling(entity):
    x = entity["x"]
    y = entity["y"]
    points = entity["patrolling_data"]["points"]
    v = entity["patrolling_data"]["velocity"]
    target = entity["patrolling_data"]["target"]
    target_x = points[target][0]
    target_y = points[target][1]
    direction_vector = (target_x - x, target_y - y)
    distance = vector_norm(direction_vector)
    if distance <= v:
        entity["vx"] += direction_vector[0]
        entity["vy"] += direction_vector[1]
        if target + 1 < len(points):
            entity["patrolling_data"]["target"] += 1
        else:
            entity["patrolling_data"]["target"] = 0
    else:
        direction_vector = (direction_vector[0] * v / distance, direction_vector[1] * v / distance)
        entity["vx"] += direction_vector[0]
        entity["vy"] += direction_vector[1]



def vector_norm(vector):
    return math.sqrt(vector[0]*vector[0] + vector[1]*vector[1])