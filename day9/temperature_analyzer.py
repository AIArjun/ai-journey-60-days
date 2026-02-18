temperatures = [30, -5, 22, -12, 18, 0, -3, 25, 15, -8]
positive = []
negative = []
highest = temperatures[0] 
lowest = temperatures[0]
for temperature in temperatures:
  if temperature >= 0:
    positive.append(temperature)
  else:
    negative.append(temperature)
  if temperature > highest:
    highest = temperature
  if temperature < lowest:
        lowest = temperature
print(positive)
print(negative)
print(highest)
print(lowest)