def twoSum(nums, target):
    """
    :type nums: List[int]
    :type target: int
    :rtype: List[int]
    """
    found = False
    indexes = []
    for i in range(len(nums)):
        ith_element = nums[i]
        for j in range(i + 1, len(nums)):
            if ith_element + nums[j] == target:
                found = True
                indexes.append(i)
                indexes.append(j)
                break
        if found:
            break

    return indexes

print(twoSum([2,0,8,1], 9))