# Day 1 – Python Basics

# 1. Variables
name = "Arjun"
age = 23
salary_goal_in_crores = 3

print("Name:", name)
print("Age:", age)
print("Salary goal (crores):", salary_goal_in_crores)

# 2. Data types
integer_num = 10
float_num = 3.14
text = "AI Engineering"
truth = True

print(type(integer_num), type(float_num), type(text), type(truth))

# 3. Lists
skills = ["Python", "AI", "Data Science"]
print("Skills:", skills)
print("First skill:", skills[0])

# 4. Loops
for i in range(5):
    print("Count:", i)

# 5. Functions
def greet(n):
    return "Hello " + n + ", welcome to Day 1!"

print(greet("Arjun"))
