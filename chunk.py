global K

def set_capacity(chunk_capacity):
    global K
    K = chunk_capacity

class chunk:

    def __init__(self):
        self.data = [0] * K
        self.head = 0
        self.size = 0

    def is_empty(self):
        return self.size == 0

    def is_full(self):
        return self.size == K

    def push(self, item):
        i = (self.head + self.size) % K
        self.data[i] = item
        self.size += 1

    def pop(self):
        i = (self.head + self.size) % K
        x = self.data[i]
        self.size -= 1
        return x

    def top(self):
        i = (self.head + self.size - 1) % K
        return self.data[i]

    def print_(self):
        for j in range(self.size):
            i = (self.head + j) % K
            print(self.data[i], end = " ")

    def clear(self):
        self.data = [0] * K
        self.head = 0
        self.size = 0