from MinHeap import *
from math import inf as INF

items = [('A',0),('B', INF), ('C', INF), ('D', INF), ('E', INF), ('F', INF), ('G', INF)]

min_heap = MinHeap(items)

print(min_heap.items)

min_heap.swap_items(0, 6)

print(min_heap.items)

min_heap.bubble_up(min_heap.items[6])

print(min_heap.items)


