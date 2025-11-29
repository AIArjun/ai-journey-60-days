nums = [12, 45, 3, 67, 23, 89, 5]
max_num = nums[0]
for n in nums:
    if n > max_num:
        max_num = n
second_max = -1
for n in nums:
    if n > second_max and n !=max_num:
        second_max= n
print(second_max)
