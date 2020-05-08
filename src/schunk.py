import echunk
import view
FRONT = __import__('direction').Direction.FRONT
BACK = __import__('direction').Direction.BACK

global K
K = 4

# create a uniquely owned schunk
def create(version):
    return Schunk(echunk.Echunk(version), view.View())

# transform chunk into uniquely owned schunk with version
def of_chunk(chunk, version):
    chunk.version = version
    return Schunk(chunk, view.View(chunk.head, chunk.size()))

class Schunk:

    def __init__(self, support = echunk.Echunk(), view = view.View()):
        self.support = support
        self.view = view

    def is_empty(self):
        return self.view.seg_size == 0

    def is_full(self):
        return self.view.seg_size == K

    def push_shared(self, pov, item):
        assert not self.is_full()
        if (self.is_aligned(pov) and not self.support.is_full()):
            # if aligned we can use the same support
            new_support = self.support
            # TODO: change version?
        else:
            # else we create a copy of the part of the support we need
            new_support = self.support.ncopy(self.view)
        new_support.push(pov, item)
        if (pov == FRONT):
            new_head = self.view.seg_head + 1
        elif (pov == BACK):
            new_head = self.view.seg_head
        new_view = view.View(new_head, self.view.seg_size + 1)
        return Schunk(new_support, new_view)

    def push_unique(self, pov, item):
        assert not self.is_full() and not self.support.is_full()
        assert self.view == self.support.view()
        self.support.push(pov, item)
        return Schunk(self.support, self.support.view())

    def push(self, pov, item, version = -1):
        if self.version() == version:
            self.push_unique(pov, item)
        else:
            self.push_shared(pov, item)

    def is_aligned(self, pov):
        if (pov == FRONT):
            return self.support.head == self.view.seg_head
        elif (pov == BACK):
            return (self.view.seg_size - self.view.seg_head) == (self.support.size() - self.support.head)

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

    def print_general(self, print_item):
        self.support.print_view(self.view, print_item)

    def push_front(self, item):
        # TODO: replace with push, use versions
        return self.push_shared(FRONT, item)

    def push_back(self, item):
        # TODO: replace with push, use versions
        return self.push_shared(BACK, item)

    def pop_front(self):
        return self.pop(FRONT)

    def pop_back(self):
        return self.pop(BACK)
