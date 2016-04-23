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

train_victor_corpus = sys.argv[1]
hidden_size = int(sys.argv[2].strip())
layers = int(sys.argv[3].strip())
embedsize = sys.argv[4].strip()
ngramsize = int(sys.argv[5].strip())
model_file = sys.argv[6].strip()

def getTrainData(corpus, embedsize, ngramsize, m):
	f = open(corpus)
	datap = []
	for line in f:
		data = line.strip().split('\t')
		s1 = data[0]
		s2 = data[1]
		label = data[2]
		for ngsize in range(2, ngramsize+1):
			s1ng = ngrams(s1.split(' '), ngsize)
			s2ng = ngrams(s2.split(' '), ngsize)
			s1ng = set([ng for ng in s1ng])
			s2ng = set([ng for ng in s2ng])
			all = s1ng.union(s2ng)
			for ng in all:
				datap.append([ng, label])
	X = np.zeros((len(datap), ngramsize, embedsize))
	Y = np.zeros(len(datap))
	wildcard = np.array([0.0]*embedsize)
	for i in range(0, len(datap)):
		item = datap[i]
		ngram = item[0]
		label = item[1]
		vectors = getEmbedVectors(ngramsize, embedsize, ngram, m, wildcard)
		labels = getLabels(label)
		X[i] = vectors
		Y[i] = labels
	return X, Y

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
	intlab = float(label)
	print('Label:' + str(label))
	print('Final: ' + str(intlab/2.0))
	return intlab/2.0

RNN = recurrent.LSTM
HIDDEN_SIZE = hidden_size
BATCH_SIZE = 500
LAYERS = layers
TRAIN = True

print('Calculating...')
w2vmodel = '/export/data/ghpaetzold/word2vecvectors/models/word_vectors_all_'+embedsize+'_cbow.bin'
m = gensim.models.word2vec.Word2Vec.load_word2vec_format(w2vmodel, binary=True)
Xtr, Ytr = getTrainData(train_victor_corpus, int(embedsize), int(ngramsize), m)
print('X: ' + str(Xtr.shape))
print('Y: ' + str(Ytr.shape))

print('Creating model...')
model = None
try:
	model = model_from_json(open(model_file+'.json').read())
	model.load_weights(model_file+'.h5')
except Exception:
	model = Sequential()
	model.add(RNN(HIDDEN_SIZE, input_shape=(int(ngramsize), int(embedsize)), return_sequences=True))
	for _ in range(LAYERS):
		model.add(RNN(HIDDEN_SIZE, return_sequences=True))
	model.add(RNN(HIDDEN_SIZE, return_sequences=False))
	model.add(Dense(1))
	model.add(Activation('softmax'))
	model.compile(loss='mean_absolute_error', optimizer='rmsprop')

print('Training...')
if TRAIN:
	model.fit(Xtr, Ytr, nb_epoch=5000, batch_size=2000)
	json_string = model.to_json()
	open(model_file+'.json', 'w').write(json_string)
	model.save_weights(model_file+'.h5', overwrite=True)
