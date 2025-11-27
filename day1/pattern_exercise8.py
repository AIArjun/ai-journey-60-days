n = 6

for i in range(1, n + 1):
    if i == 1:
        print("*")
    elif i == 2:
        print("**")
    elif i < n:
        print("*" + " " * (i - 2) + "*")
    else:  # last row
        print("*" * n)
