import nltk
from nltk.util import everygrams
import collections

#TODO: sentence is a hard boundary
#TODO: multiprocessing

text = [c.lower() for line in open('/home/ludovica/adventure-all.head.txt').readlines()[:100000] for c in line]

max_freq = 10
#eg = list(everygrams(text, min_len=2, max_len=max_freq))
#FDist = nltk.FreqDist(eg)

#FDist = {x:y for x, y in FDist.items() if y>10}

freqs_list = []
for i in range(max_freq):
  freqs_list.append(collections.defaultdict(int))
freqs_10grams = nltk.FreqDist(nltk.ngrams(text, max_freq))
freqs_list[-1] = freqs_10grams

for ngram, freq in freqs_10grams.items():
#  print(ngram)
  for i in range(max_freq-1):
#    print(ngram[:i+1])
    if freq > 100:
        freqs_list[i][ngram[:i+1]] += freq
#    print(freqs_list[i])
#  input()

voc = collections.defaultdict(list)
for x in freqs_list[0].keys():
    voc[x]=[]

for idx, dict in enumerate(freqs_list):
    dict = {x:y for x, y in dict.items() if y > 10}
    freqs_list[idx] = dict


most_frequent_bigram = sorted(freqs_list[1].items(), key=lambda x: -x[1])[0]
a, b = most_frequent_bigram[0]
s = ('{}{}'.format(a,b),)
freq = most_frequent_bigram[1]
freqs_list[0]['{}{}'.format(a,b)] = freq
del freqs_list[1][most_frequent_bigram[0]]
#print(most_frequent_bigram)
go_on = True

while go_on:
    print('found @{}@{}@ as most frequent pair, f:{} - {}'.format(a, b, freq, s[0] in voc))

    
    voc[s[0]].append(((a, b), freq))
    if len(voc[s[0]])>1:
        print(s[0], voc[s[0]])
        input()

    for idx, dict in enumerate(freqs_list[2:]):
#        print('examining dict at position {}'.format(idx+2))
        for ngram, freq in dict.items():
            for idx_ngram, char in enumerate(ngram[:-1]):
                if ngram[idx_ngram] == a and ngram[idx_ngram+1] == b:
#                    print('found ngram that contains {}: {} - {}'.format(s[0], ngram, freq))
                    remaining_part = (ngram[:idx_ngram],ngram[idx_ngram+2:])
#                    print('split {} in {}'.format(ngram, remaining_part))
                    left = remaining_part[0]+(a,)
                    right = (b,)+remaining_part[1]

                    if left in freqs_list[idx+1]:
#                        print('in dict at position {}, frequency of {} is {}'.format(idx+1, left, freqs_list[idx+1][left]))
                        freqs_list[idx+1][left] -= freq
                        if freqs_list[idx+1][left] < 10:
                            del freqs_list[idx+1][left]
#                        print('in dict at position {}, NEW frequency of {} is {}'.format(idx+1, left, freqs_list[idx+1][left]))

                    if right in freqs_list[idx+1]:
#                        print('in dict at position {}, frequency of {} is {}'.format(idx+1, right, freqs_list[idx+1][right]))
                        freqs_list[idx+1][right] -= freq
                        if freqs_list[idx+1][right] < 10:
                            del freqs_list[idx+1][right]
#                        print('in dict at position {}, NEW frequency of {} is {}'.format(idx+1, right, freqs_list[idx+1][right]))

                    if len(s) < max_freq:
                        new_tuple = remaining_part[0]+s+remaining_part[1]
                        freqs_list[idx+1][new_tuple] = freq
#                    input()

    most_frequent_bigram = sorted(freqs_list[1].items(), key=lambda x: -x[1])[0]
#    print(most_frequent_bigram)
    a, b = most_frequent_bigram[0]
    s = ('{}{}'.format(a,b),)
    freq = most_frequent_bigram[1]
    freqs_list[0]['{}{}'.format(a,b)] = freq
    del freqs_list[1][most_frequent_bigram[0]]
