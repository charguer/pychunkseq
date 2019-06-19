import ctypes

global K

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

    def push(self, item):
        i = self.size
        self.data[i] = item
        self.size += 1

    def pop(self):
        self.size -= 1
        i = self.size
        x = self.data[i]
        self.data[i] = None #writing None is useful to release objects for garbage collection
        return x

    def top(self):
        i = self.size - 1
        return self.data[i]

    def print_(self):
        for j in range(self.size):
            i = j
            print(self.data[i], end = " ")

    def print_general(self, print_item):
        print("[", end = "")
        for j in range(self.size):
            i = j
            print_item(self.data[i])
            print(", ", end = "")
        print("]", end = "")

    def clear(self):
        self.data = [0] * K
        self.head = 0
        self.size = 0