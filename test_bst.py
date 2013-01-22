import unittest
import bst
import scoring


def build_tree(L):
    '''Return the BST made from data in list L inserted in order.'''

    tree = bst.BST()
    for data in L:
        tree.insert(data)

    return tree


class TestBST(unittest.TestCase):

    def test_insert_1(self):
        '''Test inserting one node into a BST; also test size and
        is_valid_tree.'''

        tree = bst.BST()
        tree.insert(5)

        assert tree.root.data == 5, 'tree.data not correct for tree of size 1.'
        assert tree.root.parent == None, 'tree.parent should have been None.'
        assert tree.root.left == None, 'tree.left should have been None.'
        assert tree.root.right == None, 'tree.right should have been None.'
        assert bst.size(tree.root) == 1, 'tree size should be 1.'

        assert bst.is_valid_tree(tree.root), \
            'Valid tree was marked as invalid.'

    def test_insert_2_left(self):
        '''Test inserting two nodes into a BST where the second value is
        inserted into the left of the root; also test size and
        is_valid_tree.'''

        tree = build_tree([5, 3])
        #tree.display()   # Uncomment this to see the tree.

        assert tree.root.data == 5, 'tree.data not correct for tree of size 2.'
        assert tree.root.parent == None, 'tree.parent should have been None.'
        assert tree.root.right == None, 'tree.right should have been None.'

        assert tree.root.left.data == 3, 'tree.left should have been 3.'
        assert tree.root.left.parent == tree.root, \
            "tree.left's parent should be root."

        assert bst.size(tree.root) == 2, 'tree size should be 2.'
        assert bst.size(tree.root.left) == 1, "tree.left's size should be 1."

        assert bst.is_valid_tree(tree.root), \
            'Valid tree was marked as invalid.'

    def test_rotate_left(self):
        '''Test left rotation on the root of a tree.'''

        # A full binary search tree.
        tree = build_tree([4, 2, 1, 3, 6, 5, 7])
        #tree.display()

        # The expected result.
        target_tree = build_tree([6, 4, 2, 1, 3, 5, 7])
        # target_tree.display()

        assert target_tree.root.parent == None, \
            'tree.parent should have been None.'

        assert tree.root.parent == None, 'tree.parent should have been None.'
        assert bst.size(tree.root) == 7, 'tree size should be 7.'
        assert bst.is_valid_tree(tree.root), \
            'Valid tree was marked as invalid.'

        bst.rotate_left(tree, tree.root)
        assert bst.size(tree.root) == 7, 'tree size should be 7.'
        assert bst.is_valid_tree(tree.root), \
            'Valid tree was marked as invalid.'

        assert tree.root.parent == None, 'tree.parent should have been None.'

        # This calls tree.__eq__(target_tree). Cool, huh? You need to write
        # the __eq__ method in class BST to do the tree comparison.
        assert tree == target_tree, '__eq__ did not work properly.'

        # This calls tree.__ne__(target_tree).
        assert not (tree != target_tree), '__ne__ did not work properly.'

    def test_rotate_right(self):
        '''Test left rotation on the root of a tree.'''

        # A full binary search tree.
        tree = build_tree([4, 2, 1, 3, 6, 5, 7])
        old_tree = build_tree([4, 2, 1, 3, 6, 5, 7])
        #tree.display()
        #print ""

        # The expected result.
        target_tree = build_tree([2, 1, 4, 3, 6, 5, 7])
        #target_tree.display()

        assert tree.root.parent == None, 'tree.parent should have been None.'
        assert bst.size(tree.root) == 7, 'tree size should be 7.'
        assert bst.is_valid_tree(tree.root), \
            'Valid tree was marked as invalid.'

        bst.rotate_right(tree, tree.root)
        assert bst.size(tree.root) == 7, 'tree size should be 7.'
        assert bst.is_valid_tree(tree.root), \
            'Valid tree was marked as invalid.'
        assert tree.root.right.data == old_tree.root.data, \
               '''incorrect rotate, tree's new left substree should start with
               4'''
        assert tree.root.data == old_tree.root.left.data, \
               '''incorrect rotate, tree's new root should be 2'''
        assert tree.root.right.left.data == old_tree.root.left.right.data, \
               '''incorrect rotate, tree's new RL shoule be its old LR'''
        #RL is right.left, and LR is left.right

        # This calls tree.__eq__(target_tree). Cool, huh? You need to write
        # the __eq__ method in class BST to do the tree comparison.
        assert tree == target_tree, '__eq__ did not work properly.'

        # This calls tree.__ne__(target_tree).
        assert not (tree != target_tree), '__ne__ did not work properly.'

    def test_rotate_subtree_right(self):
        '''Test left rotation on the root of a tree.'''

        # A full binary search tree.
        tree = build_tree([4, 2, 1, 3, 6, 5, 7])
        old_tree = build_tree([4, 2, 1, 3, 6, 5, 7])
        #tree.display()
        #print ""

        # The expected result.
        target_tree = build_tree([4, 2, 1, 3, 5, 6, 7])
        #target_tree.display()

        assert tree.root.parent == None, 'tree.parent should have been None.'
        assert bst.size(tree.root) == 7, 'tree size should be 7.'
        assert bst.is_valid_tree(tree.root), \
            'Valid tree was marked as invalid.'

        bst.rotate_right(tree, tree.root.right)
        #tree.display()
        assert bst.size(tree.root) == 7, 'tree size should be 7.'
        assert bst.is_valid_tree(tree.root), \
            'Valid tree was marked as invalid.'
        assert tree.root.right.data == old_tree.root.right.left.data, \
               '''incorrect rotate, tree's new right substree should start
               with 5'''
        assert tree.root.data == old_tree.root.data, \
               '''incorrect rotate, tree's root should not have changed'''
        assert tree.root.right.right.right.data == \
               old_tree.root.right.right.data, \
               '''incorrect rotate, subtree's rightmost leaf should not have
               changed'''
        #RL is right.left, and LR is left.right

        # This calls tree.__eq__(target_tree). Cool, huh? You need to write
        # the __eq__ method in class BST to do the tree comparison.
        assert tree == target_tree, '__eq__ did not work properly.'

        # This calls tree.__ne__(target_tree).
        assert not (tree != target_tree), '__ne__ did not work properly.'

    def test_rotate_subtree_left(self):
        '''Test left rotation on the root of a tree.'''

        # A full binary search tree.
        tree = build_tree([4, 2, 1, 3, 6, 5, 7])
        old_tree = build_tree([4, 2, 1, 3, 6, 5, 7])
        #tree.display()
        #print ""

        # The expected result.
        target_tree = build_tree([4, 2, 1, 3, 7, 6, 5])
        #target_tree.display()

        assert tree.root.parent == None, 'tree.parent should have been None.'
        assert bst.size(tree.root) == 7, 'tree size should be 7.'
        assert bst.is_valid_tree(tree.root), \
            'Valid tree was marked as invalid.'

        bst.rotate_left(tree, tree.root.right)

        assert bst.size(tree.root) == 7, 'tree size should be 7.'
        assert bst.is_valid_tree(tree.root), \
            'Valid tree was marked as invalid.'
        assert tree.root.right.data == old_tree.root.right.right.data, \
               '''incorrect rotate, tree's new right substree should start
               with 7'''
        assert tree.root.data == old_tree.root.data, \
               '''incorrect rotate, tree's root should not have changed'''
        assert tree.root.right.left.left.data == \
               old_tree.root.right.left.data, \
               '''incorrect rotate, subtree's leftmost leaf should not have
               changed'''
        #RL is right.left, and LR is left.right

        # This calls tree.__eq__(target_tree). Cool, huh? You need to write
        # the __eq__ method in class BST to do the tree comparison.
        assert tree == target_tree, '__eq__ did not work properly.'

        # This calls tree.__ne__(target_tree).
        assert not (tree != target_tree), '__ne__ did not work properly.'


