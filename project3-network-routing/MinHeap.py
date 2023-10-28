class MinHeap():
    def __init__(self, items):
        self.PREVIOUS = 0
        self.WEIGHT = 1
        self.LEFT = True
        self.RIGHT = False

        # Stores all the items in tuples (previous, weight)
        # item[0] = previous node
        # item[1] = weight
        self.items = []
        self.make_queue(items)


    def make_queue(self, items):
        for item in items:
            self.insert(item)


    def get_parent_index(self, pos):
        if pos == 0:
            return pos
        elif pos % 2 == 0:
            return (pos - 2) // 2
        else:
            return (pos - 1) // 2


    def get_child_index(self, pos, left):
        index = None
        if left:
            index = (pos * 2) + 1
        else:
            index = (pos * 2) + 2

        if 0 <= index <= len(self.items) - 1:
            return index
        return None


    def insert(self, item):
        self.items.append(item)
        self.bubble_up(item)


    def swap_items(self, index_1, index_2):
        temp = self.items[index_2]
        self.items[index_2] = self.items[index_1]
        self.items[index_1] = temp


    def bubble_up(self, item):
        # Getting the index of the current item
        item_index = self.items.index(item)
        item_weight = item[self.WEIGHT]

        # Find the parent node
        parent_index = self.get_parent_index(item_index)
        parent = self.items[parent_index]
        parent_weight = parent[self.WEIGHT]

        # Keep looping and swapping indexes until the item weight is below a "lighter" parent
        while item_weight < parent_weight:
            # Takes the child item and swaps the contents with the parent
            self.swap_items(item_index, parent_index)

            item_index = parent_index
            parent_index = self.get_parent_index(item_index)
            parent = self.items[parent_index]
            parent_weight = parent[self.WEIGHT]

        # Maintain the completeness of the tree by comparing against the children
        self.sift_down(item, item_index)


    def sift_down(self, item, item_index):
        item_weight = item[self.WEIGHT]

        left_child_index = self.get_child_index(item_index, self.LEFT)
        if left_child_index is not None:
            left_child = self.items[left_child_index]
            left_weight = left_child[self.WEIGHT]

        right_child_index = self.get_child_index(item_index, self.RIGHT)
        if right_child_index is not None:
            right_child = self.items[right_child_index]
            right_weight = right_child[self.WEIGHT]


        # If there are more than 2 items in the heap
        if right_child_index is not None and left_child_index is not None:
            while item_weight > left_weight or item_weight > right_weight:
                # Always choose the smallest child to swap with
                if left_weight < right_weight:
                    if left_child_index is not None and item_weight > left_weight:
                        self.swap_items(item_index, left_child_index)
                        item_index = left_child_index

                else:
                    if right_child_index is not None and item_weight > right_weight:
                        self.swap_items(item_index, right_child_index)
                        item_index = right_child_index

                left_child_index = self.get_child_index(item_index, self.LEFT)
                if left_child_index is not None:
                    left_child = self.items[left_child_index]
                    left_weight = left_child[self.WEIGHT]

                right_child_index = self.get_child_index(item_index, self.RIGHT)
                if right_child_index is not None:
                    right_child = self.items[right_child_index]
                    right_weight = right_child[self.WEIGHT]

                if right_child_index is None or left_child_index is None:
                    break

        # If there are 2 items in the heap
        elif left_child_index is not None:
            if left_child_index is not None and item_weight > left_weight:
                self.swap_items(item_index, left_child_index)


    def pop(self):
        if len(self.items) > 1:
            self.swap_items(-1,0)
            min = self.items.pop()
            self.sift_down(self.items[0], 0)
            return min
        else: return self.items.pop()


    def decrease_key(self, item):
        found = False
        for i in range(len(self.items)):
            if self.items[i][0] == item[0]:
                self.items[i] = item
                found = True
                break
        if found: self.bubble_up(item)

    def find_node(self, node):
        for item in self.items:
            if node == item[0]:
                return item


