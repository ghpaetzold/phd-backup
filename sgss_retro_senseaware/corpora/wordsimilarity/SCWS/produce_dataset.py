from nltk.tag.stanford import StanfordPOSTagger
import os, math

def getClosestTag(tagged_sent, head, word):
	indexes = set([])
	for i in range(0, len(tagged_sent)):
		token = tagged_sent[i]
		if token[0].lower()==word.lower():
			indexes.add(i)
	minindex = -1
	mindiff = 99999999
	for index in indexes:
		diff = math.fabs(index-head)
		if diff<mindiff:
			mindiff = diff
			minindex = index
	return tagged_sent[minindex][1].upper()


def getGeneralisedPOS(tag):
	"""
	Returns a generalised version of a POS tag in Treebank format.

	@param tag: POS tag in Treebank format.
	@return A generalised POS tag.
	"""
	result = None
	if tag.startswith('N'):
		result = 'N'
	elif tag.startswith('V'):
		result = 'V'
	elif tag.startswith('RB'):
		result = 'A'
	elif tag.startswith('J'):
		result = 'J'
	elif tag.startswith('W'):
		result = 'W'
	elif tag.startswith('PRP'):
		result = 'P'
	else:
		result = tag.strip()
	return result

model = '/export/data/ghpaetzold/benchmarking/lexmturk/scripts/evaluators/stanford-postagger-full-2015-04-20/models/english-bidirectional-distsim.tagger'
tagger = '/export/data/ghpaetzold/benchmarking/lexmturk/scripts/evaluators/stanford-postagger-full-2015-04-20/stanford-postagger.jar'
java = '/usr/bin/java'

os.environ['JAVAHOME'] = java
tagger = StanfordPOSTagger(model, tagger, java_options='-Xmx6g')

f = open('ratings.txt')

sents1 = []
sents2 = []
heads1 = []
heads2 = []
for line in f:
	data = line.strip().split('\t')
	word1 = data[1].strip()
	word2 = data[3].strip()
	sent1 = data[5].strip()
	newsent1 = ''
	tokens = sent1.split(' ')
	index1 = -1
	for i in range(0, len(tokens)):
		token = tokens[i]
		if token=='<b>':
			index1 = i
		if token!='<b>' and token!='</b>':
			newsent1 += token + ' '
	newsent1 = newsent1.strip()
	sents1.append(newsent1.split(' '))
#	if newsent1.split(' ')[index1]!=word1:
#		print('Problem: ' + newsent1.split(' ')[index1] + ', ' + newsent1.split(' ')[index1-1] + ', ' + word1 + ', '+ str(index1))

	heads1.append(index1)

	sent2 = data[6].strip()
	newsent2 = ''
	tokens = sent2.split(' ')
	index2 = -1
	for i in range(0, len(tokens)):
		token = tokens[i]
		if token=='<b>':
			index2 = i
		if token!='<b>' and token!='</b>':
			newsent2 += token + ' '
	newsent2 = newsent2.strip()
	sents2.append(newsent2.split(' '))

	heads2.append(index2)
f.close()

tagged_sents1 = tagger.tag_sents(sents1)
tagged_sents2 = tagger.tag_sents(sents2)

f = open('ratings.txt')
o = open('dataset.txt', 'w')
c = -1
for line in f:
	c += 1
	data = line.strip().split('\t')
	word1 = data[1].strip()
	word2 = data[3].strip()
	sent1 = data[5].strip()
	sent2 = data[6].strip()
	tagged_sent1 = tagged_sents1[c]
	tagged_sent2 = tagged_sents2[c]
	head1 = heads1[c]
	head2 = heads2[c]
	similarity = data[7]
	
	tag1 = None
	tag2 = None	

	if tagged_sent1[head1][0].lower()==word1.lower():
		tag1 = tagged_sent1[head1][1].strip().upper()
	else:
		tag1 = getClosestTag(tagged_sent1, head1, word1)
	if tagged_sent2[head2][0].lower()==word2.lower():
		tag2 = tagged_sent2[head2][1].strip().upper()
	else:
		tag2 = getClosestTag(tagged_sent2, head2, word2)

	tag1 = getGeneralisedPOS(tag1)
	tag2 = getGeneralisedPOS(tag2)

	newline = word1+'|||'+tag1+'\t'+word2+'|||'+tag2+'\t'+similarity+'\n'
	o.write(newline)
f.close()
o.close()