class TestHighscores(unittest.TestCase):
    '''Tests the functions in the scoring.py file.'''

    def setUp(self):
        self.highscores = scoring.Score('test.txt')
        self.highscores.enter_score(1337)
        self.highscores.enter_score(200)
        self.highscores.insert_score([1337, 'NoobSlayer543'])
        self.highscores.insert_score([8008135, 'MASTERPWN'])
        self.highscores.insert_score([2, 'Tom from MySpace'])

    def tearDown(self):
        myfile = open('test.txt', 'w')
        myfile.write('')
        myfile.close()

    def test_highscore_list(self):
        '''Tests the highscore functions.'''

        temp = self.highscores.score_list

        assert self.highscores.score == 100, 'The score should now be 100'

        assert temp.next.data == [1337, 'NoobSlayer543'],\
               'The entry should be in the middle of the highscore list'
        assert temp.data == [8008135, 'MASTERPWN'],\
               'The entry should have been added to the top of the list'
        assert temp.next.next.data == [2, 'Tom from MySpace'],\
               'The entry should have been added to the bottom of the list'

        self.highscores.write_to_file()
        y = scoring.Score('test.txt')
        y = y.score_list
        #Checks to make sure the highscore list which was exported, was
        #successfully reimported.
        assert temp.data == y.data, \
               'The first element in both lists should be equal'
        assert temp.next.data == y.next.data, \
               'The second element in both lists should be equal'
        assert temp.next.next.data == y.next.next.data, \
               'The third element in both lists should be equal'


if __name__ == '__main__':
    unittest.main()

