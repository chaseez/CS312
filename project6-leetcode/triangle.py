def get_paths(i, j, tri):
    pass


def minimumTotal(triangle):
    """
    :type triangle: List[List[int]]
    :rtype: int
    """
    """
    Here's a visual:
    [   [1]   ] # 1 -> 2 or 3
    [  [2,3]  ] # 2 -> 4 or 5, 3 -> 5 or 6
    [ [4,5,6] ] # 4 -> 4 or 3, 5 -> 3 or 2, 6 -> 2 or 1
    [[4,3,2,1]] # These don't point to anything
    """

    prev_running_cost = {(0, 0): triangle[0][0]}

    for i in range(1, len(triangle)):
        for j in range(len(triangle[i])):
            if j == 0:
                prev_running_cost[i, j] = prev_running_cost[i - 1, j] + triangle[i][j]
            elif j + 1 == len(triangle[i]):
                prev_running_cost[i, j] = prev_running_cost[i - 1, j - 1] + triangle[i][j]
            else:
                left_parent = prev_running_cost[i - 1, j - 1] + triangle[i][j]
                right_parent = prev_running_cost[i - 1, j] + triangle[i][j]
                prev_running_cost[i, j] = left_parent if left_parent < right_parent else right_parent

    last_row = -1 * len(triangle[-1])
    min_path = min(list(prev_running_cost.values())[last_row:])
    return min_path


# print(minimumTotal([[2],[3,4],[6,5,7],[4,1,8,3]]))

a =[1, 3, 4, 2]

a.sort()

print(a)
