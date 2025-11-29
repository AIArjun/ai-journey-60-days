def analyze_list(nums):
    positive = 0
    negative = 0
    zero = 0

    for n in nums:
        if n > 0:
            positive += 1
        elif n < 0:
            negative += 1
        else:
            zero += 1
    return positive,negative,zero
        
nums = [0, -1, 5, 3, 0, -4, 10]
result = analyze_list(nums)
print(result)