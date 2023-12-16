def tribonacci(n):
    """
    :type n: int
    :rtype: int
    """
    stored_values = [0, 1, 1]
    if n == 0:
        return 0
    if n == 1:
        return 1
    if n == 2:
        return 1

    for i in range(2, n-1):
        next_value = stored_values[i - 2] + stored_values[i - 1] + stored_values[i]
        stored_values.append(next_value)

    total = sum(stored_values[-3:])
    return total

print(tribonacci(25))