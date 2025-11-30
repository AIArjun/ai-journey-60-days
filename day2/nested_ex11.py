for i in range(5):
    stars = 2 * (5 - i) - 1
    spaces = i            

    for s in range(spaces):
        print(" ", end="")

    for st in range(stars):
        print("*", end="")

    print()