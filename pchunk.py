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
        if self.is_full():
            # TODO: message d'erreur?
            return

        # si la fin du view correspond à la fin du support càd si support vide après valeurs pointées par view
        if self.view.seg_head + self.view.seg_size == self.support.head + self.support.size:
        # TODO: ajouter modulo # ajouter la condition "et support pas full"
            # on ajoute la valeur dans le même support
            self.support.push_right(item)
            # mais on crée une nouvelle vue
            new_view = view.View(self.view.seg_head, self.view.seg_size + 1)
            new_pchunk = Pchunk(self.support, new_view)
            # TODO: new_support = self.support
            # TODO: factoriser  new_view = 
            # et returnPchunk(new_support, new_view)
            return new_pchunk
        else:
            # sinon on doit copier le chunk avec les valeurs qui nous interessent
            new_view = view.View(self.view.seg_head, self.view.seg_size + 1)
            new_support = self.support.ncopy(self.view.seg_size) # TODO: passer self.view et copier que là
            new_support.push_right(item)              
            new_pchunk = Pchunk(new_support, new_view)
            return new_pchunk

    def push_left(self, item):
        if self.is_full():
            # TODO: message d'erreur?
            return

        # si la case head - 1 est vide on peut ajouter
        if (self.view.seg_head - 1 - self.support.head) % K <= self.support.size:  # TODO: vérifier head alignés
            self.support.push_left(item)
            new_view = view.View((self.view.seg_head - 1) % K, self.view.seg_size + 1)
            new_pchunk = Pchunk(self.support, new_view)
            return new_pchunk
        else:
            new_view = view.View((self.view.seg_head - 1) % K, self.view.seg_size + 1)
            new_support = self.support.ncopy(self.view.seg_size)
            new_support.push_left(item)
            new_pchunk = Pchunk(new_support, new_view)
            return new_pchunk

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