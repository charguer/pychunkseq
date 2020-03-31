import chunk
FRONT = __import__('direction').Direction.FRONT
BACK = __import__('direction').Direction.BACK

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
        if (pov == FRONT):
            return self.front
        elif (pov == BACK):
            return self.back

    def get_both(self, pov):
        if (pov == FRONT):
            return self.front, self.back
        elif (pov == BACK):
            return self.back, self.front

    def set_this(self, pov, this):
        if (pov == FRONT):
            self.front = this
        elif (pov == BACK):
            self.back = this

    def set_both(self, pov, this, that):
        if (pov == FRONT):
            self.front = this
            self.back = that
        elif (pov == BACK):
            self.front = that
            self.back = this

    # TODO: ajouter le if ici - doit ê appelé et fix si besoin
    def populate(self, pov):
        # TODO: factoriser avec set_this get_this
        if (pov == FRONT):
            assert self.front.is_empty()
            self.front = self.middle.pop(pov)
        elif (pov == BACK):
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
            if this.is_empty(): # TODO remove if and put in populate
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

    def push_front(self, item):
        self.push(FRONT, item)

    def push_back(self, item):
        self.push(BACK, item)

    def pop_front(self):
        self.pop(FRONT)

    def pop_back(self):
        self.pop(BACK)
