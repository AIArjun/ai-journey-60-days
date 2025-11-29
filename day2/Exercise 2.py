skills = ["Python", "AI", "Data", "Deep Learning", "ML"]

filtered = []

for skill in skills:
    if len(skill) > 2:
        filtered.append(skill)

print(filtered)

