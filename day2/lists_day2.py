# Day 2 - Lists & Logic Building

print("=== Day 2: Lists & Logic ===")

# 1. Creating lists
numbers = [10, 20, 30, 40, 50]
skills = ["Python", "AI", "Data Science"]
mixed = [1, "Arjun", True, 3.14]

print("Numbers:", numbers)
print("Skills:", skills)
print("Mixed:", mixed)

# 2. Indexing and slicing
print("\n--- Indexing & Slicing ---")
print("First number:", numbers[0])
print("Last number:", numbers[-1])
print("First three numbers:", numbers[0:3])
print("Middle slice:", numbers[1:4])  # 20, 30, 40

# 3. Modifying lists
print("\n--- Modifying Lists ---")
print("Original numbers:", numbers)

numbers.append(60)
print("After append 60:", numbers)

numbers.insert(1, 15)  # insert 15 at index 1
print("After insert 15 at index 1:", numbers)

removed = numbers.pop()  # remove last
print("After pop():", numbers, "| removed value:", removed)

numbers[0] = 5
print("After changing first element to 5:", numbers)

# 4. Looping over lists
print("\n--- Looping Over Lists ---")
for num in numbers:
    print("Number:", num)

print("\nSkills with index:")
for index, skill in enumerate(skills):
    print(index, "->", skill)

# 5. Basic calculations with lists
print("\n--- Calculations on Lists ---")
total = 0
for num in numbers:
    total += num

print("Sum of numbers:", total)
print("Length of list:", len(numbers))
print("Average:", total / len(numbers))

# 6. Nested loop example (pairs)
print("\n--- Nested Loop: All skill pairs ---")
for s1 in skills:
    for s2 in skills:
        print(s1, "-", s2)
