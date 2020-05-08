
chunk:
   version : int  # -1 par défaut
   data : array(a)
   front : int
   size : int

schunk:
   support: chunk
   view: int*int # size/head

# invariant: si le chunk support est possédé de manière unique, alors
# forcément schunk.view = [support.front, support.size] = support.view()

schunk_create(version) # create a uniquely owned schunk
   c = chunk()
   c.version = version
   support = c
   view = vide


# transforme un chunk en schunk possédé de manière unique par la structure
# qui a le numéro "version"
schunk_of_chunk(c, version)
   version = version
   support = c
   view = tout la vue de ce segment

chunk_of_schunk(s, version)
   if s.version == version:
      # unique owner
      assert(schunk.view = schunk.support.view())
      return schunk.support
   else:
      copy des éléments de la vue dans un chunk frais c
      return c

sschunk.push actuel -> push_shared
sschunk.push_unique -> modifie la view en place et le chunk en place
sschunk.push(self, x, version) -> if self.version == version

esek(a)
   version: int # si un chunk c de middle a c.version=version, alors possession unique
                # sinon, a toujours c.version <= version
   front, back: chunk(a) # possession unique toujours
   middle: ssek(schunk a)

ssek(a)
   version_max: int  # majorant des c.version pour les chunks c stockés dans la structure
   front, back: schunk(a) 
   middle: ssek(schunk a)



esek_to_ssek(s)
   { front = schunk_of_chunk(s.front)
     back = ..
     middle = s.middle
     version_max = version }
   clear(s)

ssek_to_esek(s)
   { front = chunk_of_schunk(s.front)
     back =
     middle = s.middle
     version = s.version_max + 1 }


esek.push_front(s, x)
   if s.front.is_full():
      s.middle = s.middle.push_front(schunk_of_chunk(s.front, s.version))
   s.front.push_front(x)

esek.pop_front(s)
   if s.front.is_empty():
      [middle2, schunk] = s.middle.pop_front()
      s.middle = middle2
      # s.front = chunk_of_schunk(schunk, s.version)


make_ssek front middle back version_max =
      { front = 
        back = 
        middle = 
        version_max = version_max }

make_ssek_and_populate_front
   if front.is_empty and not middle.is_empty ...
      make_ssek 
   else 
      make_ssek

make_ssek_and_populate front middle back version_max =


ssek.pop_front(s, version)
   if s.front.is_empty():
      assert s.middle_is.empty()
      assert not s.back.is_empty()
      [back2,x] = s.back.pop_front()
      seq2 = make_ssek s.front s.middle back2 s.version_max
      [seq2, x]
   else
      [front2, x] = s.front.pop_front()
      seq2 = make_ssek_and_populate front2 s.middle s.back s.version_max
      [seq2, x]

ssek.push_front(s, x, version)
   if s.front.is_full()
      front2 = schunk.create(version)
      middle2 = push_front(s.middle, s.front, version)


check(s)      
