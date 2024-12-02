import math

def distance(entity1, entity2):
    return math.sqrt(math.pow(entity2["x"] - entity1["x"],2) + math.pow(entity2["y"] - entity1["y"],2))

def angle_to_target(entity1, entity2):
    return -math.degrees(math.atan2(entity2["y"] - entity1["y"], entity2["x"] - entity1["x"]))