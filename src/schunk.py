from view import View
import echunk
FRONT = __import__('direction').Direction.FRONT
BACK = __import__('direction').Direction.BACK
NO_VERSION = __import__('echunk').NO_VERSION
CAPACITY = __import__('echunk').CAPACITY


# Transform echunk into uniquely owned schunk with version
def schunk_of_echunk(chunk):
    return Schunk(chunk, chunk.view())

# Transfom schunk into echunk
def echunk_of_schunk(s, version):
    if s.is_uniquely_owned(version):
        # unique owner
        assert s.is_aligned()
        return s.support
    else:
        return s.support.ncopy(s.view)

# Class Schunk:
#   support: Echunk containing elements
#   view: (head, size) allowing us to define an area of the support

class Schunk:

    # ------------------------------------------------------------------------ #
    # Constructor

    def __init__(self, support = None, view = None, direction = FRONT):
        self.support = echunk.Echunk() if support is None else support
        self.view = View() if view is None else view
        self.dir = direction


    # ------------------------------------------------------------------------ #
    # Basic utility functions 

    def head(self):
        return self.view.seg_head

    def size(self):
        return self.view.seg_size

    def is_empty(self):
        return self.size() == 0

    def is_full(self):
        return self.size() == CAPACITY


    # ------------------------------------------------------------------------ #
    # Push elements into schunk

    # Push function deciding which function to call depending on ownership
    def push(self, pov, item, version):
        assert not self.is_full()
        if self.is_uniquely_owned(version):
            return self.push_unique(pov, item)
        else:
            return self.push_shared(pov, item, version)

    # Push element if support is shared
    def push_shared(self, pov, item, version):
        # TODO: pas besoin de refaire l'assertion ici je pense,
        # ou alors sinon il faudrait la refaire aussi dans push_unique, par symétrie
        assert not self.is_full()
        if (pov ^ self.dir == FRONT):
            new_head = self.head() + 1
        else:
            new_head = self.head()
        new_view = View(new_head, self.size() + 1)
        if (self.is_aligned(pov) and not self.support.is_full()):
            # if aligned we can use the same support
            new_support = self.support
        else:
            # else we create a copy of the part of the support we need
            new_support = self.support.ncopy(self.view)
        new_support.push(pov ^ self.dir, item)
        return Schunk(new_support, new_view, self.dir)

    # Push element if unique ownership over support echunk
    def push_unique(self, pov, item):
        assert self.is_aligned()
        self.support.push(pov ^ self.dir, item)
        self.view = self.support.view()
        return self

    def push_front(self, item, version = NO_VERSION):
        return self.push(FRONT, item, version)

    def push_back(self, item, version = NO_VERSION):
        return self.push(BACK, item, version)


    # ------------------------------------------------------------------------ #
    # Pop elements from schunk

    # Pop function deciding which function to call depending on ownership
    def pop(self, pov, version):
        assert not self.is_empty()
        if self.is_uniquely_owned(version):
            return self.pop_unique(pov, version)
        else:
            return self.pop_shared(pov, version)

    # Pop element from support with shared ownership
    def pop_shared(self, pov, version):
        assert not self.is_empty()
        h = self.support.head - self.head()
        if (pov ^ self.dir == FRONT):
            index = h
            new_head = self.head() - 1
        else:
            index = h + self.size() - 1
            new_head = self.head()
        x = self.support[index]
        new_view = View(new_head, self.size() - 1)
        return (Schunk(self.support, new_view, self.dir), x)

    # Pop element from support with unique ownership
    def pop_unique(self, pov, version):
        # TODO: verify
        assert self.is_aligned()
        x = self.support.pop(pov ^ self.dir)
        self.view = self.support.view()
        return self, x

    def pop_front(self, version = NO_VERSION):
        return self.pop(FRONT, version)

    def pop_back(self, version = NO_VERSION):
        return self.pop(BACK, version)


    # ------------------------------------------------------------------------ #
    # Operations on schunks

    # Concatenate two schunks - add elements of c2 to the back of schunk
    def concat(self, c2):
        c = self
        assert c.size() + c2.size() <= CAPACITY
        for i in range(c2.size()):
            c = c.push_back(c2[i])
        return c

    # Iterate over schunk and apply given function
    def iter(self, pov, fun):
        self.support.iter(pov ^ self.dir, fun, self.view)
        
    # Reverse order of elements in schunk
    def rev(self):
        return Schunk(self.support, self.view, self.dir ^ BACK)


    # ------------------------------------------------------------------------ #
    # Printing

    def print_general(self, print_item):
        self.support.print_view(self.view, print_item, self.dir)


    # ------------------------------------------------------------------------ #
    # Access elements

    # Override [] operator
    def __getitem__(self, index):
        return self.get(index)

    # Get item at index
    def get(self, index):
        assert 0 <= index and index < self.size()
        h = self.support.head - self.head()
        if (self.dir == FRONT):
            return self.support[h + index]
        else:
            return self.support[h + self.size() - 1 - index]


    # ------------------------------------------------------------------------ #
    # Auxiliary functions

    # Get version from support
    def version(self):
        return self.support.version

    # Check if view is aligned with chunk on a side, or both sides
    def is_aligned(self, pov = None):
        # TODO: c'est assez douteux de faire des opérations avec pov=None,
        # même si peut être que ça marche.
        # je te propose de deux fonctions séparées "is_aligned" et 
        # "is_aligned_side", ça sera bien plus clair.
        # -- pour l'instant j'ai change l'ordre des tests comme hotfix,
        # mais je vais implementer cela apres
        if pov is None:
            return self.view == self.support.view()
        elif (pov ^ self.dir == FRONT):
            return self.support.head == self.head()
        else: # (pov ^ self.dir == BACK):
            view_index = self.size() - self.head()
            supp_index = self.support.size() - self.support.head
            return (view_index == supp_index)

    # Check if schunk is the unique owner of a support echunk
    def is_uniquely_owned(self, version):
        return version != NO_VERSION and self.version() == version

    # Take a peek at the element on the extremity of the echunk (front/back)
    def peek(self, pov):
        assert not self.is_empty()
        if pov == FRONT:
            i = 0
        else:
            i = self.size() - 1
        return self.get(i)

    def peek_front(self):
        return self.peek(FRONT)

    def peek_back(self):
        return self.peek(BACK)
