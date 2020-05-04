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

    def peek(self, pov):
        assert not self.is_empty()
        this, that = self.get_both(pov)
        if not this.is_empty():
            return this.peek(pov)
        else:
            assert self.middle is None or self.middle.is_empty()
            return that.peek(pov)

    def populate_sides(self):
        self.populate(FRONT)
        self.populate(BACK)

    def push_back_chunk_middle(self, c):
        m = self.middle
        if c.is_empty():
            return
        if m is None:
            self.middle = Seq()
            m = self.middle

        if m.is_empty() or c.size() + m.peek_back().size() > K:
            m.push_back(c)
        else:
            c2 = m.peek_back()
            c2.concat(c)

    def swap(self, s2):
        s1 = self
        # save s1 to tmp
        s1_front  = s1.front 
        s1_middle = s1.middle
        s1_back   = s1.back
        # move from s2 to s1
        s1.front  = s2.front
        s1.middle = s2.middle
        s1.back   = s2.back
        # move from tmp to s2
        s2.front  = s1_front
        s2.middle = s1_middle
        s2.back   = s1_back

    # auxilary function - use rev() instead
    def rev_aux(self, rev_fun):
        # TODO: can be refactored if return self in .rev() or chunk.swap()?
        # swap front and back
        tmp_front = self.front
        self.front = self.back
        self.back = tmp_front

        # reverse front & back chunks and their chunks
        self.front.rev_aux(rev_fun)
        self.back.rev_aux(rev_fun)
        
        # recursive
        if self.middle is not None and not self.middle.is_empty():
            # self.middle.rev_aux(lambda c: rev_fun(c.rev()))
            self.middle.rev_aux(lambda c: c.rev_aux(rev_fun))

    # iterate over elements and apply function fun
    # TODO: passing pov to fun
    def iter(self, pov, fun):
        this, that = self.get_both(pov)
        if not this.is_empty():
            this.iter(pov, fun)
        if self.middle is not None and not self.middle.is_empty():
            self.middle.iter(pov, lambda c: c.iter(pov, fun))
        if not that.is_empty():
            that.iter(pov, fun)

    # def iter(self, pov, fun)
    #   this.iter(pov, lambda c dir: fun c)
    #   if self.middle is not None
    #      self.middle.iter(pov, lambda c dir: c.iter(pov.xor(dir), fun))
    #   that.iter(pov, lambda c dir: fun c)

    # to test iter on a sequence of integers:
    # total = 0
    # def f(x):
    #   total += x
    # s.iter(FRONT, f)

    # puts data from s2 to the back of current object, and clears s2
    def concat_back(self, s2):
        s1 = self
        if (s1.is_empty()):
            s1.swap(s2)
            return
        elif (s2.is_empty()):
            return
        else:
            m1 = s1.middle
            m2 = s2.middle

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

            # push s1.back and s2.front into s1.middle
            s1.push_back_chunk_middle(s1.back)
            s1.push_back_chunk_middle(s2.front)
            m1 = s1.middle # because m1 != s1.middle
            
            # if m1 is empty replace with m2
            if m1 is None or m1.is_empty():
                s1.middle = m2
            # else concatenate m1 and m2
            elif m2 is not None and not m2.is_empty():
                if m1.peek_back().size() + m2.peek_front().size() <= K:
                    p = m2.pop_front() # in fact, p = m2f
                    s1.push_back_chunk_middle(p)
                    m1 = s1.middle # TODO: necessary? same case as above?
                m1.concat_back(m2)
            
            # place s2 back into s1.back & populate
            s1.back = s2.back
            s1.populate_sides()

            # clear s2
            s2.front = chunk_list.ChunkList()
            s2.middle = None
            s2.back = chunk_list.ChunkList()


    def push_front(self, item):
        self.push(FRONT, item)

    def push_back(self, item):
        self.push(BACK, item)

    def pop_front(self):
        return self.pop(FRONT)

    def pop_back(self):
        return self.pop(BACK)

    def peek_back(self):
        return self.peek(BACK)

    def peek_front(self):
        return self.peek(FRONT)

    # reverses element ordering
    def rev(self):
        self.rev_aux(lambda c: None)
    