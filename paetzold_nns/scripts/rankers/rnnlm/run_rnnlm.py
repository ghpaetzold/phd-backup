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

def createTemp(dataset, tags, vocab, valid):
	tpath = './temp/input_'+valid+'.txt'
	o = open(tpath, 'w')
	f1 = open(dataset)
	f2 = open(tags)
	all = []
	c = 0
#	for i in range(1, 3):
#		line1 = f1.readline()
	for line1 in f1:
		c += 1
#		print(str(c))
		line2 = f2.readline()
		data1 = line1.strip().split('\t')
		data2 = line2.strip().split(' ')
		tokens = data1[0].split(' ')
		target = data1[1]
		head = int(data1[2])
		tag = data2[head].split('|||')[1]
		cands = set([target])
		if tag in vocab:
			cands.update(vocab[tag])
		#cands = list(cands)[0:10]
		cands = list(cands)
		all.append(cands)
		for cand in cands:
			newsent = getNewSent(tokens, head, cand)
			o.write(newsent + '\n')
	o.close()
	return all
		
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

valid = sys.argv[1]

vocab = loadVocab('../../../corpora/vocab_rnnlm_20.txt')

all = createTemp('../../../corpora/paetzold_nns_dataset.txt', '../../../corpora/tagged_sents_paetzold_nns_dataset.txt', vocab, valid)

comm = '/export/tools/rnnlm/rnnlm -rnnlm ../../../corpora/rnnlm_models/5kk_'+valid+'_model.txt -test ./temp/input_'+valid+'.txt -nbest -debug 0 > ./temp/output_'+valid+'.txt'
os.system(comm)

rankings = getRankings(all, valid)

f = open('../../../corpora/paetzold_nns_dataset.txt')
o = open('../../../rankings/rnnlm/ranks_allvocab_void_'+valid+'.txt', 'w')
for rank in rankings:
	newline = ''
	for word in rank:
		newline += word + '\t'
	o.write(newline.strip() + '\n')
f.close()
o.close()
#	data = f.readline().strip().split('\t')
#	sent = data[0].strip()
#	target = data[1].strip()
#	final = rank[0]
#	if final==target:
#		final = rank[1]
#	print('\n\nSentence: ' + sent)
#	print('Candidate: ' + final)
#	tops = rank[0:5]
#	bots = rank[len(rank)-5:len(rank)]
#	print('Tops:')
#	for top in tops:
#		print('\t'+top)
#	print('Bottoms:')
#	for bot in bots:
#		print('\t'+bot)
