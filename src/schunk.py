import echunk
import view
FRONT = __import__('direction').Direction.FRONT
BACK = __import__('direction').Direction.BACK
NO_VERSION = __import__('echunk').NO_VERSION

global K

# TODO: retirer ça ?
K = 4

# transform chunk into uniquely owned schunk with version
# TODO: je me demande s'il est possible de fixer le bon numéro de version
# lors de la création du chunk, et de ne pas avoir besoin de le mettre à jour ici,
# autrement dit, cette fonction n'aurais pas besoin de prendre "version" en argument.
def schunk_of_echunk(chunk, version):
    chunk.version = version
    return Schunk(chunk, chunk.view(), version)

# transfom schunk into chunk
def echunk_of_schunk(s, version):
    if s.version() == version:
        # unique owner
        assert s.is_aligned()
        return s.support
    else:
        return s.support.ncopy(s.support.view())

class Schunk:

    def __init__(self, support = None, _view = None, version = NO_VERSION):
        self.support = echunk.Echunk() if support is None else support
        # TODO: idem, je me demande s'il est utile de fixer le numéro de version ici,
        # car si on fournit le support, on peut avoir déjà réglé le bon numéro de version,
        # et si on prend un echunk vide, alors il aura déjà NO_VERSION et c'est ce qu'on veut.
        self.support.version = version
        self.view = view.View() if _view is None else _view

    def is_empty(self):
        return self.view.seg_size == 0

    def is_full(self):
        return self.view.seg_size == K

    def push_shared(self, pov, item, version):
        assert not self.is_full()
        if (pov == FRONT):
            new_head = self.view.seg_head + 1
        elif (pov == BACK):
            new_head = self.view.seg_head
        new_view = view.View(new_head, self.view.seg_size + 1)
        if (self.is_aligned(pov) and not self.support.is_full()):
            # if aligned we can use the same support
            new_support = self.support
        else:
            # else we create a copy of the part of the support we need
            new_support = self.support.ncopy(self.view)
        new_support.push(pov, item)
        return Schunk(new_support, new_view)

    def push_unique(self, pov, item):
        assert self.is_aligned()
        self.support.push(pov, item)
        self.view = self.support.view()
        return self

    def push(self, pov, item, version):
        assert not self.is_full()
        if self.is_uniquely_owned(version):
            return self.push_unique(pov, item)
        else:
            return self.push_shared(pov, item, version)

    def pop_shared(self, pov, version):
        assert not self.is_empty()
        if (pov == FRONT):
            index = self.support.head - self.view.seg_head
            new_head = self.view.seg_head - 1
        elif (pov == BACK):
            index = self.support.head - self.view.seg_head + self.view.seg_size - 1
            new_head = self.view.seg_head
        x = self.support[index]
        new_view = view.View(new_head, self.view.seg_size - 1)
        return (Schunk(self.support, new_view, version), x)

    # TODO: verify
    def pop_unique(self, pov, version):
        assert self.is_aligned()
        x = self.support.pop(pov)
        self.view = self.support.view()
        return self, x

    def pop(self, pov, version):
        assert not self.is_empty()
        if self.is_uniquely_owned(version):
            return self.pop_unique(pov, version)
        else:
            return self.pop_shared(pov, version)

    def is_aligned(self, pov = None):
        if (pov == FRONT):
            return self.support.head == self.view.seg_head
        elif (pov == BACK):
            return (self.view.seg_size - self.view.seg_head) == (self.support.size() - self.support.head)
        else:
            return self.view == self.support.view()

    def is_uniquely_owned(self, version):
        return version != NO_VERSION and self.version() == version

    # get version (of support)
    def version(self):
        return self.support.version

    def iter(self, pov, fun):
        self.support.iter_view(pov, self.view, fun)

    def print_general(self, print_item):
        self.support.print_view(self.view, print_item)

    def push_front(self, item, version = NO_VERSION):
        return self.push(FRONT, item, version)

    def push_back(self, item, version = NO_VERSION):
        return self.push(BACK, item, version)

    def pop_front(self, version = NO_VERSION):
        return self.pop(FRONT, version)

    def pop_back(self, version = NO_VERSION):
        return self.pop(BACK, version)
