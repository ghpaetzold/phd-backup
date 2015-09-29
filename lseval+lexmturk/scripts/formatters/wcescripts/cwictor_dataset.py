import random

def getErrorInstance(word, head, sent):
	tokens = sent.split(' ')
	ehead = head
	while ehead==head:
		ehead = random.randint(0, len(tokens)-1)
	esent = ''
	eword = tokens[ehead]
	for i in range(0, len(tokens)):
		if i==ehead:
			esent += word + ' '
		elif i==head:
			esent += eword + ' '
		else:
			esent += tokens[i] + ' '
	return esent.strip(), ehead

def getHead(word, sent):
	tokens = sent.split(' ')
	head = -1
	for i in range(0, len(tokens)):
		if tokens[i]==word:
			head = i
	return head

#Read targets and candidates:
print('Getting words...')
words = set([])
f = open('../../../substitutions/paetzold/substitutions.txt')
for line in f:
        data = line.strip().split('\t')
        words.add(data[0].strip())
        for word in data[1].strip().split('|||'):
                words.add(word.strip())
f.close()

print(str(len(words)))

#Create count map:
countmap = {}
for word in words:
	countmap[word] = 0

#Create CWIctor instances:
c = 0
f = open('../../../corpora/wcefiles/word_to_sents.txt')
o = open('../../../corpora/wcefiles/cwictor_corpus.txt', 'w')
for line in f:
	c += 1
#	print(str(c))
	data = line.strip().split('\t')
	word = data[0]
	sent = data[1]
	tokens = sent.strip().split(' ')
	if countmap[word]<40:
		head = getHead(word, sent)
		hypword = None
		try:
			hypword = tokens[head]
		except Exception:
			hypword = None
		if hypword and hypword==word:
			esent, ehead = getErrorInstance(word, head, sent)
			if head>-1:
				o.write(sent + '\t' + word + '\t' + str(head) + '\t1\n')
				o.write(esent + '\t' + word + '\t' + str(ehead) + '\t0\n')
				countmap[word] += 1
f.close()
o.close()
