for i in range(1, 7):
    if i == 1:
        print("*")
    elif i == 6:
        print("*" * 6)
    else:
        print("*" + " " * (i - 2) + "*")
