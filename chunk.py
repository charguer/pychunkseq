import ctypes

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

    def push_right(self, item):
        i = (self.head + self.size) % K
        self.data[i] = item
        self.size += 1

    def push_left(self, item):
        i = (self.head + K - 1) % K
        self.head = i
        self.data[i] = item
        self.size += 1

    def pop_right(self):
        i = (self.head + self.size - 1) % K
        self.size -= 1
        x = self.data[i]
        self.data[i] = None #writing None is useful to release objects for garbage collection
        return x

    def pop_left(self):
        i = self.head
        x = self.data[i]
        self.data[i] = None
        self.size -= 1
        self.head = (self.head + 1) % K
        return x

    def print_general(self, print_item):
        print("[", end = "")
        for j in range(self.size):
            i = (self.head + j) % K
            print_item(self.data[i])
            print(", ", end = "")
        print("]", end = "")

    def clear(self):
        self.data = [0] * K
        self.head = 0
        self.size = 0