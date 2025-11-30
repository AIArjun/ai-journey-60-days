for i in range(5):
    for j in range(5 - i):
        if i == 0:                     # first row → all stars
            print("*", end="")
        elif j == 0 or j == (5 - i - 1):   # first or last star of row
            print("*", end="")
        else:
            print(" ", end="")
    print()
