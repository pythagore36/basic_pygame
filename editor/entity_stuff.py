entity_data={}

def init():
    global entity_data
    entities = [{
        "id":0,
        "name":"player",
        "image":"player"
    },{
        "id":1,
        "name":"mine",
        "image":"mine"
    },{
        "id":2,
        "name":"flag",
        "image":"flag"
    }]
    entity_data["entities"] = entities
    entity_data["image_width"] = 40
    entity_data["image_height"] = 40

def get_entity_data():
    return entity_data