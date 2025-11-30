for i in range(1, 6):
    spaces = 5 - i          # number of spaces before stars
    stars = i               # number of stars in that row

    for s in range(spaces):
        print(" ", end="")

    for st in range(stars):
        print("*", end="")

    print()


