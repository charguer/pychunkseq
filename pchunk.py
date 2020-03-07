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
        # précondition: pchunk non rempli
        if self.is_full():
            return self
        # on crée la nouvelle vue
        if ((self.view.seg_head + self.view.seg_size) % K) == ((self.support.head + self.support.size) % K) and (not self.support.is_full()):
            # si il y a de la place dans le chunk on peut ajouter l'élément directement
            new_support = self.support
        else:
            # sinon on fait une copie du support
            new_support = self.support.ncopy(self.view)
        # on ajoute l'élément et on renvoie le nouveau pchunk
        new_view = view.View(self.view.seg_head, self.view.seg_size + 1)
        new_support.push_right(item)              
        return Pchunk(new_support, new_view)

    def push_left(self, item):
        # précondition: pchunk non rempli
        if self.is_full():
            return self
        if self.support.head == self.view.seg_head and (not self.support.is_full()):
            # si la case [head - 1] est vide on peut ajouter
            new_support = self.support
        else:
            # sinon on doit copier le support
            new_support = self.support.ncopy(self.view)
        # on ajoute le nouveau élément et on renvoie le résultat
        new_view = view.View((self.view.seg_head - 1) % K, self.view.seg_size + 1)
        new_support.push_left(item)
        return Pchunk(new_support, new_view)

    # TODO: vérifier valeur de retour? (element ou nouveau obj?)
    def pop_right(self):
        if self.is_empty():
            return self
        new_view = view.View(self.view.seg_head, self.view.seg_size - 1)
        new_pchunk = Pchunk(self.support, new_view)
        return new_pchunk # TODO return direct
        # TODO: self.support.get_absolute(self.view.seg_head);
        # TODO return a pair [x;new_pchunk]

    def pop_left(self):
        if self.is_empty():
            return self
        new_view = view.View((self.view.seg_head + 1) % K, self.view.seg_size - 1)
        new_pchunk = Pchunk(self.support, new_view)
        return new_pchunk

    def print_general(self, print_item):
        self.support.print_view(self.view, print_item)