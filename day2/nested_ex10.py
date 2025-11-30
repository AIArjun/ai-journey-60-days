for i in range(5):
    spaces = 5 - i - 1       # number of spaces before stars
    stars = 2 * i + 1             # number of stars in that row

    for s in range(spaces):
        print(" ", end="")

    for st in range(stars):
        print("*", end="")

    print()