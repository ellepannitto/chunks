import nltk
import collections

#TODO: sentence is a hard boundary

text = [c.lower() for line in open('/home/ludovica/adventure-all.head.txt').readlines()[:10000] for c in line if c.isalpha() or c in ['.', ',', '?', '!', ' ']]

max_freq = 10
freqs_list = []
for i in range(max_freq):
  freqs_list.append(collections.defaultdict(int))
freqs_10grams = nltk.FreqDist(nltk.ngrams(text, 10))
freqs_list[-1] = freqs_10grams

for ngram, freq in freqs_10grams.items():
#  print(ngram)
  for i in range(max_freq-1):
#    print(ngram[:i+1])
    freqs_list[i][ngram[:i+1]] += freq
#    print(freqs_list[i])
#  input()

for idx in range(len(freqs_list)-1):
    list = freqs_list[len(freqs_list)-idx-1]
    for ngram, freq in list.items():
        condprob = freq*1.0 / freqs_list[len(freqs_list)-idx-2][ngram[:-1]]
        list[ngram] = condprob

most_frequent_bigram = sorted(freqs_list[1].items(), key=lambda x: -x[1])[0]
a, b = most_frequent_bigram[0]
freq = most_frequent_bigram[1]
freqs_list[0]['{}{}'.format(a,b)] = freq
del freqs_list[1][most_frequent_bigram[0]]
print(most_frequent_bigram)
go_on = True

while go_on:
    for idx, dict in enumerate(freqs_list[2:]):
        for ngram, freq in dict.items():
            if ngram[0]==a and ngram[1]==b:
                remaining_part = ngram[2:]
                s = '{}{}'.format(a,b)
                if len(s) < 10:
                    new_tuple = tuple([s])+remaining_part
                    freqs_list[idx+1][new_tuple] = freq
#                print(new_tuple)
#                input()

    most_frequent_bigram = sorted(freqs_list[1].items(), key=lambda x: -x[1])[0]
    print(most_frequent_bigram)
    a, b = most_frequent_bigram[0]
    freq = most_frequent_bigram[1]
    freqs_list[0]['{}{}'.format(a,b)] = freq
    del freqs_list[1][most_frequent_bigram[0]]

#    input()
