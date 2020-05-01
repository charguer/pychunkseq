import chunk_list
FRONT = __import__('direction').Direction.FRONT
BACK = __import__('direction').Direction.BACK

class Seq:
    
    def __init__(self):
        self.front = chunk_list.ChunkList()
        self.back = chunk_list.ChunkList()
        self.middle = None # appel au constructeur donne boucle infinie
        # self.free_front = chunk_list.ChunkList()
        # self.free_back = chunk_list.ChunkList()

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

    def populate(self, pov):
        this = self.get_this(pov)
        if this.is_empty() and self.middle is not None and not self.middle.is_empty():
            this = self.middle.pop(pov)
            self.set_this(pov, this)

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
                self.set_this(pov, chunk_list.ChunkList())
        this = self.get_this(pov)
        this.push(pov, item)

    def pop(self, pov):
        assert not self.is_empty()
        this, that = self.get_both(pov)
        if this.is_empty():
            assert self.middle is None or self.middle.is_empty()
            x = that.pop(pov)
        else:
            x = this.pop(pov)
            self.populate(pov)
        return x

    # print structure (front middle back)
    def print_debug(self, print_item):
        self.front.print_general(print_item)
        print("")
        if self.middle is not None:
            self.middle.print_general(lambda c: c.print_general(print_item))
            print("")
        else:
            print(".")
        self.back.print_general(print_item)
        print("")

    # general print of container [item1, item2, ..., itemN]
    def print_general(self, print_item):
        print("[", end="")
        self.print_general_aux(print_item)
        print("]")

    # auxiliary function
    def print_general_aux(self, print_item):
        put_comma = False
        if (not self.front.is_empty()):
            self.front.print_content(print_item)
            put_comma = True
            
        if self.middle is not None and not self.middle.is_empty():
            if (put_comma):
                print(", ", end="")
            self.middle.print_general_aux(lambda c: c.print_content(print_item))

        if (not self.back.is_empty()):
            if (put_comma):
                print(", ", end="")
            self.back.print_content(print_item)

    def push_front(self, item):
        self.push(FRONT, item)

    def push_back(self, item):
        self.push(BACK, item)

    def pop_front(self):
        return self.pop(FRONT)

    def pop_back(self):
        return self.pop(BACK)
