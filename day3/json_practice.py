import json
profile = {
    "name": "Arjun",
    "age": "24",
    "skills": ["python","ai"]
}
with open("profile.json", "w") as f:
    json.dump(profile, f)