import chunk
import view

global K
K = 4

class Pchunk:

    def __init__(self, support = chunk.chunk(), view = view.View()):
        self.support = support
        self.view = view

    def is_empty(self):
        return self.view.seg_size == 0

    def is_full(self):
        return self.view.seg_size == K

    def push_right(self, item):
        if self.support.is_full():
            # TODO: message d'erreur?
            return

        # si la fin du view correspond à la fin du support càd si support vide après valeurs pointées par view
        if self.view.seg_head + self.view.seg_size == self.support.head + self.support.size:
            # on ajoute la valeur dans le même support
            self.support.push_right(item)
            # mais on crée une nouvelle vue
            new_view = view.View(self.view.seg_head, self.view.seg_size + 1)
            new_pchunk = Pchunk(self.support, new_view)
            return new_pchunk
        else:
            # sinon on doit copier le chunk avec les valeurs qui nous interessent
            new_view = view.View(self.view.seg_head, self.view.seg_size + 1)
            new_support = chunk.chunk()
            new_support.head = self.support.head
            new_support.size = 0
            # copier support
            for i in range(self.view.seg_size):
                new_support.push_right(self.support.data[i + self.support.head]) # copier objet?? deep copy pcq pas tjrs type primitif?
            # push nouveau objet
            new_support.push_right(item)              
            new_pchunk = Pchunk(new_support, new_view)
            return new_pchunk

    def print_general(self, print_item):
        print("[", end = "")
        for j in range(self.view.seg_size):
            i = (self.view.seg_head + j) % K
            print_item(self.support.data[i])
            print(", ", end = "")
        print("]", end = "")