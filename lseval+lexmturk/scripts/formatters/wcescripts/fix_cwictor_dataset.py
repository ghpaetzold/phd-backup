


f = open('../../../corpora/wcefiles/cwictor_corpus.txt')
fts = open('../../../corpora/wcefiles/tagged_sents_cwictor_corpus.txt')
insts = []
for line in f:
	data = line.strip().split('\t')
	sent = data[0].strip().split(' ')
	posent = fts.readline()
	pos = posent.strip().split(' ')
	if len(sent)==len(pos) and len(data)>3:
		insts.append((line, posent))
f.close()
fts.close()

o = open('../../../corpora/wcefiles/cwictor_corpus_fixed.txt', 'w')
op = open('../../../corpora/wcefiles/tagged_sents_cwictor_corpus_fixed.txt', 'w')
for inst in insts:
	line = inst[0]
	pline = inst[1]
	o.write(line)
	op.write(pline)
o.close()
op.close()
