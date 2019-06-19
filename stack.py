import chunk

"""def set_capacity(chunk_capacity):
    global K
    K = chunk_capacity"""

class stack:

    def __init__(self):
        self.head = chunk.chunk()
        self.tail = None
        self.nb_tail = 0
        self.spare = None

    def push(self, item):
        if self.head.is_full():
            if self.tail == None:
                self.tail = stack()
            self.tail.push(self.head)
            self.nb_tail += 1
            if self.spare != None:
                self.head = self.spare
                self.spare = None
            else:
                self.head = chunk.chunk()
        self.head.push(item)

    def pop(self):
        x = self.head.pop()
        if self.head.is_empty():
            if self.nb_tail > 0:
                self.spare = self.head
                self.head = self.tail.pop()
                self.nb_tail -= 1
        return x

    def print_general(self, print_item):
        def f(c):
            c.print_general(print_item)
            print(" | ", end ="")
        if self.tail != None:
            self.tail.print_general(f)
            print()
        self.head.print_general(print_item)


    def print_(self):
        def f(x):
            print(x, end = "")
        self.print_general(f)
        print("\n=====================")
