def load_door(door_data):
    door = {
        "type":"door",
        "x":int(door_data["x"]),
        "y":int(door_data["y"]),        
        "state": "closed",        
        "current_image": 0
    }

    if "angle" in door_data:
        door["angle"] = int(door_data["angle"])

    if "open_condition" in door_data:
        door["open_condition"] = parse_condition(door_data["open_condition"])[1]

    return door

#format:
#true
#false
# (id,state)
# and(condition_1, condition_2, ..., condition_n)
# or(condition_1, condition_2, ..., condition_n)
def parse_condition(s):    
    s=s.strip()
    if s.upper() == 'FALSE':
        return ('', {"type": "false"})
    if s.upper() == 'TRUE':
        return ('', {"type": "true"})
    if s.startswith("(") and len(s)>1 and s[1:2].isdigit():
        if not ')' in s:
            return ("",None)
        end = s.index(")")        
        values = s[1:end].split(",")
        if len(values) != 2:
            return ("",None)
        id = values[0].strip()
        state = values[1].strip()
        return (s[end+1:], {
                    "type": "state",
                    "id": int(id),
                    "state": int(state)
                })
    elif s.startswith("and("):
        children = []
        s = s[4:]
        done = False
        while not done:
            (s, child) = parse_condition(s)
            if child == None:
                return ("",None)
            children.append(child)
            s = s.strip()
            if s.startswith(')'):
                done = True
            elif s.startswith(','):
                s = s[1:]
            else:
                return ("",None)
        return (s[1:],{"type":"and",
                "children":children})
    elif s.startswith("or("):
        children = []
        s = s[3:]
        done = False
        while not done:
            (s, child) = parse_condition(s)
            if child == None:
                return ("",None)
            children.append(child)
            s = s.strip()
            if s.startswith(')'):
                done = True
            elif s.startswith(','):
                s = s[1:]
            else:
                return ("",None)
        return (s[1:],{"type":"or",
                "children":children})
    else:
        return ("",None)