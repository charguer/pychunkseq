import ctypes

class dynamic_array:

    def __init__(self): #create an empty array
        self.n = 0
        self.capacity = 1
        self.tab = self.make_array(self.capacity)

    def make_array(self, c ): #return new array with capacity c
        return (c * ctypes.py_object) ()

    def len(self):
        return self.n

    def get_item(self, k):
        if not 0 <= k < self.n:
            raise IndexError("invalid index")
        return self.tab[k]

    def resize(self, c):
        new_array = self.make_array(c)
        for k in range(self.n):
            new_array[k] = self.tab[k]
        self.tab = new_array
        self.capacity = c

    def push(self, obj):
        if self.n == self.capacity:
            self.resize(2 * self.capacity)
        self.tab[self.n] = obj
        self.n += 1

    def pop(self):
        if self.n == 0:
            raise IndexError("empty array")
        x = self.tab[self.n - 1]
        self.tab[self.n - 1] = None
        return x

    def print_(self):
        for k in range(self.n):
            pass
