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

    def push(self, pov, item):
        assert not self.is_full()
        if (self.is_aligned(pov)):
            new_support = self.support # if aligned we can use the same support
        else:
            new_support = self.support.ncopy(self.view)
        new_support.push(pov, item)
        if (pov == 'front'):
            new_view = view.View((self.view.seg_head - 1) % K, self.view.seg_size + 1)
        elif (pov == 'back'):
            new_view = view.View(self.view.seg_head, self.view.seg_size + 1)
        return Pchunk(new_support, new_view)

    def is_aligned(self, pov):
        if (pov == 'front'):
            return self.support.head == self.view.seg_head and (not self.support.is_full())
        elif (pov == 'back'):
            return ((self.view.seg_head + self.view.seg_size) % K) == ((self.support.head + self.support.size) % K) and (not self.support.is_full())

    def pop(self, pov):
        assert not self.is_empty()
        if (pov == 'front'):
            element = self.support.get_absolute(self.view.seg_head)
            new_view = view.View((self.view.seg_head + 1) % K, self.view.seg_size - 1)
        elif (pov == 'back'):
            element = self.support.get_absolute((self.view.seg_head + self.view.seg_size - 1) % K)
            new_view = view.View(self.view.seg_head, self.view.seg_size - 1)
        return (Pchunk(self.support, new_view), element)

    def print_general(self, print_item):
        self.support.print_view(self.view, print_item)