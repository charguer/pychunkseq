import chunk_list
FRONT = __import__('direction').Direction.FRONT
BACK = __import__('direction').Direction.BACK
K = __import__('chunk_list').K

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

    # TODO: peek(self,pov)  follow the same structure as pop.
    # TODO: verifier
    def peek_back(self):
        # assert (not self.is_empty())
        # if not self.back.is_empty()
        #    return self.back.peek_back()
        # else
        #    assert self.middle is None or self.middle.is_empty()
        #    return self.front.peek_back()
        return self.back.peek_back()

    def peek_front(self):
    #idem here.
        return self.front.peek_front()

    def populate_sides(self):
        self.populate(FRONT)
        self.populate(BACK)

    # push_back_chunk_middle(self, c)
    #  m = self.middle
    #  if c.is_empty():
    #     return
    #  if m is None:
    #     self.middle = Seq()
    #     m = self.middle
    #  if smiddle.is_empty() or c.size() + m.peek_back().size() > K:
    #     smiddle.push_back(c)
    # ...
    def push_back_chunk_middle(self, smiddle, c):
        if not c.is_empty():
            if smiddle is None or smiddle.is_empty() or c.size() + smiddle.peek_back().size() > K:
                if smiddle is None:
                    smiddle = Seq()
                smiddle.push_back(c)
            else:
                c2 = smiddle.peek_back()
                c2.concat(c)
                # not needed cause peek:  smiddle.push_back(c2)
        return smiddle

    # puts data from s2 to the back of current object, and clears s2
    def concat_back(self, s2):
        s1 = self
        if (s1.is_empty()):
            # s1.swap(s2)
            s1.front = s2.front
            s1.middle = s2.middle
            s1.back = s2.back
            return
        elif (s2.is_empty()):
            return
        else:
            m1 = s1.middle
            m2 = s2.middle
            # s1.front   m1   s1.back    s2.front    m2   s2.back

            # push data to the outside to simplify small cases
            if s1.front.is_empty():
                assert m1 is None or m1.is_empty()
                b = s1.back
                s1.back = s1.front        
                s1.front = b
            if s2.back.is_empty():
                assert m2 is None or m2.is_empty()
                f = s2.front
                s2.front = s2.back
                s2.back = f
            m1 = self.push_back_chunk_middle(m1, s1.back)
            m1 = self.push_back_chunk_middle(m1, s2.front)
            
            if m1 is None or m1.is_empty():
                s1.middle = m2
            elif m2 is not None and not m2.is_empty():
                # m1b = m1.peek_back()
                # m2f = m2.peek_front()
                # if m1b.size() + m2f + size() > K
                m1pbs = 0 if m1.peek_back() == [] else m1.peek_back().size()
                m2pfs = 0 if m2.peek_front() == [] else m2.peek_front().size()
                if m1pbs + m2pfs <= K:
                    p = m2.pop_front() # in fact, p = m2f
                    self.push_back_chunk_middle(m1, p)
                m1.concat_back(m2)
            
            s1.back = s2.back
            # not needed: s1.middle = m1
            s1.populate_sides()
            # TODO s2.front = chunk vide
            s2.middle = None
            # TODO s2.back = chunk vide
                