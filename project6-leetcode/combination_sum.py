def combinationSum(candidates, target):
    """
    :type candidates: List[int]
    :type target: int
    :rtype: List[List[int]]
    """

    outputs = []

    for i in range(len(candidates)):
        # If the number is divisible by the target
        if target % candidates[i] == 0:
            repeats = []
            num_repeats = target // candidates[i]
            for _ in range(num_repeats):
                repeats.append(candidates[i])
            repeats.sort()
            outputs.append(repeats)



    return list(outputs)

# candidates = [2,3,5], target = 8
# candidates = [2,3,6,7], target = 7
print(combinationSum(candidates = [2,3,6,7], target = 7))