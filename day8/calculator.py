first = input("Enter the first number: ")
second = input("Enter the second number: ")
user = input("operation is: +, -, *, /")
first = float(first)
second = float(second)
if user == "/" and second == 0:
  print ("Cannot divide by zero") 
elif user == "+":
  print ("Result:",first + second)
elif user == "-":
  print ("Result:",first - second)
elif user == "*":
  print ("Result:",first * second)
elif user == "/":
  print ("Result:",first / second)
else:
    print("Invalid operation")