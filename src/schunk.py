import echunk
import view
FRONT = __import__('direction').Direction.FRONT
BACK = __import__('direction').Direction.BACK
NO_VERSION = __import__('echunk').NO_VERSION

global K

# TODO: retirer ça ?
K = 4

# TODO: utilité de cette fonction ?
# je te propose de déplacer cette fonction dans le module Schunk
# et de l'appeler create_empty.

# create a uniquely owned schunk
def create(version):
    return Schunk(echunk.Echunk(version), view.View(), version)

# transform chunk into uniquely owned schunk with version
# TODO: rename to schunk_of_echunk
# TODO: je me demande s'il est possible de fixer le bon numéro de version
# lors de la création du chunk, et de ne pas avoir besoin de le mettre à jour ici,
# autrement dit, cette fonction n'aurais pas besoin de prendre "version" en argument.
# TODO: utiliser la fonction chunk.view() pour créer la view
def schunk_of_chunk(chunk, version):
    chunk.version = version
    return Schunk(chunk, view.View(chunk.head, chunk.size()), version)

# transfom schunk into chunk
# TODO: rename to echunk_of_schunk
def chunk_of_schunk(s, version):
    if s.version() == version:
        # unique owner
        assert s.view == s.support.view()
        return s.support
    else:
        # TODO: tu peux faire le return direct
        c = s.support.ncopy(s.support.view())
        return c

class Schunk:

    def __init__(self, support = echunk.Echunk(), view = view.View(), version = NO_VERSION):
        self.support = support
        # TODO: idem, je me demande s'il est utile de fixer le numéro de version ici,
        # car si on fournit le support, on peut avoir déjà réglé le bon numéro de version,
        # et si on prend un echunk vide, alors il aura déjà NO_VERSION et c'est ce qu'on veut.
        self.support.version = version
        self.view = view

    def is_empty(self):
        return self.view.seg_size == 0

    def is_full(self):
        return self.view.seg_size == K

    def push_shared(self, pov, item, version):
        assert not self.is_full()
        if (self.is_aligned(pov) and not self.support.is_full()):
            # if aligned we can use the same support
            new_support = self.support
            # TODO: on pourra en parler, mais je crois qu'on n'a pas besoin de 
            # se préoccuper du new_version dans le cas où l'on conserve le chunk 
            # il suffit de faire dès ici un return  Schunk(new_support, new_view),
            # en bougeant plus haut le code de new_view.
            new_version = self.support.version
        else:
            # else we create a copy of the part of the support we need
            new_support = self.support.ncopy(self.view)
            new_version = version
        new_support.push(pov, item)
        if (pov == FRONT):
            new_head = self.view.seg_head + 1
        elif (pov == BACK):
            new_head = self.view.seg_head
        new_view = view.View(new_head, self.view.seg_size + 1)
        return Schunk(new_support, new_view, new_version)

    def push_unique(self, pov, item, version):
        # TODO: si les view sont égales, is_aligned est forcément vrai, 
        # donc tu peux retirer la première partie du test.
        # En fait, la fonction "is_aligned" en caml, c'est celle qui test
        # si self.view == self.support.view(), c'est-à-dire si
        # self.is_aligned(FRONT) and self.is_aligned(BACK),
        # tout ça est équivalent.
        assert self.is_aligned(pov) and self.view == self.support.view()
        self.support.push(pov, item)
        # TODO: ci-dessous, il ne faut pas construire un nouveau schunk, mais faire :
        #   self.view <- self.support.view() 
        #   return self
        return Schunk(self.support, self.support.view(), version)

    def push(self, pov, item, version):
        assert not self.is_full()
        if self.is_uniquely_owned(version):
            return self.push_unique(pov, item, version)
        else:
            return self.push_shared(pov, item, version)

    # TODO: séparer pop_unique et pop_shared comme dans le code caml.
    def pop(self, pov, version):
        assert not self.is_empty()
        if (pov == FRONT):
            index = self.support.head - self.view.seg_head
            new_head = self.view.seg_head - 1
        elif (pov == BACK):
            index = self.support.head - self.view.seg_head + self.view.seg_size - 1
            new_head = self.view.seg_head
        element = self.support[index]
        new_view = view.View(new_head, self.view.seg_size - 1)
        return (Schunk(self.support, new_view, version), element)

    def is_aligned(self, pov):
        if (pov == FRONT):
            return self.support.head == self.view.seg_head
        elif (pov == BACK):
            return (self.view.seg_size - self.view.seg_head) == (self.support.size() - self.support.head)

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
