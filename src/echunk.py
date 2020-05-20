from view import View
FRONT = __import__('direction').Direction.FRONT
BACK = __import__('direction').Direction.BACK
NO_VERSION = -1

global CAPACITY
# TODO: est-il possible d'enlever cette ligne qui risque de poser des problèmes ?
CAPACITY = 4

# Set capacity of chunks
def set_capacity(chunk_capacity):
    global CAPACITY
    CAPACITY = chunk_capacity
    
# Class Echunk:
#   data: list containing chunk elements, limited by CAPACITY
#   head: index of the original first element - used for views
#   dir:  direction of the chunk (FRONT, BACK)
#   version: integer used to keep track of ownership
        
class Echunk:

    # ------------------------------------------------------------------------ #
    # Constructor

    def __init__(self, version = NO_VERSION):
        self.mydata = []
        self.data = []
        self.head = 0
        self.dir  = FRONT
        self.version = version


    # ------------------------------------------------------------------------ #
    # Basic utility functions 

    def size(self):
        return len(self.data) # O(1)

    def is_empty(self):
        return self.size() == 0

    def is_full(self):
        return self.size() == CAPACITY


    # ------------------------------------------------------------------------ #
    # Insert & remove elements
    # TODO: je te suggère une section pour PUSH, une pour POP, et une pour PEEK, ici.
    # TODO: les fonctions push_front, push_back, pop_front et pop_back, et peek..
    #  ne sont pas forcément indispensables, car le client final n'y accède jamais.

    def push(self, pov, item):
        assert not self.is_full()
        if (pov ^ self.dir == FRONT):
            self.data.insert(0, item)
            self.head += 1
        else:
            self.data.append(item)

    def pop(self, pov):
        assert not self.is_empty()
        if (pov ^ self.dir == FRONT):
            x = self.data.pop(0)
            self.head = max(0, self.head - 1)
        else:
            x = self.data.pop()
        return x

    def push_front(self, item):
        self.push(FRONT, item)

    def push_back(self, item):
        self.push(BACK, item)

    def pop_front(self):
        return self.pop(FRONT)

    def pop_back(self):
        return self.pop(BACK)


    # ------------------------------------------------------------------------ #
    # Operations on chunks

    # Concatenate two echunks - add elements of c2 to the back of echunk
    def concat(self, c2):
        assert self.size() + c2.size() <= CAPACITY
        for i in range(c2.size()):
            self.push_back(c2[i])
            c2.clear()

    # Reverse order of elements
    def rev(self):
        self.dir ^= BACK
        return self

    # Iterate over elements and apply function, area can be limited by view
    def iter(self, pov, fun, view = None):
        if view is None:
            h = 0
            size = self.size()
        else:
            h = self.head - view.seg_head
            size = view.seg_size
        if pov ^ self.dir == FRONT:
            for i in range(size):
                fun(self.data[h + i])
        else:
            for i in reversed(range(size)):
                fun(self.data[h + i])

    # Swap data of two echunks
    def swap(self, c2):
        tmp_data = self.data
        tmp_head = self.head
        tmp_dir  = self.dir
        self.data = c2.data
        self.head = c2.head
        self.dir  = c2.dir
        c2.data = tmp_data
        c2.head = tmp_head
        c2.dir  = tmp_dir

    # Clear echunk data
    def clear(self):
        self.data.clear()
        self.head = 0

    # Copy complete echunk or area as defined by view
    def ncopy(self, view):
        new_chunk = Echunk()
        # TODO: copy function? for types
        for i in range(view.seg_size):
            new_chunk.push_back(self.data[self.head - view.seg_head + i])
            new_chunk.head = view.seg_head
        return new_chunk


    # ------------------------------------------------------------------------ #
    # Printing

    # Print entire chunk
    def print_general(self, print_item):
        self.print_view(self.view(), print_item)

    # Print chunk area as defined by view
    def print_view(self, view, print_item, pov = FRONT):
        def print_fun(item):
            print_item(item)
            print(", ", end="")
        print("[", end="")
        self.iter(pov, print_fun, view)
        print("\b\b]") if self.size() != 0 else print("]")


    # ------------------------------------------------------------------------ #
    # Access elements

    # Override [] operator
    def __getitem__(self, index):
        return self.get(index)

    # Get item at index
    def get(self, index):
        assert 0 <= index and index < self.size()
        if self.dir == FRONT:
            return self.data[index]
        else:
            return self.data[self.size() - index - 1]
        
    
    # ------------------------------------------------------------------------ #
    # Auxiliary methods

    # Get view on complete echunk
    def view(self):
        return View(self.head, self.size())

    # Take a peek at the element on the extremity of the echunk (front/back)
    def peek(self, pov):
        assert not self.is_empty()
        if pov ^ self.dir == FRONT:
            i = 0
        else:
            i = self.size() - 1
        return self.data[i]

    def peek_front(self):
        return self.peek(FRONT)

    def peek_back(self):
        return self.peek(BACK)

    # auxilary function used in seq - gets size of chunk (chunks of chunks)
    def deep_size(self, level):
        if level == 1:
            return self.size()
        else:
            total = 0
            for i in range(self.size()):
                total += self.data[i].deep_size(level-1)
            return total

    # auxilary function used in seq (get from chunk of chunk)
    def get_deep(self, i, level, pov):
        if level == 1:
            assert i < self.size()
            if pov ^ self.dir == FRONT:
                return self.data[i]
            else:
                return self.data[self.size() - i - 1]
        else:
            # TODO: ce code ne fonctionne a priori que si les chunks sont toujours pleins.
            bigindex = i // pow(CAPACITY, level - 1)
            newindex = i - bigindex * pow(CAPACITY, level - 1)
            if pov ^ self.dir == BACK:
                bigindex = self.size() - bigindex - 1
            return self.data[bigindex].get_deep(newindex, level-1, pov ^ self.dir)
