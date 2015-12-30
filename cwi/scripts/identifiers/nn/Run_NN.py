from keras.optimizers import *
from keras.models import *
from keras.layers.core import *
from lexenstein.morphadorner import *
from lexenstein.identifiers import *
from lexenstein.features import *
import sys
import numpy as np

train_victor_corpus = sys.argv[1]
hidden_size = int(sys.argv[2].strip())
lr = float(sys.argv[3].strip())
momentum = float(sys.argv[4].strip())
decay = float(sys.argv[5].strip())
nesterov = sys.argv[6].strip()
if nesterov=='1':
	nesterov = True
elif nesterov=='0':
	nesterov = False
else:
	print('Problem!')
layers = int(sys.argv[7].strip())
test_victor_corpus = sys.argv[8].strip()
out_file = sys.argv[9].strip()

def getLabels(corpus):
	result = []
	f = open(corpus)
	for line in f:
		data = line.strip().split('\t')
		label = float(data[3].strip())
		if label==0:
			result.append([1.0, 0.0])
		elif label==1:
			result.append([0.0, 1.0])
		else:
			print('Problem!')
		#result.append(label)
	f.close()
	return np.array(result)

m = MorphAdornerToolkit('/export/data/ghpaetzold/LEXenstein/morph/')

fe = FeatureEstimator(norm=False)
fe.addLexiconFeature('../../../../semeval/corpora/basic/basic_words.txt', 'Simplicity')
fe.addLexiconFeature('../../../../semeval/corpora/vocabularies/wikisimple.vocab.txt', 'Simplicity')
fe.addLengthFeature('Complexity')
fe.addSyllableFeature(m, 'Complexity')
fe.addCollocationalFeature('../../../../../benchmarking/semeval/corpora/lm/simplewiki/simplewiki.5gram.bin.txt', 2, 2, 'Complexity')
fe.addSentenceProbabilityFeature('../../../../../benchmarking/semeval/corpora/lm/simplewiki/simplewiki.5gram.bin.txt', 'Complexity')
fe.addCollocationalFeature('../../../../lexmturk/corpora/subtleximdb.5gram.bin.unk.txt', 2, 2, 'Complexity')
fe.addSentenceProbabilityFeature('../../../../lexmturk/corpora/subtleximdb.5gram.bin.unk.txt', 'Complexity')
#fe.addCollocationalFeature('/export/data/ghpaetzold/wordnetlmranking/corpora/corpus/subtlex/lm/corpus.clean.5.bin.txt', 2, 2, 'Simplicity')
#fe.addSentenceProbabilityFeature('/export/data/ghpaetzold/wordnetlmranking/corpora/corpus/subtlex/lm/corpus.clean.5.bin.txt', 'Simplicity')
#fe.addCollocationalFeature('/export/data/ghpaetzold/subtitlesimdb/corpora/160715/subimdb.5gram.unk.bin.txt', 2, 2, 'Simplicity')
#fe.addSentenceProbabilityFeature('/export/data/ghpaetzold/subtitlesimdb/corpora/160715/subimdb.5gram.unk.bin.txt', 'Simplicity')
#fe.addCollocationalFeature('/export/data/ghpaetzold/wordnetlmranking/corpora/corpus/wiki/lm/corpus.clean.5.bin.txt', 2, 2, 'Simplicity')
#fe.addSentenceProbabilityFeature('/export/data/ghpaetzold/wordnetlmranking/corpora/corpus/wiki/lm/corpus.clean.5.bin.txt', 'Simplicity')
fe.addSenseCountFeature('Simplicity')
fe.addSynonymCountFeature('Simplicity')
fe.addHypernymCountFeature('Simplicity')
fe.addHyponymCountFeature('Simplicity')
fe.addMinDepthFeature('Complexity')
fe.addMaxDepthFeature('Complexity')
#fe.addWordVectorValues('/export/data/ghpaetzold/word2vecvectors/models/word_vectors_all_100_cbow.bin', 100, 'Complexity')

print('Calculating...')
Xtr = np.array(fe.calculateFeatures(train_victor_corpus, format='cwictor'))
Ytr = getLabels(train_victor_corpus)
Xte = np.array(fe.calculateFeatures(test_victor_corpus, format='cwictor'))
Yte = getLabels(test_victor_corpus)
print('X: ' + str(Xtr.shape))
print('Y: ' + str(Ytr.shape))

model = Sequential()
model.add(Dense(output_dim=hidden_size, input_dim=Xtr.shape[1], init="glorot_uniform"))
model.add(Activation("tanh"))
model.add(Dropout(0.5))
for i in range(0, layers):
	model.add(Dense(output_dim=hidden_size, init="glorot_uniform"))
	model.add(Activation("tanh"))
	model.add(Dropout(0.5))
model.add(Dense(output_dim=2, init="glorot_uniform"))
model.add(Activation("sigmoid"))
sgd = SGD(lr=lr, decay=decay, momentum=momentum, nesterov=nesterov)
model.compile(loss='mean_absolute_error', optimizer=sgd)

print('Training...')
model.fit(Xtr, Ytr, nb_epoch=1000, batch_size=Xtr.shape[0], verbose=0)
#model.fit(Xtr, Ytr, nb_epoch=1000, batch_size=100, show_accuracy=True)

print('Predicting...')
labels_raw = model.predict_classes(Xte, batch_size=Xte.shape[0])
labels = []
for label in labels_raw:
	labels.append(label)
#	if label>0:
#		labels.append(1)
#	else:
#		labels.append(0)

o = open(out_file, 'w')
for label in labels:
	o.write(str(label) + '\n')
o.close()
