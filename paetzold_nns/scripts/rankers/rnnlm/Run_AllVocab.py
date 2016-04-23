import os, sys

def getRankings(all, valid):
	result = []
	f = open('./temp/output_'+valid+'.txt')
	for line in all:
		scoremap = {}
		for candidate in line:
			score = float(f.readline().strip())
			scoremap[candidate] = score
		ranked = sorted(scoremap.keys(), key=scoremap.__getitem__, reverse=True)
		result.append(ranked)
	f.close()
	return result

def getNewSent(tokens, head, cand):
	sent = ''
	for i in range(0, head):
		sent += tokens[i] + ' '
	sent += cand + ' '
	for i in range(head+1, len(tokens)):
		sent += tokens[i] + ' '
	return sent.strip()

def createMap(dataset, tags, vocab):
	subs = {}
	f1 = open(dataset)
	f2 = open(tags)
	for line1 in f1:
		line2 = f2.readline()
		data1 = line1.strip().split('\t')
		data2 = line2.strip().split(' ')
		tokens = data1[0].split(' ')
		target = data1[1]
		if target not in subs:
			subs[target] = set([])

		head = int(data1[2])
		tag = data2[head].split('|||')[1]
		if tag in vocab:
			subs[target].update(vocab[tag])
	f1.close()
	f2.close()
	return subs
		
def loadVocab(vocab):
	result = {}
	f = open(vocab)
	for line in f:
		data = line.strip().split('\t')[0]
		tokens = data.split('|||')
		word = tokens[0]
		POS = tokens[1]
		if POS not in result:
			result[POS] = set([])
		result[POS].add(word)
	return result

vocab = loadVocab('../../../corpora/vocab_rnnlm_20.txt')

subs = createMap('../../../corpora/paetzold_nns_dataset.txt', '../../../corpora/tagged_sents_paetzold_nns_dataset.txt', vocab)

o = open('../../../substitutions/allvocab/substitutions.txt', 'w')
for word in subs:
	newline = word + '\t'
	for sub in subs[word]:
		newline += sub + '|||'
	o.write(newline[0:len(newline)-3].strip() + '\n')
o.close()
