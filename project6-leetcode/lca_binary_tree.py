class TreeNode():
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class BST():
    def __init__(self, head):
        self.head = head
        self.depth = 1
        self.items = set()
        self.items.add(self.head)

    def insert(self, item):
        if item == None:
            return
        self.put_in_tree(item)

    def put_in_tree(self, item):
        curr_depth = 1
        curr_node = self.head
        while True:
            if item.val > curr_node.val:
                if curr_node.left is None:
                    curr_node.left = item
                    break
                else:
                    curr_node = curr_node.left
            elif item.val < curr_node.val:
                if curr_node.right is None:
                    curr_node.right = item
                    break
                else:
                    curr_node = curr_node.right
            else:
                print('Item is already in the tree')
                return
            curr_depth += 1
        if curr_depth > self.depth:
            self.depth = curr_depth
        self.items.add(item)

def lowestCommonAncestor(root, p, q):
    """
    :type root: TreeNode
    :type p: TreeNode
    :type q: TreeNode
    :rtype: TreeNode
    """
    head = root[0]
    items = root[1:]

    bst = BST(head)
    for item in items:
        bst.insert(item)

    for node in bst.items:
        print(node, node.val, node.left, node.right)


root = None






# bst = BST(TreeNode(2))
#
# for i in [15,1,3,0,6,8,-1]:
#     bst.insert(TreeNode(i))
#
# for node in bst.items:
#     print(node, node.val, node.left, node.right)
#
# print(bst.depth)