import os
import numpy as np
import re
dict = '/usr/lib64/thunderbird/dictionaries/'
files = [a for a in os.listdir(dict)  if a[-3:] == 'dic']
wordlist = []
for file in files:
	words = open(dict+file).readlines()
	for word in words:
		wordlist.append(word.split('/')[0].strip())
		
words = ''
while len(words) < 100000:
	
	paragraph_length = np.random.randint(10,20)
	for line in range(paragraph_length):
		sentence_length = np.random.randint(3,20)
		sentence = ' '.join(np.random.choice(wordlist, sentence_length))
		sentence = re.sub(r'[^a-zA-Z0-9\s]', '', sentence)
		sentence = sentence[0].upper() + sentence[1:]+'. '
		comma = np.random.choice(range(10), 1)[0]
		if comma == 0:
			sentence = sentence.split()
			wordchoice = np.random.choice(range(len(sentence)), 1)[0]
			sentence[wordchoice] = sentence[wordchoice]+','
			sentence = ' '.join(sentence)
		words += sentence
	sentence += '\n'
print words

	

	


