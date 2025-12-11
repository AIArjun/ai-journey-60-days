import json
with open("profile.json", "r") as f:
    data = json.load(f)
    print(data)
    print(data["name"])
    print(data["age"])
    print(data["skills"])

    
