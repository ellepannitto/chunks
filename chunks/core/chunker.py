"""Basic chunking functions"""
import logging

import collections
import nltk

__all__ = ('linear')

logger = logging.getLogger(__name__)


def linear(input_filepath):
    voc = set()
    text = []

    with open(input_filepath, errors='ignore') as fin:
        for lineno, line in enumerate(fin):
            line = line.strip()
            for char in line:
                text.append(char)
                voc.add(char)
            if not lineno % 100000:
                logger.info('processing line {}...'.format(lineno))
            text.append(' ')

    go_on = True
    to_replace_a, to_replace_b = None, None
    sample = text[500:1000]
    logger.info('_'.join(sample))

	max_freq = 10
	freqs_list = []
	for i in range(max_freq):
		freqs_list.append(collections.defaultdict(int))
	freqs_10grams = nltk.FreqDist(nltk.ngrams(text, 10))
	freqs_list[-1] = freqs_10grams

	for ngram, freq in freqs_10grams:
		for i in range(len(max_freq)-1):
			freqs_list[i][ngram[:i+1]] + = freq

    iter = 0
    subs_list = []
    while go_on:

#        freqs_1grams = nltk.FreqDist(text)
#        print(freqs_1grams)
#        freqs_2grams = nltk.FreqDist(nltk.ngrams(text, 2))
#        freqs_3grams = nltk.FreqDist(nltk.ngrams(text, 3))
#        freqs_4grams = nltk.FreqDist(nltk.ngrams(text, 4))

        freqs_2grams = collections.defaultdict(int)
        freqs_3grams = collections.defaultdict(int)
        for ngram, freq in freqs_5grams.items():
            freqs_2grams[(ngram[0], ngram[1])] += freq
            freqs_3grams[(ngram[0], ngram[1], ngram[2])] += freq

        sorted_2grams = sorted(freqs_2grams.items(), key=lambda x: -x[1])[:10]
        a, b = sorted_2grams[0][0]
        most_freq_3gram = {x:y for x, y in freqs_3grams.items() if x[0]==a and x[1]==b}
        sorted_3grams = sorted(most_freq_3gram.items(), key=lambda x: -x[1])[:10]
        print(sorted_2grams)
        print(sorted_3grams)
        input()


        freqs_bigrams = collections.defaultdict(int)
        freqs_unigrams = collections.defaultdict(int)
        prev_char = None
        charno = 0
        new_text = []

        while charno < len(text)-1:
            char = text[charno]
            next_char = text[charno+1]

            if char == to_replace_a and next_char == to_replace_b:
                new_text.append(char+next_char)
                charno += 1
            else:
                new_text.append(char)

            if prev_char:
                freqs_bigrams[(prev_char, new_text[-1])] += 1
            freqs_unigrams[new_text[-1]] += 1
            charno += 1
            prev_char = new_text[-1]

#            if prev_char:
#                freqs[(prev_char,char)]+=1
            #~ prev_char = char
            prev_char = new_text[-1]
            if not charno % 10000000:
                logger.info('processing char no. {}'.format(charno))

        prev_char = None
        charno = 0
        new_sample = []
        while charno < len(sample)-1:
            char = sample[charno]
            next_char = sample[charno+1]
            if char == to_replace_a and next_char == to_replace_b:
                new_sample.append(char+next_char)
                charno += 1
            else:
                new_sample.append(char)
            charno += 1
            prev_char = new_sample[-1]


        #~ freqs_bigrams = {x:math.log2(y)*y/freqs_unigrams[x[0]] for x, y in freqs_bigrams.items()}
#        print(sorted(freqs_bigrams.items(), key = lambda x: -x[1])[:50])
#        input()

        to_substitute = sorted(freqs_bigrams.items(), key=lambda x: -x[1])[0]
        to_sub_voc, to_sub_freq = to_substitute
        to_replace_a, to_replace_b = to_sub_voc
        voc.add(to_sub_voc[0]+to_sub_voc[1])
        subs_list.append(to_sub_voc[0]+to_sub_voc[1])
#        logger.info('merging "{}" and "{}"'.format(to_substitute[0][0],
#                                                   to_substitute[0][1]))
        if not iter % 10:
            logger.info('_'.join(subs_list[iter-10:]))
            logger.info('_'.join(new_sample))
        iter += 1
        text = new_text
        sample = new_sample
