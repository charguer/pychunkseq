import schunk
FRONT = __import__('direction').Direction.FRONT
BACK = __import__('direction').Direction.BACK
NO_VERSION = __import__('schunk').NO_VERSION


class Ssek:
    # class constructor - use class methods to create ssek
    def __init__(self, front, middle, back, version_max):
        self.front = front
        self.back = back
        self.middle = middle
        # TODO: verifier - schunk tjrs créé avec version = NO_VERSION
        self.version_max = version_max

    # class method - create empty ssek
    @classmethod
    def create_empty(cls, version_max = 0):
        front = schunk.Schunk()
        back = schunk.Schunk()
        middle = None
        return cls(front, middle, back, version_max)

    # class method - create ssek with parameters
    @classmethod
    def create(cls, front, middle, back, version_max = 0, pov = FRONT):
        if (pov == FRONT):
            return cls(front, middle, back, version_max)
        else:
            return cls(back, middle, front, version_max)

    @classmethod
    def create_and_populate(cls, this, middle, that, version_max, pov = FRONT):
        if this.is_empty() and middle is not None and not middle.is_empty():
            middle, this = middle.pop(pov ^ FRONT, version_max) 
        if that.is_empty() and middle is not None and not middle.is_empty():
            middle, that = middle.pop(pov ^ BACK, version_max)
        return Ssek.create(this, middle, that, version_max, pov)

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

    def push(self, pov, item, version = NO_VERSION):
        this, that = self.get_both(pov)
        if this.is_full():
            if that.is_empty():
                assert self.middle is None or self.middle.is_empty()
                new_this = that.push(pov, item, version)
                new_that = this
                new_ssek = Ssek.create(new_this, None, new_that, self.version_max, pov)
            else:
                new_this = schunk.Schunk()
                new_this = new_this.push(pov, item, version)
                middle = self.middle
                if middle is None:
                    middle = Ssek.create_empty()
                new_middle = middle.push(pov, this, version)
                new_ssek = Ssek.create(new_this, new_middle, that, self.version_max, pov)
        else:
            new_this = this.push(pov, item, version)
            new_ssek = Ssek.create(new_this, self.middle, that, self.version_max, pov)
        return new_ssek

    def pop(self, pov, version = NO_VERSION):
        assert not self.is_empty()
        this, that = self.get_both(pov)
        if this.is_empty():
            assert self.middle is None or self.middle.is_empty()
            new_that, x = that.pop(pov, version)
            new_ssek = Ssek.create(this, self.middle, new_that, self.version_max, pov)
        else:
            new_this, x = this.pop(pov, version)
            new_ssek = Ssek.create_and_populate(new_this, self.middle, that,
                self.version_max, pov)
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

    def push_front(self, item, version = NO_VERSION):
        return self.push(FRONT, item, version)

    def push_back(self, item, version = NO_VERSION):
        return self.push(BACK, item, version)

    def pop_front(self, version = NO_VERSION):
        return self.pop(FRONT, version)

    def pop_back(self, version = NO_VERSION):
        return self.pop(BACK, version)
