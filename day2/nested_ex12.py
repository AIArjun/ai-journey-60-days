for i in range(5):
    spaces = 5 - i - 1
    stars = 2*i + 1
    for s in range(spaces):
        print(" ", end="")

    for st in range(stars):
        print("*", end="")
    print()
for i in range(4):
    spaces = i + 1
    stars = 2*(4 - i) - 1

    for s in range(spaces):
        print(" ", end="")

    for st in range(stars):
        print("*", end="")
    print()