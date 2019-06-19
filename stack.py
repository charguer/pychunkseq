import chunk

"""def set_capacity(chunk_capacity):
    global K
    K = chunk_capacity"""

class stack:

    def __init__(self):
        self.head = chunk.chunk()
        self.tail = list()
        self.nb_tail = 0
        self.spare = None

    def push(self, item):
        if self.head.is_full():
            self.tail.append(self.head)
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

    def print_(self):
        #print("stack =", end = " ")
        for i in range(self.nb_tail):
            self.tail[i].print_()
            print(" | ", end = " ")
        self.head.print_()
        print()
