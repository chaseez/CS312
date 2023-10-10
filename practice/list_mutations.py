alpha = ['a','b','c','d','e','f','g']

def change_list(foo, n):
    if n > 1:
        change_list(foo[:n//2], len(foo[:n//2]))
        change_list(foo[n//2:], len(foo[n//2:]))
    foo[n - 1] = 5


change_list(alpha, len(alpha))
print(alpha)