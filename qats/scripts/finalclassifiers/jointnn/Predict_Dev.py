from keras.optimizers import *
from keras.models import *
from keras.layers.core import *
from keras.models import Sequential, slice_X
from keras.layers.core import Activation, TimeDistributedDense, RepeatVector
from keras.layers import recurrent
from keras.preprocessing.text import *
import sys
import numpy as np
from nltk.util import ngrams
import gensim

hidden_size = int(sys.argv[1].strip())
layers = int(sys.argv[2].strip())
embedsize = sys.argv[3].strip()
ngramsize = int(sys.argv[4].strip())
test_victor_corpus = sys.argv[5].strip()
out_file = sys.argv[6].strip()
model_file = sys.argv[7].strip()

def getTestData(corpus, embedsize, ngramsize, m):
	f = open(corpus)
	datap = []
	for line in f:
		data = line.strip().split('\t')
		s1 = data[0]
		s2 = data[1]
		label = data[2]
		all = set([])
		for ngsize in range(2, ngramsize+1):
			s1ng = ngrams(s1.split(' '), ngramsize)
			s2ng = ngrams(s2.split(' '), ngramsize)
			s1ng = set([ng for ng in s1ng])
			s2ng = set([ng for ng in s2ng])
			all.update(s1ng.union(s2ng))
		datap.append(list(all))
	Xs = []
	wildcard = np.array([0.0]*embedsize)
	for ngs in datap:
		X = np.zeros((len(ngs), ngramsize, embedsize))
		for i in range(0, len(ngs)):
			ngram = ngs[i]
			vectors = getEmbedVectors(ngramsize, embedsize, ngram, m, wildcard)
			X[i] = vectors
		Xs.append(X)
	return Xs

def getEmbedVectors(ngramsize, embedsize, ngram, m, wildcard):
	result = np.zeros((ngramsize, embedsize))
	for i in range(0, len(ngram)):
		word = ngram[i]
		try:
			v = m[word.lower()]
			result[i] = v
		except Exception:
			result[i] = wildcard
	if len(ngram)<ngramsize:
		for i in range(len(ngram), ngramsize):
			result[i] = wildcard
	return result

def getLabels(label):
	answer = np.zeros(3)
	answer[int(label)]=1.0
	return answer

print('Calculating...')
w2vmodel = '/export/data/ghpaetzold/word2vecvectors/models/word_vectors_all_'+embedsize+'_cbow.bin'
m = gensim.models.word2vec.Word2Vec.load_word2vec_format(w2vmodel, binary=True)
Xtes = getTestData(test_victor_corpus, int(embedsize), int(ngramsize), m)

model = model_from_json(open(model_file+'.json').read())
model.load_weights(model_file+'.h5')
print('Loaded!')

print('Predicting...')
labels = []
for Xte in Xtes:
	labels_raw = model.predict_classes(Xte, batch_size=Xte.shape[0])
	final_label = np.average(labels_raw)
	if final_label<0.6666:
		final_label = 0
	elif final_label<1.3333:
		final_label = 1
	else:
		final_label = 2
	float_label = np.average(labels_raw)
	labels.append((final_label, float_label))

o = open(out_file, 'w')
for label in labels:
	o.write(str(label[0])+'\t'+str(label[1]) + '\n')
o.close()
