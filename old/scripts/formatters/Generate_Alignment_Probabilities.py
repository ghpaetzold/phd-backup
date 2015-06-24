from nltk.stem.porter import *

forw = open('../../corpora/alignment_probabilities/all.fastalign.forward.txt')
inve = open('../../corpora/alignment_probabilities/all.fastalign.inverse.txt')
sents = open('../../corpora/alignment_probabilities/all.fastalign.txt')

stemmer = PorterStemmer()

cands = {}
total = {}
c = 0
#for i in range(0, 1000):
#	line = sents.readline()
for line in sents:
	c += 1
	print(str(c))
	data = line.strip().split('|||')
	sent1 = data[0].strip().split(' ')
	sent2 = data[1].strip().split(' ')
	
	faligns = forw.readline().strip().split(' ')
	ialigns = inve.readline().strip().split(' ')

	aligns = set(faligns).union(set(ialigns))

	for align in aligns:
		alignd = align.strip().split('-')
		left = int(alignd[0].strip())
		right = int(alignd[1].strip())
		target = stemmer.stem(sent1[left].lower())
		candidate = stemmer.stem(sent2[right].lower())
		if target in cands.keys():
			total[target] += 1
			if candidate in cands[target].keys():
				cands[target][candidate] += 1
			else:
				cands[target][candidate] = 1
		else:
			total[target] = 1
			cands[target] = {candidate:1}
forw.close()
inve.close()
sents.close()

out = open('../../corpora/alignment_probabilities/alignment_probabilities.txt', 'w')
for key in cands.keys():
	for cand in cands[key].keys():
		out.write(key + '\t' + cand + '\t' + str(float(cands[key][cand])/float(total[key])) + '\n')
out.close()

lexf = open('../../corpora/lexmturk/lexmturk.txt')
targets = set([])
for line in lexf:
	targets.add(stemmer.stem(line.strip().split('\t')[1].strip()))
lexf.close()

out5 = open('../../corpora/alignment_probabilities/alignment_probabilities_lexmturk.txt', 'w')
for key in cands.keys():
	if key in targets:
		for cand in cands[key].keys():
			out5.write(key + '\t' + cand + '\t' + str(float(cands[key][cand])/float(total[key])) + '\n')
out5.close()
