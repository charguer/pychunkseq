import pchunk

class Pstack:

    def __init__(self):
        self.head = pchunk.Pchunk()
        self.tail = []

    # TODO: verifier fonctionnement (return self?)
    def push(self, item):
        if self.head.is_full():
            self.tail.append(self.head)
            self.head = pchunk.Pchunk()
        self.head = self.head.push_right(item)
        return self

    # TODO: verifier valeur de retour, (renvoyer elt? persistent?)
    def pop(self):
        self.head = self.head.pop_right()
        if (self.head.is_empty()):
            self.head = self.tail.pop()
        return self

    def print_general(self, print_item):
        print("{", end = "")
        self.head.print_general(print_item)
        for i in self.tail:
            i.print_general(print_item)
            print(", ", end = "")
        print("}")