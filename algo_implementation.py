from tqdm import tqdm
import string
import collections
import sys

class LinkedListRecord:
    def __init__(self, sym, pos, EOS = False):

        self.pair = None
        self.sym = sym
        self.pos = pos
        self.EOS = EOS

        self.next_occ = -1
        self.prev_occ = -1

        self.prev_pos = self.pos-1
        self.next_pos = -1

    def __str__(self):
        return "\t".join (str(x) for x in [ self.pos+1, self.pair, self.prev_occ+1, self.next_occ+1 ])

    def __repr__(self):
        return "\t".join (str(x) for x in [ self.pos+1, self.pair, self.prev_occ+1, self.next_occ+1 ])


class PriorityRecord:
    def __init__(self, pair, first_occ):

        self.pair = pair
        self.first_occ = first_occ
        self.freq = 0

    def __str__(self):
        return str(vars(self))

    def __repr__(self):
        return self.__str__ ()


charset = string.printable
text_ll = []
i=0
fname = sys.argv[1]
with open(fname, errors="ignore") as fin:
    for line in tqdm(fin):
        line = line.strip()
        for c in line:
            if c.lower() in charset:
                text_ll.append(LinkedListRecord(c.lower(), i))
                i += 1

        text_ll.append(LinkedListRecord(' ', i, EOS=True))
        i += 1


#text = [["a", "a", "b", "a", "b", "a", "a", "b", "c", "a"], ["b", "d", "a", "a", "b", "c", "b", "c", "a", "a", "c", "b", "k"]]

#i=0
#for line in text:
#    for c in line:
#        text_ll.append(LinkedListRecord(c.lower(), i))
#        i += 1
#    text_ll.append(LinkedListRecord(' ', i, EOS=True))
#    i += 1

#print("\n".join(str(x) for x in text_ll))

hash_table = {}
last_occurrence = {}

for i in tqdm(range(len(text_ll)-1)):
    char = text_ll[i]
    next_char = text_ll[i+1]

    pair = (char.sym, next_char.sym)
#    print(pair)

    char.pair = pair
#    ll_pair_record = LinkedListRecord(pair, i)

    if char.prev_pos > -1:
        text_ll[char.prev_pos].next_pos = i

    if not char.EOS and not next_char.EOS:
        if pair in last_occurrence:
            char.prev_occ = last_occurrence[pair]
            text_ll[last_occurrence[pair]].next_occ = i

        last_occurrence[pair] = i
        #text_ll.append(ll_pair_record)

        if not pair in hash_table:
            pq_pair_record = PriorityRecord(pair, i)
            hash_table[pair] = pq_pair_record

        hash_table[pair].freq += 1

#print("\n".join(str(x) for x in text_ll))
#input('fine file')

def print_connected_text(text):
    first = text[0]

    #print(first)
    s = [first.sym]
    next = first.next_pos

    while next > -1:
    #    print(text[next])
        s.append(text[next].sym)
        next = text[next].next_pos

    #~ print(" ".join(s))


fout = open('adventure_output.tsv', 'w')

#cerco coppia a, b con frequenza massima
most_frequent_record = sorted(hash_table.items(), key = lambda x: -x[1].freq)[0][1]
a, b = most_frequent_record.pair
max_freq = most_frequent_record.freq


