import chunk

class stack:

    global K
    K = 4

    def __init__(self):
        self.head = chunk.chunk()
        self.tail = list()
        self.nb_tail = len(self.tail)

    def push(self, item):
        if self.head.is_full():
            self.tail.append(self.head)
            self.nb_tail += 1
            self.head = chunk.chunk()
        self.head.push(item)

    def pop(self):
        x = self.head.pop()
        if self.head.is_empty():
            if self.nb_tail > 0:
                self.head = self.tail.pop()
                self.nb_tail -= 1
            else:
                pass
        return x

    def print_(self):
        print("stack =", end = ' ')
        for i in range(self.nb_tail):
            self.tail[i].print_()
            print(" | ", end = " ")
        self.head.print_()
        print()
