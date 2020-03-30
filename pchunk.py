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

    def push_back(self, item):
        assert not self.is_full()
        # on crée la nouvelle vue
        if ((self.view.seg_head + self.view.seg_size) % K) == ((self.support.head + self.support.size) % K) and (not self.support.is_full()):
            # si il y a de la place dans le chunk on peut ajouter l'élément directement
            new_support = self.support
        else:
            # sinon on fait une copie du support
            new_support = self.support.ncopy(self.view)
        # on ajoute l'élément et on renvoie le nouveau pchunk
        new_view = view.View(self.view.seg_head, self.view.seg_size + 1)
        new_support.push('back', item)              
        return Pchunk(new_support, new_view)

    def push_front(self, item):
        assert not self.is_full()
        if self.support.head == self.view.seg_head and (not self.support.is_full()):
            # si la case [head - 1] est vide on peut ajouter
            new_support = self.support
        else:
            # sinon on doit copier le support
            new_support = self.support.ncopy(self.view)
        # on ajoute le nouveau élément et on renvoie le résultat
        new_view = view.View((self.view.seg_head - 1) % K, self.view.seg_size + 1)
        new_support.push('front', item)
        return Pchunk(new_support, new_view)

    def pop_back(self):
        if self.is_empty():
            return (self, None)
        element = self.support.get_absolute((self.view.seg_head + self.view.seg_size - 1) % K)
        new_view = view.View(self.view.seg_head, self.view.seg_size - 1)
        return (Pchunk(self.support, new_view), element)

    def pop_front(self):
        if self.is_empty():
            return (self, None)
        element = self.support.get_absolute(self.view.seg_head)
        new_view = view.View((self.view.seg_head + 1) % K, self.view.seg_size - 1)
        return (Pchunk(self.support, new_view), element)

    def print_general(self, print_item):
        self.support.print_view(self.view, print_item)