#~ print_connected_text(text_ll)
#~ print ('\n'.join(str(x) for x in text_ll))
#~ input()
subs_no = 1
while max_freq > 10:
    last_occurrence = {}
    #~ print ('merging @{}@{}@'.format(a,b))
    #creo nuovo simbolo A
    A = '{}{}'.format(a, b)

    print('{}\t{}\t{}'.format(A, a, b), file = fout)

    #rimuovo (a, b) dalle coppie attive
    hash_table[(a, b)].freq = 0

    #trovo la prima occorrenza della coppia a, b
    first_occ = most_frequent_record.first_occ
    while first_occ > -1:

        a_record = text_ll[first_occ]
        prossimo_first_occ = a_record.next_occ
        b_record = text_ll[a_record.next_pos]

        x_record = text_ll[a_record.prev_pos]
        y_record = text_ll[b_record.next_pos]

        new_left_pair = (x_record.sym, A)
        new_right_pair = (A, y_record.sym)


        #Cose da cambiare in a_record:
        #1. simbolo a -> A
        a_record.sym = A
        #2. pair (a, b) -> (A, y)
        a_record.pair = new_right_pair
        #3. prev_pos va bene così
        #4. next_pos va spostata per saltare la b
        a_record.next_pos = y_record.pos
        y_record.prev_pos = a_record.pos


        #Disconnettere (x, a) dalla sua LinkedList
        p = x_record.prev_occ
        n = x_record.next_occ

        if p > -1:
            text_ll[p].next_occ = n
        else:
            if not (x_record.sym, a) in hash_table:
                hash_table[(x_record.sym, a)] = PriorityRecord((x_record.sym, a), n)
            hash_table[(x_record.sym, a)].first_occ = n

        if n > -1:
            text_ll[n].prev_occ = p


        #Decrementare frequenza di (x, a)
        if not (x_record.sym, a) in hash_table:
            hash_table[(x_record.sym, a)] = PriorityRecord((x_record.sym, a), n)
        hash_table[(x_record.sym, a)].freq -= 1

        #Modificare la coppia (x, a) in (x, A)
        x_record.pair = new_left_pair


        #Disconnettere (b, y) dalla sua LinkedList
        p = b_record.prev_occ
        n = b_record.next_occ
        if p > -1:
            text_ll[p].next_occ = n
        else:
            if not (b, y_record.sym) in hash_table:
                hash_table[(b, y_record.sym)] = PriorityRecord((b, y_record.sym), n)
            hash_table[(b, y_record.sym)].first_occ = n

        if n > -1:
            text_ll[n].prev_occ = p

        #Decrementare frequenza di (b, y)
        if not (b, y_record.sym) in hash_table:
            hash_table[(b, y_record.sym)] = PriorityRecord((b, y_record.sym), n)
        hash_table[(b, y_record.sym)].freq -= 1


        #aggiornare frequenza di (x, A)
        if not new_left_pair in hash_table:
            hash_table[new_left_pair] = PriorityRecord(new_left_pair, x_record.pos)
        hash_table[new_left_pair].freq +=1

        #aggiornare frequenza di (A, y)
        if not new_right_pair in hash_table:
            hash_table[new_right_pair] = PriorityRecord(new_right_pair, a_record.pos)
        hash_table[new_right_pair].freq +=1


        #metto -1 come successivo e precedente di (x, A) e (A, y)
        x_record.next_occ = -1
        x_record.prev_occ = -1
        a_record.prev_occ = -1
        a_record.next_occ = -1

        #aggiornare linkedList di (x, A)
        if new_left_pair in last_occurrence and not last_occurrence[new_left_pair] == x_record.pos:
            x_record.prev_occ = last_occurrence[new_left_pair]
            text_ll[last_occurrence[new_left_pair]].next_occ = x_record.pos

        last_occurrence[new_left_pair] = x_record.pos

        #aggiornare likedList di (A, y)
        if prossimo_first_occ == y_record.pos:
            new_right_pair = (A,A)

        if new_right_pair in last_occurrence:
            a_record.prev_occ = last_occurrence[new_right_pair]
            text_ll[last_occurrence[new_right_pair]].next_occ = a_record.pos

        last_occurrence[new_right_pair] = a_record.pos

        first_occ = prossimo_first_occ

    #trova la prossima coppia a, b con frequenza massima K:
    most_frequent_record = sorted(hash_table.items(), key = lambda x: -x[1].freq)[0][1]
    a, b = most_frequent_record.pair
    max_freq = most_frequent_record.freq

    if not subs_no % 10:
        print(max_freq)
    subs_no += 1
