from keras.optimizers import *
from keras.models import *
from keras.layers.core import *
from keras.models import Sequential, slice_X
from keras.layers.core import Activation, TimeDistributedDense, RepeatVector
from keras.layers import recurrent
from keras.preprocessing.text import *
import sys, os
import numpy as np
from nltk.util import ngrams
import gensim

hidden_size = int(sys.argv[1].strip())
layers = int(sys.argv[2].strip())
embedsize = sys.argv[3].strip()
ngramsize = int(sys.argv[4].strip())
model_file = sys.argv[5].strip()

def getTrainData(embedsize, ngramsize, m):
	files = []
	for type in ['G', 'M', 'S', 'O']:
		files.append(open('../../../corpora/'+type+'_train.txt'))
	f = files[0]
	datap = []
	for line in f:
		data = line.strip().split('\t')
		s1 = data[0]
		s2 = data[1]
		labels = [data[2]]
		for ftype in files[1:]:
			linetype = ftype.readline()
			datatype = linetype.strip().split('\t')
			labels.append(datatype[2])
		for ngsize in range(2, ngramsize+1):
			s1ng = ngrams(s1.split(' '), ngsize)
			s2ng = ngrams(s2.split(' '), ngsize)
			s1ng = set([ng for ng in s1ng])
			s2ng = set([ng for ng in s2ng])
			all = s1ng.union(s2ng)
			for ng in all:
				datap.append([ng, labels])
	X = np.zeros((len(datap), ngramsize, embedsize))
	Y = np.zeros((len(datap), 12))
	wildcard = np.array([0.0]*embedsize)
	for i in range(0, len(datap)):
		item = datap[i]
		ngram = item[0]
		labels = item[1]
		vectors = getEmbedVectors(ngramsize, embedsize, ngram, m, wildcard)
		labelsfinal = getLabels(labels)
		X[i] = vectors
		Y[i] = labelsfinal
	for file in files:
		file.close()
	return X, Y

def getTestData(embedsize, ngramsize, m):
	files = []
	for type in ['G', 'M', 'S', 'O']:
		files.append(open('../../../corpora/'+type+'_test.txt'))
	f = files[0]
	datap = []
	for line in f:
		data = line.strip().split('\t')
		s1 = data[0]
		s2 = data[1]
		label = data[2]
		labels = [data[2]]
                for ftype in files[1:]:
                        linetype = ftype.readline()
                        datatype = linetype.strip().split('\t')
                        labels.append(datatype[2])
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
	for file in files:
		file.close()
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

def getLabels(labels):
	answer = np.zeros(12)
	for i in range(0, len(labels)):
		label = labels[i]
		answer[3*i+int(label)]=1.0
	return answer

RNN = recurrent.LSTM
HIDDEN_SIZE = hidden_size
BATCH_SIZE = 500
LAYERS = layers
TRAIN = True

print('Calculating...')
w2vmodel = '/export/data/ghpaetzold/word2vecvectors/models/word_vectors_all_'+embedsize+'_cbow.bin'
m = gensim.models.word2vec.Word2Vec.load_word2vec_format(w2vmodel, binary=True)
Xtr, Ytr = getTrainData(int(embedsize), int(ngramsize), m)
Xtes = getTestData(int(embedsize), int(ngramsize), m)
print('X: ' + str(Xtr.shape))
print('Y: ' + str(Ytr.shape))

model = None
try:
	model = model_from_json(open(model_file+'.json').read())
	model.load_weights(model_file+'.h5')
	print('Loaded!')
except Exception:
	model = Sequential()
	model.add(RNN(HIDDEN_SIZE, input_shape=(int(ngramsize), int(embedsize)), return_sequences=True))
	for _ in range(LAYERS):
		model.add(RNN(HIDDEN_SIZE, return_sequences=True))
	model.add(RNN(HIDDEN_SIZE, return_sequences=False))
	model.add(Dense(12))
	model.add(Activation('softmax'))
	model.compile(loss='categorical_crossentropy', optimizer='rmsprop')

print('Training...')
if TRAIN:
	model.fit(Xtr, Ytr, nb_epoch=2000, batch_size=2000)
	json_string = model.to_json()
	open(model_file+'.json', 'w').write(json_string)
	model.save_weights(model_file+'.h5', overwrite=True)

print('Predicting...')
files = []
for type in ['G', 'M', 'S', 'O']:
	os.system('mkdir ../../../labels/'+type+'/nn_adadelta_joint')
	files.append(open('../../../labels/'+type+'/nn_adadelta_joint/labels_NeuralNetwork_ADADELTAJOINT_'+str(hidden_size)+'_'+str(layers)+'_'+str(embedsize)+'_'+str(ngramsize)+'.txt', 'w'))
labels = []
for Xte in Xtes:
	labels_raw = model.predict(Xte, batch_size=Xte.shape[0])
	final_labels = [0.0, 0.0, 0.0, 0.0]
	for percentages in labels_raw:
		for i in range(0, 4):
			localpercs = percentages[i*3:i*3+3]
			locallabel = float(np.argmax(localpercs))
			final_labels[i] += locallabel
	for i in range(0, 4):
		final_labels[i] /= float(len(labels_raw))
		float_label = final_labels[i]
		if final_labels[i]<0.6666:
			final_labels[i] = 0
		elif final_labels[i]<1.3333:
			final_labels[i] = 1
		else:
			final_labels[i] = 2
		files[i].write(str(final_labels[i])+'\t'+str(float_label)+'\n')

for file in files:
	file.close()
