import view
FRONT = __import__('direction').Direction.FRONT
BACK = __import__('direction').Direction.BACK

global K
K = 4

def set_capacity(chunk_capacity):
    global K
    K = chunk_capacity

class ChunkList:

    def __init__(self):
        self.data = []
        self.head = 0 # TODO: necessary?
        self.dir  = 0 # direction (0: front, 1: back)

    def size(self):
        return len(self.data) # O(1)

    def is_empty(self):
        return self.size() == 0

    def is_full(self):
        return self.size() == K

    def push(self, pov, item):
        assert not self.is_full()
        if (pov == FRONT):
            self.data.insert(0, item)
            self.head = (self.head + K - 1) % K
        elif (pov == BACK):
            self.data.append(item)

    def pop(self, pov):
        assert not self.is_empty()
        if (pov == FRONT):
            x = self.data.pop(0)
            self.head = (self.head + 1) % K
        elif (pov == BACK):
            x = self.data.pop()
        return x

    def peek(self, pov):
        assert not self.is_empty()
        if pov == FRONT:
            i = 0
        elif pov == BACK:
            i = self.size() - 1
        return self.data[i]

    def concat(self, c2):
        assert self.size() + c2.size() <= K
        for i in range(c2.size()):
            self.push_back(c2.get_absolute(i))
            c2.clear()

    # get relatif
    def get(self, index):
        return self.data[(self.head + index) % K]

    # get absolu
    def get_absolute(self, index):
        return self.data[index]

    # TODO: refactoring?
    def print_view(self, view, print_item):
        print("[", end = "")
        if self.dir == 0: # direction = front
            for i in range(view.seg_size):
                print_item(self.data[(view.seg_head - self.head + i) % K])
                print(", ", end = "")
        else: # direction = back
            for i in reversed(range(view.seg_size)):
                print_item(self.data[(view.seg_head - self.head + i) % K])
                print(", ", end = "")
        print("]", end = "")

    def print_general(self, print_item):
        self.print_view(view.View(self.head, self.size()), print_item)

    # print content, without '[',']'; used in seq
    # TODO: refactoring?
    def print_content(self, print_item):
        size = self.size()
        if self.dir == 0: # direction = front
            for i in range(size):
                # print_item(self.data[(i + self.head) % K])
                print_item(self.data[i])
                if (i != size - 1):
                    print(", ", end = "")
        else: # direction = back
            for i in reversed(range(size)):
                print_item(self.data[i])
                if (i != 0):
                    print(", ", end = "")

    def clear(self):
        self.data.clear()
        self.head = 0

    # créer une copie (partielle ou complete - size elts) d'un chunk
    def ncopy(self, view):
        new_chunk = ChunkList()
        # copier size elements
        for i in range(view.seg_size):
            new_chunk.push(BACK, self.data[view.seg_head - self.head + i]) # copier item?
            new_chunk.head = self.head
        return new_chunk

    # auxilary function used by seq.rev() (and maybe chunk.rev()?)
    def rev_aux(self, rev_fun):
        self.dir ^= 1
        size = self.size()
        for i in range(size):
            rev_fun(self.data[i])

    # spec de iter(self, pov, fun): 
    # iterate elements in direction pov,
    # and call "fun(x, pov2)" on each element "x"
    # where "pov2" is the direction to use for traversing "x"
    # when it is a chunk in the same direction as pov.
    def iter(self, pov, fun):
        size = self.size()
        # dir = pov.xor(self.dir) 
        # if dir == FRONT
        if (pov == FRONT and self.dir == 0) or (pov == BACK and self.dir == 1):
            for i in range(size):
                # fun(self.data[i], dir)
                fun(self.data[i])
        else:
            for i in reversed(range(size)):
                fun(self.data[i])

    # reverse chunk order
    # TODO: recursive?
    def rev(self):
        # self.rev_aux(lambda c: None)
        self.dir ^= 1
        return self

    def push_front(self, item):
        self.push(FRONT, item)

    def push_back(self, item):
        self.push(BACK, item)

    def pop_front(self):
        self.pop(FRONT)

    def pop_back(self):
        self.pop(BACK)

    def peek_front(self):
        return self.peek(FRONT)

    def peek_back(self):
        return self.peek(BACK)
        