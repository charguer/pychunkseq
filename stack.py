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
            self.head.clear()
        self.head.push(item)

    def pop(self):
        self.head.pop()
        if self.head.is_empty():
            if self.nb_tail > 0:
                self.head.data = self.tail[self.nb_tail - 1]
                self.head.size = K
                self.tail.pop()
                self.nb_tail -= 1
            else:
                print("Tail et Head sont vides")


    def print_(self):
        for i in range(self.nb_tail):
            print(type(self.tail[i]), self.tail[i].data)
        self.head.print_()
