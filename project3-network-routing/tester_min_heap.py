from MinHeap import *
from math import inf as INF

items = [('A',6),('B', 0), ('C', 0), ('D', 4), ('E', 7), ('F', 1), ('G', 0)]

min_heap = MinHeap(items)

print(min_heap.items)

print(min_heap.pop())
print(min_heap.items)

print(min_heap.pop())
print(min_heap.items)

print(min_heap.pop())
print(min_heap.items)

print(min_heap.pop())
print(min_heap.items)

print(min_heap.pop())
print(min_heap.items)

print(min_heap.pop())
print(min_heap.items)

print(min_heap.pop())
print(min_heap.items)

min_heap.insert(('b', 6))
min_heap.insert(('q', INF))
min_heap.insert(('d', 3))
min_heap.insert(('e', INF))
min_heap.insert(('a', 9))
min_heap.insert(('c', 4))
min_heap.insert(('n', INF))
min_heap.insert(('l', INF))

print(min_heap.items)

min_heap.decrease_key(('q', 4))
min_heap.decrease_key(('e', 10))
min_heap.decrease_key(('n', 15))
min_heap.decrease_key(('q', 0))

print(min_heap.items)





