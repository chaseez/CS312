import time

def f(n):
    if 0 <= n <= 2:
        return 1

    numbers = [1,1,1]
    value = 0

    for i in range(3, n + 1):
        value += numbers[i-1] + numbers[i-2] * numbers[i-3]
        numbers.append(value)
        value = 0

    return numbers[-1]


def f1(n):
    if 0 <= n <= 2:
        return 1
    return f1(n-1) + f1(n-2) * f(n-3)

start_time = time.time_ns()
print(f"Here's the linear start: {time.time_ns() - start_time}")
print(f(15))
print(f"Here's the linear stop: {time.time_ns() - start_time}")
start_time = time.time_ns()
print(f"Here's the exponential start: {time.time_ns() - start_time}")
print(f1(15))
print(f"Here's the exponential stop: {time.time_ns() - start_time}")
