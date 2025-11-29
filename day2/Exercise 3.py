nums = [12, 45, 3, 67, 23, 89, 5]

# Assume the first number is the maximum
max_num = nums[0]

# Loop through each number in the list
for n in nums:
    if n > max_num:
        max_num = n

print("Maximum number:", max_num)
