for i in range(5):  
    letter = chr(65 + i)        # A, B, C, D, E
    for j in range(i + 1):      # repeat based on row number
        print(letter, end="")
    print()

