import urllib2, re, gensim
from nltk.corpus import wordnet as wn
import numpy as np
from sklearn.decomposition import PCA

pairs = [(line.strip().split(' ')[0], line.strip().split(' ')[1]) for line in open('adj_adv.txt')]
print(str(pairs))

wvmodel = '/export/data/ghpaetzold/word2vecvectors/models/word_vectors_all_100_cbow.bin'
wvrmodel = '/export/data/ghpaetzold/word2vecvectors/models/word_vectors_all_100_cbow_retrofitted.bin'
pwvmodel = '/export/data/ghpaetzold/word2vecvectors/models/word_vectors_all_generalized_100_cbow.bin'
pwvrmodel = '/export/data/ghpaetzold/word2vecvectors/models/word_vectors_all_generalized_100_cbow_retrofitted.bin'
m = gensim.models.word2vec.Word2Vec.load_word2vec_format(wvmodel, binary=True)
pm = gensim.models.word2vec.Word2Vec.load_word2vec_format(pwvmodel, binary=True)
mr = gensim.models.word2vec.Word2Vec.load_word2vec_format(wvrmodel, binary=True)
pmr = gensim.models.word2vec.Word2Vec.load_word2vec_format(pwvrmodel, binary=True)

types = ['TEM', 'REM', 'SEM', 'RSEM']
outs = []
for type in types:
	outs.append(open(type+'.txt', 'w'))

all = []
X = []
for pair in pairs:
	print(str(pair))
	adj = pair[0]
	adv = pair[1]
	adjTEM = m[adj]
	advTEM = m[adv]
	adjREM = mr[adj]
	advREM = mr[adv]
	adjSEM = pm[adj+'|||J']
	advSEM = pm[adv+'|||A']
	adjRSEM = pmr[adj+'|||J']
	advRSEM = pmr[adv+'|||A']
	X.extend([adjTEM, advTEM, adjREM, advREM, adjSEM, advSEM, adjRSEM, advRSEM])
	all.append((adj, adv))

#Perform PCA:
print('PCA...')
X = np.array(X)
pca = PCA(n_components=2)
X = pca.fit_transform(X)

#Create vector map:
for i in range(0, len(all)):
	adj = all[i][0]
	adv = all[i][1]
	for j in range(0, len(types)):
		type = types[j]
		out = outs[j]
		offset = (i*8)+(j*2)
		out.write(adj + '\t' + str(X[offset][0]) + '\t' + str(X[offset][1]) + '\n')
		out.write(adv + '\t' + str(X[offset+1][0]) + '\t' + str(X[offset+1][1]) + '\n')
for out in outs:
	out.close()
