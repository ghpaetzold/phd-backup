

#Read targets and candidates:
print('Getting words...')
words = set([])
f = open('../../../substitutions/paetzold/substitutions.txt')
for line in f:
	data = line.strip().split('\t')
	words.add(data[0].strip())
	for word in data[1].strip().split('|||'):
		words.add(word.strip())

print(str(len(words)))

#Get sentences:
print('Getting sentences...')
c = 0
f = open('/export/data/ghpaetzold/corpora/wikipedia/corpus.clean.txt')
o = open('../../../corpora/wcefiles/word_to_sents.txt', 'w')
for line in f:
	c += 1
#	print(str(c))
	for word in words:
		if word in line:
			o.write(word + '\t' + line)
f.close()
o.close()
