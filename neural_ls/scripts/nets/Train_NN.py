from keras.models import *
from keras.layers.core import *
from keras.layers.recurrent import *
import gensim, sys
import numpy as np

def canBeUsed(tokens, m):
	errors = 0
	for token in tokens:
		try:
			v = m[token]
		except Exception:
			errors += 1
	if errors > 0 :
		return False
	else:
		return True

size = int(sys.argv[1])
arch = sys.argv[2]
retro = sys.argv[3]
corpus = sys.argv[4]
lines = int(sys.argv[5])
epochs = int(sys.argv[6])
hidden = int(sys.argv[7])
output_arch = str(size)+'_'+arch+'_'+retro+'_'+corpus+'_'+str(lines)+'_'+str(epochs)+'_'+str(hidden)+'.json'
output_weights = str(size)+'_'+arch+'_'+retro+'_'+corpus+'_'+str(lines)+'_'+str(epochs)+'_'+str(hidden)+'.h5'

#Load embeddings model:
wvmodel = '/export/data/ghpaetzold/word2vecvectors/models/word_vectors_all_'+str(size)+'_'+arch
if retro == '1':
	wvmodel += '_retrofitted'
wvmodel += '.bin'
m = gensim.models.word2vec.Word2Vec.load_word2vec_format(wvmodel, binary=True)

#Create training data:
f = open('../../corpora/training_corpora/'+corpus+'.txt')
bos = np.array([0.0]*size)
eos = np.array([1.0]*size)

#Create buckets of sentence size:
buckets = {}
for j in range(0, lines):
	line = f.readline()
	tokens = line.strip().split(' ')
	bsize = len(tokens)
	if bsize > 1:
		if bsize not in buckets:
			buckets[bsize] = ([], [])
		instXtr = []
		instYtr = []
		if canBeUsed(tokens, m) and len(tokens)>1:
			instXtr.append(bos)
			instYtr.append(m[tokens[0]])
			for i in range(0, len(tokens)-1):
				instXtr.append(m[tokens[i]])
				instYtr.append(m[tokens[i+1]])
			instXtr.append(m[tokens[len(tokens)-1]])
			instYtr.append(eos)
		buckets[bsize][0].append(instXtr)
		buckets[bsize][1].append(instYtr)
f.close()

#Create equally sized batches:
batches = []
for bsize in buckets:
	data = buckets[bsize]
	X = np.array(data[0])
	Y = np.array(data[1])
	if len(X)>=128:
		mbatches = len(X) // 128
		for i in range(0, mbatches):
			newbatchX = []
			newbatchY = []
			for j in range(0, 128):
				newbatchX.append(X[i*128+j])
				newbatchY.append(Y[i*128+j])
			batches.append((np.array(newbatchX), np.array(newbatchY)))

#Create model:
model = Sequential()
model.add(LSTM(output_dim=hidden, init='glorot_uniform', inner_init='glorot_uniform', activation='tanh', inner_activation='hard_sigmoid',
	weights=None, truncate_gradient=-1, input_dim=size, return_sequences=True))
model.add(LSTM(output_dim=size, init='glorot_uniform', inner_init='glorot_uniform', activation='tanh', inner_activation='hard_sigmoid',
        weights=None, truncate_gradient=-1, input_dim=hidden, return_sequences=True))
#model.add(TimeDistributedDense(output_dim=size, init='glorot_uniform', activation='linear'))
model.compile(loss='mean_squared_error', optimizer='rmsprop')

#Run epochs:
for i in range(0, epochs):
	print('Epoch: ' + str(i))
	for batch in batches:
		model.train_on_batch(batch[0], batch[1])

#Save model:
json_string = model.to_json()
open('../../models/'+output_arch, 'w').write(json_string)
model.save_weights('../../models/'+output_weights, overwrite=True)
