import schunk
FRONT = __import__('direction').Direction.FRONT
BACK = __import__('direction').Direction.BACK

def create(pov, this, middle, that, version_max):
    if pov == FRONT:
        return Ssek(this, middle, that, version_max)
    else:
        return Ssek(that, middle, this, version_max)

def create_and_populate(pov, this, middle, that, version_max):
    if this.is_empty() and middle is not None and not middle.is_empty():
        middle, this = middle.pop(pov, version_max)
    if that.is_empty() and middle is not None and not middle.is_empty():
        middle, that = middle.pop(pov ^ BACK, version_max)
    return create(pov, this, middle, that, version_max)


class Ssek:

    def __init__(self, front = None, middle = None, back = None, version_max = 0):
        self.version_max = version_max
        self.front = schunk.create(version_max) if front == None else front
        self.back = schunk.create(version_max) if back == None else back
        self.middle = middle

    def is_empty(self):
        return self.front.is_empty() and self.back.is_empty()

    def get_this(self, pov):
        if (pov == FRONT):
            return self.front
        elif (pov == BACK):
            return self.back

    def get_both(self, pov):
        if (pov == FRONT):
            return self.front, self.back
        elif (pov == BACK):
            return self.back, self.front

    def set_both(self, pov, this, that):
        if (pov == FRONT):
            self.front = this
            self.back = that
        else:
            self.front = that
            self.back = this

    def push(self, pov, item, version):
        this, that = self.get_both(pov)
        if this.is_full():
            if that.is_empty():
                assert self.middle is None or self.middle.is_empty()
                new_this = that.push(pov, item, version)
                new_ssek = Ssek()   # TODO: avoid allocating if replacing
                new_ssek.set_both(pov, new_this, this)
            else:
                new_this = schunk.create(version)
                new_this = new_this.push(pov, item, version)
                if self.middle is None:
                    self.middle = Ssek()
                new_middle = self.middle.push(pov, this, version)
                new_ssek = Ssek()   # TODO: avoid allocating if replacing
                new_ssek.set_both(pov, new_this, that)
                new_ssek.middle = new_middle
        else:
            new_this = this.push(pov, item, version)
            new_ssek = Ssek()
            new_ssek.set_both(pov, new_this, that)
            new_ssek.middle = self.middle
        return new_ssek

    
    def pop(self, pov, version):
        assert not self.is_empty()
        this, that = self.get_both(pov)
        if this.is_empty():
            assert self.middle is None or self.middle.is_empty()
            new_that, x = that.pop(pov)
            new_ssek = create(pov, this, self.middle, new_that, self.version_max)
        else:
            new_this, x = this.pop(pov)
            new_ssek = create_and_populate(pov, new_this, self.middle, that,
                self.version_max)
        return new_ssek, x

    # iterate over ssek and apply function
    def iter(self, pov, fun):
        this, that = self.get_both(pov)
        this.iter(pov, fun)
        if self.middle is not None:
            self.middle.iter(pov, lambda c: c.iter(pov ^ this.support.dir, fun))
        that.iter(pov, fun)

    # print ssek using print_item
    def print_general(self, print_item):
        def print_fun(item):
            print_item(item)
            print(", ", end="")
        print("[", end="")
        self.iter(FRONT, print_fun)
        if self.is_empty():
            print("]")
        else:
            print("\b\b]")

    def push_front(self, item, version):
        return self.push(FRONT, item, version)

    def push_back(self, item, version):
        return self.push(FRONT, item, version)

    def pop_front(self, version):
        return self.pop(FRONT, version)

    def pop_back(self, version):
        return self.pop(BACK, version)
