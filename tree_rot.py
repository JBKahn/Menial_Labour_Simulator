import media
import sys
import bst
import time
import scoring
import platform
import os
import pygame
import key_detector as KD


# The width and height of the picture.
WIDTH, HEIGHT = 400, 400

# The number of pixels wide for each node we draw.
NODE_WIDTH = 10

# The number of pixels high for each node we draw.
NODE_HEIGHT = 15

# The number of pixels to leave above the root of the entire tree.
HEIGHT_OFFSET = 20

# The number of pixels to leave to the left of the entire tree.
WIDTH_OFFSET = 20


class Linked_Node(object):
    """A node in a linked list."""

    def __init__(self, data):
        '''Create a Node containing data with None as next.'''
        self.data = data
        self.prev = None
        self.next = None


def draw(pic, root, d, side, curr):
    '''Draw on Picture pic a picture of the tree rooted at BTNode root, which
    appears at depth d in a tree. 'side' is the coordinate that marks the left
    of the tree being drawn, and curr is the currently selected value. Most
    values appear in black; only the value in curr appears in red.'''

    if root != None:
        left_size = bst.size(root.left)

        # the coordinate where the root will be drawn; the root has
        # left_size nodes to the left of it.
        x = side + left_size * NODE_WIDTH

        # The y coordinate of the root value.
        y = d * NODE_HEIGHT

        if curr == root:
            color = media.red
        else:
            color = media.black

        # Draw the current node's value.
        media.add_text(pic, WIDTH_OFFSET + x, HEIGHT_OFFSET + y, \
            str(root.data), color)

        if root.left:
            draw(pic, root.left, d + 1, side, curr)
        if root.right:
            draw(pic, root.right, d + 1, x + NODE_WIDTH, curr)


def random_tree(n):
    '''Return a BST containing n values randomly inserted.'''

    import random
    tree = bst.BST()
    values = range(n)
    random.shuffle(values)
    for i in values:
        tree.insert(i)
    return tree


def process_user_command(game_tree, target_tree, curr, pic):
    '''Read and process one command from the user, modifying BTNode game_tree
    and current BTNode curr as appropriate and redrawing the new game_tree and
    BTNode target_tree on Picture pic.  Return the new value of curr.'''

    d = {'Left': 'l', 'Right': 'r', 'Up': 'u', 'a': 'L', 's': 'R', 'q': 'q'}
    cmd = d.get(KD.moving_by_keys().key, 'm')

    # Only listen to valid commands.
    if len(cmd) != 1 or cmd[0] not in 'qulrLR':
        return curr

    # Erase the old tree and redraw target_tree halfway across the window.
    media.add_rect_filled(pic, 0, 0, WIDTH, HEIGHT, media.white)
    draw(pic, target_tree.root, 0, WIDTH / 2, curr)

    # Process user commands.
    if cmd == 'q':
        media.close(pic)
        sys.exit(0)
    elif cmd == 'u' and curr != None and curr.parent != None:
        curr = curr.parent
    elif cmd == 'l' and curr.left != None:
        curr = curr.left
    elif cmd == 'r' and curr.right != None:
        curr = curr.right
    elif cmd == 'L' and curr.right != None:
        curr = bst.rotate_left(game_tree, curr)
    elif cmd == 'R' and curr.left != None:
        curr = bst.rotate_right(game_tree, curr)

    # The parent attribute of the nodes of the new tree must be corrected.
    # If curr is at the top, a rotation may have moved it there. Set the
    # game_tree root to curr if that happened.

    if curr.parent == None:
        game_tree.root = curr

    # Draw the new game tree.
    draw(pic, game_tree.root, 0, 0, curr)
    media.update(pic)

    return curr


def play_game(tree_size):
    '''Play the rotation game with tree_size nodes in the tree.'''

    # Blank the screen and make the trees.
    media.add_rect_filled(pic, 0, 0, 400, 400, media.white)
    game_tree = random_tree(tree_size)
    target_tree = random_tree(tree_size)

    # Draw the new trees; the current node is initially the root.
    curr = game_tree.root
    draw(pic, game_tree.root, 0, 0, curr)
    draw(pic, target_tree.root, 0, WIDTH / 2, curr)
    media.show(pic)

    # Ask for user operations until the game tree and target tree are the
    # same.
    while game_tree != target_tree:
        curr = process_user_command(game_tree, target_tree, curr, pic)
        assert bst.is_valid_tree(game_tree.root)


def clear():
    '''Clears the terminal window.'''
    #Code copied from ubuntu help forums

    if platform.system() in ('Windows', 'Microsoft'):
        os.system('cls')
    else:
        os.system('clear')


def print_title():
    '''Prints the title screen of the game found in 'title.txt'.'''

    title_screen = open('title.txt')
    for line in title_screen:
        print line.strip('\n')
    title_screen.close()


def play_sound_clip(sound_clip, loop=False):
    '''Plays the sound clip sound_clip with an option to loop the music.'''

    pygame.mixer.init()
    pygame.mixer.music.load(sound_clip)
    pygame.mixer.music.set_volume(.1113)
    if loop:
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.play()

if __name__ == '__main__':

    pic = media.create_picture(WIDTH, HEIGHT)
    highscore = scoring.Score('highscore.txt')

    # Play the game as long as the user wants, adding one to the number of
    # nodes every round.

    print_title()
    play_sound_clip('intro.mp3')
    #Obtained intro music from the tron video game.
    name = raw_input('What is your name? ')
    #clear()
    print "Hello %s and welcome to the menial labour simulator" % (name)
    print '''
    The rules are simple:
    Rotate the nodes in the tree to recreate the target tree. There are eight
    levels, each with one more node then the last, and your score per level
    will be calculated based on how much the level takes to complete. You are
    only awarded points for finishing a level in under five minutes. Your score
    will be reccorded and entered into the high score list below.
    The controls are: Right, Left, Up, a  to Rotate Counter Clockwise, s to
    Rotate Clockwise, q quit.
    When the level has been solved, push y to contine and n to quit.'''
    scoring.print_highscore_list(highscore.score_list)
    raw_input("enter a key to begin: ")

    tree_size = 2
    cont = 'y'
    while cont == 'y':
        start = time.time()
        play_game(tree_size)
        end = time.time() - start
        highscore.enter_score(end)
        if tree_size < 8:
            print ("Congrats!  You finished tree size " + \
            str(tree_size) + ".  Continue (y/n)? ")
            cont = KD.moving_by_keys().key
            while cont != 'y' and cont != 'n':
                cont = KD.moving_by_keys().key
            #clear()
        else:
            #clear()
            print '''Congrats! You finished level 8 and have completed the game
            and scored a vlue of %i.''' % (int(highscore.score))
            highscore.insert_score([int(highscore.score), name])
            highscore.write_to_file()
            cont = 'n'
        tree_size += 1
    scoring.print_highscore_list(highscore.score_list)
    raw_input("Press enter to exit.")
    media.close(pic)

