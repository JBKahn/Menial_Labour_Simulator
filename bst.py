'''Binary search tree module.'''


class BTNode(object):
    '''A node in a binary search tree.'''

    def __init__(self, data):
        '''A BTNode containing data with no left and right children.'''

        self.data = data
        self.left = None
        self.right = None
        self.parent = None


class BST(object):
    '''A binary search tree (BST). All data inserted into a BST must be
    mutually comparable.'''

    def __init__(self):
        '''Create a new empty BST.'''

        self.root = None

    def __eq__(self, target_tree):
        '''Return if target_tree is identical to this BST.'''

        return _compare(self.root, target_tree.root)

    def __ne__(self, target_tree):
        '''Return if target_tree is not identical to this BST.'''

        return not _compare(self.root, target_tree.root)

    def insert(self, data):
        ''' Insert data into this BST. Silently ignore duplicate data.'''

        self.root = _insert_helper(self.root, data)

    def display(self):
        '''Display a representation of this BST to the console.'''

        _print_helper(self.root, "")


def _compare(root, target_root):
    '''Return if all the nodes, after and including the current node, are equal
    in value for both root and target_root.'''

    return (root != None and (root.data == target_root.data) and
            (_compare(root.left, target_root.left)) and
             (_compare(root.right, target_root.right))) or not root


def size(root):
    '''Returns the number of nodes with data in the tree'''

    if not root:
        return 0
    return 1 + size(root.left) + size(root.right)


def is_valid_tree(root, parent=None):
    '''Return if the nodes in the tree correctly refrence the parent node and
    if the BST properties are upheld.'''

    return (root.parent == parent
            and((not root.left or
            (root.left.data > root.data and is_valid_tree(root.left, root))) or
            (not root.right or
            (root.right.data < root.data and is_valid_tree(root.right, root)))
            or (root != None)))


def _insert_helper(node, data):
    '''Insert data into the BST rooted at BSTNode node and return the new BST
    rooted at that node.'''

    if node == None:
        return BTNode(data)
    elif data < node.data:
        node.left = _insert_helper(node.left, data)
        if not node.left.parent:
            node.left.parent = node
        return node
    else:
        node.right = _insert_helper(node.right, data)
        if not node.right.parent:
            node.right.parent = node
        return node


def _print_helper(root, indent):
    '''Print the BST rooted at BSTNode root in inorder order, with str indent
    preceding all lines of output.'''
    if root == None:
        return

    ## Pick a pretty indent.
    new_indent = ""
    if indent == "":
        new_indent = ".. "
    else:
        new_indent = "..." + indent

    _print_helper(root.right, new_indent)
    print(indent + str(root.data))
    _print_helper(root.left, new_indent)


def _reparent(root):
    '''Given the root, returns the root with the correct parent paramets for
    each node.'''

    if root.left:
        root.left.parent = root
        root.left = _reparent(root.left)
    if root.right:
        root.right.parent = root
        root.right = _reparent(root.right)
    return root


def reparent(root):
    '''Given the root, returns the root with the correct parent paramets for
    each node.'''

    root.parent = None
    return _reparent(root)


def rotate_right(game_tree, curr):
    '''Returns the node from game_tree which has been rotated right
    at position curr.'''

    new_curr = curr.left
    curr.left = new_curr.right
    new_curr.right = curr
    game_tree.root = find_and_replace(game_tree.root, curr, new_curr)
    game_tree.root = reparent(game_tree.root)
    return new_curr


def rotate_left(game_tree, curr):
    '''Returns the node from game_tree which has been rotated right
    at position curr.'''

    new_curr = curr.right
    curr.right = new_curr.left
    new_curr.left = curr
    game_tree.root = find_and_replace(game_tree.root, curr, new_curr)
    game_tree.root = reparent(game_tree.root)
    return new_curr


def find_and_replace(root, curr, new_curr):
    '''Returns the tree at node root with the node at curr replaced with the
    node new_curr.'''

    if root == curr:
        return new_curr
    else:
        if curr.data > root.data:
            root.right = find_and_replace(root.right, curr, new_curr)
        else:
            root.left = find_and_replace(root.left, curr, new_curr)
        return root

