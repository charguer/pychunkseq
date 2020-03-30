import ctypes
import view

global K
K = 4

def set_capacity(chunk_capacity):
    global K
    K = chunk_capacity

def create_chunk_array():
    global K
    return (K * ctypes.py_object) ()

class chunk:

    def __init__(self):
        self.data = create_chunk_array()
        self.head = 0
        self.size = 0

    def is_empty(self):
        return self.size == 0

    def is_full(self):
        return self.size == K

    def push(self, pov, item):
        if (pov == 'front'):
            i = (self.head + K - 1) % K
            self.head = i
        elif (pov == 'back'):
            i = (self.head + self.size) % K
        self.data[i] = item
        self.size += 1

    def pop(self, pov):
        if (pov == 'front'):
            i = self.head
            self.head = (self.head + 1) % K
        elif (pov == 'back'):
            i = (self.head + self.size - 1) % K
        x = self.data[i]
        self.data[i] = None #writing None is useful to release objects for garbage collection
        self.size -= 1
        return x

    # get relatif
    def get(self, index):
        return self.data[(self.head + index) % K]

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
        self.print_view(view.View(self.head, self.size), print_item)

    def clear(self):
        self.data = [0] * K
        self.head = 0
        self.size = 0

    # créer une copie (partielle ou complete - size elts) d'un chunk
    def ncopy(self, view):
        new_chunk = chunk()
        new_chunk.head = view.seg_head
        new_chunk.size = 0
        # copier size elements
        for i in range(view.seg_size):
            new_chunk.push('back', self.data[(i + view.seg_head) % K]) # copier item?
        return new_chunk