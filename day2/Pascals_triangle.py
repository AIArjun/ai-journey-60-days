import math

for n in range(6):
    for r in range(n + 1):
        val = math.factorial(n) // (math.factorial(r) * math.factorial(n - r))
        print(val, end=" ")
    print()
