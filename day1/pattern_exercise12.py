for i in range(1, 6):
    if i == 1:
        print("*")
    elif i == 2:
        print("**")
    elif i == 5:
        print("*" * 6)
    else:
        # print hollow structure
        print("*" + " " * (i-2) + "*")
