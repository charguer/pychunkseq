import echunk
import view
FRONT = __import__('direction').Direction.FRONT
BACK = __import__('direction').Direction.BACK
NO_VERSION = __import__('echunk').NO_VERSION

global K
K = 4

# create a uniquely owned schunk
def create(version):
    return Schunk(echunk.Echunk(version), view.View(), version)

# transform chunk into uniquely owned schunk with version
def of_chunk(chunk, version):
    chunk.version = version
    return Schunk(chunk, view.View(chunk.head, chunk.size()), version)

class Schunk:

    def __init__(self, support = echunk.Echunk(), view = view.View(), version = NO_VERSION):
        self.support = support
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
        assert self.is_aligned(pov) and self.view == self.support.view()
        self.support.push(pov, item)
        return Schunk(self.support, self.support.view(), version)

    def push(self, pov, item, version):
        assert not self.is_full()
        if self.is_uniquely_owned(version):
            return self.push_unique(pov, item, version)
        else:
            return self.push_shared(pov, item, version)

    def pop(self, pov):
        assert not self.is_empty()
        if (pov == FRONT):
            index = self.support.head - self.view.seg_head
            new_head = self.view.seg_head - 1
        elif (pov == BACK):
            index = self.support.head - self.view.seg_head + self.view.seg_size - 1
            new_head = self.view.seg_head
        element = self.support[index]
        new_view = view.View(new_head, self.view.seg_size - 1)
        return (Schunk(self.support, new_view), element)

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

    # corresponds to chunk_of_schunk
    def get_chunk(self, version):
        if self.version() == version:
            # unique owner
            assert self.view == self.support.view()
            return self.support
        else:
            c = self.support.ncopy(self.support.view())
            return c

    def iter(self, pov, fun):
        self.support.iter_view(pov, self.view, fun)

    def print_general(self, print_item):
        self.support.print_view(self.view, print_item)

    def push_front(self, item, version = NO_VERSION):
        return self.push(FRONT, item, version)

    def push_back(self, item, version = NO_VERSION):
        return self.push(BACK, item, version)

    def pop_front(self):
        return self.pop(FRONT)

    def pop_back(self):
        return self.pop(BACK)
