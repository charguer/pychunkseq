import schunk
FRONT = __import__('direction').Direction.FRONT
BACK = __import__('direction').Direction.BACK
NO_VERSION = __import__('schunk').NO_VERSION
CAPACITY = __import__('echunk').CAPACITY

# class Ssek:
#   front: schunk containing first elements
#   back: schunk containing last elements 
#   middle: ssek containing the rest of the elements
#   version_max: number indicating the max version number

class Ssek:

    # ------------------------------------------------------------------------ #
    # Constructors

    # Constructor - used internally by create and create_empty functions
    def __init__(self, front, middle, back, version_max):
        self.front = front
        self.back = back
        self.middle = middle
        # TODO: verifier - schunk tjrs créé avec version = NO_VERSION
        self.version_max = version_max

    # Class method - creates & returns empty ssek
    @classmethod
    def create_empty(cls, version_max = 0):
        front = schunk.Schunk()
        back = schunk.Schunk()
        middle = None
        return cls(front, middle, back, version_max)

    # Class method - create ssek with given parameters
    @classmethod
    # TODO: je crois qu'il faut renommer front->this, back->that dans les arguments
    def create(cls, front, middle, back, version_max = 0, pov = FRONT):
        if (pov == FRONT):
            return cls(front, middle, back, version_max)
        else:
            return cls(back, middle, front, version_max)

    # Class method - create ssek with given parameters and populate
    @classmethod
    def create_and_populate(cls, this, middle, that, version_max, pov = FRONT):
        # TODO: bug: il faut passer NO_VERSION à middle.pop,
        # la valeur de version_max ne doit jamais être passée à aucune fonction,
        # elle ne sert que pour pour la conversion vers esek.
        if this.is_empty() and middle is not None and not middle.is_empty():
            middle, this = middle.pop(pov ^ FRONT, version_max) 
        if that.is_empty() and middle is not None and not middle.is_empty():
            middle, that = middle.pop(pov ^ BACK, version_max)
        return Ssek.create(this, middle, that, version_max, pov)
        # LATER: populate pourrait renforcer l'invariant en disant que si
        # front ou back est vide, alors middle doit devenir None,
        # et pas juste satisfaire "self.middle.is_empty()"


    # ------------------------------------------------------------------------ #
    # Basic utility functions

    def is_empty(self):
        return self.front.is_empty() and self.back.is_empty()


    # ------------------------------------------------------------------------ #
    # Push & pop elements

    def push(self, pov, item, version = NO_VERSION):
        this, that = self.get_both(pov)
        if this.is_full():
            if that.is_empty():
                assert self.middle is None or self.middle.is_empty()
                new_this = that.push(pov, item, version)
                new_that = this
                new_ssek = Ssek.create(new_this, None, new_that,
                                        self.version_max, pov)
            else:
                new_this = schunk.Schunk(direction=this.dir)
                new_this = new_this.push(pov, item, version)
                middle = self.middle
                if middle is None:
                    middle = Ssek.create_empty()
                new_middle = middle.push(pov, this, version)
                new_ssek = Ssek.create(new_this, new_middle, that,
                                        self.version_max, pov)
        else:
            new_this = this.push(pov, item, version)
            new_ssek = Ssek.create(new_this, self.middle, that,
                                    self.version_max, pov)
        return new_ssek

    def pop(self, pov, version = NO_VERSION):
        assert not self.is_empty()
        this, that = self.get_both(pov)
        if this.is_empty():
            assert self.middle is None or self.middle.is_empty()
            new_that, x = that.pop(pov, version)
            new_ssek = Ssek.create(this, self.middle, new_that,
                                    self.version_max, pov)
        else:
            new_this, x = this.pop(pov, version)
            new_ssek = Ssek.create_and_populate(new_this, self.middle, that,
                                                self.version_max, pov)
        return new_ssek, x

    def push_front(self, item, version = NO_VERSION):
        return self.push(FRONT, item, version)

    def push_back(self, item, version = NO_VERSION):
        return self.push(BACK, item, version)

    def pop_front(self, version = NO_VERSION):
        return self.pop(FRONT, version)

    def pop_back(self, version = NO_VERSION):
        return self.pop(BACK, version)


    # ------------------------------------------------------------------------ #
    # Operations on ssek

    # Iterate over elements and apply function
    def iter(self, pov, fun):
        this, that = self.get_both(pov)
        this.iter(pov, fun)
        if self.middle is not None:
            self.middle.iter(pov, lambda c: c.iter(pov ^ this.dir, fun))
        that.iter(pov, fun)

    # Reverse order of elements
    def rev(self):
        # reverse front & back and swap them
        front = self.back.rev()
        back = self.front.rev()
        # recursive reverse
        middle = self.middle.rev() if self.middle is not None else None
        # TODO: check version!!!
        return Ssek.create(front, middle, back, self.version_max)


    # ------------------------------------------------------------------------ #
    # Printing

    # Print ssek using print_item function
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

    # ------------------------------------------------------------------------ #
    # Auxiliary methods

    # Access front/back elements depending on pov
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

    # Set front/back elements depending on pov
    def set_both(self, pov, this, that):
        if (pov == FRONT):
            self.front = this
            self.back = that
        else:
            self.front = that
            self.back = this

    # Peek elements on the extremities of the esek (front/back)
    def peek(self, pov):
        assert not self.is_empty()
        this, that = self.get_both(pov)
        if this.is_empty():
            assert self.middle is None or self.middle.is_empty()
            return that.peek(pov)
        else:
            return this.peek(pov)

    def peek_back(self):
        return self.peek(BACK)

    def peek_front(self):
        return self.peek(FRONT)

    # Push back chunk by either push or concat to existing chunk
    # TODO: renommer chunk en schunk ici, et idem pour last_chunk
    # Used in concat
    def push_back_concat(self, c):
        m = self
        if c.is_empty():
            return m
        if m.is_empty() or c.size() + m.peek_back().size() > CAPACITY:
            return m.push_back(c)
        else:
            # TODO: essayer de faire: 
            #   p = m.peek_back();
            #   p.concat(c)
            # pour éviter de faire pop puis push du même objet.
            m, last_chunk = m.pop_back()
            new_chunk = last_chunk.concat(c)
            return m.push_back(new_chunk)


    # ------------------------------------------------------------------------ #
    # Concatenation

    # Puts data from s2 to the back of current object, and clears s2
    def concat_back(self, s2):
        s1 = self
        # TODO: parenthèses superflues ?
        if (s2.is_empty()):
            return s1
        if (s1.is_empty()):
            return s2

        # TODO: il me semble que si m2=None il n'y a rien à faire d'autre
        # que de tester ça aussi dans le "elif not m2.is_empty():".
        # c'est juste le m1 qu'il faut toujours créer (en tous cas
        # c'est nécessaire quand s1.back et s2.front ne sont pas vide).
        m1 = Ssek.create_empty() if s1.middle is None else s1.middle 
        m2 = Ssek.create_empty() if s2.middle is None else s2.middle

        # Set back and front of new ssek
        if s1.front.is_empty():
            assert m1.is_empty()
            front = s1.back
            s1_back = s1.front
        else:
            front = s1.front
            s1_back = s1.back

        if s2.back.is_empty():
            assert m2.is_empty()
            back = s2.front
            s2_front = s2.back
        else:
            back = s2.back
            s2_front = s2.front

        # push s1.back and s2.front into s1.middle
        m1 = m1.push_back_concat(s1_back)
        m1 = m1.push_back_concat(s2_front)
        
        if m1.is_empty():
            # if m1 is empty m2 is the new middle
            middle = m2
        # TODO: tu peux mettre elif m2 = None or m2.is_empty() ici,
        # et ensuite faire la branche else pour la concaténation.
        elif not m2.is_empty():
            # else concatenate m1 and m2
            if m1.peek_back().size() + m2.peek_front().size() <= CAPACITY:
                m2, p = m2.pop_front()
                m1 = m1.push_back_concat(p)
            middle = m1.concat_back(m2)
        else:
            middle = m1

        # TODO: pour la version, il faut prendre le max des version_max de s1 et de s2.
        return Ssek.create_and_populate(front, middle, back, self.version_max)
