class MinHeap():
    def __init__(self, items):
        # Stores all the items in tuples (previous, weight)
        # item[0] = previous node
        # item[1] = weight
        self.items = []
        self.make_queue(items)
        self.PREVIOUS = 0
        self.WEIGHT = 1
        self.LEFT = True
        self.RIGHT = False

    def make_queue(self, items):
        self.items = items

    def get_parent_index(self, pos):
        if pos == 0:
            return pos
        elif pos % 2 == 0:
            return (pos - 2) // 2
        else:
            return (pos - 1) // 2

    def get_child_index(self, pos, left):
        if left:
            return (pos * 2) + 1
        else:
            return (pos * 2) + 2

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
        left_child = self.items[left_child_index]
        left_weight = left_child[self.WEIGHT]

        right_child_index = self.get_child_index(item_index, self.RIGHT)
        right_child = self.items[right_child_index]
        right_weight = right_child[self.WEIGHT]

        while item_weight > left_weight and item_weight > right_weight:
            if left_weight > right_weight:
                if item_weight > left_weight:
                    self.swap_items(item_index, left_child_index)

                    item_index = left_child_index
                    left_child_index = self.get_child_index(item_index, self.LEFT)
                    left_child = self.items[left_child_index]
                    left_weight = left_child[self.WEIGHT]

                    right_child_index = self.get_child_index(item_index, self.RIGHT)
                    right_child = self.items[right_child_index]
                    right_weight = right_child[self.WEIGHT]


