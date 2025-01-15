def load_projectile(projectile_data):
    projectile = {
        "type":"projectile",
        "x":int(projectile_data["x"]),
        "y":int(projectile_data["y"]),
        "angle":int(projectile_data["angle"]),
        "source":projectile_data["source"]   
    }
    
    return projectile