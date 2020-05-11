import echunk
import schunk
import ssek
FRONT = __import__('direction').Direction.FRONT
BACK = __import__('direction').Direction.BACK
K = __import__('echunk').K

# TODO: peut être renommer K en CAPACITY, ça serait mieux pour la doc

def ssek_to_esek(s):
    version = s.version_max + 1
    front = schunk.echunk_of_schunk(s.front, version)
    back  = schunk.echunk_of_schunk(s.back,  version)
    middle = s.middle
    return create(front, middle, back, version)

def esek_to_ssek(e):
    # TODO: j'ai un commentaire dans schunk qui dit qu'a priori
    # les fonctions schunk_of_echunk n'ont pas besoin de numéro de 
    # version en argument, car les chunk supports peuvent
    # garder le numéro de version qu'ils stockent actuellement.
    front = schunk.schunk_of_echunk(e.front, e.version)
    back  = schunk.schunk_of_echunk(e.back,  e.version)
    middle = e.middle
    version_max = e.version
    e.empty()
    return ssek.create(FRONT, front, middle, back, version_max)


def init(size, fun):
    result = Esek()
    for i in range(size):
        result.push_back(fun(i))
    return result

def create(front, middle, back, version):
    return Esek(front, middle, back, version)

class Esek:
    # TODO je trouverai ça plus propre d'avoir une fonction avec aucun argument pour construire
    # une séquence vide, et une fonction de construction qui prend tous les arguments explicitement.
    # tu peux choisir celle que tu veux comme constructeur, et appeler l'autre create_empty ou
    # bien init_fields; mais faire les deux en une seule fonction, ça donne du code un peu moche.
    # note que le code de create_empty appelle init_aux.
    def __init__(self, front = None, middle = None, back = None, version = 0):
        self.front = echunk.Echunk(version) if front is None else front
        self.back = echunk.Echunk(version) if back is None else back
        self.middle = ssek.Ssek() if middle is None else middle
        self.version = version

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

    # get size of esek
    def size(self):
        return self.size_aux(0, 1)
       
    def size_aux(self, total, level):
        total += self.front.deep_size(level)
        total += self.back.deep_size(level)
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
        middle_size = self.middle.size_aux(0, level+1)
        # if it's in the front we get it from there
        if i < front_size:
            return self.front.get_deep(i, level, FRONT)
        # if it's in the back we get it from there
        elif i >= front_size + middle_size:
            new_index = i - front_size - middle_size
            return self.back.get_deep(new_index, level, FRONT)
        # else we calculate index in middle and we look there
        else:
            new_index = i - front_size
            return self.middle.get_aux(new_index, level + 1)

    def populate(self, pov):
        this = self.get_this(pov)
        if this.is_empty() and not self.middle.is_empty():
            # TODO: tu as le droit d'écrire comme ça dans self.middle ? formidable !
            self.middle, this = self.middle.pop(pov, self.version)
            self.set_this(pov, this)
         # LATER: populate pourrait renforcer l'invariant en disant que si
         # front ou back est vide, alors middle doit devenir None,
         # et pas juste satisfaire "self.middle.is_empty()"

    def populate_sides(self):
        self.populate(FRONT)
        self.populate(BACK)

    def push(self, pov, item):
        this, that = self.get_both(pov)
        if this.is_full():
            if that.is_empty():
                assert self.middle.is_empty()
                self.set_both(pov, that, this)
            else:
                sthis = schunk.schunk_of_echunk(this, self.version)
                self.middle = self.middle.push(pov, sthis, self.version)
                self.set_this(pov, echunk.Echunk())
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
            self.populate(pov)
        return x

    def peek(self, pov):
        assert not self.is_empty()
        this, that = self.get_both(pov)
        if this.is_empty():
            assert self.middle.is_empty()
            return that.peek(pov)
        else:
            return this.peek(pov)

    # print structure (front middle back)
    def print_debug(self, print_item, indent):
        def print_fun(item):
            print_item(item)
            print(" ", end="")
        print(" " * indent, end="")
        self.front.print_general(print_fun)
        if not self.middle.is_empty():
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
        # TODO: ici tu fais un swap, mais je crois que tu peux tout aussi
        # bien faire temp = self.front; self.front = self.back; self.back = tmp,
        # ça échange moins de données.
        self.front.swap(self.back)
        # TODO: normalement c'est pas utile de tester is is_empty(), car rev marchera quand même
        if not self.middle.is_empty():
            self.middle.rev()

    # iterate over seq and apply function
    def iter(self, pov, fun):
        this, that = self.get_both(pov)
        this.iter(pov, fun)
        self.middle.iter(pov, lambda c: c.iter(pov ^ this.dir, fun))
        that.iter(pov, fun)

    def empty(self):
        self.version = 0
        self.front   = echunk.Echunk()
        self.back    = echunk.Echunk()
        self.middle  = ssek.Ssek()

    def invalidate(self):
        self.version = 0
        s2.front = None
        s2.middle = None
        s2.back = None


    def push_back_chunk_middle(self, c):
        m = self.middle
        if c.is_empty():
            return
        if m.is_empty() or c.size() + m.peek_back().size() > K:
            m.push_back(c)
        else:
            c2 = m.peek_back()
            c2.concat(c)

    # puts data from s2 to the back of current object, and clears s2
    def concat_back(self, s2):
        s1 = self
        if (s2.is_empty()):
            return
        # TODO: ça pourrait être juste un "if"
        elif (s1.is_empty()):
            s1.swap(s2)
            return
        # TODO: le else peut être enlevé
        else:
            m1 = s1.middle
            m2 = s2.middle

            # push data to the outside to simplify small cases
            if s1.front.is_empty():
                assert m1.is_empty()
                b = s1.back
                s1.back = s1.front        
                s1.front = b
            if s2.back.is_empty():
                assert m2.is_empty()
                f = s2.front
                s2.front = s2.back
                s2.back = f

            # push s1.back and s2.front into s1.middle
            s1.push_back_chunk_middle(s1.back)
            s1.push_back_chunk_middle(s2.front)
            # TODO: en fait, la fonction "push_back_chunk_middle" pourrait prendre
            # directement m1 en argument, et ne pas travailler sur "self" du tout.
            m1 = s1.middle # s1 was just modified, thus m1 might not be s1.middle
            
            # if m1 is empty replace with m2
            if m1.is_empty():
                s1.middle = m2
            # else concatenate m1 and m2
            elif not m2.is_empty():
                if m1.peek_back().size() + m2.peek_front().size() <= K:
                    p = m2.pop_front()
                    s1.push_back_chunk_middle(p) # TODO: could be push_back_chunk_middle(m1, p)
                    m1 = s1.middle # TODO: necessary? same case as above? => a priori on pourra s'en passer
                m1.concat_back(m2)
            
            # place s2 back into s1.back
            s1.back = s2.back
            # restore the invariant
            s1.populate_sides()
            s2.empty()


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
    