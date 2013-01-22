class Linked_Node(object):
    """A node in a linked list."""

    def __init__(self, data):
        '''Create a Node containing data with None as next.'''

        self.data = data
        self.prev = None
        self.next = None


class Score():
    '''Keeps score for the player.'''

    def __init__(self, filename):
        '''Initializes the scoring class.'''

        self.filename = filename
        self.score = 0
        self.score_list = self.read_list()

    def enter_score(self, time):
        '''Adds the player's score into the class's score value based on the
        time taken to finish a level.'''

        if time <= 300:
            self.score += 300 - time

    def read_list(self):
        '''Reads the latest highscore list from 'highscore.txt' in a linked
        list format. If no highscore exists, the function returns None.'''

        score_list = []
        old_list = []
        try:
            myfile = open(self.filename)
            old_list_unstriped = myfile.readlines()
            for item in old_list_unstriped:
                old_list.append(item.strip())
            myfile.close()
        except IOError:
            return None
        if old_list:
            linked_scores = insert_linked(None,
                                          ([int(old_list[0]), old_list[1]]))
            for i in range(2, len(old_list), 2):
                linked_scores = insert_linked(linked_scores,
                           [int(old_list[i]), old_list[i + 1]])
            return linked_scores
        return None

    def write_to_file(self):
        '''Writes the current highscore list to 'highscore.txt' and overwrites
        the file if it exists.'''

        myfile = open(self.filename, 'w')
        score_node = self.score_list
        while score_node:
            myfile.write(str(score_node.data[0]) + '\n' + score_node.data[1] +
                         '\n')
            score_node = score_node.next
        myfile.close

    def insert_score(self, user_score):
        '''Replaces the linked list highscore list with a new linked list
        highscore list cotaining user_score.'''

        if self.score_list:
            self.score_list = _insert_score(self.score_list, user_score)
        else:
            self.score_list = insert_linked(None, user_score)


def _insert_score(current_score, user_score):
    '''Return the linked list highscore list with user_score added to it.'''

    if current_score.data[0] < user_score[0]:
        new_node = Linked_Node(user_score)
        new_node.next = current_score
        current_score.prev = new_node
        return new_node
    elif current_score.next:
        if current_score.next.data[0] > user_score[0]:
            current_score.next = _insert_score(current_score.next, user_score)
            return current_score
        else:
            new_node = Linked_Node(user_score)
            new_node.prev = current_score
            new_node.next = current_score.next
            current_score.next = new_node
            current_score.next.prev = new_node
            return current_score
    else:
        current_score.next = Linked_Node(user_score)
        current_score.next.prev = current_score
        return current_score


def insert_linked(head, new_data):
    '''Returns the linked list head with new_data attached at the end.'''

    if head:
        head.next = insert_linked(head.next, new_data)
        head.next.prev = head
        return head
    return Linked_Node(new_data)


def print_highscore_list(head):
    '''Prints the highscore_list contained in the linked list head.'''

    if head == None:
        return "No scores entered."
    while head:
        middle = 80 - 26 - len(head.data[1]) - len(str(head.data[0]))
        print ' ' * 13 + head.data[1] + middle * ' ' + str(head.data[0])
        head = head.next

