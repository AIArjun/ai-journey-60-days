rows = 5
cols = 5

for i in range(rows):
    if i == 0 or i == rows - 1:
        print("*" * cols)
    else:
        print("*" + " " * (cols - 2) + "*")
