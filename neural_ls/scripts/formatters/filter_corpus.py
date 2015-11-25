import gensim, sys

wvmodel = '/export/data/ghpaetzold/word2vecvectors/models/word_vectors_all_100_cbow.bin'
m = gensim.models.word2vec.Word2Vec.load_word2vec_format(wvmodel, binary=True)

f = open(sys.argv[1])
o = open(sys.argv[2], 'w')

for line in f:
	tokens = line.strip().split(' ')
	hasunk = False
	for token in tokens:
		try:
			v = m[token]
		except Exception:
			hasunk = True
	if not hasunk:
		o.write(line)
f.close()
o.close()
