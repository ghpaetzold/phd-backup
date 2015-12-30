from __future__ import print_function
from keras.models import Sequential, slice_X
from keras.layers.core import Activation, TimeDistributedDense, RepeatVector
from keras.layers import recurrent
from keras.preprocessing.text import *
import numpy as np
from copy import copy
import gc, random

#Functions:
def mydecode(preds, vocab, probs=False):
#	print('Vocab: ' + str(vocab))
	sent = ''
	if not probs:
		for value in preds:
			if value<len(vocab):
				sent += vocab[value]
	else:
		for v in preds:
			index = -1
			maxv = -1
			for i in range(0, len(v)):
				if v[i]>maxv:
					maxv = v[i]
					index = i
			sent += vocab[index]
	return sent.strip()

def myonehot(text, vlist, size):
	vmap = {}
	for i in range(0, len(vlist)):
		vmap[vlist[i]] = i

	blank = np.array([0.0]*len(vlist))
	blank[len(vlist)-1] = 1.0

	sents = text
	Xtr = np.zeros((len(sents), size, len(vlist)))
	Ytr = np.zeros((len(sents), size, len(vlist)))

	for j in range(0, len(sents)):
		sent = sents[j]
		newX = np.zeros((size, len(vlist)))
		tokens = sent
		for i in range(0, len(tokens)):
			token = tokens[i]
			tokenv = copy(blank)
			tokenv[vmap[token]] = 1.0
			newX[i] = tokenv
		newY = np.zeros((size, len(vlist)))
		for i in range(0, len(sent)):
			newY[i] = newX[len(sent)-1-i]
		for i in range(0, size-len(sent)):
			newX[len(sent)+i] = blank
			newY[len(sent)+i] = blank
		Xtr[j]=newX
		Ytr[j]=newY
	return Xtr, Ytr, sents, vlist, vmap

#Parameters:
N_WORDS = 30000
RNN = recurrent.LSTM
HIDDEN_SIZE = 100
BATCH_SIZE = 500
LAYERS = 2
MAX_SIZE = 5
CONTINUE = True

#Extract training instances:
print('Creating data...')
text = set([])
vocab = 'abcdefghijklmnopqstuvwxyz0123456789 '
while len(text)<N_WORDS:
        size = random.randint(2, MAX_SIZE-1)
        word = ''
        for j in range(0, size):
                word += vocab[random.randint(0, len(vocab)-2)]
	text.add(word)
text = list(text)
X, Y, text, vocab, index_to_word = myonehot(text, vocab, MAX_SIZE)
print(str(X.shape))
print(str(Y.shape))

#for i in range(0, len(X)):
#	x = X[i]
#	y = Y[i]
#	xt = mydecode(x, vocab, probs=True)
#	yt = mydecode(y, vocab, probs=True)
#	print('xt: ' + str(xt))
#	print('yt: ' + str(yt))	

#Create model:
print('Creating model...')
model = Sequential()
model.add(RNN(HIDDEN_SIZE, input_shape=(None, len(vocab))))
model.add(RepeatVector(MAX_SIZE))
for _ in range(LAYERS):
    model.add(RNN(HIDDEN_SIZE, return_sequences=True))
model.add(TimeDistributedDense(len(vocab)))
model.add(Activation('softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam')

gc.collect()

#Train model:
for iteration in range(1, 200):
	print()
	print('-' * 50)
	print('Iteration', iteration)
	model.fit(X, Y, batch_size=BATCH_SIZE, nb_epoch=1)
	
	for i in range(10):
		ind = np.random.randint(0, len(X))
		rowX, rowy = X[np.array([ind])], Y[np.array([ind])]
		preds = model.predict_classes(rowX, verbose=0)
		correct = text[ind]
		guess = mydecode(preds[0], vocab)
		print('\nCorrect: ' + correct)
		print('Inverted: ' + guess)

json_string = model.to_json()
open('model_arch_char.json', 'w').write(json_string)
model.save_weights('model_weights_char.h5', overwrite=True)
