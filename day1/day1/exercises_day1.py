# Day 1 Exercises - Solutions

# -----------------------------------------
# 1. Sum of two numbers
# -----------------------------------------
def add(a, b):
    return a + b

print("Exercise 1 - Sum:", add(10, 25))


# -----------------------------------------
# 2. Find largest number in a list
# -----------------------------------------
numbers = [12, 99, 4, 27, 56]

largest = numbers[0]
for num in numbers:
    if num > largest:
        largest = num

print("Exercise 2 - Largest number:", largest)


# -----------------------------------------
# 3. Count vowels in a string
# -----------------------------------------
text = "Arjun is becoming an AI Engineer"
vowels = "aeiouAEIOU"
count = 0

for char in text:
    if char in vowels:
        count += 1

print("Exercise 3 - Vowel count:", count)


# -----------------------------------------
# 4. Reverse a string
# -----------------------------------------
word = "AI ENGINEER"
reversed_word = word[::-1]

print("Exercise 4 - Reversed:", reversed_word)


# -----------------------------------------
# 5. Simple calculator
# -----------------------------------------
def calculator(a, b, operation):
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        return a / b
    else:
        return "Invalid operation"

print("Exercise 5 - Calculator:", calculator(12, 6, "multiply"))

