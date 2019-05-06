import collections
import nltk
import math

def replace(list, new_item):
	new_list = []
	a, b = new_item
	to_rep = a+b
	i=0
	while i<len(list)-1:
		if list[i]==a and list[i+1]==b:
			new_list.append(to_rep)
			i+=1
		else:
			new_list.append(list[i])
		i+=1
	#    if not i%100000:
	#        print(i)
	return new_list
	
	
def linear(input_filepath):
	voc = set()
	text = []

	with open(input_filepath, errors='ignore') as fin:
		for lineno, line in enumerate(fin):
			line = line.strip()
			for char in line:
				text.append(char)
				voc.add(char)
			if not lineno%10000:
				print(lineno)
			text.append(' ')
	
	go_on = True
	to_replace_a, to_replace_b = None, None

	while go_on:
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
				charno+=1
			else:
				new_text.append(char)

			if prev_char:
				freqs_bigrams[(prev_char, new_text[-1])]+=1
			freqs_unigrams[new_text[-1]]+=1
			charno+=1
			prev_char = new_text[-1]
			
#			if prev_char:
#				freqs[(prev_char,char)]+=1
			#~ prev_char = char
			prev_char = new_text[-1]
			#~ if not charno%1000000:
				#~ print(charno)


		#~ freqs_bigrams = {x:math.log2(y)*y/freqs_unigrams[x[0]] for x, y in freqs_bigrams.items()}
#		print(sorted(freqs_bigrams.items(), key = lambda x: -x[1])[:50])
#		input()
		
		to_substitute = sorted(freqs_bigrams.items(), key = lambda x:-x[1])[0]
		to_sub_voc, to_sub_freq = to_substitute
		to_replace_a, to_replace_b = to_sub_voc
		voc.add(to_sub_voc[0]+to_sub_voc[1])

		#~ print(len(text), to_substitute)
		print('-{}{}-'.format(to_substitute[0][0],to_substitute[0][1]))
		#~ text = replace(text, to_sub_voc)
		text = new_text
		#~ print(len(text))
		#~ print('-'.join(text[600:1000]))
		#~ input()	
