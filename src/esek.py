import echunk
FRONT = __import__('direction').Direction.FRONT
BACK = __import__('direction').Direction.BACK
K = __import__('echunk').K


def init(size, fun):
    result = Esek()
    for i in range(size):
        result.push_back(fun(i))
    return result


class Esek:
    
    def __init__(self):
        self.front = echunk.Echunk()
        self.back = echunk.Echunk()
        self.middle = None # appel au constructeur donne boucle infinie
        # self.free_front = echunk.Echunk()
        # self.free_back = echunk.Echunk()

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

    # get size of esek
    def size(self):
        return self.size_aux(0, 1)
        
    def size_aux(self, total, level):
        total += self.front.deep_size(level)
        total += self.back.deep_size(level)
        if self.middle is not None:
            total = self.middle.size_aux(total, level + 1)
        return total

    # get item at index i
    def get(self, i):
        assert not self.is_empty()
        return self.get_aux(i, 1)

    # override [] operator
    def __getitem__(self, i):
        return self.get(i)

    def get_aux(self, i, level):
        front_size = self.front.deep_size(level) 
        middle_size = 0 if self.middle is None else self.middle.size_aux(0, level+1)
        # if it's in the front we get it from there
        if i < front_size:
            return self.front.get_deep(i, level, FRONT)
        # if it's in the back we get it from there
        elif i >= front_size + middle_size:
            return self.back.get_deep(i - front_size - middle_size, level, FRONT)
        # else we calculate index in middle and we look there
        else:
            new_index = i - front_size
            return self.middle.get_aux(new_index, level + 1)

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
                    self.middle = Esek()
                self.middle.push(pov, this)
                self.set_this(pov, echunk.Echunk())
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
    def print_debug(self, print_item, indent):
        def print_fun(item):
            print_item(item)
            print(" ", end="")
        print(" " * indent, end="")
        self.front.print_general(print_fun)
        if self.middle is not None and not self.middle.is_empty():
            self.middle.print_debug(lambda c: c.iter(FRONT, print_fun), indent + 2)
        else:
            print(".")
        print(" " * indent, end="")
        self.back.print_general(print_fun)

    # print seq using print_item
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
            self.middle = Esek()
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

    # reverses element ordering
    def rev(self):
        self.front.rev()
        self.back.rev()
        self.front.swap(self.back)
        if self.middle is not None and not self.middle.is_empty():
            self.middle.rev()

    # iterate over seq and apply function
    def iter(self, pov, fun):
        this, that = self.get_both(pov)
        this.iter(pov, fun)
        if self.middle is not None:
            self.middle.iter(pov, lambda c: c.iter(pov ^ this.dir, fun))
        that.iter(pov, fun)

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
            s2.front = echunk.Echunk()
            s2.middle = None
            s2.back = echunk.Echunk()


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
    