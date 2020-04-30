import view
FRONT = __import__('direction').Direction.FRONT
BACK = __import__('direction').Direction.BACK
K = 4

class ChunkList:

    def __init__(self):
        self.data = []
        self.head = 0 # TODO: necessary?

    def is_empty(self):
        return len(self.data) == 0

    def is_full(self):
        return len(self.data) == K

    def push(self, pov, item):
        if (pov == FRONT):
            self.data.insert(0, item)
        elif (pov == BACK):
            self.data.append(item)

    def pop(self, pov):
        if (pov == FRONT):
            x = self.data.pop(0)
        elif (pov == BACK):
            x = self.data.pop()
        return x

    # get absolu
    def get_absolute(self, index):
        return self.data[index]

    def print_view(self, view, print_item):
        print("[", end = "")
        for i in range(view.seg_size):
            print_item(self.data[(i + view.seg_head) % K])
            print(", ", end = "")
        print("]", end = "")

    def print_general(self, print_item):
        self.print_view(view.View(0, len(self.data)), print_item)

    # print content, without []; used in seq
    def print_content(self, print_item):
        size = len(self.data)
        for i in range(size):
            # print_item(self.data[(i + self.head) % K])
            print_item(self.data[(i) % K])
            if (i != size - 1):
                print(", ", end = "")

    def clear(self):
        self.data.clear()

    # créer une copie (partielle ou complete - size elts) d'un chunk
    def ncopy(self, view):
        new_chunk = ChunkList()
        # copier size elements
        for i in range(view.seg_size):
            new_chunk.push(BACK, self.data[(i) % K]) # copier item?
        return new_chunk

    def push_front(self, item):
        self.push(FRONT, item)

    def push_back(self, item):
        self.push(BACK, item)

    def pop_front(self):
        self.pop(FRONT)

    def pop_back(self):
        self.pop(BACK)