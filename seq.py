import chunk

class Seq:
    
    def __init__(self):
        self.front = chunk.chunk()
        self.back = chunk.chunk()
        self.middle = None # appel au constructeur donne boucle infinie
        # self.free_front = chunk.chunk()
        # self.free_back = chunk.chunk()

    def is_empty(self):
        return self.front.is_empty() and self.back.is_empty() and (self.middle is None or self.middle.is_empty())

    def push_front(self, item):
        if self.front.is_full():
            if self.back.is_empty():
                if (self.middle is not None or not self.middle.is_empty()): # TODO: assert
                    # erreur: conditions non respectées
                    return self
                else:
                    f = self.front
                    self.front = self.back
                    self.back = f
            else:
                if self.middle is None:
                    self.middle = Seq()
                self.middle.push_front(self.front)
                self.front = chunk.chunk() # TODO: utiliser free_front
        self.front.push('front', item)

    # TODO: fix print si on est dans middle
    def print_general(self, print_item):
        print("front = ", end="")
        self.front.print_general(print_item)
        if self.middle is None:
            print("middle = None")
        else:
            print("middle =", end="")
            self.middle.print_general(chunk.chunk.print_general)
        print("back = ", end="")
        self.back.print_general(print_item)
