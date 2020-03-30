import chunk

class Seq:
    
    def __init__(self):
        self.front = chunk.chunk()
        self.back = chunk.chunk()
        self.middle = None # appel au constructeur donne boucle infinie
        # self.free_front = chunk.chunk()
        # self.free_back = chunk.chunk()

    def is_empty(self):
        return self.front.is_empty() and self.back.is_empty()

    def get_this(self, pov):
        if (pov == 'front'):
            return self.front
        elif (pov == 'back'):
            return self.back

    def get_both(self, pov):
        if (pov == 'front'):
            return self.front, self.back
        elif (pov == 'back'):
            return self.back, self.front

    def set_this(self, pov, this):
        if (pov == 'front'):
            self.front = this
        elif (pov == 'back'):
            self.back = this

    def set_both(self, pov, this, that):
        if (pov == 'front'):
            self.front = this
            self.back = that
        elif (pov == 'back'):
            self.front = that
            self.back = this

    def populate(self, pov):
        if (pov == 'front'):
            assert self.front.is_empty()
            self.front = self.middle.pop(pov)
        elif (pov == 'back'):
            assert self.back.is_empty()
            self.back = self.middle.pop(pov)

    def push(self, pov, item):
        this, that = self.get_both(pov)
        if this.is_full():
            if that.is_empty():
                assert(self.middle is None or self.middle.is_empty())
                self.set_both(pov, that, this)
            else:
                if self.middle is None:
                    self.middle = Seq()
                self.middle.push(pov, this)
                self.set_this(pov, chunk.chunk())
        this = self.get_this(pov)
        this.push(pov, item)

    def pop(self, pov):
        assert not self.is_empty()
        this, that = self.get_both(pov)
        if this.is_empty():
            assert self.middle.is_empty()
            x = that.pop(pov)
        else:
            x = this.pop(pov)
            if this.is_empty():
                self.populate(pov)
        return x

    # TODO: fix print si on est dans middle
    def print_general(self, print_item):
        self.front.print_general(print_item)
        print("")
        if self.middle is not None:
            self.middle.print_general(lambda c: c.print_general(print_item))
            print("")
        else:
            print(".")
        self.back.print_general(print_item)
