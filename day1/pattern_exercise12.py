for i in range(5):
    spaces = 5 - i - 1
    if i == 0:
        print(" " * spaces + "*")
    elif i == 4:
        print("*" * 9)
    else:
        print(" " * spaces + "*" + " " * (2*i - 1) + "*")
