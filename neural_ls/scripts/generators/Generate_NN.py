from keras.models import *
from keras.layers.core import *
from keras.layers.recurrent import *
import gensim, sys, os
import numpy as np

modelpath = sys.argv[1]
model_json = '../../models/' + modelpath + '.json'
model_h5 = '../../models/' + modelpath + '.h5'

# Extract data from model:
modeld = modelpath.strip().split('_')
size = int(modeld[0])
arch = modeld[1]
retro = modeld[2]
corpus = modeld[3]
lines = int(modeld[4])
epochs = int(modeld[5])
hidden = int(modeld[6])
wvmodel = '/export/data/ghpaetzold/word2vecvectors/models/word_vectors_all_'+str(size)+'_'+arch
if retro == '1':
	wvmodel += '_retrofitted'
wvmodel += '.bin'

# Read input corpora:
f = open('../../corpora/ls_dataset_benchmarking.txt')
data = []
for line in f:
	data.append(line.strip().split('\t'))
f.close()

# Load embeddings model:
m = gensim.models.word2vec.Word2Vec.load_word2vec_format(wvmodel, binary=True)

# Create instances:
X = []
Y = []
bos = np.array([0.0]*size)
eos = np.array([1.0]*size)
for i in range(0, len(data)):
	sentence = data[i][0]
	tokens = sentence.strip().split(' ')
	instXtr = []
	instYtr = []
	instXtr.append(bos)
	try:
		instYtr.append(m[tokens[0]])
	except Exception:
		try:
			instYtr.append(m[tokens[0].lower()])
		except Exception:
			instYtr.append(m[','])
	for i in range(0, len(tokens)-1):
		try:
			instXtr.append(m[tokens[i]])
		except Exception:
			try:
				instXtr.append(m[tokens[i].lower()])
			except Exception:
				instXtr.append(m[','])
		try:
			instYtr.append(m[tokens[i+1]])
		except Exception:
			try:
				instYtr.append(m[tokens[i+1].lower()])
			except Exception:
				instYtr.append(m[','])
	instXtr.append(m[tokens[len(tokens)-1]])
	instYtr.append(eos)
	X.append(np.array([instXtr]))
	Y.append(np.array([instYtr]))
f.close()

# Load model:
model = model_from_json(open(model_json).read())
model.load_weights(model_h5)

# Predict output:
subs = {}
for i in range(0, len(X)):
	inst = data[i]
	tokens = inst[0].strip().split(' ')
	target = inst[1]
	head = int(inst[2])
	x = X[i]
	y = Y[i]
	pred = model.predict(x, batch_size=1)
	pred = model.predict(x, batch_size=1)
	result = pred[0][head]
	closest = m.most_similar(positive=[result], topn=10)
	closest = set([item[0] for item in closest])
	if target not in subs:
		subs[target] = closest
	else:
		subs[target].update(closest)

os.system('mkdir ../../substitutions/'+modelpath)
out = open('../../substitutions/'+modelpath+'/substitutions.txt', 'w')
for k in subs.keys():
        newline = k + '\t'
        if len(subs[k])>0:
                for c in subs[k]:
                        newline += c + '|||'
                newline = newline[0:len(newline)-3]
                out.write(newline.strip() + '\n')
out.close()
