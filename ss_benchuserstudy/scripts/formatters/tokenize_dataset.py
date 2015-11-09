import nltk

f = open('../../corpora/ss_dataset_userstudy.txt')
o = open('../../corpora/ss_dataset_userstudy_tokenized.txt', 'w')

for line in f:
	data = line.strip().split('\t')
	tokens = nltk.word_tokenize(data[0])
	sent = ''
	for token in tokens:
		sent += token + ' '
	newline = sent.strip() + '\t'
	for item in data[1:]:
		newline += item + '\t'
	o.write(newline.strip() +  '\n')
	
f.close()
o.close()
