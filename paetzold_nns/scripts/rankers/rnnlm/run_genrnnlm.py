import os, sys

def getSubs(generator):
        result = {}
        f = open('../../../substitutions/' + generator + '/substitutions.txt')
        for line in f:
                data = line.strip().split('\t')
                target = data[0].strip()
                candidates = data[1].strip().split('|||')
                result[target] = candidates
        f.close()
        return result

def getRankings(all, valid, generator):
	result = []
	f = open('./temp/outputgen_'+generator+'_'+valid+'.txt')
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

def createTemp(dataset, tags, vocab, valid, generator):
	tpath = './temp/inputgen_'+generator+'_'+valid+'.txt'
	o = open(tpath, 'w')
	f1 = open(dataset)
	f2 = open(tags)
	all = []
	c = 0
	for line1 in f1:
		c += 1
		line2 = f2.readline()
		data1 = line1.strip().split('\t')
		data2 = line2.strip().split(' ')
		tokens = data1[0].split(' ')
		target = data1[1]
		head = int(data1[2])
		cands = set([target])
		if target in vocab:
			cands.update(vocab[target])
		cands = list(cands)
		all.append(cands)
		for cand in cands:
			newsent = getNewSent(tokens, head, cand)
			o.write(newsent + '\n')
	o.close()
	return all
		
valid = sys.argv[1]
generator = sys.argv[2]

vocab = getSubs(generator)

all = createTemp('../../../corpora/paetzold_nns_dataset.txt', '../../../corpora/tagged_sents_paetzold_nns_dataset.txt', vocab, valid, generator)

comm = '/export/tools/rnnlm/rnnlm -rnnlm ../../../corpora/rnnlm_models/5kk_'+valid+'_model.txt -test ./temp/inputgen_'+generator+'_'+valid+'.txt -nbest -debug 0 > ./temp/outputgen_'+generator+'_'+valid+'.txt'
os.system(comm)

rankings = getRankings(all, valid, generator)

f = open('../../../corpora/paetzold_nns_dataset.txt')
o = open('../../../rankings/rnnlm/ranks_'+generator+'_void_'+valid+'.txt', 'w')
for rank in rankings:
	newline = ''
	for word in rank:
		newline += word + '\t'
	o.write(newline.strip() + '\n')
f.close()
o.close()
