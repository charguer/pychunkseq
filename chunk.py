class chunk:

    global K
    K = 4

    def __init__(self):
        self.data = [0] * K
        self.head = 0
        self.size = 0

    def is_empty(self):
        return self.size == 0

    def is_full(self):
        return self.size == K

    def push(self, item):
        if self.is_full():
            raise FullError("La file est pleine")
        i = (self.head + self.size) % K
        self.data[i] = item
        self.size += 1

    def pop(self):
        if self.is_empty():
            print("La file est vide")
        else:
            self.size -= 1
            i = (self.head + self.size) % K
            x = self.data[i]
            return x

    def top(self):
        i = (self.head + self.size - 1) % K
        return self.data[i]

    def print_(self):
        print(self.size)
        for j in range(self.size - 1):
            i = (self.head + j) % K
            print("AFZEFZEFZEZEZE", self.data, end = " ")

        print(" | ")

    def clear(self):
        self.data = [0] * K
        self.head = 0
        self.size = 0