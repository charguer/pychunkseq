import view
FRONT = __import__('direction').Direction.FRONT
BACK = __import__('direction').Direction.BACK
NO_VERSION = -1

global K

# TODO: est-il possible d'enlever cette ligne qui risque de poser des problèmes ?
K = 4

def set_capacity(chunk_capacity):
    global K
    K = chunk_capacity
    
# TODO: documenter ici en 5 lignes quels sont les champs utilisés et ce qu'ils représentent.
        
class Echunk:

    def __init__(self, version = NO_VERSION):
        self.data = []
        self.head = 0
        self.dir  = FRONT
        self.version = version

    # TODO: dans le code caml, "version" s'appelle "owner", si tu trouves ça plus clair
    # tu peux changer.

    def size(self):
        return len(self.data) # O(1)

    def is_empty(self):
        return self.size() == 0

    def is_full(self):
        return self.size() == K

    def push(self, pov, item):
        assert not self.is_full()
        if (pov ^ self.dir == FRONT):
            self.data.insert(0, item)
            self.head += 1
        else:
            self.data.append(item)

    def pop(self, pov):
        assert not self.is_empty()
        if (pov ^ self.dir == FRONT):
            x = self.data.pop(0)
            self.head = max(0, self.head - 1)
        else:
            x = self.data.pop()
        return x

    def peek(self, pov):
        assert not self.is_empty()
        if pov ^ self.dir == FRONT:
            i = 0
        else:
            i = self.size() - 1
        return self.data[i]

    def concat(self, c2):
        assert self.size() + c2.size() <= K
        for i in range(c2.size()):
            self.push_back(c2[i])
            c2.clear()

    # get item at index
    def get(self, index):
        assert 0 <= index and index < self.size()
        if self.dir == FRONT:
            return self.data[index]
        else:
            return self.data[self.size() - index - 1]

    # override [] operator
    def __getitem__(self, index):
        return self.get(index)

    def print_view(self, view, print_item):
        def print_fun(item):
            print_item(item)
            print(", ", end="")
        print("[", end="")
        self.iter(FRONT, print_fun, view)
        print("\b\b]") if self.size() != 0 else print("]")
        

    def print_general(self, print_item):
        self.print_view(self.view(), print_item)

    def clear(self):
        self.data.clear()
        self.head = 0

    # partial or complete copy of a chunk using view
    def ncopy(self, view):
        new_chunk = Echunk()
        # TODO: copy function? for types
        for i in range(view.seg_size):
            new_chunk.push_back(self.data[self.head - view.seg_head + i])
            new_chunk.head = view.seg_head
        return new_chunk

    # auxilary function used in seq - gets size of chunk (chunks of chunks)
    def deep_size(self, level):
        if level == 1:
            return self.size()
        else:
            total = 0
            for i in range(self.size()):
                total += self.data[i].deep_size(level-1)
            return total

    # auxilary function used in seq (get from chunk of chunk)
    def get_deep(self, i, level, pov):
        if level == 1:
            assert i < self.size()
            if pov ^ self.dir == FRONT:
                return self.data[i]
            else:
                return self.data[self.size() - i - 1]
        else:
            # TODO: ce code ne fonctionne a priori que si les chunks sont toujours pleins.
            bigindex = i // pow(K, level - 1)
            newindex = i - bigindex * pow(K, level - 1)
            if pov ^ self.dir == BACK:
                bigindex = self.size() - bigindex - 1
            return self.data[bigindex].get_deep(newindex, level-1, pov ^ self.dir)

    # iterate over chunk elements and apply function, view optional
    def iter(self, pov, fun, _view = None):
        if _view is None:
            h = 0
            size = self.size()
        else:
            h = self.head - _view.seg_head
            size = _view.seg_size
        if pov ^ self.dir == FRONT:
            for i in range(size):
                fun(self.data[h + i])
        else:
            for i in reversed(range(size)):
                fun(self.data[h + i])

    # reverse chunk order
    def rev(self):
        self.dir ^= BACK
        return self

    def swap(self, c2):
        tmp_data = self.data
        tmp_head = self.head
        tmp_dir  = self.dir
        self.data = c2.data
        self.head = c2.head
        self.dir  = c2.dir
        c2.data = tmp_data
        c2.head = tmp_head
        c2.dir  = tmp_dir

    # return view on complete echunk
    def view(self):
        return view.View(self.head, self.size())

    def push_front(self, item):
        self.push(FRONT, item)

    def push_back(self, item):
        self.push(BACK, item)

    def pop_front(self):
        return self.pop(FRONT)

    def pop_back(self):
        return self.pop(BACK)

    def peek_front(self):
        return self.peek(FRONT)

    def peek_back(self):
        return self.peek(BACK)
        